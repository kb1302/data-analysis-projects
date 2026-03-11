# Exercise 3 Diode Experiment


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
df = pd.read_csv("data_diode.csv")


# Save data as arrays
power = np.asarray(df["power"])
voltmeter = np.asarray(df["voltmeter"])
ammeter = np.asarray(df["ammeter"])
voltmeter_range = np.asarray(df["voltmeter_range"])
ammeter_range = np.asarray(df["ammeter_range"])


# Split data into two based on if voltage is negative or not
positive_voltage = voltmeter[voltmeter >= 0]
negative_voltage = voltmeter[voltmeter < 0]

positive_current = ammeter[voltmeter >= 0]
negative_current = ammeter[voltmeter < 0]


# Create model power function based off Shockley's diode equation
def positive_power(x, a, b):
    return a * (np.e ** (x * b) - 1)


# Linear function better models the negative voltage components
def linear(x, a, b):
    return (a * x) + b


# Curve fit power function for all data
coefficients, unc_matrix = curve_fit(
    positive_power,
    voltmeter,
    ammeter,
    absolute_sigma=True,
)


# X and Y fits
x_fit = np.linspace(-21, 1, 10000)
y_fit = positive_power(x_fit, coefficients[0], coefficients[1])


# Sigfigs and uncertainty for coefficients
a_sigfig, a_unc = sigfig(
    coefficients[0], np.sqrt(unc_matrix[0][0])
)
b_sigfig, b_unc = sigfig(
    coefficients[1], np.sqrt(unc_matrix[1][1])
)
print("a (all data, with sigfigs):", a_sigfig, "±", a_unc)
print("b (all data, with sigfigs):", b_sigfig, "±", b_unc)


# Graph data
equation = "I = " + str(a_sigfig) + " (e^(" + str(b_sigfig) + "V) - 1)"
plt.scatter(voltmeter, ammeter, color="red")  # shows our points
plt.plot(
    x_fit,
    y_fit,
    label = equation
)  # shows our curved fit


# Graphing
plt.grid()
plt.xlabel("Voltmeter Readings (V)")
plt.ylabel("Ammeter Readings (mA)")
plt.xlim(-21, 2)
plt.ylim(-5, 95)
plt.legend()
plt.title("Figure 1: Power Diode Experiment")
plt.show()


# Curve fit power function for positive volts
coefficients_positive, unc_matrix_positive = curve_fit(
    positive_power,
    positive_voltage,
    positive_current,
    absolute_sigma=True,
)


# Curve fit power function for negative volts
coefficients_negative, unc_matrix_negative = curve_fit(
    linear,
    negative_voltage,
    negative_current,
    absolute_sigma=True,
)


# Sigfigs and uncertainty for coefficients
a_sigfig_pos, a_unc_pos = sigfig(
    coefficients_positive[0], np.sqrt(unc_matrix_positive[0][0])
)
b_sigfig_pos, b_unc_pos = sigfig(
    coefficients_positive[1], np.sqrt(unc_matrix_positive[1][1])
)

a_sigfig_neg, a_unc_neg = sigfig(
    coefficients_negative[0], np.sqrt(unc_matrix_negative[0][0])
)
b_sigfig_neg, b_unc_neg = sigfig(
    coefficients_negative[1], np.sqrt(unc_matrix_negative[1][1])
)


# Print out positive coefficients with sigfigs
print("a (positive, with sigfigs):", a_sigfig_pos, "±", a_unc_pos)
print("b (positive, with sigfigs):", b_sigfig_pos, "±", b_unc_pos)

# Print out negative coefficients with sigfigs
print("a (negative, with sigfigs):", a_sigfig_neg, "±", a_unc_neg)
print("b (negative, with sigfigs):", b_sigfig_neg, "±", b_unc_neg)

# Print out negative coefficients without sigfigs
# Because the numbers are 0 if displayed with appropriate unc
print("a (negative, without sigfigs):", coefficients_negative[0])
print("b (negative, without sigfigs):", coefficients_negative[1])


# X and Y fits
x_fit_positive = np.linspace(0, 0.8, 10000)
y_fit_positive = positive_power(
    x_fit_positive, coefficients_positive[0], coefficients_positive[1]
)


