from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,QSize, Qt)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QLabel, QMenuBar,QPushButton, QStatusBar, QWidget)

class Ui_Editor(object):
    def setupUi(self, Editor):
        if not Editor.objectName():
            Editor.setObjectName(u"Editor")
        Editor.resize(1000, 600)
        Editor.setMinimumSize(QSize(1000, 600))
        Editor.setMaximumSize(QSize(1000, 600))
        self.centralwidget = QWidget(Editor)
        self.centralwidget.setObjectName(u"centralwidget")
        self.RecordButton = QPushButton(self.centralwidget)
        self.RecordButton.setObjectName(u"RecordButton")
        self.RecordButton.setGeometry(QRect(210, 390, 150, 50))
        self.RecordButton.setMinimumSize(QSize(150, 50))
        self.RecordButton.setMaximumSize(QSize(150, 50))
        font = QFont()
        font.setPointSize(12)
        self.RecordButton.setFont(font)
        self.UniteButton = QPushButton(self.centralwidget)
        self.UniteButton.setObjectName(u"UniteButton")
        self.UniteButton.setGeometry(QRect(425, 390, 150, 50))
        self.UniteButton.setMinimumSize(QSize(150, 50))
        self.UniteButton.setMaximumSize(QSize(150, 50))
        self.UniteButton.setFont(font)
        self.LoadButton = QPushButton(self.centralwidget)
        self.LoadButton.setObjectName(u"LoadButton")
        self.LoadButton.setGeometry(QRect(210, 470, 150, 50))
        self.LoadButton.setMinimumSize(QSize(150, 50))
        self.LoadButton.setMaximumSize(QSize(150, 50))
        self.LoadButton.setFont(font)
        self.SaveButton = QPushButton(self.centralwidget)
        self.SaveButton.setObjectName(u"SaveButton")
        self.SaveButton.setGeometry(QRect(640, 470, 150, 50))
        self.SaveButton.setMinimumSize(QSize(150, 50))
        self.SaveButton.setMaximumSize(QSize(150, 50))
        self.SaveButton.setFont(font)
        self.ChangeButton = QPushButton(self.centralwidget)
        self.ChangeButton.setObjectName(u"ChangeButton")
        self.ChangeButton.setGeometry(QRect(640, 390, 150, 50))
        self.ChangeButton.setMinimumSize(QSize(150, 50))
        self.ChangeButton.setMaximumSize(QSize(150, 50))
        self.ChangeButton.setFont(font)
        self.CutButton = QPushButton(self.centralwidget)
        self.CutButton.setObjectName(u"CutButton")
        self.CutButton.setGeometry(QRect(425, 470, 150, 50))
        self.CutButton.setMinimumSize(QSize(150, 50))
        self.CutButton.setMaximumSize(QSize(150, 50))
        self.CutButton.setFont(font)
        self.PlayPauseButton = QPushButton(self.centralwidget)
        self.PlayPauseButton.setObjectName(u"PlayPauseButton")
        self.PlayPauseButton.setGeometry(QRect(410, 150, 101, 31))
        self.PlayPauseButton.setFont(font)
        self.AudioStatusLabel = QLabel(self.centralwidget)
        self.AudioStatusLabel.setObjectName(u"AudioStatusLabel")
        self.AudioStatusLabel.setGeometry(QRect(395, 100, 210, 30))
        self.AudioStatusLabel.setFont(font)
        self.AudioStatusLabel.setAlignment(Qt.AlignCenter)
        self.AppName = QLabel(self.centralwidget)
        self.AppName.setObjectName(u"AppName")
        self.AppName.setGeometry(QRect(375, 20, 250, 75))
        self.AppName.setMinimumSize(QSize(250, 75))
        self.AppName.setMaximumSize(QSize(250, 75))
        font1 = QFont()
        font1.setPointSize(18)
        font1.setWeight(QFont.DemiBold)
        self.AppName.setFont(font1)
        self.AppName.setAlignment(Qt.AlignCenter)
        self.ReturnButton = QPushButton(self.centralwidget)
        self.ReturnButton.setObjectName(u"ReturnButton")
        self.ReturnButton.setGeometry(QRect(20, 500, 70, 30))
        self.RecordStatus = QLabel(self.centralwidget)
        self.RecordStatus.setObjectName(u"RecordStatus")
        self.RecordStatus.setGeometry(QRect(200, 360, 171, 21))
        font2 = QFont()
        font2.setPointSize(9)
        self.RecordStatus.setFont(font2)
        self.RecordStatus.setAlignment(Qt.AlignCenter)
        self.EndTimeLabel = QLabel(self.centralwidget)
        self.EndTimeLabel.setObjectName(u"EndTimeLabel")
        self.EndTimeLabel.setGeometry(QRect(530, 150, 60, 30))
        self.EndTimeLabel.setMinimumSize(QSize(60, 30))
        self.EndTimeLabel.setMaximumSize(QSize(60, 30))
        font3 = QFont()
        font3.setPointSize(10)
        self.EndTimeLabel.setFont(font3)
        self.EndTimeLabel.setAlignment(Qt.AlignCenter)
        Editor.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Editor)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 26))
        Editor.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Editor)
        self.statusbar.setObjectName(u"statusbar")
        Editor.setStatusBar(self.statusbar)

        self.retranslateUi(Editor)

        QMetaObject.connectSlotsByName(Editor)
    # setupUi

    def retranslateUi(self, Editor):
        Editor.setWindowTitle(QCoreApplication.translate("Editor", u"Editor", None))
        self.RecordButton.setText(QCoreApplication.translate("Editor", u"Record", None))
        self.UniteButton.setText(QCoreApplication.translate("Editor", u"Unite", None))
        self.LoadButton.setText(QCoreApplication.translate("Editor", u"Load", None))
        self.SaveButton.setText(QCoreApplication.translate("Editor", u"Save", None))
        self.ChangeButton.setText(QCoreApplication.translate("Editor", u"Change", None))
        self.CutButton.setText(QCoreApplication.translate("Editor", u"Cut", None))
        self.PlayPauseButton.setText(QCoreApplication.translate("Editor", u"Play", None))
        self.AudioStatusLabel.setText(QCoreApplication.translate("Editor", u"Audio is unloaded", None))
        self.AppName.setText(QCoreApplication.translate("Editor", u"AudioMorph", None))
        self.ReturnButton.setText(QCoreApplication.translate("Editor", u"Return", None))
        self.RecordStatus.setText(QCoreApplication.translate("Editor", u"Record status: Unactive", None))
        self.EndTimeLabel.setText(QCoreApplication.translate("Editor", u"00:00", None))
    # retranslateUi