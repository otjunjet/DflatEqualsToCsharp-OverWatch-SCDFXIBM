import math
import csv

# Check whether the person fallen
def fallcheck(total_accel, previous_accel):
    # Person fall at an accel near gravity, then abruptly stop when he hit the ground
    if previous_accel > 9.0:
        if total_accel < 0.5:
            print(f"Person has fallen at {address} on {timestamp}")
            # Further develop to send help (if needed) to CFR
            return 1
    else:
        return 0

# Check whether the person tio cardiac arrest
def cardiac_arrest(heart_rate):
    # Official cardiac arrest detection
    if heart_rate < 30:
        print(f"Cardiac arrest confirmed at {address} on {timestamp}, notifying hospital")
        # Further develop to send an emergency notification to SCDF to activate hospital and nearby CFRs
        return 1
    # Possible issue that can escalate to a cardiac arrest
    elif heart_rate > 180:
        print(f"Possible heart issue at {address} on {timestamp}, notifying hospital")
        # Further develop to schedule an appointment with hospital or whatever
        return 1
    else:
        return 0

# Check whether got fire
def atmospheric_temperature(pressure):
    # Temp affects pressure, at that point, there is likely a fire
    if pressure > 300000:
        print(f"Fire detected at {address} on {timestamp} notifying SCDF")
        # Further develop to send an emergency notification to SCDF to activate fire fighters
        return 1
    else:
        return 0

# Check whether watch is worn, based on body temp
def bodypresence(body_temp):
    if 39.9 > body_temp > 35.5:
        return 1
    else:
        return 0

# Reading from dataset
address = input("Location: ")
prev_accel = 0

# Reading from dataset (for now), can read directly in a watch and send event immediately to SCDF
with open("dataset.csv", "r") as file:
    data = csv.DictReader(file)
    for row in data:
        total_accel = math.sqrt((float(row["gyroX"]) ** 2) + (float(row["gyroY"]) ** 2) + (float(row["gyroZ"]) ** 2))
        timestamp = row["timestamp"]
        # Check if someone is wearing a watch, then check for fall and cardiac arrest
        if bodypresence(float(row["body_temp"])) == 1:
            fallcheck(total_accel, prev_accel)
            cardiac_arrest(int(row["heart_rate"]))
        atmospheric_temperature(float(row["pressure"]))
        prev_accel = total_accel