from Program.Software.Windows.editor import Editor
from Program.Software.Windows.mainmenu import MainMenu
from Program.Software.Windows.manual import Manual
from Program.Software.Windows.cutter import Cutter
from Program.Software.Windows.uniter import Uniter
from Program.Software.Windows.changer import Changer
from Program.Software.Database.audio_db import AudioDatabase

from PySide6.QtWidgets import QMessageBox

class AppController:
    def __init__(self):
        # Инициализация оставшихся компонентов
        self.main_menu = MainMenu()
        self.manual = Manual()
        self.editor = Editor()
        self.cutter = Cutter()
        self.uniter = Uniter()
        self.changer = Changer()
        self.audio_db = AudioDatabase()

        # Настройка соединений для главного меню
        self.main_menu.ui.ManualButton.clicked.connect(self.show_manual)
        self.main_menu.ui.EditorButton.clicked.connect(self.show_editor)
        self.main_menu.ui.ExitButton.clicked.connect(self.close)

        # Настройка соединений для редактора
        self.editor.ui.CutButton.clicked.connect(self.show_cutter)
        self.editor.ui.UniteButton.clicked.connect(self.show_uniter)
        self.editor.ui.ChangeButton.clicked.connect(self.show_changer)
        self.editor.closed.connect(self.show_main_menu)

        # Настройка соединений для закрытия окон
        self.manual.closed.connect(self.show_main_menu)
        self.cutter.closed.connect(self.show_editor)
        self.uniter.closed.connect(self.show_editor)
        self.changer.closed.connect(self.show_editor)

        # Настройка соединений для Cutter
        self.cutter.ui.LoadButton.clicked.connect(self.save_cutter_audio)
        self.cutter.closed.connect(self.show_editor)

        # Настройка соединений для Uniter
        self.uniter.ui.LoadButton.clicked.connect(self.load_uniter_audio)
        self.uniter.closed.connect(self.show_editor)

        # Настройка соединений для Uniter
        self.changer.ui.LoadButton.clicked.connect(self.save_changer_audio)
        self.changer.closed.connect(self.show_editor)

    def close(self):
        self.main_menu.close()

    def show_main_menu(self):
        self.main_menu.show()

    def show_manual(self):
        self.main_menu.hide()
        self.manual.show()

    def show_editor(self):
        self.main_menu.hide()
        self.editor.show()

    def show_cutter(self):
        if self.editor.final_audio is None:
            QMessageBox.warning(self.editor, "Warning", "Please select an audio file to process.")
        else:
            self.audio_db.set_audio_file(self.editor.final_audio)
            self.cutter.set_audio(self.audio_db.get_audio_file())  # Устанавливаем аудиофайл в Cutter
            self.audio_db.clear_audio_file()
            self.editor.hide()
            self.cutter.show()

    def show_changer(self):
        if self.editor.final_audio is None:
            QMessageBox.warning(self.editor, "Warning", "Please select an audio file to process.")
        else:
            self.audio_db.set_audio_file(self.editor.final_audio)
            self.changer.set_audio(self.audio_db.get_audio_file())  # Устанавливаем аудиофайл в Cutter
            self.audio_db.clear_audio_file()
            self.editor.hide()
            self.changer.show()

    def show_uniter(self):
        self.editor.hide()
        self.uniter.show()

    def run(self):
        self.main_menu.show()

    def save_cutter_audio(self):
        if self.cutter.changed_audio:
            self.editor.final_audio = self.cutter.changed_audio  # Передаем аудиофайл из Cutter_ui в Editor_ui
            self.editor.update_audio_duration()  # Обновляем отображение в Editor_ui
            self.cutter.close()  # Закрываем окно Cutter_ui
            self.show_editor()  # Показываем окно Editor_ui с новым аудиофайлом
        else:
            QMessageBox.warning(self.cutter, "Error", "No audio file to save!")

    def load_uniter_audio(self):
        if self.uniter.changed_audio is None:
            QMessageBox.warning(self, "Warning", "No audio files to save. Please add some files first.")
            return
        self.editor.final_audio = self.uniter.changed_audio  # Передаем объединённое аудио из Uniter в Editor
        self.editor.update_audio_duration()  # Обновляем отображение в Editor_ui
        self.uniter.close()  # Закрываем окно Uniter_ui
        self.show_editor()  # Показываем окно Editor_ui с новым аудиофайлом

    def save_changer_audio(self):
        if self.changer.changed_audio:
            self.editor.final_audio = self.changer.changed_audio  # Передаем аудиофайл из Cutter_ui в Editor_ui
            self.editor.update_audio_duration()  # Обновляем отображение в Editor_ui
            self.changer.close()  # Закрываем окно Cutter_ui
            self.show_editor()  # Показываем окно Editor_ui с новым аудиофайлом
        else:
            QMessageBox.warning(self.changer, "Error", "No audio file to save!")