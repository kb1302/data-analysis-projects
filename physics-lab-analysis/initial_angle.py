import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2
from scipy.optimize import curve_fit

# ----------------- style -----------------
plt.rcParams.update({"font.size": 14})

# ----------------- files & trials -----------------
data_file_main = "pendulum_data.xlsx"              # trials 1–9
data_file_sym  = "pendulum_symmetry_data.xlsx"     # trials 10–14

excel_path_for_trial = {
    **{f"trial{i}": data_file_main for i in range(1, 10)},
    **{f"trial{i}": data_file_sym  for i in range(10, 15)},
}

trial_names = [f"trial{i}" for i in range(1, 15)]  # 1–14

# signed initial angles (rad)
initial_angle = {
    "trial1": -0.55, "trial2": -0.82, "trial3": -0.62,
    "trial4": -1.52, "trial5": -0.32, "trial6": -0.26,
    "trial7": -1.21, "trial8": -1.19, "trial9": -0.89,
    "trial10": 0.34, "trial11": 0.57, "trial12": 0.96,
    "trial13": 1.04, "trial14": 0.61,
}

# uncertainties
SIGMA_THETA = 0.02   # rad, horizontal
SIGMA_T_SYS = 0.002  # s, timing floor

# ----------------- helpers -----------------
def recenter(theta_rad):
    """Re-center Tracker angle to physical φ around 0, wrap to (−π, π]."""
    phi = theta_rad - np.pi/2
    return (phi + np.pi) % (2*np.pi) - np.pi

def periods_from_zero_crossings(t, phi):
    """Rising zero-crossings → list of full-cycle periods."""
    t = np.asarray(t, float)
    p = np.asarray(phi, float)
    idx = np.where((p[:-1] < 0) & (p[1:] >= 0))[0]
    if len(idx) < 2:
        return []
    t_cross = t[idx] + (0 - p[idx]) * (t[idx+1] - t[idx]) / (p[idx+1] - p[idx])
    return np.diff(t_cross)

def summarize_period(t, phi):
    """Return (T_central, sigma_T, n_periods)."""
    P = periods_from_zero_crossings(t, phi)
    if len(P) == 0:
        return np.nan, np.nan, 0
    T_med = np.median(P)
    sigma = np.std(P, ddof=1) if len(P) > 1 else 0.0
    sigma_SE = sigma / np.sqrt(len(P)) if len(P) > 1 else 0.0
    sigma_tot = np.sqrt(sigma_SE**2 + SIGMA_T_SYS**2)
    return T_med, sigma_tot, len(P)

# symmetric quadratic model: T(θ0) = T0 + A2 θ0^2
def symmetric_quad(theta0, T0, A2):
    return T0 + A2 * theta0**2

# ----------------- collect one point per trial -----------------
x, xerr, y, yerr, labels = [], [], [], [], []

for sh in trial_names:
    df = pd.read_excel(excel_path_for_trial[sh], sheet_name=sh)
    t = df["t"].to_numpy()
    phi = recenter(df["theta_rad"].to_numpy())

    T_cen, sT, nP = summarize_period(t, phi)
    if np.isnan(T_cen) or nP == 0:
        print(f"[WARN] {sh}: insufficient cycles.")
        continue

    th0 = initial_angle[sh]
    x.append(th0)
    xerr.append(SIGMA_THETA)
    y.append(T_cen)
    yerr.append(sT)
    labels.append(sh)

x = np.array(x)
xerr = np.array(xerr)
y = np.array(y)
yerr = np.array(yerr)

# sort by angle
order = np.argsort(x)
x, xerr, y, yerr = x[order], xerr[order], y[order], yerr[order]

# ====================================================
# 1) SMALL-ANGLE CONSTANT MODEL (NUMERICAL TEST ONLY)
# ====================================================

# pick a "small-angle" range to test, e.g. |θ0| <= 0.40 rad
mask_small = np.abs(x) <= 0.40
xs, ys, yerrs = x[mask_small], y[mask_small], yerr[mask_small]

if len(xs) >= 2:
    w_small = 1.0 / (yerrs**2)
    T_const = np.sum(w_small * ys) / np.sum(w_small)
    sigma_T_const = np.sqrt(1.0 / np.sum(w_small))
    chi2_const = np.sum(((ys - T_const) / yerrs)**2)
    dof_const = len(ys) - 1
    chi2_red_const = chi2_const / dof_const
    p_const = chi2.sf(chi2_const, dof_const)

    print("=== Small-angle constant model test (|theta0| <= 0.40 rad) ===")
    print(f"T_const = {T_const:.5f} ± {sigma_T_const:.5f} s")
    print(f"chi2 = {chi2_const:.2f}, dof = {dof_const}, "
          f"chi2_red = {chi2_red_const:.2f}, p = {p_const:.3f}, N = {len(ys)}")
