# Cansat Icaro19

_Este archivo corresponde al software que se ejecuta en la unidad cansat, el cual es el encargado de leer la información de los sensores, componer el mensaje con esa información y enviarlo a través de la red LORA._

## Comenzando 🚀

_El proyecto se puede desarrollar sobre una Raspberry Pi Zero o 3 B+. Los sensores utilizados son el BMP280, LSM303D, SGP30 y VEML6075, todos ellos de Pimoroni._

### Pre-requisitos 📋

_Es necesario tener instalado en su equipo Python 3 y las siguientes librerías:_

```
GPIO
PySerial
BMP280 # Sensor temperatura y presión
LSM303d # Sensor acelerómetro
SGP30 # Sensor C02
VEML6075 # Sensor UV
```

### Instalación 🔧

_Para instalar los distintos paquetes y sensores debes seguir los siguientes pasos:_

_Librería para utilizar puerto GPIO_

```
sudo pip3 install RPi.GPIO
```

_Librería PySerial_

```
sudo pip3 install pyserial
```

_Sensor temperatura y presión BMP280_

```
sudo pip3 install bmp280
```

_Sensor acelerómetro LSM303d_

```
sudo pip3 install lsm303d
```

_Sensor CO2 SGP30_

```
sudo pip3 pimoroni-sgp30
```

_Sensor UV VEML6075_

```
sudo pip3 install veml6075
```

_En el archivo emisor.py puede ver como inicializar y realizar la lectura de datos de los distintos sensores_

## Enlaces: 🛠️

_Las librerías y ejemplos de uso puedes encontrarlos en los siguientes enlaces:_


* [Sensor BMP280](https://github.com/adafruit/Adafruit_CircuitPython_BMP280) - Temperatura y presión
* [Sensor LSM303d](https://github.com/adafruit/Adafruit_CircuitPython_LSM303_Accel) - Acelerómetro y magnetómetro
* [Sensor SGP30](https://github.com/adafruit/Adafruit_CircuitPython_SGP30) - Calidad del aire CO2
* [Sensor VEML6075](https://github.com/adafruit/Adafruit_CircuitPython_VEML6075) - Radiación ultravioleta UV



## Autores ✒️

* **Antonio Otalora** - *Equipo Tierra*
* **Pablo Carrillo** - *Equipo Tierra*
* **David López** - *Equipo Aire*
* **Armando Barragan** - *Equipo Aire*
* **Adrián Murcia** - *Equipo Dieño*
* **Francisco Párraga** - *Equipo Diseño*

## Expresiones de Gratitud 🎁


---
⌨️ con ❤️ por [Villanuevand](https://github.com/Villanuevand) 😊

