import serial
from PyQt5.QtCore import pyqtSignal, QThread
import time

class serialThreadClass(QThread):
    mensaje = pyqtSignal(str)


    def __init__(self, parent = None):
        super().__init__(parent)
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        time.sleep(2)


    def run(self):
        while True:

            error = 0


            lectura = self.ser.readline()


            try:
                lectura = lectura.decode()
            except UnicodeDecodeError:
                print ("Error de lectura")
                error = 1

            if not error and lectura[0:3] == "MMM":
                self.mensaje.emit(str(lectura))  # Pipe con la aplicacion
            else:
                print ("Esperando señal")
                self.mensaje.emit("error")

            time.sleep(0.5)



    def sendSerial(self):
        self.ser.write(b'A')
