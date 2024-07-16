import os
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox
from PySide6.QtCore import Signal,QStringListModel
from PySide6.QtWidgets import QAbstractItemView
from pydub import AudioSegment
from PySide6.QtWidgets import QProgressDialog

from Program.Windows_ui.uniterform import Ui_Uniter
from Program.Software.Windows.loaders import AudioExporter, AudioLoader

class Uniter(QWidget):
    closed = Signal()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Uniter()
        self.ui.setupUi(self)

        self.initial_dir = "../../Source/Storage"

        self.changed_audio = AudioSegment.empty()  # Инициализируем пустым аудио
        self.audio_files = QStringListModel(self)
        self.full_paths = []  # Сохраняем полные пути
        self.ui.listView.setModel(self.audio_files)
        self.ui.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.ui.CancelButton.clicked.connect(self.close)
        self.ui.HSPButton.clicked.connect(self.on_HSPButton_click)
        self.ui.AddButton.clicked.connect(self.add_audio)
        self.ui.DeleteButton.clicked.connect(self.delete_audio)
        self.ui.SaveButton.clicked.connect(self.save_audio)
        self.ui.UpButton.clicked.connect(self.move_item_up)
        self.ui.DownButton.clicked.connect(self.move_item_down)

    def rebuild_changed_audio(self):
        self.changed_audio = AudioSegment.empty()
        for path in self.full_paths:
            audio = AudioSegment.from_file(path)
            self.changed_audio += audio

    def add_audio(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Audio Files", self.initial_dir,
                                                     "Audio Files (*.mp3 *.wav *.ogg *.flac)")
        if file_names:
            self.full_paths.extend(file_names)
            self.update_displayed_paths()

            progress_dialog = QProgressDialog("Loading audio files...", "Abort", 0, 100, self)
            progress_dialog.setAutoClose(True)
            progress_dialog.setMinimumDuration(0)

            loader = AudioLoader(file_names)
            loader.progress.connect(progress_dialog.setValue)
            loader.finished_loading.connect(lambda: progress_dialog.accept())  # Закрывать прогресс бар
            loader.finished_loading.connect(self.update_changed_audio)
            loader.start()
            progress_dialog.exec()

    def update_changed_audio(self, audio_segment):
        if isinstance(audio_segment, AudioSegment):
            self.changed_audio += audio_segment

    def delete_audio(self):
        indexes = self.ui.listView.selectedIndexes()
        if indexes:
            index = indexes[0].row()
            del self.full_paths[index]
            self.update_displayed_paths()
            self.rebuild_changed_audio()
        else:
            QMessageBox.warning(self, "Warning", "Please select an audio file to delete.")

    def save_audio(self):
        if not self.changed_audio:
            QMessageBox.warning(self, "Warning", "No audio files to save. Please add some files first.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Audio File", self.initial_dir,
                                                   "Audio Files (*.mp3 *.wav *.ogg *.flac)")
        if file_name:
            progress_dialog = QProgressDialog("Saving audio file...", "Abort", 0, 100, self)
            progress_dialog.setAutoClose(True)
            progress_dialog.setMinimumDuration(0)

            exporter = AudioExporter(self.changed_audio, file_name, file_name.split('.')[-1])
            exporter.progress.connect(progress_dialog.setValue)
            exporter.finished_exporting.connect(progress_dialog.accept)  # Подключаем сигнал к закрытию диалога
            exporter.start()
            progress_dialog.exec()

            if progress_dialog.wasCanceled():
                QMessageBox.warning(self, "Canceled", "Audio saving canceled!")
            else:
                QMessageBox.information(self, "Success", "Audio saved successfully!")

    def update_displayed_paths(self):
        if self.ui.HSPButton.text() == "Show Path":
            display_names = [os.path.basename(path) for path in self.full_paths]
        else:
            display_names = self.full_paths[:]
        self.audio_files.setStringList(display_names)

    def on_HSPButton_click(self):
        if self.ui.HSPButton.text() == u"Hide path":
            self.ui.HSPButton.setText(u"Show Path")
        else:
            self.ui.HSPButton.setText(u"Hide path")
        self.update_displayed_paths()  # Обновляем отображаемые пути при каждом нажатии

    def move_item_up(self):
        index = self.get_selected_index()
        if index is not None and index > 0:
            self.full_paths[index], self.full_paths[index - 1] = self.full_paths[index - 1], self.full_paths[index]
            self.update_displayed_paths()
            self.rebuild_changed_audio()
            self.ui.listView.setCurrentIndex(self.audio_files.index(index - 1))

    def move_item_down(self):
        index = self.get_selected_index()
        if index is not None and index < len(self.full_paths) - 1:
            self.full_paths[index], self.full_paths[index + 1] = self.full_paths[index + 1], self.full_paths[index]
            self.update_displayed_paths()
            self.rebuild_changed_audio()
            self.ui.listView.setCurrentIndex(self.audio_files.index(index + 1))

    def get_selected_index(self):
        indexes = self.ui.listView.selectedIndexes()
        if indexes:
            return indexes[0].row()
        QMessageBox.warning(self, "Warning", "Please select an audio file to move.")
        return None

