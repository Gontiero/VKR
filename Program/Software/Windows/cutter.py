from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Signal, QTime
import pyaudio
import threading

from Program.Windows_ui.cutterform import Ui_Cutter

class Cutter(QWidget):
    closed = Signal()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def __init__(self, parent=None, audio_path=None):
        super().__init__(parent)
        self.ui = Ui_Cutter()
        self.ui.setupUi(self)
        self.changed_audio = audio_path

        if audio_path:
            self.load_audio()

        self.ui.CancelButton.clicked.connect(self.close)
        self.ui.BeginButton.clicked.connect(self.set_begin_position)
        self.ui.EndButton.clicked.connect(self.set_end_position)
        self.ui.CPPButton.clicked.connect(self.on_cppb_click)
        self.ui.CutButton.clicked.connect(self.on_cut_click)
        self.ui.LoadButton.clicked.connect(self.load_audio_from_editor)  # Добавлено для загрузки аудио из Editor

    def set_audio(self, audio_segment):
        self.changed_audio = audio_segment
        self.load_audio()

    def load_audio(self):
        if self.changed_audio:
            self.update_audio_duration()
        else:
            QMessageBox.warning(self, "Error", "No audio file loaded!")

    def load_audio_from_editor(self):
        #self.changed_audio = self.parent().audio_db.get_audio_file()
        self.load_audio()

    def update_audio_duration(self):
        duration_seconds = len(self.changed_audio) / 1000  # Получаем длительность в секундах
        duration_time = QTime(0, 0).addSecs(int(duration_seconds))  # Преобразуем секунды в QTime
        self.ui.EndLabel.setText(duration_time.toString("mm:ss"))
        self.ui.EndPosition.setTime(duration_time)
        self.ui.AudioSlider.setMaximum(duration_seconds * 1000)  # Устанавливаем максимум слайдера в миллисекундах

    def set_begin_position(self):
        position = self.ui.AudioSlider.value()  # Получаем текущее положение слайдера в миллисекундах
        time = QTime(0, 0).addMSecs(position)
        self.ui.BeginPosition.setTime(time)

    def set_end_position(self):
        position = self.ui.AudioSlider.value()  # Получаем текущее положение слайдера в миллисекундах
        time = QTime(0, 0).addMSecs(position)
        self.ui.EndPosition.setTime(time)

    def UnloadedAudioWarning(self):
        # Создаем экземпляр QMessageBox
        msg_box = QMessageBox()

        # Устанавливаем заголовок и текст
        msg_box.setWindowTitle("Audio not find")
        msg_box.setText("You haven't uploaded or recorded audio!")

        # Устанавливаем тип сообщения (в данном случае - информационное)
        msg_box.setIcon(QMessageBox.Critical)

        # Добавляем кнопку "Close"
        msg_box.setStandardButtons(QMessageBox.Close)

        # Отображаем диалоговое окно
        msg_box.exec()

    def on_cppb_click(self):
        if self.changed_audio is None:
            self.UnloadedAudioWarning()
            return

        if self.ui.CPPButton.text() == u"Play":
            self.ui.CPPButton.setText(u"Stop")
            self.start_playing()
        else:
            self.ui.CPPButton.setText(u"Play")
            self.stop_playing()

    def start_playing(self):
        self.audio_data = self.changed_audio.raw_data
        self.num_channels = self.changed_audio.channels
        self.bytes_per_sample = self.changed_audio.sample_width
        self.sample_rate = self.changed_audio.frame_rate

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.bytes_per_sample),
                                  channels=self.num_channels,
                                  rate=self.sample_rate,
                                  output=True)
        self.is_playing = True
        self.stop_event = threading.Event()

        # Воспроизведение аудио в отдельном потоке для избежания блокировки GUI
        self.play_thread = threading.Thread(target=self.play_audio)
        self.play_thread.start()

    def play_audio(self):
        chunk_size = 1024  # Размер блока данных
        start = 0
        end = chunk_size * self.bytes_per_sample * self.num_channels

        while self.is_playing and start < len(self.audio_data):
            if self.stop_event.is_set():
                break
            data = self.audio_data[start:end]
            if not data:
                break
            self.stream.write(data)
            start = end
            end += chunk_size * self.bytes_per_sample * self.num_channels

        # Закрываем поток и PyAudio только если аудио завершилось или остановлено
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.ui.CPPButton.setText(u"Play")

    def stop_playing(self):
        self.is_playing = False
        self.stop_event.set()
        if self.play_thread is not None:
            self.play_thread.join()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        if self.p is not None:
            self.p.terminate()

    def on_cut_click(self):
        start_time = QTime(0, 0).secsTo(self.ui.BeginPosition.time()) * 1000
        end_time = QTime(0, 0).secsTo(self.ui.EndPosition.time()) * 1000
        if end_time > start_time:
            part_before = self.changed_audio[:start_time]
            part_after = self.changed_audio[end_time:]
            self.changed_audio = part_before + part_after
            self.update_audio_duration()
            QMessageBox.information(self, "Success", "The specified segment has been removed.")
            self.ui.AudioSlider.setValue(0)  # Сброс слайдера в начало
        else:
            QMessageBox.warning(self, "Warning", "End time must be greater than start time.")