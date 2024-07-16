from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QLabel, QMenuBar, QPushButton, QStatusBar, QWidget)

class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        if not MainMenu.objectName():
            MainMenu.setObjectName(u"MainMenu_ui")
        MainMenu.resize(800, 600)
        MainMenu.setMinimumSize(QSize(800, 600))
        MainMenu.setMaximumSize(QSize(800, 600))
        self.centralwidget = QWidget(MainMenu)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ExitButton = QPushButton(self.centralwidget)
        self.ExitButton.setObjectName(u"ExitButton")
        self.ExitButton.setGeometry(QRect(300, 400, 200, 80))
        self.ExitButton.setMinimumSize(QSize(200, 80))
        self.ExitButton.setMaximumSize(QSize(200, 80))
        font = QFont()
        font.setPointSize(16)
        self.ExitButton.setFont(font)
        self.ManualButton = QPushButton(self.centralwidget)
        self.ManualButton.setObjectName(u"ManualButton")
        self.ManualButton.setGeometry(QRect(300, 300, 200, 80))
        self.ManualButton.setMinimumSize(QSize(200, 80))
        self.ManualButton.setMaximumSize(QSize(200, 80))
        self.ManualButton.setFont(font)
        self.EditorButton = QPushButton(self.centralwidget)
        self.EditorButton.setObjectName(u"EditorButton")
        self.EditorButton.setGeometry(QRect(300, 200, 200, 80))
        self.EditorButton.setMinimumSize(QSize(200, 80))
        self.EditorButton.setMaximumSize(QSize(200, 80))
        self.EditorButton.setFont(font)
        self.AppName = QLabel(self.centralwidget)
        self.AppName.setObjectName(u"AppName")
        self.AppName.setGeometry(QRect(225, 70, 350, 100))
        self.AppName.setMinimumSize(QSize(350, 100))
        self.AppName.setMaximumSize(QSize(350, 100))
        font1 = QFont()
        font1.setPointSize(36)
        font1.setWeight(QFont.DemiBold)
        self.AppName.setFont(font1)
        self.AppName.setAlignment(Qt.AlignCenter)
        MainMenu.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainMenu)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        MainMenu.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainMenu)
        self.statusbar.setObjectName(u"statusbar")
        MainMenu.setStatusBar(self.statusbar)

        self.retranslateUi(MainMenu)

        QMetaObject.connectSlotsByName(MainMenu)
    # setupUi

    def retranslateUi(self, MainMenu):
        MainMenu.setWindowTitle(QCoreApplication.translate("MainMenu_ui", u"Main Menu", None))
        self.ExitButton.setText(QCoreApplication.translate("MainMenu_ui", u"Exit", None))
        self.ManualButton.setText(QCoreApplication.translate("MainMenu_ui", u"Manual", None))
        self.EditorButton.setText(QCoreApplication.translate("MainMenu_ui", u"Editor", None))
        self.AppName.setText(QCoreApplication.translate("MainMenu_ui", u"AudioMorph", None))
    # retranslateUi