import serial
from PyQt5.QtCore import pyqtSignal, QThread
import time

class serialThreadClass(QThread):
    mensaje = pyqtSignal(str)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        time.sleep(2)

    def run(self):
        while True:

            lectura = self.ser.readline()
            self.mensaje.emit(str(lectura.decode()))  # Pipe con la aplicacion
            print (lectura)
            time.sleep(1)

    def sendSerial(self):
        self.ser.write(b'A')
