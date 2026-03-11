# Capacitors Experiment using Oscilloscopes
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


# Create expected model where a = V_0, b = RC, and x = time
def expected(x, a, b):
    return a * np.exp((-x) / b)


# read data file
df = pd.read_csv("capacitor_data.csv")
df2 = pd.read_csv("channel2_data.csv")


# Save data as arrays
time_ch = np.asarray(df2["time"])
volt_ch = np.asarray(df2["volt"])
time_cap = np.asarray(df["time"])
volt1_cap = np.asarray(df["volt1"])
volt2_cap = np.asarray(df["volt2"])


"""
###########################################################################################
###########################################################################################
"""
# Cursor Data

# Voltage uncertainty
volt_ch_unc = 0.05 * volt_ch  # Taking 5%


# Curve fit expected function
coefficients_exp, unc_matrix_exp = curve_fit(
    expected,
    time_ch,
    volt_ch,
    sigma=volt_ch_unc,
    absolute_sigma=True,
)


# Sigfigs and uncertainty for expected coefficients
a_sigfig_exp, a_unc_exp = sigfig(coefficients_exp[0], np.sqrt(unc_matrix_exp[0][0]))
b_sigfig_exp, b_unc_exp = sigfig(coefficients_exp[1], np.sqrt(unc_matrix_exp[1][1]))
print("a (channel 2 cursor data with sigfigs):", a_sigfig_exp, "±", a_unc_exp)
print("b (channel 2 cursor data with sigfigs):", b_sigfig_exp, "±", b_unc_exp)


# The calculated RC Value (ideally 0.027)
print(
    "RC value (cursor data with proper units): "
    + str(round(coefficients_exp[1] / 100, 3))
)


# X and Y fits for expected function
x_fit_exp = np.linspace(-1, 11, 10000)
y_fit_exp = expected(x_fit_exp, coefficients_exp[0], coefficients_exp[1])


# Graph data
equation_ch = "V = " + str(a_sigfig_exp) + "e^(-t/" + str(b_sigfig_exp) + ")"
plt.scatter(time_ch, volt_ch, color="red")  # shows our points
plt.plot(x_fit_exp, y_fit_exp, label=equation_ch)  # shows our curved fit


# Graphing
plt.grid()
plt.xlabel("Time (t) (ms)")
plt.ylabel("Voltmeter Readings (v)")
plt.xlim(-1, 11)
plt.legend()
plt.title("Figure 1: Channel 2 Cursor Data")
plt.show()

"""
###########################################################################################
###########################################################################################
"""
# Imported Data section

# Voltage uncertainty
volt2_cap_unc = 0.05 * volt2_cap[1003:1179]  # Taking 5%


# Need to select one curve from the capacitor data for channel2
time2_segment = time_cap[1003:1179]
volt2_segment = volt2_cap[1003:1179]


# Curve fit expected function for capactior data 2
coefficients_cap2, unc_matrix_cap2 = curve_fit(
    expected,
    time2_segment,
    volt2_segment,
    sigma=volt2_cap_unc,
    absolute_sigma=True,
    p0=[6.984924600, 0.000027],
)


# Sigfigs and uncertainty for expected coefficients volt2
a_sigfig_cap2, a_unc_cap2 = sigfig(coefficients_cap2[0], np.sqrt(unc_matrix_cap2[0][0]))
b_sigfig_cap2, b_unc_cap2 = sigfig(coefficients_cap2[1], np.sqrt(unc_matrix_cap2[1][1]))
print("\na (channel 2 imported data with sigfigs):", a_sigfig_cap2, "±", a_unc_cap2)
print("b (channel 2 imported data with sigfigs):", b_sigfig_cap2, "±", b_unc_cap2)


# The calculated RC Value (ideally 0.027)
print(
    "RC value (imported data with proper units): "
    + str(round(coefficients_cap2[1] * 100, 3))
)


# X and Y fits for expected function channel 2 imported
x_fit_cap2 = np.linspace(0.0000028, 0.0005, 10000)
y_fit_cap2 = expected(x_fit_cap2, coefficients_cap2[0], coefficients_cap2[1])


# Graph data
equation_cap2 = "V = " + str(a_sigfig_cap2) + "e^(-t/" + str(b_sigfig_cap2) + ")"
plt.scatter(time2_segment, volt2_segment, color="red")  # shows our points
plt.plot(
    x_fit_cap2,
    y_fit_cap2,
    label=equation_cap2,
)  # shows our curved fit


# Graphing
plt.grid()
plt.xlabel("Time (t) (µs)")
plt.ylabel("Voltmeter Readings (v)")
plt.legend()
plt.title("Figure 2: Channel 2 Imported Data")
plt.show()

"""
###########################################################################################
###########################################################################################
"""

# Residuals (observed - fitted)
fit_ch = expected(time_ch, coefficients_exp[0], coefficients_exp[1])
fit_cap2 = expected(time2_segment, coefficients_cap2[0], coefficients_cap2[1])

residuals_ch = volt_ch - fit_ch
residuals_cap2 = volt2_segment - fit_cap2


# Plot residuals for cursor data
plt.scatter(time_ch, residuals_ch, color="green")
plt.axhline(0, color="black", lw=2)  # Zero line for reference
plt.xlabel("Time (t) (ms)")
plt.ylabel("Residuals (I - Fit)")
plt.title("Figure 3: Residuals for Cursor Data")
plt.grid()
plt.show()


# Plot residuals for imported data
plt.scatter(time2_segment, residuals_cap2, color="green")
plt.axhline(0, color="black", lw=2)  # Zero line for reference
plt.xlabel("Time (t) (µs)")
plt.ylabel("Residuals (I - Fit)")
plt.title("Figure 4: Residuals for Imported Data")
plt.grid()
plt.show()


# Chi-squared for cursor data
chi2_ch = chi2reduced(volt_ch, fit_ch, volt_ch_unc, len(coefficients_exp))
print("\nReduced Chi-squared (cursor data):", chi2_ch)


# Chi-squared for imported data
chi2_cap2 = chi2reduced(volt2_segment, fit_cap2, volt2_cap_unc, len(coefficients_cap2))
print("\nReduced Chi-squared (imported data):", chi2_cap2)
