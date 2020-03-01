# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './git_repo/OCT_calibration/src/processing/gui2.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(914, 602)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LP01_widget = Canvas(self.centralwidget)
        self.LP01_widget.setGeometry(QtCore.QRect(30, 10, 251, 251))
        self.LP01_widget.setObjectName("LP01_widget")
        self.Update_button = QtWidgets.QPushButton(self.centralwidget)
        self.Update_button.setGeometry(QtCore.QRect(460, 310, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Update_button.setFont(font)
        self.Update_button.setObjectName("Update_button")
        self.LP11_widget = Canvas(self.centralwidget)
        self.LP11_widget.setGeometry(QtCore.QRect(30, 280, 251, 251))
        self.LP11_widget.setObjectName("LP11_widget")
        self.Next_button = QtWidgets.QPushButton(self.centralwidget)
        self.Next_button.setGeometry(QtCore.QRect(460, 450, 93, 28))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Next_button.setFont(font)
        self.Next_button.setObjectName("Next_button")
        self.Previous_button = QtWidgets.QPushButton(self.centralwidget)
        self.Previous_button.setGeometry(QtCore.QRect(460, 500, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Previous_button.setFont(font)
        self.Previous_button.setObjectName("Previous_button")
        self.widget_ratio = Canvas(self.centralwidget)
        self.widget_ratio.setGeometry(QtCore.QRect(460, 10, 251, 251))
        self.widget_ratio.setObjectName("widget_ratio")
        self.histo_LP01 = Canvas(self.centralwidget)
        self.histo_LP01.setGeometry(QtCore.QRect(300, 10, 81, 251))
        self.histo_LP01.setObjectName("histo_LP01")
        self.histo_LP11 = Canvas(self.centralwidget)
        self.histo_LP11.setGeometry(QtCore.QRect(300, 280, 81, 251))
        self.histo_LP11.setObjectName("histo_LP11")
        self.histo_ratio = Canvas(self.centralwidget)
        self.histo_ratio.setGeometry(QtCore.QRect(730, 10, 81, 251))
        self.histo_ratio.setObjectName("histo_ratio")
        self.Save_button = QtWidgets.QPushButton(self.centralwidget)
        self.Save_button.setGeometry(QtCore.QRect(650, 310, 93, 28))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Save_button.setFont(font)
        self.Save_button.setObjectName("Save_button")
        self.Frame_number = QtWidgets.QTextEdit(self.centralwidget)
        self.Frame_number.setGeometry(QtCore.QRect(460, 340, 91, 41))
        self.Frame_number.setObjectName("Frame_number")
        MainWindow.setCentralWidget(self.centralwidget)
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


    def update(self, frame_number=0):

        self.LP01_widget.ax.clear()
        self.LP11_widget.ax.clear()
        self.widget_ratio.ax.clear()

        frame_number = 400

        LP01_data = np.log(self.LP01_Cscan[:,:,frame_number])
        LP11_data = np.log(self.LP11_Cscan[:,:,frame_number])
        ratio_data = LP01_data - LP11_data

        self.LP01_widget.ax.imshow(LP01_data, cmap='gray')
        self.LP11_widget.ax.imshow(LP11_data, cmap='gray')
        self.widget_ratio.ax.imshow(ratio_data, cmap='gray')

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


        self.histo_LP01.ax.set_ylim([LP01_data.min(), LP01_data.max()])
        self.histo_LP11.ax.set_ylim([LP11_data.min(), LP11_data.max()])
        self.histo_ratio.ax.set_ylim([ratio_data.min(), ratio_data.max()])

        self.LP01_widget.show()
        self.LP11_widget.show()
        self.histo_LP01.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Update_button.setText(_translate("MainWindow", "update"))
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
    ui.update()
    sys.exit(app.exec_())
