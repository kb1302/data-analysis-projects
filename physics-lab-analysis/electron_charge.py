# Free Choice experiment #1 Charge to mass ratio of electron
# Used black capacitor.py to format

# imports
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import csv
from matplotlib import pyplot as plt


# sig fig function
def sigfig(meas, unc):
    digits = int(np.floor(np.log10(unc)))
    punc = np.round(unc, -digits)
    pmeas = np.round(meas, -digits)
    return pmeas, punc


# Chi squared value functions
def chi2(y_measure, y_predict, errors):
    """Calculate the chi squared value given a measurement with errors and prediction"""
    return np.sum((y_measure - y_predict) ** 2 / errors**2)


def chi2reduced(
    y_measure, y_predict, errors, number_of_parameters
):
    """Calculate the reduced chi squared value given a measurement with errors and prediction,
    and knowing the number of parameters in the model."""
    return chi2(y_measure, y_predict, errors) / (y_measure.size - number_of_parameters)


# Uncertainty function for voltmeter and ammeter
def get_multimeter_unc(reading, reading_range, is_from_voltmeter):
    """Calculate uncertainty based on multimeter's accuracy specifications."""
    final_uncertainty = 0
    if is_from_voltmeter:
        # 0.05% of reading
        final_uncertainty += (reading / 100) * 0.05
        if reading_range == 3:
            # 5 counts of least significant digit
            final_uncertainty += 0.0005
        elif reading_range == 30:
            # 2 counts of least significant digit
            final_uncertainty += 0.002
    else:
        # Measuring current (ammeter)
        # 0.2% of reading
        final_uncertainty += (reading / 100) * 0.2
        if reading_range == 30:
            # 5 counts of least significant digit
            final_uncertainty += 0.005
    return final_uncertainty


# read data file
df = pd.read_csv("electron_constant_current.csv")
df2 = pd.read_csv("electron_constant_voltage.csv")


# Save constant current data as arrays
voltage_cc = np.asarray(df["voltage"])
radius_cc = np.asarray(df["radius"]) / 100  # convert to meters
voltage_low_cc = np.asarray(df["voltage_low"])
voltage_high_cc = np.asarray(df["voltage_high"])

voltage_avg_cc = (voltage_low_cc + voltage_high_cc) / 2
radius_cc_inverse = 1 / radius_cc


# Save constant voltage data as arrays
radius_cv = np.asarray(df2["radius"]) / 100  # convert to meters
current_low_cv = np.asarray(df2["current_low"])
current_high_cv = np.asarray(df2["current_high"])

current_avg_cv = (current_low_cv + current_high_cv) / 2
radius_cv_inverse = 1 / radius_cv


# Uncertainty propogation for inverse radius
radius_unc_cc = np.sqrt((-(1 / (radius_cc**2)) * 0.0005) ** 2)
radius_unc_cv = np.sqrt((-(1 / (radius_cv**2)) * 0.0005) ** 2)


# Model equation for constant voltage (voltage constant at 150.5)
# based on the chargetomassratio.pdf
# k/a was calculated separately
def coil_cv(x, a, b):
    return np.sqrt(a) * 0.000554737 * ((x + ((1 / np.sqrt(2)) * b)) / np.sqrt(150.5))


# Model equation for constant current (Current constant at 1.005A)
def coil_cc(x, a, b):
    return np.sqrt(a) * 0.000554737 * ((1.005 + ((1 / np.sqrt(2)) * b)) / np.sqrt(x))


# Model equation for constant current with horizontal offset variable
def coil_cc2(x, a, b, c):
    return (
        np.sqrt(a) * 0.000554737 * ((1.005 + ((1 / np.sqrt(2)) * b)) / np.sqrt(x - c))
    )


# Model equation for constant current with horizontal and vertical offset variables
def coil_cc3(x, a, b, c, d):
    return (
        np.sqrt(a) * 0.000554737 * ((1.005 + ((1 / np.sqrt(2)) * b)) / np.sqrt(x - c))
        + d
    )


"""
###########################################################################################
###########################################################################################
"""

# Constant Current
coefficients_cc, unc_matrix_cc = curve_fit(
    coil_cc,
    voltage_avg_cc,
    radius_cc_inverse,
    absolute_sigma=True,
    maxfev=10000,
    p0=[175870000000, 1],
    sigma=radius_unc_cc,
)


# Sigfigs and uncertainty for cc coefficients
a_sigfig_cc, a_unc_cc = sigfig(coefficients_cc[0], np.sqrt(unc_matrix_cc[0][0]))
b_sigfig_cc, b_unc_cc = sigfig(coefficients_cc[1], np.sqrt(unc_matrix_cc[1][1]))
print("\na (Charge to mass ratio with constant current):", a_sigfig_cc, "±", a_unc_cc)
print("b (Initial current with constant current):", b_sigfig_cc, "±", b_unc_cc)
print(coefficients_cc[0], coefficients_cc[1])


