# Form implementation generated from reading ui file 'design/MainForm.ui'
#
# Created by: PyQt6 UI code generator 6.2.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(662, 538)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblVideo = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblVideo.sizePolicy().hasHeightForWidth())
        self.lblVideo.setSizePolicy(sizePolicy)
        self.lblVideo.setMinimumSize(QtCore.QSize(640, 480))
        self.lblVideo.setAutoFillBackground(True)
        self.lblVideo.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.lblVideo.setText("")
        self.lblVideo.setScaledContents(False)
        self.lblVideo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblVideo.setObjectName("lblVideo")
        self.verticalLayout.addWidget(self.lblVideo)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnStartCapture = QtWidgets.QPushButton(self.centralwidget)
        self.btnStartCapture.setEnabled(True)
        self.btnStartCapture.setMinimumSize(QtCore.QSize(150, 0))
        self.btnStartCapture.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btnStartCapture.setObjectName("btnStartCapture")
        self.horizontalLayout.addWidget(self.btnStartCapture)
        self.btnSwitchDetection = QtWidgets.QPushButton(self.centralwidget)
        self.btnSwitchDetection.setEnabled(False)
        self.btnSwitchDetection.setObjectName("btnSwitchDetection")
        self.horizontalLayout.addWidget(self.btnSwitchDetection)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnTakeBackground = QtWidgets.QPushButton(self.centralwidget)
        self.btnTakeBackground.setEnabled(False)
        self.btnTakeBackground.setObjectName("btnTakeBackground")
        self.horizontalLayout.addWidget(self.btnTakeBackground)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnStartCapture.setText(_translate("MainWindow", "Start capture"))
        self.btnSwitchDetection.setText(_translate("MainWindow", "Start detection"))
        self.btnTakeBackground.setText(_translate("MainWindow", "Take background"))
