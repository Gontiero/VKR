from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Signal, QTime
import pyaudio
import threading
from Program.Windows_ui.changerform import Ui_Changer

class Changer(QMainWindow):
    closed = Signal()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def __init__(self, parent=None, audio_segment=None):
        super().__init__(parent)
        self.ui = Ui_Changer()
        self.ui.setupUi(self)
        self.original_audio = audio_segment
        self.changed_audio = audio_segment

        if audio_segment:
            self.load_audio()

        self.ui.CancelButton.clicked.connect(self.close)
        self.ui.AcceptButton.clicked.connect(self.on_accept_button_click)
        self.ui.PlayPauseButton.clicked.connect(self.on_ppb_click)

    def set_audio(self, audio_segment):
        self.original_audio = audio_segment
        self.changed_audio = audio_segment
        self.load_audio()

    def load_audio(self):
        if self.changed_audio:
            self.update_audio_duration()
        else:
            QMessageBox.warning(self, "Error", "No audio file loaded!")

    def update_audio_duration(self):
        duration_seconds = len(self.changed_audio) / 1000  # Получаем длительность в секундах
        duration_time = QTime(0, 0).addSecs(int(duration_seconds))  # Преобразуем секунды в QTime
        self.ui.TimeLabel.setText(duration_time.toString("mm:ss"))

    def on_accept_button_click(self):
        if self.original_audio is None:
            self.UnloadedAudioWarning()
            return

        # Получаем значения слайдеров
        amplitude_value = self.ui.AmplitudeSlider.value()
        pitch_value = self.ui.PitchingSlider.value()
        frequency_value = self.ui.FrequencySlider.value()

        # Применение амплитуды
        self.changed_audio = self.original_audio.apply_gain(amplitude_value - self.original_audio.dBFS)

        # Применение питча
        self.changed_audio = self.changed_audio._spawn(self.changed_audio.raw_data, overrides={
            "frame_rate": int(self.changed_audio.frame_rate * (2.0 ** (pitch_value / 12.0)))
        }).set_frame_rate(self.changed_audio.frame_rate)

        # Применение частоты
        new_sample_rate = int(20 * (10 ** (frequency_value / 1000.0)))

        # Проверка допустимых значений частоты дискретизации
        if new_sample_rate < 8000:
            new_sample_rate = 8000
        elif new_sample_rate > 192000:
            new_sample_rate = 192000

        self.changed_audio = self.changed_audio.set_frame_rate(new_sample_rate)

        # Обновление длительности аудио
        self.update_audio_duration()

        # Уведомление об успешном применении параметров
        QMessageBox.information(self, "Success", "Audio parameters applied successfully!")

    def UnloadedAudioWarning(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Audio not find")
        msg_box.setText("You haven't uploaded or recorded audio!")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStandardButtons(QMessageBox.Close)
        msg_box.exec()

    def on_ppb_click(self):
        if self.changed_audio is None:
            self.UnloadedAudioWarning()
            return

        if self.ui.PlayPauseButton.text() == "Play":
            self.ui.PlayPauseButton.setText("Stop")
            self.start_playing()
        else:
            self.ui.PlayPauseButton.setText("Play")
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

        self.play_thread = threading.Thread(target=self.play_audio)
        self.play_thread.start()

    def play_audio(self):
        chunk_size = 1024
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

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.ui.PlayPauseButton.setText("Play")

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