# X and Y fits
x_fit_cc = np.linspace(90, 251, 10000)
y_fit_cc = coil_cc(x_fit_cc, coefficients_cc[0], coefficients_cc[1])


plt.xlabel("Voltage (V)")
plt.ylabel("Inverse Radius (1/R) (1/m)")
plt.scatter(voltage_avg_cc, radius_cc_inverse, color="red")  # shows our points
plt.plot(x_fit_cc, y_fit_cc)  # show our curved fit
plt.title("Figure 1: Radius over Voltage (constant current)")
plt.grid()
plt.show()


"""
###########################################################################################
###########################################################################################
"""

# Constant Current with horizontal offset
coefficients_cc2, unc_matrix_cc2 = curve_fit(
    coil_cc2,
    voltage_avg_cc,
    radius_cc_inverse,
    absolute_sigma=True,
    maxfev=10000,
    p0=[175870000000, 1, 1],
    sigma=radius_unc_cc,
)


# Sigfigs and uncertainty for cc2 coefficients
a_sigfig_cc2, a_unc_cc2 = sigfig(coefficients_cc2[0], np.sqrt(unc_matrix_cc2[0][0]))
b_sigfig_cc2, b_unc_cc2 = sigfig(coefficients_cc2[1], np.sqrt(unc_matrix_cc2[1][1]))
c_sigfig_cc2, c_unc_cc2 = sigfig(coefficients_cc2[2], np.sqrt(unc_matrix_cc2[2][2]))
print(
    "\na (Charge to mass ratio with constant current (extra variable)):",
    a_sigfig_cc2,
    "±",
    a_unc_cc2,
)
print(
    "b (Initial current with constant current (extra variable)):",
    b_sigfig_cc2,
    "±",
    b_unc_cc2,
)
print("c (horizontal offset):", c_sigfig_cc2, "±", c_unc_cc2)
print(coefficients_cc2[0], coefficients_cc2[1], coefficients_cc2[2])


# X and Y fits
x_fit_cc2 = np.linspace(90, 251, 10000)
y_fit_cc2 = coil_cc2(
    x_fit_cc2, coefficients_cc2[0], coefficients_cc2[1], coefficients_cc2[2]
)


plt.xlabel("Voltage (V)")
plt.ylabel("Inverse Radius (1/R) (1/m)")
plt.scatter(voltage_avg_cc, radius_cc_inverse, color="red")  # shows our points
plt.plot(x_fit_cc2, y_fit_cc2)  # show our curved fit
plt.title("Figure 2: Radius over Voltage (constant current) with horizontal offset")
plt.grid()
plt.show()


"""
###########################################################################################
###########################################################################################
"""

# Constant Current with horizontal and vertical offset
coefficients_cc3, unc_matrix_cc3 = curve_fit(
    coil_cc3,
    voltage_avg_cc,
    radius_cc_inverse,
    absolute_sigma=True,
    maxfev=10000,
    p0=[175870000000, 1, 1, 1],
    sigma=radius_unc_cc,
)


# Sigfigs and uncertainty for cc3 coefficients
a_sigfig_cc3, a_unc_cc3 = sigfig(coefficients_cc3[0], np.sqrt(unc_matrix_cc3[0][0]))
b_sigfig_cc3, b_unc_cc3 = sigfig(coefficients_cc3[1], np.sqrt(unc_matrix_cc3[1][1]))
c_sigfig_cc3, c_unc_cc3 = sigfig(coefficients_cc3[2], np.sqrt(unc_matrix_cc3[2][2]))
d_sigfig_cc3, d_unc_cc3 = sigfig(coefficients_cc3[3], np.sqrt(unc_matrix_cc3[3][3]))
print(
    "\na (Charge to mass ratio with constant current (extra variable)):",
    a_sigfig_cc3,
    "±",
    a_unc_cc3,
)
print(
    "b (Initial current with constant current (extra variable)):",
    b_sigfig_cc3,
    "±",
    b_unc_cc3,
)
print("c (horizontal offset):", c_sigfig_cc3, "±", c_unc_cc3)
print("d (vertical offset):", d_sigfig_cc3, "±", d_unc_cc3)
print(
    coefficients_cc3[0], coefficients_cc3[1], coefficients_cc3[2], coefficients_cc3[3]
)


# X and Y fits
x_fit_cc3 = np.linspace(90, 251, 10000)
y_fit_cc3 = coil_cc3(
    x_fit_cc3,
    coefficients_cc3[0],
    coefficients_cc3[1],
    coefficients_cc3[2],
    coefficients_cc3[3],
)


plt.xlabel("Voltage (V)")
plt.ylabel("Inverse Radius (1/R) (1/m)")
plt.scatter(voltage_avg_cc, radius_cc_inverse, color="red")  # shows our points
plt.plot(x_fit_cc3, y_fit_cc3)  # show our curved fit
plt.title(
    "Figure 3: Radius over Voltage (constant current) with horizontal and vertical offset"
)
plt.grid()
plt.show()


