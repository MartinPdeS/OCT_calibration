import matplotlib
matplotlib.use('Qt4Agg')

import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

qtCreatorFile = "./src/processing/gui.ui" # my Qt Designer file

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.csvbutton.clicked.connect(self.plot)


    def load_data(self):
        dir = "citrus_LP11.npy"
        self.Cscan = np.load(dir)


    def update(self):

        #self.canvas.figure.cla()  # clear the axes content
        self.ax_LP01.imshow(self.Cscan[:,:,4],cmap='gray')
        self.canvas.figure.draw_idle()  # actually draw the new content


    def plot(self):

        self.ax_LP01 = self.canvas.figure.add_subplot(121)
        self.ax_LP01.set_title('LP01 en-face')

        self.ax_LP11 = self.canvas.figure.add_subplot(122)
        self.ax_LP11.set_title('LP11 en-face')

        self.ax_LP01.imshow(self.Cscan[:,:,350],cmap='gray')
        self.ax_LP11.imshow(self.Cscan[:,:,350], cmap='gray')
        self.canvas.draw()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    window.load_data()
    window.plot()
    window.update()
    sys.exit(app.exec_())
