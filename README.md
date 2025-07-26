# 🌞 SolarSmart-DAQ: Real-Time Solar Panel Monitoring & Analytics

This project focuses on real-time acquisition of solar panel parameters such as voltage, current, and power, followed by data analysis to derive energy efficiency and performance trends.

## 🛠️ Technologies Used

- Arduino (Sensor interfacing and data acquisition)
- Python (Serial communication & data analysis)
- Matplotlib & Pandas (Plotting + analysis)
- Excel/CSV logging for post-analysis
- Real-time dashboard (Tkinter or Streamlit optional)

## ⚡ Hardware Overview

- Solar Panel (12V mini)
- Voltage and Current Sensors (INA219 / ACS712)
- Arduino UNO/Nano
- USB Serial Connection

## 🖥️ Software Flow

1. **Data is acquired** from sensors connected to the Arduino.
2. **Data is sent via Serial** to the PC.
3. **Python script reads** the serial stream and logs it into a `.csv`.
4. **Analysis script** computes:
   - Instantaneous power
   - Peak efficiency periods
   - Day-to-day trends

## 📟 Arduino Firmware (Basic)

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  float voltage = analogRead(A0) * (5.0 / 1023.0);
  float current = analogRead(A1) * (5.0 / 1023.0); // adjust with calibration
  float power = voltage * current;

  Serial.print(voltage);
  Serial.print(",");
  Serial.print(current);
  Serial.print(",");
  Serial.println(power);

  delay(1000); // 1 second delay
}
```

## 🐍 Python Data Logger

```cpp
import serial
import pandas as pd
from datetime import datetime

ser = serial.Serial('COM3', 9600)
data = []

while True:
    line = ser.readline().decode().strip()
    voltage, current, power = map(float, line.split(','))
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data.append([timestamp, voltage, current, power])
    df = pd.DataFrame(data, columns=['Timestamp', 'Voltage', 'Current', 'Power'])
    df.to_csv("solar_data.csv", index=False)
    print(f"{timestamp} | V: {voltage}V | I: {current}A | P: {power}W")
```

## 📈 Data Analysis Capabilities

- Daily energy generation (kWh)
- Efficiency vs time graphs
- Voltage vs current plotting
- Export to Excel for reporting

## 🔮 Future Scope

- Wireless module (ESP32 + WiFi)
- Cloud dashboard (Thingspeak / Firebase / Grafana)
- Mobile notifications for abnormal dips in output
- ML model for anomaly detection