"""
###########################################################################################
###########################################################################################
"""

# Constant Voltage
coefficients_cv, unc_matrix_cv = curve_fit(
    coil_cv,
    current_avg_cv,
    radius_cv_inverse,
    absolute_sigma=True,
    maxfev=10000,
    p0=[175870000000, 1],
    sigma=radius_unc_cv,
)


# Sigfigs and uncertainty for cc coefficients
a_sigfig_cv, a_unc_cv = sigfig(coefficients_cv[0], np.sqrt(unc_matrix_cv[0][0]))
b_sigfig_cv, b_unc_cv = sigfig(coefficients_cv[1], np.sqrt(unc_matrix_cv[1][1]))
print("\na (Charge to mass ratio with constant current):", a_sigfig_cv, "±", a_unc_cv)
print("b (Initial current with constant current):", b_sigfig_cv, "±", b_unc_cv)
print(coefficients_cv[0], coefficients_cv[1])


# X and Y fits
x_fit_cv = np.linspace(0.8, 2.8, 10000)
y_fit_cv = coil_cv(x_fit_cv, coefficients_cv[0], coefficients_cv[1])


plt.xlabel("Current (A)")
plt.ylabel("Inverse Radius (1/R) (1/m)")
plt.scatter(current_avg_cv, radius_cv_inverse, color="red")  # shows our points
plt.plot(x_fit_cv, y_fit_cv)  # show our curved fit
plt.title("Figure 4: Radius over Current (constant voltage)")
plt.grid()
plt.show()

"""
###########################################################################################
###########################################################################################
"""

# Residuals (observed - fitted)
fit_cc = coil_cc(voltage_avg_cc, coefficients_cc[0], coefficients_cc[1])
fit_cc2 = coil_cc2(
    voltage_avg_cc, coefficients_cc2[0], coefficients_cc2[1], coefficients_cc2[2]
)
fit_cc3 = coil_cc3(
    voltage_avg_cc,
    coefficients_cc3[0],
    coefficients_cc3[1],
    coefficients_cc3[2],
    coefficients_cc3[3],
)
fit_cv = coil_cv(current_avg_cv, coefficients_cv[0], coefficients_cv[1])


residuals_cc = radius_cc_inverse - fit_cc
residuals_cc2 = radius_cc_inverse - fit_cc2
residuals_cc3 = radius_cc_inverse - fit_cc3
residuals_cv = radius_cv_inverse - fit_cv


# Plot residuals for constant current data
plt.scatter(voltage_avg_cc, residuals_cc, color="green")
plt.axhline(0, color="black", lw=2)  # Zero line for reference
plt.xlabel("Voltage (V)")
plt.ylabel("Residuals (I - Fit)")
plt.title("Figure 5: Residuals for Constant Current Data")
plt.grid()
plt.show()


# Plot residuals for constant current data with horizontal offset
plt.scatter(voltage_avg_cc, residuals_cc2, color="green")
plt.axhline(0, color="black", lw=2)  # Zero line for reference
plt.xlabel("Voltage (V)")
plt.ylabel("Residuals (I - Fit)")
plt.title("Figure 6: Residuals for Constant Voltage Data with Horizontal Offset")
plt.grid()
plt.show()


# Plot residuals for constant current data with horizontal offset
plt.scatter(voltage_avg_cc, residuals_cc3, color="green")
plt.axhline(0, color="black", lw=2)  # Zero line for reference
plt.xlabel("Voltage (V)")
plt.ylabel("Residuals (I - Fit)")
plt.title(
    "Figure 7: Residuals for Constant Voltage Data with Horizontal and Vertical Offset"
)
plt.grid()
plt.show()


# Plot residuals for constant voltage data
plt.scatter(current_avg_cv, residuals_cv, color="green")
plt.axhline(0, color="black", lw=2)  # Zero line for reference
plt.xlabel("Current (A)")
plt.ylabel("Residuals (I - Fit)")
plt.title("Figure 8: Residuals for Constant Voltage Data")
plt.grid()
plt.show()


# Chi-squared for constant current data
chi2_cc = chi2reduced(radius_cc_inverse, fit_cc, radius_unc_cc, len(coefficients_cc))
print("\nReduced Chi-squared (constant current):", chi2_cc)

chi2_cc2 = chi2reduced(radius_cc_inverse, fit_cc2, radius_unc_cc, len(coefficients_cc2))
print("\nReduced Chi-squared (constant current w/ horizontal offset):", chi2_cc2)

chi2_cc3 = chi2reduced(radius_cc_inverse, fit_cc3, radius_unc_cc, len(coefficients_cc3))
print(
    "\nReduced Chi-squared (constant current w/ horizontal and vertical offset):",
    chi2_cc3,
)

chi2_cv = chi2reduced(radius_cv_inverse, fit_cv, radius_unc_cv, len(coefficients_cv))
print("\nReduced Chi-squared (constant voltage):", chi2_cv)
