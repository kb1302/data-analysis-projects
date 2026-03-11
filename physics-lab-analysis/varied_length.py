import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from numpy.polynomial.polynomial import polyfit

# -----------------------------
# 1. Metadata for the 5 trials
# -----------------------------
excel_file = "pendulum_length_data.xlsx"
sheet_names = [f"trial{n}" for n in range(15, 20)]

# String lengths (L) in *cm* from your message
L_cm = np.array([33.2, 29.0, 24.2, 19.8, 15.3], dtype=float)
L_m = L_cm / 100.0  # convert to meters

# Distance from CoM to attachment point (D) from your methodology
D_cm = 3.21
D_m = D_cm / 100.0

# Effective lengths L_eff = L + D (in meters)
L_eff = L_m + D_m

# For plotting on x-axis as sqrt(L_eff)
sqrt_Leff = np.sqrt(L_eff)

# -----------------------------
# 2. Function to compute period from theta(t)
# -----------------------------
def compute_period_from_theta(df, theta_col="theta_rad", t_col="t"):
    """
    Given a DataFrame with time t and angle theta,
    find successive peaks in theta(t) and estimate the period.

    Returns:
        T_mean : mean period
        T_err  : standard error on the mean
        T_all  : array of individual periods between peaks
    """
    t = df[t_col].values
    theta = df[theta_col].values

    # find peaks in theta(t)
    peaks, _ = find_peaks(theta)

    # need at least 3 peaks to get 2 intervals
    if len(peaks) < 3:
        raise RuntimeError("Not enough peaks found to estimate period.")

    t_peaks = t[peaks]

    # time differences between consecutive peaks ~ 1 period
    T_all = np.diff(t_peaks)

    T_mean = np.mean(T_all)
    # sample standard deviation
    T_std = np.std(T_all, ddof=1)
    # standard error on the mean
    T_err = T_std / np.sqrt(len(T_all))

    return T_mean, T_err, T_all

# -----------------------------
# 3. Loop over trials and compute T and dT
# -----------------------------
T_values = []
T_errors = []

for sheet in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet)
    T_mean, T_err, T_all = compute_period_from_theta(df)
    T_values.append(T_mean)
    T_errors.append(T_err)
    print(f"{sheet}: T = {T_mean:.4f} s ± {T_err:.4f} s, from {len(T_all)} cycles")

T_values = np.array(T_values)
T_errors = np.array(T_errors)

# -----------------------------
# 4. Fit T vs sqrt(L_eff) to a straight line
#    T = a * sqrt(L_eff) + b
# -----------------------------
weights = 1.0 / T_errors

# polyfit in "polynomial" form returns coefficients [b, a] for b + a x
b_fit, a_fit = polyfit(sqrt_Leff, T_values, deg=1, w=weights)

# Covariance matrix via normal equations
X = np.vstack([np.ones_like(sqrt_Leff), sqrt_Leff]).T
W = np.diag(weights**2)

beta = np.array([b_fit, a_fit])
residuals = T_values - X @ beta      # <-- we'll plot these below
dof = len(T_values) - 2
sigma2 = np.sum((weights * residuals)**2) / dof  # chi^2_red as sigma2

cov = sigma2 * np.linalg.inv(X.T @ W @ X)
b_err = np.sqrt(cov[0, 0])
a_err = np.sqrt(cov[1, 1])

chi2 = np.sum(((T_values - (a_fit * sqrt_Leff + b_fit)) / T_errors) ** 2)
chi2_red = chi2 / dof

print("\nFit results for T = a * sqrt(L_eff) + b:")
print(f"a = {a_fit:.4f} ± {a_err:.4f} s·m^(-1/2)")
print(f"b = {b_fit:.4f} ± {b_err:.4f} s")
print(f"chi^2_red = {chi2_red:.2f} with dof = {dof}")

# Optional: compare to theoretical a_th = 2π / sqrt(g)
g = 9.81  # m/s^2
a_th = 2 * np.pi / np.sqrt(g)
print(f"Theoretical a_th = 2π / √g = {a_th:.4f} s·m^(-1/2)")
print(f"Relative deviation (a - a_th)/a_th = {(a_fit - a_th)/a_th:.2%}")

# -----------------------------
# 5. Plot T vs sqrt(L_eff) with fit, theory line, and residuals
# -----------------------------
fig, (ax, ax_res) = plt.subplots(
    2, 1,
    sharex=True,
    gridspec_kw={"height_ratios": [3, 1]}
)

# --- top panel: data + fit + theory ---
ax.errorbar(
    sqrt_Leff,
    T_values,
    yerr=T_errors,
    fmt="o",
    capsize=3,
    label="Measured periods"
)

x_fit = np.linspace(sqrt_Leff.min() * 0.95, sqrt_Leff.max() * 1.05, 200)
T_fit = a_fit * x_fit + b_fit
ax.plot(x_fit, T_fit, label="Best-fit $T = a\\sqrt{L + D} + b$")

T_theory = a_th * x_fit  # assumes zero intercept
ax.plot(x_fit, T_theory, linestyle="--",
        label="Theory $T = (2\\pi/\\sqrt{g})\\sqrt{L + D}$")

ax.set_ylabel(r"Period $T$ (s)")
ax.legend()
ax.grid(True)

# --- bottom panel: residuals ---
ax_res.errorbar(
    sqrt_Leff,
    residuals,
    yerr=T_errors,
    fmt="o",
    capsize=3
)
ax_res.axhline(0, color="k", linewidth=1)
ax_res.set_xlabel(r"$\sqrt{L + D}\ \mathrm{(m^{1/2})}$")
ax_res.set_ylabel("Residuals (s)")
ax_res.grid(True)

plt.tight_layout()
plt.savefig("pendulum_period_vs_length_with_residuals.png",
            dpi=300, bbox_inches="tight")
plt.show()
