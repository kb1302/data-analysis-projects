# Logarithmic relation between CO2 in atmosphere and Temp Change


# imports
import pandas as pd
import csv
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


# Sig fig function
# Modified sigfig function to handle small or zero uncertainty
def sigfig(meas, unc):
    if unc == 0 or np.isnan(unc) or np.isinf(unc):
        # If uncertainty is zero or undefined, return the measurement without rounding
        return meas, unc
    else:
        # Otherwise, calculate significant figures based on uncertainty
        digits = int(np.floor(np.log10(unc)))
        punc = np.round(unc, -digits)
        pmeas = np.round(meas, -digits)
        return pmeas, punc


# read csv file
df = pd.read_csv("co2_temp_1000_cleanend.csv")


# Save data as arrays
year_array = np.asarray(list(df["Year"]))
temp_mean = np.asarray(list(df["temp_mean"]))
temp_std = np.asarray(list(df["temp_std"]))
co2_mean = np.asarray(list(df["co2_mean"]))
co2_std = np.asarray(list(df["co2_std"]))


# Create Logarithmic function to model temp over co2
def log(x, a, b, c):
    return (a * (np.log(x - c))) + b


# Curve fit for temperature over co2
coefficients, unc_matrix = curve_fit(log, co2_mean, temp_mean, absolute_sigma=True)


# Sigfigs and uncertainty for coefficients
a_sigfig, a_unc = sigfig(coefficients[0], unc_matrix[0][0])
b_sigfig, b_unc = sigfig(coefficients[1], unc_matrix[1][1])
c_sigfig, c_unc = sigfig(coefficients[2], unc_matrix[2][2])


# Print out coefficients
# for some reason unc is messed up for c (being around 2000), which messes
# up sigfigs for c, so I just rounded it for now
print("a:", a_sigfig, "±", a_unc)
print("b:", b_sigfig, "±", b_unc)
print("c:", round(coefficients[2]), "±", c_unc)  # insane unc so have to round


# Just to get the fitted curve to extend beyond just the points
x_fit = np.linspace(270, 370, 100)


# Calculate the y-values for the fitted curve
y_fit = log(x_fit, coefficients[0], coefficients[1], coefficients[2])


# Equation with coefficients for the table
equation = (
    "∆T = "
    + str(a_sigfig)
    + " x log(C - "
    + str(round(coefficients[2]))  # insane unc so have to round
    + ") + "
    + str(b_sigfig)
)


# Graph temp and year data points, temperature curve fit
plt.scatter(
    co2_mean, temp_mean, color="red", s=1, label="Data points"
)  # shows our points
plt.plot(x_fit, y_fit, label=equation)  # shows our predicted logarithmic curve fit
plt.grid()
plt.xlabel("Mean CO2 in Atmosphere")
plt.ylabel("Surface Temperature difference from mean of 1970-2000")
plt.xlim(270, 370)
plt.legend()
plt.title("Surface Temperature over CO2 in Atmosphere (Years: 1000-1995)")
plt.show()


"""











"""

# Residual plot for the fit (1000-1995)
residuals = temp_mean - log(co2_mean, coefficients[0], coefficients[1], coefficients[2])
plt.scatter(co2_mean, residuals, color="blue", s=1, label="Residuals")
plt.grid()
plt.xlabel("Mean CO2 in Atmosphere")
plt.ylabel("Residuals (Temp Observed - Temp Fitted)")
plt.title("Residuals for the Temperature-CO2 Logarithmic Fit (Years: 1000-1995)")
plt.legend()
plt.show()

# Calculate standard deviation of residuals
residual_std = np.std(residuals)
print("Standard deviation of residuals:", residual_std)

"""











"""
# Now lets filter out the first 700 years as CO2 didn't change much
after1700 = df[df["Year"] >= 1700]

# Save each data category as arrays (After 1700)
year_after1700 = np.asarray(after1700["Year"])
temp_mean_after1700 = np.asarray(after1700["temp_mean"])
temp_std_after1700 = np.asarray(after1700["temp_std"])
co2_mean_after1700 = np.asarray(after1700["co2_mean"])
co2_std_after1700 = np.asarray(after1700["co2_std"])


# Curve fit for temperature over co2 (after 1700)
coefficients_after1700, unc_matrix_after1700 = curve_fit(
    log, co2_mean_after1700, temp_mean_after1700, absolute_sigma=True
)


