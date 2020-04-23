from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ground_station import *
import pyqtgraph as pg


from serialThreadFile import serialThreadClass

import sys

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        #pg.setConfigOption("background", "w") # Descomentar para interface blanca
        #pg.setConfigOption("foreground", "k") # Descomentar para interface blanca
        self.setupUi(self)

        self.inicializar_uvmeter()

        self.lectura = []

        self.mySerial = serialThreadClass()
        self.mySerial.mensaje.connect(self.leer_serial)

        self.mySerial.start()

        self.x = list(range(10))
        self.y = [0 for _ in range(10)]

        self.temperature_y = [0 for _ in range(10)]
        self.presure_y = [0 for _ in range(10)]
        pen = pg.mkPen(color=(0, 100, 255))

        self.graphicsConfig(self.graphicsTemperature, "Sensor Temperatura", "Temperatura (ºC)", "Lectura", self.temperature_y)
        self.data_line_temp = self.graphicsTemperature.plot(self.x, self.temperature_y, pen=pen, symbol="+")

        self.graphicsConfig(self.graphicsPresure, "Sensor Presión", "Presión (hPa)", "Lectura", self.presure_y)
        self.data_line_pres = self.graphicsPresure.plot(self.x, self.presure_y, pen=pen, symbol="+")

        # No es necesario el timer, utilizamos signal para actualizar
        #self.timer = QtCore.QTimer()
        #self.timer.setInterval(1000)
        #self.timer.timeout.connect(self.update_plot_data)
        #self.timer.start()

    def graphicsConfig(self, graphics,sensor, lbl_y, lbl_x, lista):
        graphics.setYRange(0, 40, padding=0)
        graphics.showGrid(x=True, y=True)
        graphics.setTitle(sensor)
        graphics.setLabel('left', lbl_y)
        graphics.setLabel('bottom', lbl_x)


    def update_plot_data(self):
        self.x = self.x[1:] # Eliminamos el primer elemento de la lista
        self.x.append(self.x[-1] + 1) # Añadimos nuevo elemento sumando 1 al anterior
        self.data_line_temp.setData(self.x, self.temperature_y) # Actualizamos la curva de la grafica
        self.data_line_pres.setData(self.x, self.presure_y)



    def leer_serial(self, msg):
        self.textEdit_2.append(msg)
        self.temperature_y = self.temperature_y[1:] # Eliminamos el primer valor de la lista
        self.presure_y = self.presure_y[1:]

        self.lectura = msg.split(",")
        print(self.lectura[0])
        print(self.lectura[1])
        print(self.lectura[2])
        print(self.lectura[3])

        self.lcdTemperature.display(float(self.lectura[1]))
        self.lcdPresure.display(float(self.lectura[2]))
        self.lcdAltitude.display(float(self.lectura[3]))
        self.lcdArqppm.display(float(self.lectura[5]))
        self.lcdArqppb.display(float(self.lectura[6]))
        self.lcdUV.display(float(self.lectura[7]))
        self.actualizar_uvmeter(float(self.lectura[7])*10)

        self.temperature_y.append(float(self.lectura[1]))
        self.presure_y.append(float(self.lectura[2]))

        self.update_plot_data()



    def plot(self, h, t):
        self.graphicsTemperature.plot(h,t)
        self.graphicsPresure.plot()

    def inicializar_uvmeter(self):
        self.niveles = {1: self.nivel1, 2: self.nivel2, 3: self.nivel3, 4: self.nivel4, 5: self.nivel5, 6: self.nivel6,
                        7: self.nivel7
            , 8: self.nivel8, 9: self.nivel9, 10: self.nivel10, 11: self.nivel11}
        niv = self.niveles.values()


        for n in niv:
            n.setVisible(False)

    def actualizar_uvmeter(self, valor):
        for i in range(1, 12):
            if i <= valor:
                self.niveles[i].setVisible(True)
            else:
                self.niveles[i].setVisible(False)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()