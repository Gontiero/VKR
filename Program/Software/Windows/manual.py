from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal

from Program.Windows_ui.manualform import Ui_Manual

class Manual(QMainWindow):

    closed = Signal()

    def closeEvent(self, event):
        self.closed.emit()  # Испускаем сигнал перед закрытием
        super().closeEvent(event)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Manual()
        self.ui.setupUi(self)

        # Начальная установка изображения для первой страницы
        self.ui.Pictures.setPixmap(QPixmap("../../Source/ManualPages/11.png"))
        self.ui.Pictures.setScaledContents(True)  # Растягиваем изображение на весь QLabel

        # Подключаем сигнал изменения текущего индекса к слоту для обновления изображения
        self.ui.Pager.currentIndexChanged.connect(self.updateImage)

        # Подключаем слоты к кнопкам
        self.ui.NextButton.clicked.connect(self.nextPage)
        self.ui.PrevButton.clicked.connect(self.prevPage)

        self.ui.ReturnButton.clicked.connect(self.close)

    def nextPage(self):
        # Переход к следующей странице
        current_index = self.ui.Pager.currentIndex()
        next_index = (current_index + 1) % self.ui.Pager.count()  # Циклический переход
        self.ui.Pager.setCurrentIndex(next_index)

    def prevPage(self):
        # Переход к предыдущей странице
        current_index = self.ui.Pager.currentIndex()
        prev_index = (current_index - 1 + self.ui.Pager.count()) % self.ui.Pager.count()
        self.ui.Pager.setCurrentIndex(prev_index)

    def updateImage(self, index):
        # Определяем относительные пути к изображениям
        image_paths = {0: "../../Source/ManualPages/11.png",
                       1: "../../Source/ManualPages/22.png",
                       2: "../../Source/ManualPages/33.png",
                       3: "../../Source/ManualPages/44.png",
                       4: "../../Source/ManualPages/55.png",
                       5: "../../Source/ManualPages/66.png"}

        # Получаем путь к изображению в зависимости от выбранной страницы
        image_path = image_paths.get(index, "../../Source/ManualPages/11.png")

        # Обновляем изображение в QLabel
        self.ui.Pictures.setPixmap(QPixmap(image_path))