# Sigfigs and uncertainty for coefficients
a_sigfig_after1700, a_unc_after1700 = sigfig(
    coefficients_after1700[0], unc_matrix_after1700[0][0]
)
b_sigfig_after1700, b_unc_after1700 = sigfig(
    coefficients_after1700[1], unc_matrix_after1700[1][1]
)
c_sigfig_after1700, c_unc_after1700 = sigfig(
    coefficients_after1700[2], unc_matrix_after1700[2][2]
)


# Print out coefficients (For year 1700+)
print(
    "a (after 1700):", round(coefficients_after1700[0], 2), "±", a_unc_after1700
)  # insane unc so have to round
print(
    "b (after 1700):", round(coefficients_after1700[1], 2), "±", b_unc_after1700
)  # insane unc so have to round
print(
    "c (after 1700):", round(coefficients_after1700[2]), "±", c_unc_after1700
)  # insane unc so have to round


# Just to get the fitted curve to extend beyond just the points
x_fit_after1700 = np.linspace(270, 370, 100)


# Calculate the y-values for the fitted curve
y_fit_after1700 = log(
    x_fit_after1700,
    coefficients_after1700[0],
    coefficients_after1700[1],
    coefficients_after1700[2],
)


# Equation with coefficients for the table
equation_after1700 = (
    "∆T = "
    + str(round(coefficients_after1700[0], 2))
    + " x log(C - "
    + str(round(coefficients_after1700[2]))  # insane unc so have to round
    + ") + "
    + str(round(coefficients_after1700[1], 2))  # insane unc so have to round
)


# Graph temp and year data points, temperature curve fit
plt.scatter(
    co2_mean_after1700, temp_mean_after1700, color="red", s=1, label="Data points"
)  # shows our points
plt.plot(
    x_fit_after1700, y_fit_after1700, label=equation_after1700
)  # shows our predicted logarithmic curve fit
plt.grid()
plt.xlabel("Mean CO2 in Atmosphere")
plt.ylabel("Surface Temperature difference from mean of 1970-2000")
plt.xlim(270, 370)
plt.legend()
plt.title("Surface Temperature over CO2 in Atmosphere (Years: 1700-1995)")
plt.show()

"""










"""

# Split data into two: <1769 and >=1769 (Modern Steam Engine Invention)
before1769 = df[df["Year"] < 1769]
after1769 = df[df["Year"] >= 1769]


# Save each data category as arrays (Before 1769)
year_before1769 = np.asarray(before1769["Year"])
temp_mean_before1769 = np.asarray(before1769["temp_mean"])
temp_std_before1769 = np.asarray(before1769["temp_std"])
co2_mean_before1769 = np.asarray(before1769["co2_mean"])
co2_std_before1769 = np.asarray(before1769["co2_std"])


# Save each data category as arrays (After 1769, inclusive)
year_after1769 = np.asarray(after1769["Year"])
temp_mean_after1769 = np.asarray(after1769["temp_mean"])
temp_std_after1769 = np.asarray(after1769["temp_std"])
co2_mean_after1769 = np.asarray(after1769["co2_mean"])
co2_std_after1769 = np.asarray(after1769["co2_std"])


# Graph of temperature before 1769
plt.hist(temp_mean_before1769, bins=30, density=True, alpha=0.6)
plt.grid()
plt.xlabel("Temperature difference from 1970-2000 mean")
plt.ylabel("Density")
plt.title("Pre-Industrial Surface Temperature Distribution (1000-1769)")
plt.show()


# Graph of Carbon Dioxide in atmosphere before 1769
plt.hist(co2_mean_before1769, bins=30, density=True, alpha=0.6)
plt.grid()
plt.xlabel("Mean Carbon Dioxide in Atmosphere")
plt.ylabel("Density")
plt.title("Pre-Industrial Carbon Dioxide in Atmosphere Distribution (1000-1769)")
plt.show()


# Graph of temperature after 1769
plt.hist(temp_mean_after1769, bins=30, density=True, alpha=0.6)
plt.grid()
plt.xlabel("Temperature difference from 1970-2000 mean")
plt.ylabel("Density")
plt.title("Industrial Period Surface Temperature Distribution (1769-1995)")
plt.show()


