import time
from bmp280 import BMP280 

try:
	from smbus2 import SMBus
except:
	from smbus import SMBus
	
#Inicializar el BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

while True:
	temperature = bmp280.get_temperature()
	pressure = bmp280.get_pressure()
	print ("{:05.2f}*C {:05.2f}hpa".format(temperature,pressure))
	time.sleep(1)

