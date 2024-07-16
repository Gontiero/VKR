from PySide6.QtWidgets import QMainWindow

from Program.Windows_ui.mainmenuform import Ui_MainMenu

class MainMenu(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainMenu()
        self.ui.setupUi(self)
