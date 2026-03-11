import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 16,
    "axes.labelsize": 15,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13
})

# ===========================
# Data
# ===========================

# B = 1071 mT
I_1071 = np.array([18.90,  9.10, 26.06, 21.05, 14.05,  9.72, 23.23, 14.32])
VH_1071 = np.array([-0.0126, -0.0059, -0.0173, -0.0151,
                    -0.0090, -0.0065, -0.0152, -0.0100])

# B = 482 mT
I_482 = np.array([5.30,  8.92, 12.33, 16.19, 19.27,
                  22.69, 24.52, 26.45, 28.38, 14.00])
VH_482 = np.array([-0.0017, -0.0028, -0.0041, -0.0051, -0.0060,
                   -0.0066, -0.0075, -0.0080, -0.0080, -0.0044])

# B = 780 mT
I_780 = np.array([5.60,  9.00, 12.30, 16.23, 19.49,
                  21.01, 24.25, 26.02, 27.83, 29.02])
VH_780 = np.array([-0.0027, -0.0045, -0.0066, -0.0083, -0.0099,
                   -0.0100, -0.0117, -0.0127, -0.0129, -0.0141])

datasets = [
    {"B_mT": 482,  "I": I_482,  "VH": VH_482},
    {"B_mT": 780,  "I": I_780,  "VH": VH_780},
    {"B_mT": 1071, "I": I_1071, "VH": VH_1071},
]

# Define uncertainties (constants)
I_err = 0.01    # mA
VH_err = 0.0007 # mV

# ===========================
# Plotting + Printing Function
# ===========================

def plot_hall_fit(I_mA, VH_mV, B_mT):
    # Make weights array for polyfit (1/sigma for each point)
    w = np.ones_like(VH_mV) / VH_err

    # Weighted linear fit: VH = a * I + b
    coeffs, cov = np.polyfit(I_mA, VH_mV, 1, w=w, cov=True)
    a, b = coeffs
    a_err, b_err = np.sqrt(np.diag(cov))

    # Evaluate fit + residuals
    VH_fit = np.polyval(coeffs, I_mA)
    residuals = VH_mV - VH_fit

    # Chi-squared and reduced chi-squared
    chi2 = np.sum((residuals / VH_err)**2)
    red_chi2 = chi2 / (len(I_mA) - 2)

    # Print results in linear equation format
    print(f"\n=== B = {B_mT} mT ===")
    print("Best-fit line:")
    print(f"V_H = ({a:.6e} ± {a_err:.6e}) * I_E  +  ({b:.6e} ± {b_err:.6e})   [mV]")
    print(f"Reduced chi-squared = {red_chi2:.4f}")
    print()

    # ---------- Plot ----------
    fig, (ax_main, ax_res) = plt.subplots(
        2, 1, sharex=True, gridspec_kw={"height_ratios": [3, 1]}, figsize=(6,6)
    )
    fig.suptitle(f"Hall Voltage vs Current at B = {B_mT} mT", fontsize=12)

    # Data points with error bars (blue)
    ax_main.errorbar(I_mA, VH_mV,
                     xerr=I_err, yerr=VH_err,
                     fmt='o', color='blue', ecolor='gray', capsize=3)

    # Fit line (orange)
    I_sorted = np.linspace(I_mA.min(), I_mA.max(), 200)
    VH_sorted = np.polyval(coeffs, I_sorted)
    ax_main.plot(I_sorted, VH_sorted, color='orange')

    ax_main.set_ylabel(r"$V_H$ (mV)")
    ax_main.grid(True, alpha=0.3)

    # Residuals with error bars
    ax_res.axhline(0, color='k', linewidth=1)
    ax_res.errorbar(I_mA, residuals,
                    xerr=I_err, yerr=VH_err,
                    fmt='o', color='blue', ecolor='gray', capsize=3)

    ax_res.set_xlabel(r"$I_E$ (mA)")
    ax_res.set_ylabel("Residuals (mV)")
    ax_res.grid(True, alpha=0.3)


    fig.suptitle(f"Hall Voltage vs Current at B = {B_mT} mT",
             fontsize=16, y=0.96)   # <-- manually move title down
    plt.subplots_adjust(top=0.90)
    plt.tight_layout()

    # Save figure
    filename = f"hall_B{B_mT}.png"
    plt.savefig(filename, dpi=300)
    print(f"Saved: {filename}")

    plt.show()


# ===========================
# Generate all 3 plots + print fit info
# ===========================
for ds in datasets:
    plot_hall_fit(ds["I"], ds["VH"], ds["B_mT"])