# Graph data
equation_positive = "I = " + str(a_sigfig_pos) + " (e^(" + str(b_sigfig_pos) + "V) - 1)"
plt.scatter(positive_voltage, positive_current, color="red")  # shows our points
plt.plot(
    x_fit_positive, y_fit_positive, label=equation_positive
)  # shows our curved fit


# Graphing
plt.grid()
plt.xlabel("Voltmeter Readings (V)")
plt.ylabel("Ammeter Readings (mA)")
plt.xlim(0.6, 0.8)
plt.legend()
plt.title("Figure 2: Power Diode Experiment (Only Positive Voltage)")
plt.show()


# Negative X and Y fits
x_fit_negative = np.linspace(-21, 0, 10000)
y_fit_negative = linear(
    x_fit_negative, coefficients_negative[0], coefficients_negative[1]
)


# Graph data
equation_negative = "I = " + str(format(coefficients_negative[0], ".2e")) + "V + " + str(format(coefficients_negative[1], ".2e"))
plt.scatter(negative_voltage, negative_current, color="red")  # shows our points
plt.plot(
    x_fit_negative, y_fit_negative, label=equation_negative
)  # shows our curved fit


# Graphing
plt.grid()
plt.xlabel("Voltmeter Readings (V)")
plt.ylabel("Ammeter Readings (mA)")
plt.xlim(-21, 0)
plt.legend()
plt.title("Figure 3: Power Diode Experiment (Only Negative Voltage)")
plt.show()


# Get uncertainties based on range of the multimeters
for i in range(len(ammeter)):
    current_unc = get_multimeter_unc(ammeter[i], ammeter_range[i], False)


for i in range(len(positive_current)):
    positive_current_unc = get_multimeter_unc(
        positive_current[i], ammeter_range[i], False
    )


for i in range(len(negative_current)):
    negative_current_unc = get_multimeter_unc(
        negative_current[i], ammeter_range[i], False
    )


# Residuals for the positive and negative regions
all_fit = positive_power(voltmeter, coefficients[0], coefficients[1])
positive_fit = positive_power(
    positive_voltage, coefficients_positive[0], coefficients_positive[1]
)
negative_fit = linear(
    negative_voltage, coefficients_negative[0], coefficients_negative[1]
)


# Residuals (observed - fitted)
residuals = ammeter - all_fit
positive_residuals = positive_current - positive_fit
negative_residuals = negative_current - negative_fit


# Plot residuals for all data
plt.scatter(voltmeter, residuals, color="green")
plt.axhline(0, color="black", lw=2)  # Zero line for reference
plt.xlabel("Voltage (V)")
plt.ylabel("Residuals (I - Fit)")
plt.title("Figure 4: Residuals for All Data")
plt.grid()
plt.show()


# Plot residuals for positive voltage
plt.scatter(positive_voltage, positive_residuals, color="green")
plt.axhline(0, color="black", lw=2)  # Zero line for reference
plt.xlabel("Voltage (V)")
plt.ylabel("Residuals (I - Fit)")
plt.title("Figure 5: Residuals for Positive Voltage")
plt.grid()
plt.show()


# Plot residuals for negative voltage
plt.scatter(negative_voltage, negative_residuals, color="green")
plt.axhline(0, color="black", lw=2)  # Zero line for reference
plt.xlabel("Voltage (V)")
plt.ylabel("Residuals (I - Fit)")
plt.title("Figure 6: Residuals for Negative Voltage")
plt.grid()
plt.show()


# Chi-squared for all data
chi2_all = chi2reduced(ammeter, all_fit, current_unc, len(coefficients))
print("Reduced Chi-squared (all data):", chi2_all)


# Chi-squared for positive voltage
chi2_positive = chi2reduced(
    positive_current, positive_fit, positive_current_unc, len(coefficients_positive)
)
print("Reduced Chi-squared (positive region):", chi2_positive)


# Chi-squared for negative voltage
chi2_negative = chi2reduced(
    negative_current, negative_fit, negative_current_unc, len(coefficients_negative)
)
print("Reduced Chi-squared (negative region):", chi2_negative)
