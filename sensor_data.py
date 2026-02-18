import adafruit_bme680
import time 
import board
import csv
import numpy as np
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
import serial
from adafruit_pm25.uart import PM25_UART
import sys

arguments = sys.argv
print(arguments)

data_path = 'data/' + arguments[1]

runtime = int(arguments[2])

i2c = board.I2C()

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_level = 1013.25

now = time.time()

stop = runtime*60

reset_pin = None

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

pm25 = PM25_UART(uart, reset_pin)

meta = ['time'] 
particle_list = ["particles 03um", "particles 05um", "particles 10um", "particles 25um", "particles 50um", "particles 100um"]
weather_list = ["Temperature C", "Gas Ohm", "Humidity %%" , "Pressure hPa", "Altitude meters"]
meta = meta+particle_list+weather_list
file = open(data_path, 'w', newline = None)
csvwriter = csv.writer(file, delimiter = ',')
csvwriter.writerow(meta)


while now < stop:
	data_weather = [now, bme680.temperature, bme680.gas, bme680.relative_humidity , bme680.pressure , bme680.altitude]
	temp = ("Temperature: %0.1f c " % bme680.temperature)
	gas = ("Gas: %d ohm: " % bme680.gas)
	hum = ("Humidity: %0.1f %% " % bme680.relative_humidity)
	press = ("Pressure: %0.3f hPa " % bme680.pressure)
	alt = ("Altitude = %0.2f meters " % bme680.altitude)
	value7 =bme680.temperature
  value8 =bme680.gas
  value9 =bme680.relative_humidity
  value10 =bme680.pressure
  value11 = bme680.altitude
	data_string = [temp, gas, hum, press, alt]
  for i, data in enumerate(data_weather):
		data_string[i] += str(data)
    
  try:
      aqdata = pm25.read()
      # print(aqdata)
  except RuntimeError:
      print("Unable to read from sensor, retrying...")
      continue
    
  nowtime = time.time()
  value1 = aqdata["particles 03um"]
  value2 = aqdata["particles 05um"]
  value3 = aqdata["particles 10um"]
  value4 = aqdata["particles 25um"]
  value5 = aqdata["particles 50um"]
  value6 = aqdata["particles 100um"]

  csvwriter.writerow([nowtime, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11])

  
        
file.close()
