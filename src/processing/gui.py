# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './git_repo/OCT_calibration/src/processing/gui2.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import matplotlib.pyplot as plt
from functools import partial

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.frame = 400
        self.vmin = None
        self.vmax = None

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 602)

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Update_Vmin_button = QtWidgets.QPushButton(self.centralwidget)
        self.Update_Vmin_button.setGeometry(QtCore.QRect(900, 310, 93, 28))
        self.Update_Vmin_button.setFont(font)
        self.Update_Vmin_button.setObjectName("Update_Vmin_button")
        self.Update_Vmin_button.clicked.connect(self.update_vmin)

        self.Update_Vmax_button = QtWidgets.QPushButton(self.centralwidget)
        self.Update_Vmax_button.setGeometry(QtCore.QRect(900, 400, 93, 28))
        self.Update_Vmax_button.setFont(font)
        self.Update_Vmax_button.setObjectName("Update_Vmax_button")
        self.Update_Vmax_button.clicked.connect(self.update_vmax)

        self.Vmin_text = QtWidgets.QTextEdit(self.centralwidget)
        self.Vmin_text.setGeometry(QtCore.QRect(900, 340 , 91, 41))
        self.Vmin_text.setObjectName("V min")

        self.Vmax_text = QtWidgets.QTextEdit(self.centralwidget)
        self.Vmax_text.setGeometry(QtCore.QRect(900, 430 , 91, 41))
        self.Vmax_text.setObjectName("V max")

        self.Update_button = QtWidgets.QPushButton(self.centralwidget)
        self.Update_button.setGeometry(QtCore.QRect(560, 310, 93, 28))
        self.Update_button.setFont(font)
        self.Update_button.setObjectName("Update_button")
        self.Update_button.clicked.connect(self.select_frame)

        self.LP11_widget = Canvas(self.centralwidget)
        self.LP11_widget.setGeometry(QtCore.QRect(30, 280, 251, 251))
        self.LP11_widget.setObjectName("LP11_widget")

        self.LP01_widget = Canvas(self.centralwidget)
        self.LP01_widget.setGeometry(QtCore.QRect(30, 10, 251, 251))
        self.LP01_widget.setObjectName("LP01_widget")

        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.Next_button = QtWidgets.QPushButton(self.centralwidget)
        self.Next_button.setGeometry(QtCore.QRect(560, 450, 93, 28))
        self.Next_button.setFont(font)
        self.Next_button.setObjectName("Next_button")
        self.Next_button.clicked.connect(self.Next)

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.Previous_button = QtWidgets.QPushButton(self.centralwidget)
        self.Previous_button.setGeometry(QtCore.QRect(560, 500, 93, 28))
        self.Previous_button.setFont(font)
        self.Previous_button.setObjectName("Previous_button")
        self.Previous_button.clicked.connect(self.Previous)


        self.widget_ratio = Canvas(self.centralwidget)
        self.widget_ratio.setGeometry(QtCore.QRect(560, 10, 251, 251))
        self.widget_ratio.setObjectName("widget_ratio")

        self.histo_LP01 = Canvas(self.centralwidget)
        self.histo_LP01.setGeometry(QtCore.QRect(300, 10, 200, 251))
        self.histo_LP01.setObjectName("histo_LP01")

        self.histo_LP11 = Canvas(self.centralwidget)
        self.histo_LP11.setGeometry(QtCore.QRect(300, 280, 200, 251))
        self.histo_LP11.setObjectName("histo_LP11")

        self.histo_ratio = Canvas(self.centralwidget)
        self.histo_ratio.setGeometry(QtCore.QRect(830, 10, 81, 251))
        self.histo_ratio.setObjectName("histo_ratio")

        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.Save_button = QtWidgets.QPushButton(self.centralwidget)
        self.Save_button.setGeometry(QtCore.QRect(650, 310, 93, 28))
        self.Save_button.setFont(font)
        self.Save_button.setObjectName("Save_button")

        MainWindow.setCentralWidget(self.centralwidget)

        self.Frame_number = QtWidgets.QTextEdit(self.centralwidget)
        self.Frame_number.setGeometry(QtCore.QRect(560, 340, 91, 41))
        self.Frame_number.setObjectName("Frame_number")

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 914, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def load_data(self):
        dir_LP01 = "citrus_LP01.npy"
        dir_LP11 = "citrus_LP11.npy"
        self.LP01_Cscan = np.load(dir_LP01)
        self.LP11_Cscan = np.load(dir_LP11)


    def Next(self):
        self.frame += 1
        self.update()


    def Previous(self):
        self.frame -= 1
        self.update()


    def select_frame(self):
        self.frame = eval(self.Frame_number.toPlainText())
        self.update()


    def update_vmin(self, vmin=None, vmax=None):
        self.vmax = eval(self.Vmax_text.toPlainText())
        self.vmin = eval(self.Vmin_text.toPlainText())
        self.fig_LP01.set_clim([self.vmin, self.vmax])
        self.fig_LP11.set_clim([self.vmin, self.vmax])
        self.update()

    def update_vmax(self, vmin=None, vmax=None):
        self.vmax = eval(self.Vmax_text.toPlainText())
        self.update()


    def set_fig(self):

        LP01_data = np.log(self.LP01_Cscan[:,:,self.frame])
        LP11_data = np.log(self.LP11_Cscan[:,:,self.frame])
        ratio_data = LP01_data - LP11_data
        print(np.shape(self.LP01_Cscan))

        self.fig_LP01 = self.LP01_widget.ax.imshow(LP01_data,
                                                   cmap='gray',
                                                   vmin=self.vmin,
                                                   vmax=self.vmax)

        self.fig_LP11 = self.LP11_widget.ax.imshow(LP11_data,
                                                   cmap='gray',
                                                   vmin=self.vmin,
                                                   vmax=self.vmax)

        self.fig_ratio = self.widget_ratio.ax.imshow(ratio_data,
                                                     cmap='gray')

        plt.tick_params(axis='both', which='minor', labelsize=2)

        self.LP01_widget.ax.set_title('LP01 Cscan "en-face"')
        self.LP11_widget.ax.set_title('LP11 Cscan "en-face"')
        self.widget_ratio.ax.set_title('LP11 ratio "en-face"')

        self.LP01_widget.ax.axis('off')
        self.LP11_widget.ax.axis('off')
        self.widget_ratio.ax.axis('off')

        self.histo_LP01.ax.hist(LP01_data.ravel(),
                                bins=255,
                                orientation='horizontal',
                                density=1
                                )

        self.histo_LP11.ax.hist(LP11_data.ravel(),
                                bins=255,
                                orientation='horizontal',
                                density=1
                                )

        self.histo_ratio.ax.hist(ratio_data.ravel(),
                                bins=255,
                                orientation='horizontal',
                                density=1
                                )

    def update(self):

        self.histo_LP01.ax.clear()
        self.histo_LP11.ax.clear()
        self.histo_ratio.ax.clear()

        LP01_data = np.log(self.LP01_Cscan[:,:,self.frame])
        LP11_data = np.log(self.LP11_Cscan[:,:,self.frame])
        ratio_data = LP01_data - LP11_data


        self.fig_LP01.set_data(LP01_data)

        self.fig_LP11.set_data(LP11_data)

        self.fig_ratio.set_data(ratio_data)


        self.histo_LP01.ax.hist(LP01_data.ravel(),
                                bins=255,
                                orientation='horizontal',
                                density=1
                                )

        self.histo_LP11.ax.hist(LP11_data.ravel(),
                                bins=255,
                                orientation='horizontal',
                                density=1
                                )

        self.histo_ratio.ax.hist(ratio_data.ravel(),
                                bins=255,
                                orientation='horizontal',
                                density=1
                                )


        self.histo_LP01.ax.set_ylim([LP01_data.min(), LP01_data.max()])
        self.histo_LP11.ax.set_ylim([LP11_data.min(), LP11_data.max()])
        self.histo_ratio.ax.set_ylim([ratio_data.min(), ratio_data.max()])

        self.LP01_widget.draw()
        self.LP11_widget.draw()
        self.widget_ratio.draw()
        self.histo_LP01.draw()
        self.histo_LP11.draw()
        self.histo_ratio.draw()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Update_button.setText(_translate("MainWindow", "update"))
        self.Update_Vmin_button.setText(_translate("MainWindow", "Vmin"))
        self.Update_Vmax_button.setText(_translate("MainWindow", "Vmax"))
        self.Next_button.setText(_translate("MainWindow", "Next"))
        self.Previous_button.setText(_translate("MainWindow", "Previous"))
        self.Save_button.setText(_translate("MainWindow", "Save"))
        self.Frame_number.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p></body></html>"))


from canvas import Canvas


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.load_data()
    ui.set_fig()
    sys.exit(app.exec_())
