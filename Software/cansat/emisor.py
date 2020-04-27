
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import serial
import time
import sys
import veml6075


#SENSOR SGP30 - sensor de calidad del aire
from sgp30 import SGP30

# SENSOR SMP280 - temperatura y presión
from bmp280 import BMP280

#SENSOR LSM303D  - acelerómetro
from lsm303d import LSM303D
	
	
	
M0 = 22
M1 = 27
#MODE = ["BROADCAST_AND_MONITOR","P2P"]

CFG_REG = [b'\xC2\x00\x09\xFF\xFF\x00\x62\x00\x17\x03\x00\x00',
		   b'\xC2\x00\x09\x00\x00\x00\x62\x00\x17\x03\x00\x00']
RET_REG = [b'\xC1\x00\x09\xFF\xFF\x00\x62\x00\x17\x03\x00\x00',
		   b'\xC1\x00\x09\x00\x00\x00\x62\x00\x17\x03\x00\x00']
r_buff = ""
delay_temp = 1

	
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(M0,GPIO.OUT)
GPIO.setup(M1,GPIO.OUT)

GPIO.output(M0,GPIO.LOW)
GPIO.output(M1,GPIO.HIGH)
time.sleep(0.01)

ser = serial.Serial("/dev/ttyS0",9600)
ser.flushInput()

#Inicializar el BMP280
try:
	from smbus2 import SMBus
except:
	from smbus import SMBus

bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)


baseline_values = []
baseline_size = 26

print("inicializando linea base...")
for i in range(baseline_size):
	pressure = bmp280.get_pressure()
	baseline_values.append(pressure)
	time.sleep(1)
	print(i,"% calculando linea base") 
baseline = sum(baseline_values[:-25]) / len(baseline_values[:-25])

#Inicializar el LSM303D
lsm = LSM303D(0x1d)

#Inicializar y crear instancia del VEML6075
uv_sensor = veml6075.VEML6075(i2c_dev=bus)
uv_sensor.set_shutdown(False)
uv_sensor.set_high_dynamic_range(False)
uv_sensor.set_integration_time('100ms') #por defecto 100ms

#Inicialización del sensor de calidad de aire
sgp30 = SGP30()
print("Sensor warming up, please wait...")
def crude_progress_bar():
    sys.stdout.write('.')
    sys.stdout.flush()

sgp30.start_measurement(crude_progress_bar)
sys.stdout.write('\n')


try :

	if ser.isOpen() :
		print("It's setting P2P mode")
		ser.write(CFG_REG[1])
		contador = 0
		
	while True :
				
		
		
		if ser.inWaiting() > 0 :
			time.sleep(0.1)
			r_buff = ser.read(ser.inWaiting())
			if r_buff == RET_REG[1] :
				print("P2P modo activado")
				GPIO.output(M1,GPIO.LOW)
				time.sleep(0.01)
				r_buff = ""
			if r_buff != "" :
				print("receive a P2P message:")
				print(r_buff)
				r_buff = ""
		delay_temp += 1
				
		if delay_temp > 5000 :
			
			# LEER DATOS
			print ("Leyendo temperatura...")
			temperature = bmp280.get_temperature()
							
			print ("Leyendo presion...")
			pressure = bmp280.get_pressure()
							
			print ("Leyendo altitud...")
			altitude = bmp280.get_altitude(qnh=baseline)
							
			print ("Leyendo acelerometro...")
			xyz = lsm.accelerometer()
			accel = "{:06.2f}:{:06.2f}:{:06.2f}".format(*xyz)
			
			print ("Leyendo calidad del aire...")
			airq = sgp30.get_air_quality()
			print (airq)

			print ("Leyendo radiacion uv...")
			uva, uvb = uv_sensor.get_measurements()
			print ("----> Medidas  tomadas")
			uv_comp1, uv_comp2 = uv_sensor.get_comparitor_readings()
			print ("----> Lecturas comparador")
			uv_indices = uv_sensor.convert_to_index(uva, uvb, uv_comp1, uv_comp2)

			print('UVA : {0} UVB : {1} COMP 1 : {2} COMP 2 : {3}'.format(uva, uvb, uv_comp1, uv_comp2))
			print('UVA INDEX: {0[0]} UVB INDEX : {0[1]} AVG UV INDEX : {0[2]}\n'.format(uv_indices))
			
			
			#mensaje = str(contador) +" | Temperatura: "+str(round(temperature,2))+" | Presion: "+str(round(pressure,2))+"\r\n"
			mensaje ="MMM" + "," + str(round(temperature,2))+","+str(round(pressure,2))+","+ str(round(altitude,2))+","+ accel + "," + str(airq.equivalent_co2) + "," + str(airq.total_voc) + "," + str(uv_indices[0]) +  "\r\n"
			print(mensaje)
			
			ser.write(mensaje.encode())
			delay_temp = 0
			contador += 1

			# Almacenamiento de datos en archivo
			# Preparamos el mensaje a escribir, indicando al comienzo el numero de lectura
			# y eleminamos el codigo de verificacion de mensaje MMM
			with open('data.csv', 'a') as f:
				mensaje = str(contador)+mensaje[3:]  # Preparacion del mensaje
				f.writelines(mensaje) # Escritura de la lectura

except :
	if ser.isOpen() :
		ser.close()
	GPIO.cleanup()
