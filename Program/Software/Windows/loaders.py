from pydub import AudioSegment
from PySide6.QtCore import QThread, Signal

class AudioExporter(QThread):
    progress = Signal(int)
    finished_exporting = Signal()  # Сигнал завершения экспорта

    def __init__(self, audio_segment, file_name, file_format):
        super().__init__()
        self.audio_segment = audio_segment
        self.file_name = file_name
        self.file_format = file_format

    def run(self):
        # Экспортируем аудиофайл
        self.audio_segment.export(self.file_name, format=self.file_format)
        self.progress.emit(100)  # Обновляем прогресс до 100%
        self.finished_exporting.emit()  # Излучаем сигнал завершения экспорта

class AudioLoader(QThread):
    progress = Signal(int)
    finished_loading = Signal(AudioSegment)

    def __init__(self, file_paths):
        super().__init__()
        self.file_paths = file_paths

    def run(self):
        total_files = len(self.file_paths)
        loaded_audio = AudioSegment.empty()
        for index, path in enumerate(self.file_paths):
            audio = AudioSegment.from_file(path)
            loaded_audio += audio
            # Обновляем прогресс после добавления каждого файла
            self.progress.emit(int((index + 1) / total_files * 100))
        self.finished_loading.emit(loaded_audio)  # Возвращаем загруженное аудио и закрываем прогресс бар