import json
import csv
import random
import numpy
import datetime

# def generate_time_segment(lowerbound, upperbound):
# 	result = str(random.randint(lowerbound, upperbound))
# 	result = result.zfill(2)
# 	return result

# def generate_random_time():
# 	hour_probability = [0.02, 0.01, 0.01, 0.01, 0.02, 0.02, 0.07, 0.08,
# 	0.03, 0.04, 0.03, 0.03, 0.08, 0.08, 0.09, 0.03, 0.04, 0.03, 0.07, 0.08, 0.03, 0.02, 0.05, 0.03]
# 	hour = str(numpy.random.choice(numpy.arange(0, 24), p = hour_probability))
# 	hour = hour.zfill(2)
# 	minutes = generate_time_segment(0, 59)
# 	seconds = generate_time_segment(0, 59)
# 	timestamp = hour + ":" + minutes + ":" + seconds
# 	return timestamp

# def choose_random_type():
# 	types = ['Fire Accident', 'Medical Assistance', 'Cardiac Arrest']
# 	return random.choice(types)

def generate_random_location():
	east = random.randint(45000, 93500)
	north = random.randint(33750, 62585)
	return str(east) + str(north)

# def generate_alerts():
# 	alerts = []
# 	n = 1000
# 	for i in range(0, n):
# 		alert = {
# 			"id": i,
# 			"location": generate_random_location(),
# 			"time": generate_random_time(),
# 			"type": choose_random_type(),
# 		}
# 		alerts.append(alert)
# 	return alerts

def generate_random_bodytemp():
	temperature = round(random.normalvariate(37, 1), 1)
	return temperature

def generate_random_heartrate():
	heartrate = int(random.normalvariate(100, 30))
	return heartrate

def generate_pressure():
	pressure = 0
	while (pressure < 100000):
		pressure = round(random.expovariate(1/110000), 3)
	return pressure

def generate_gyro():
	gyro = round(random.uniform(0,7), 2)
	return gyro

def generate_fall_gyro():
	# isAllZero = random.uniform(0,1)
	# if (isAllZero > 0.5):
	# 	gyro = 0
	# else:
	# 	gyro = round(random.uniform(0,0.1), 2)
	return 0

def calculate_accel(x, y, z):
	accel = (x**2 + y**2 + z**2)**0.5
	return accel

def generate_events(user):
	global events
	dt = datetime.datetime(2020, 6, 1)
	step = datetime.timedelta(seconds=0.5)
	n = 100
	previous_accel = 0
	for i in range(0, n):
		fall_accident = 0
		cardiac_arrest = 0
		fire_accident = 0

		isNotMoving = random.uniform(0,1)
		if previous_accel > 9 or isNotMoving > 0.7: #30% chance that user is just not moving/false alarm
			gyroX = generate_fall_gyro()
			gyroY = generate_fall_gyro()
			gyroZ = generate_fall_gyro()
			if isNotMoving <= 0.7:
				fall_accident = 1
		else:
			gyroX = generate_gyro()
			gyroY = generate_gyro()
			gyroZ = generate_gyro()


		pressure = generate_pressure()
		if (pressure > 200000):
			isFireAccident = random.uniform(0,1)
			if isFireAccident > 0.3: #30% chance that it is a false alarm
				fire_accident = 1

		heart_rate = generate_random_heartrate()
		if (heart_rate < 30):
			isCardiacArrest = random.uniform(0,1)
			if isCardiacArrest > 0.3:
				cardiac_arrest = 1

		previous_accel = calculate_accel(gyroX, gyroY, gyroZ)
		event = {
			"user": user,
			"timestamp": dt.strftime('%Y-%m-%d %H:%M:%S'),
			"body_temp": generate_random_bodytemp(),
			"heart_rate": heart_rate,
			"pressure": pressure,
			"gyroX": gyroX,
			"gyroY:": gyroY,
			"gyroZ": gyroZ,
			"mgr": generate_random_location(),
			"fall_accident": fall_accident,
			"fire_accident": fire_accident,
			"cardiac_arrest": cardiac_arrest
		}
		dt += step
		events.append(event)
	return events

def generate_users():
	users = 100
	for i in range(1, users+1):
		generate_events(i)

def generate_json(data):
	json_file = open("dataset.json", "w+");		
	json.dump(data, json_file, indent=4)

def generate_csv(data):
	csv_columns = data[0].keys()
	csv_file = open("dataset.csv", "w")
	writer = csv.DictWriter(csv_file, fieldnames = csv_columns)
	writer.writeheader()
	for datarow in data:
		writer.writerow(datarow)
 
def run():
	global events
	generate_users()
	generate_csv(events)


events = []
run()