else:
    print("Not enough small-angle points to test constant-period model.")

# ====================================================
# 2) FULL-RANGE SYMMETRIC QUADRATIC MODEL (finite angles)
# ====================================================

# initial guess from constant fit (or mean y) & rough A2; enforce A2 >= 0
T0_guess = np.mean(y) if len(xs) < 2 else T_const
p0 = [T0_guess, 0.04]   # 0.04 s/rad^2 is order-of-mag for finite-angle correction
bounds = ([0.0, 0.0], [np.inf, np.inf])

popt_sym, pcov_sym = curve_fit(
    symmetric_quad,
    x, y,
    p0=p0,
    sigma=yerr,
    absolute_sigma=True,
    bounds=bounds
)
T0_sym, A2_sym = popt_sym
sigma_T0_sym, sigma_A2_sym = np.sqrt(np.diag(pcov_sym))

y_sym = symmetric_quad(x, T0_sym, A2_sym)
chi2_sym = np.sum(((y - y_sym) / yerr)**2)
dof_sym = len(y) - 2
chi2_red_sym = chi2_sym / dof_sym
p_sym = chi2.sf(chi2_sym, dof_sym)

print("\n=== Full-range symmetric quadratic model ===")
print(f"T0 = {T0_sym:.5f} ± {sigma_T0_sym:.5f} s")
print(f"A2 = {A2_sym:.5f} ± {sigma_A2_sym:.5f} s/rad^2")
print(f"chi2 = {chi2_sym:.2f}, dof = {dof_sym}, "
      f"chi2_red = {chi2_red_sym:.2f}, p = {p_sym:.3f}")

# ---- linear asymmetry slope, for quantitative asymmetry estimate ----
w_full = 1.0 / (yerr**2)
W = np.sum(w_full)
Wx = np.sum(w_full * x)
Wy = np.sum(w_full * y)
Wxx = np.sum(w_full * x * x)
Wxy = np.sum(w_full * x * y)
Delta = W * Wxx - Wx**2
m = (W * Wxy - Wx * Wy) / Delta
b_lin = (Wxx * Wy - Wx * Wxy) / Delta
sigma_m = np.sqrt(W / Delta)
print(f"\nAsymmetry slope (linear fit, not plotted): "
      f"m = {m:.5f} ± {sigma_m:.5f} s/rad")

# ---- Single clean figure: full-range symmetric quadratic ----
fig = plt.figure(figsize=(7.5, 5.0), constrained_layout=True)
gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])

ax = fig.add_subplot(gs[0, 0])
ax.errorbar(x, y, yerr=yerr, xerr=xerr, fmt='o', capsize=3,
            label="data")

xx = np.linspace(x.min()*1.05, x.max()*1.05, 400)
ax.plot(xx, symmetric_quad(xx, T0_sym, A2_sym), '-.',
        label=fr"$T = {T0_sym:.3f} + {A2_sym:.3f}\,\theta_0^2$ s")

# (optional) show the small-angle constant as a horizontal dashed line
if len(xs) >= 2:
    ax.axhline(T_const, color='grey', linestyle=':',
               label=fr"small-angle const: $T={T_const:.3f}$ s")
    # and shade the small-angle region
    ax.axvspan(-0.40, 0.40, color='grey', alpha=0.1)

ax.set_xlabel(r"Initial angle $\theta_0$ (rad)")
ax.set_ylabel("Period (s)")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left")

txt = fr"$\chi^2_\mathrm{{red}} = {chi2_red_sym:.2f}$ (dof={dof_sym}, p={p_sym:.3f})"
ax.text(0.02, 0.02, txt, transform=ax.transAxes,
        fontsize=11, va="bottom")

axr = fig.add_subplot(gs[1, 0], sharex=ax)
res_sym = y - y_sym
axr.axhline(0, color='k', lw=1)
axr.errorbar(x, res_sym, yerr=yerr, xerr=xerr, fmt='o', capsize=3)
axr.set_xlabel(r"Initial angle $\theta_0$ (rad)")
axr.set_ylabel("Residuals (s)")
axr.grid(True, alpha=0.3)

plt.savefig("pendulum_period_vs_angle.png", dpi=300, bbox_inches="tight")
plt.show()
