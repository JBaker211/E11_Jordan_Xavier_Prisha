import adafruit_bme680
import time 
import board

i2c = board.I2C()

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_level = 1013.25

now = time.time()

stop = now +300



while now < stop:
	data_weather = [now, bme680.temperature, bme680.gas, bme680.relative_humidity , bme680.pressure , bme680.altitude]
	
	snow = "Time: "
	temp = ("Temperature: %0.1f c " % bme680.temperature)
	gas = ("Gas: %d ohm: " % bme680.gas)
	hum = ("Humidity: %0.1f %% " % bme680.relative_humidity)
	press = ("Pressure: %0.3f hPa " % bme680.pressure)
	alt = ("Altitude = %0.2f meters " % bme680.altitude)
	
	data_string = [snow, temp, gas, hum, press, alt]
	
	for i, data in enumerate(data_weather):
		data_string[i] += str(data)
	
	print(data_string)
	
	now += 1
	time.sleep(1)
