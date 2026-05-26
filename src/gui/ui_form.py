# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpinBox,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(871, 511)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayoutCentral = QGridLayout()
        self.gridLayoutCentral.setObjectName(u"gridLayoutCentral")
        self.imgComprLabel = QLabel(self.centralwidget)
        self.imgComprLabel.setObjectName(u"imgComprLabel")
        self.imgComprLabel.setEnabled(False)

        self.gridLayoutCentral.addWidget(self.imgComprLabel, 6, 1, 1, 1)

        self.qLabel = QLabel(self.centralwidget)
        self.qLabel.setObjectName(u"qLabel")
        self.qLabel.setEnabled(False)
        self.qLabel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.qLabel.setFrameShape(QFrame.Shape.StyledPanel)
        self.qLabel.setFrameShadow(QFrame.Shadow.Plain)

        self.gridLayoutCentral.addWidget(self.qLabel, 3, 0, 1, 1)

        self.spinBox = QSpinBox(self.centralwidget)
        self.spinBox.setObjectName(u"spinBox")

        self.gridLayoutCentral.addWidget(self.spinBox, 2, 1, 1, 1)

        self.fileSysPushButton = QPushButton(self.centralwidget)
        self.fileSysPushButton.setObjectName(u"fileSysPushButton")
        self.fileSysPushButton.setAutoFillBackground(False)
        self.fileSysPushButton.setCheckable(False)
        self.fileSysPushButton.setAutoDefault(False)
        self.fileSysPushButton.setFlat(False)

        self.gridLayoutCentral.addWidget(self.fileSysPushButton, 0, 0, 1, 2)

        self.textOrigLabel = QLabel(self.centralwidget)
        self.textOrigLabel.setObjectName(u"textOrigLabel")

        self.gridLayoutCentral.addWidget(self.textOrigLabel, 5, 0, 1, 1)

        self.textComprLabel = QLabel(self.centralwidget)
        self.textComprLabel.setObjectName(u"textComprLabel")

        self.gridLayoutCentral.addWidget(self.textComprLabel, 5, 1, 1, 1)

        self.spinBox_2 = QSpinBox(self.centralwidget)
        self.spinBox_2.setObjectName(u"spinBox_2")

        self.gridLayoutCentral.addWidget(self.spinBox_2, 3, 1, 1, 1)

        self.imgOrigLabel = QLabel(self.centralwidget)
        self.imgOrigLabel.setObjectName(u"imgOrigLabel")
        self.imgOrigLabel.setEnabled(False)

        self.gridLayoutCentral.addWidget(self.imgOrigLabel, 6, 0, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayoutCentral.addWidget(self.pushButton, 4, 0, 1, 2)

        self.fLabel = QLabel(self.centralwidget)
        self.fLabel.setObjectName(u"fLabel")
        self.fLabel.setEnabled(False)
        self.fLabel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.fLabel.setFrameShape(QFrame.Shape.StyledPanel)
        self.fLabel.setFrameShadow(QFrame.Shadow.Plain)

        self.gridLayoutCentral.addWidget(self.fLabel, 2, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayoutCentral, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.imgComprLabel.setText("")
        self.qLabel.setText(QCoreApplication.translate("MainWindow", u"Inserisci la soglia di taglio delle frequenze d (0 <= d <= 2F-2))", None))
        self.fileSysPushButton.setText(QCoreApplication.translate("MainWindow", u"Seleziona un'immagine .bmp dal filesystem", None))
        self.textOrigLabel.setText("")
        self.textComprLabel.setText("")
        self.imgOrigLabel.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Calcola l'immagine compressa", None))
        self.fLabel.setText(QCoreApplication.translate("MainWindow", u"Inserisci la grandezza dei blocchi F (0 < F <= dimensione img)", None))
    # retranslateUi

