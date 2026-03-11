# Millikan Free Choice Experiment

# imports
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import csv
from matplotlib import pyplot as plt
import os
import glob
import re


# Constants
CALIBRATION_LEFT = 1 / 540  # mm/px for the left device
CALIBRATION_RIGHT = 1 / 520  # mm/px for the right device
DELTA_T = 0.1  # Time step in seconds (10Hz sampling rate)


# Stop voltage data
stop_voltage_data = {
    "1": 260.1,
    "2": 111.4,
    "3": 304.2,
    "4": 83.7,
    "5": 98.4,
    "6": 155.3,
    "7": 149.9,
    "8": 101.1,
    "9": 278.1,
    "10": 196.2,
    "11": 238.0,
    "12": 131.1,
    "13": 94.0,
    "14": 288.5,
    "15": 612.5,
    "16": 357.2,
    "17": 245.0,
    "18": 215.7,
    "19": 341.0,
    "20": 266.6,
    "21": 185.9,
    "22": 299.5,
    "23": 250.4,
    "24": 217.7,
    "25": 144.4,
    "26": 168.5,
    "27": 433.9,
    "28": 516.5,
    "29": 342.1,
    "30": 166.9,
    "31": 526.3,
    "32": 205.3,
    "33": 159.2,
    "34": 160.9,
    "35": 443.5,
    "36": 253.5,
    "37": 292.9,
    "38": 352.6,
    "39": 292.4,
    "40": 372.2,
    "41": 358.4,
    "42": 290.8,
    "43": 121.7,
    "44": 563.2,
    "45": 170.0,
    "46": 161.1,
    "47": 186.3,
    "48": 212.4,
    "49": 257.9,
    "50": 374.4,
}


# Path to the folder containing the Excel files
folder_path = "./data/"


# Get a list of all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))


# Function to calculate speeds for a single file
def calculate_average_speed(file_path, calibration_factor):
    # Read the CSV file (assuming no header)
    data = pd.read_csv(file_path, header=None)
    positions_px = data.iloc[:, 0]  # Extract the column of positions in pixels

    # Convert positions from pixels to millimeters
    positions_mm = positions_px * calibration_factor

    # Calculate speeds (differences in positions / DELTA_T)
    speeds = (positions_mm.diff() / DELTA_T).dropna().values

    # Calculate and return the average speed
    average_speed = np.mean(speeds) / 1000  # convert to meters/s
    return average_speed


# Function to determine calibration factor based on the oil drop number
# This is because we switched setups, starting with the 15th oil drop
def get_calibration_factor(oil_drop_number):
    # Convert oil drop number to integer for comparison
    oil_drop_number = int(oil_drop_number)
    if oil_drop_number >= 15:
        return CALIBRATION_LEFT  # Left device (1/540)
    else:
        return CALIBRATION_RIGHT  # Right device (1/520)


# Store the average speeds for each oil drop
average_speeds = []

# Store the results with original oil drop numbers
results = []

# Process all files and calculate average speeds and radii
for file in csv_files:
    try:
        # Extract the original oil drop number from the filename
        oil_drop_number = re.search(r"\d+", os.path.basename(file))
        oil_drop_number = oil_drop_number.group() if oil_drop_number else "Unknown"

        # Get the calibration factor for this oil drop
        calibration_factor = get_calibration_factor(oil_drop_number)

        # Get the Stop Voltage for the oil drop (default to "Unknown" if not found)
        stop_voltage = stop_voltage_data.get(oil_drop_number, "Unknown")

        # Calculate the average speed for the current file
        average_speed = calculate_average_speed(file, calibration_factor)

        # Calculate the radius using the equation r = sqroot(9vn/2gp)
        radius = np.sqrt(
            (9 * (1.827 * (10 ** (-5))) * average_speed) / (2 * 9.8 * (875.3 - 1.204))
        )

        # Calculate the volume using the equation V = 4/3 * pi * r^3
        volume = (4 / 3) * np.pi * (radius**3)
        
        # Calculate oil mass using m = volume * density
        oil_mass = volume * 875.3
        
        # Calculate air mass using mass(air) = volume(oil) * air density
        air_mass = volume * 1.204

        # Calculate charge using = (distaneBetweenPlates * gravity * (oilMass - airMass) ) / stopVoltage
        charge = (0.006 * 9.8 * (oil_mass - air_mass) ) /stop_voltage
        
        # Calculate number of elementary charges
        elementary_charge = charge / (1.602 * (10**(-19)))
        
        # Append the results
        results.append(
            {
                "Oil Drop Number": oil_drop_number,
                "Stop Voltage (V)": stop_voltage,
                "Average Speed (m/s)": average_speed,
                "Radius (m)": radius,
                "Volume (m^3)": volume,
                "Oil Mass (kg)": oil_mass,
                "Air Mass (kg)": air_mass,
                "Charge (C)": charge,
                "Number of Elementary Charge": elementary_charge
            }
        )

    except Exception as e:
        print("Error processing " + file + ": " + str(e))

# Save the results to a CSV
output_path = os.path.join(folder_path, "oil_drops_results.csv")
pd.DataFrame(results).to_csv(output_path, index=False)
print("\nResults saved to " + output_path)


# We know now the average terminal speed of each falling droplet
# We also know the stopping voltage required to keep each droplet afloat
# 1) we need to find the mass of droplets using mass = density * volume
# The density is a constant, but to find volume we need the radius
# r = square root ( 9vn / 2gp ) where p = p_oil - p_air
# Now we found the radius, we can fine the volume:
# volume = 4/3 * pi * r^3
# Now we find the mass using mass = density * volume
# 2) Find the charge using the equation:
# q = (distaneBetweenPlates * gravity * (oilMass - airMass) ) / stopVoltage
# Added the stopVoltage data
# Then we need to analyze the number of elementary charges so we:
# divide the charge by the elementary charge: q/ 1.602 x 10e-19