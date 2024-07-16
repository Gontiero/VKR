from PySide6.QtWidgets import QApplication
from Program.Software.Controller.appcontroller import AppController

if __name__ == "__main__":
    app = QApplication([])
    controller = AppController()
    controller.run()
    app.exec()