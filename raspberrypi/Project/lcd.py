from RPLCD.i2c import CharLCD
from time import sleep
import bme280
import smbus2 

import RPi.GPIO as GPIO

port = 1
address = 0x76 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)

try:
    while True:
        bme280_data = bme280.sample(bus, address, calibration_params)
        temp = bme280_data.temperature
        print("Temperature = {:.2f} °C".format(temp))
        sleep(1)  # นี่คือการรอ 1 วินาทีระหว่างการวนลูป
except KeyboardInterrupt:
    GPIO.cleanup()