# Graph of Carbon Dioxide in atmosphere after 1769
plt.hist(co2_mean_after1769, bins=30, density=True, alpha=0.6)
plt.grid()
plt.xlabel("Mean Carbon Dioxide in Atmosphere")
plt.ylabel("Density")
plt.title("Industrial Period Carbon Dioxide in Atmosphere Distribution (1769-1995)")
plt.show()

"""






"""

# Mean and standard deviation for pre-industrial temperature and CO2
temp_mean_before1769 = np.mean(temp_mean_before1769)
temp_std_before1769 = np.std(temp_mean_before1769)
co2_mean_before1769 = np.mean(co2_mean_before1769)
co2_std_before1769 = np.std(co2_mean_before1769)

# Mean and standard deviation for industrial temperature and CO2
temp_mean_after1769 = np.mean(temp_mean_after1769)
temp_std_after1769 = np.std(temp_mean_after1769)
co2_mean_after1769 = np.mean(co2_mean_after1769)
co2_std_after1769 = np.std(co2_mean_after1769)


# Apply sigfig to pre-industrial temperature and CO2
temp_mean_pre1769_sig, temp_std_pre1769_sig = sigfig(
    temp_mean_before1769, temp_std_before1769
)
co2_mean_pre1769_sig, co2_std_pre1769_sig = sigfig(
    co2_mean_before1769, co2_std_before1769
)

# Apply sigfig to industrial temperature and CO2
temp_mean_post1769_sig, temp_std_post1769_sig = sigfig(
    temp_mean_after1769, temp_std_after1769
)
co2_mean_post1769_sig, co2_std_post1769_sig = sigfig(
    co2_mean_after1769, co2_std_after1769
)

# Print means and standard deviations with proper significant figures
print(
    "Pre-Industrial (1000-1768): Temperature Difference Mean =",
    temp_mean_pre1769_sig,
    "±",
    temp_std_pre1769_sig,
)
print(
    "Pre-Industrial (1000-1768): CO2 Mean =",
    co2_mean_pre1769_sig,
    "±",
    co2_std_pre1769_sig,
)

print(
    "Industrial (1769-1995): Temperature Difference Mean =",
    temp_mean_post1769_sig,
    "±",
    temp_std_post1769_sig,
)
print(
    "Industrial (1769-1995): CO2 Mean =",
    co2_mean_post1769_sig,
    "±",
    co2_std_post1769_sig,
)

"""






"""


# Group data by decades and calculate means for temperature and CO2
df["decade"] = (df["Year"] // 10) * 10
decade_means = df.groupby("decade").mean()
decade_stds = df.groupby("decade").std()

# Identify the first decade where temperature and CO2 diverge significantly
for decade in decade_means.index:
    if (
        decade >= 1500
    ):  # Skips 1000-1499 where its less indicative of an industrial change
        if (
            abs(decade_means.loc[decade, "temp_mean"] - temp_mean_before1769)
            > 2 * temp_std_before1769
            or abs(decade_means.loc[decade, "co2_mean"] - co2_mean_before1769)
            > 2 * co2_std_before1769
        ):
            print(
                "Significant divergence from pre-industrial levels starts around decade:",
                decade,
            )
            break


"""












"""
# Check for temperature overlap
temp_overlap = max(
    temp_mean_before1769 - temp_std_before1769, temp_mean_after1769 - temp_std_after1769
) < min(
    temp_mean_before1769 + temp_std_before1769, temp_mean_after1769 + temp_std_after1769
)
print(
    "Is there temperature overlap between pre-industrial and industrial periods?",
    temp_overlap,
)

# Check for CO2 overlap
co2_overlap = max(
    co2_mean_before1769 - co2_std_before1769, co2_mean_after1769 - co2_std_after1769
) < min(
    co2_mean_before1769 + co2_std_before1769, co2_mean_after1769 + co2_std_after1769
)
print(
    "Is there CO2 overlap between pre-industrial and industrial periods?", co2_overlap
)


# Predict temperature change with doubling of CO2
co2_doubling = co2_mean_before1769 * 2
temp_change_prediction = log(
    co2_doubling, coefficients[0], coefficients[1], coefficients[2]
)
temp_change_prediction_sig, temp_unc = sigfig(
    temp_change_prediction, temp_std_before1769
)  # Using pre-industrial temp std for uncertainty
print(
    "Predicted temperature change from doubling CO2 (from pre-industrial levels):",
    temp_change_prediction_sig,
    "±",
    temp_unc,
    "°C",
)
