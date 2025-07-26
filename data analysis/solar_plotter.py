import serial
import time
import re
import matplotlib.pyplot as plt
from datetime import datetime

# CONFIG
PORT = 'COM3'  # Change to your Arduino port (e.g., '/dev/ttyUSB0' on Linux)
BAUD = 9600
LOG_DURATION = 60  # seconds

# REGEX for parsing serial data
pattern = re.compile(r"([\w\s]+):\s+([-+]?[0-9]*\.?[0-9]+)")

# Data storage
timestamps = []
voltage_log = []
current_log = []
power_log = []
temperature_log = []
humidity_log = []

# Start serial connection
print("Connecting to Arduino...")
ser = serial.Serial(PORT, BAUD, timeout=2)
time.sleep(2)
print("Connected!\nLogging data...")

start_time = time.time()

while (time.time() - start_time) < LOG_DURATION:
    line = ser.readline().decode('utf-8').strip()
    
    if "Solar Voltage" in line:
        data = {}
        timestamp = datetime.now().strftime('%H:%M:%S')
        timestamps.append(timestamp)

        # Read next 5 lines of parameters
        for _ in range(5):
            l = ser.readline().decode('utf-8').strip()
            match = pattern.search(l)
            if match:
                key = match.group(1).strip()
                value = float(match.group(2))
                data[key] = value

        # Store data
        voltage_log.append(data.get("Solar Voltage (V)", 0))
        current_log.append(data.get("Solar Current (A)", 0))
        power_log.append(data.get("Solar Power   (W)", 0))
        temperature_log.append(data.get("Temperature (°C)", 0))
        humidity_log.append(data.get("Humidity    (%)", 0))

ser.close()
print("Data logging complete.\nPlotting...")

# Plotting
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(timestamps, voltage_log, label='Voltage (V)', color='orange')
plt.plot(timestamps, current_log, label='Current (A)', color='blue')
plt.ylabel("Electrical")
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(timestamps, power_log, label='Power (W)', color='green')
plt.ylabel("Power")
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(timestamps, temperature_log, label='Temperature (°C)', color='red')
plt.plot(timestamps, humidity_log, label='Humidity (%)', color='purple')
plt.xlabel("Time")
plt.ylabel("Environment")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
