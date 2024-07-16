from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from pydub import AudioSegment
from PySide6.QtCore import QTime, Signal

import pyaudio
import threading

from Program.Windows_ui.editorform import Ui_Editor

class Editor(QMainWindow):
    closed = Signal()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Editor()
        self.ui.setupUi(self)

        self.initial_dir = "../../Source/Storage"

        # Аудио настройки
        self.final_audio = None
        self.audio_format = pyaudio.paInt16  # 16 бит на семпл
        self.channels = 1  # Моно канал
        self.rate = 44100  # Частота дискретизации 44100 Гц
        self.chunk = 1024  # Размер блока для захвата
        self.pyaudio_instance = pyaudio.PyAudio()
        self.mic_index = self.find_microphone_index()  # Поиск микрофона в системе
        self.stream = None
        self.is_recording = False
        self.recorded_frames = []  # Список для хранения фреймов аудио

        self.ui.ReturnButton.clicked.connect(self.close)
        self.ui.PlayPauseButton.clicked.connect(self.on_ppb_click)
        self.ui.SaveButton.clicked.connect(self.on_SaveButton_click)
        self.ui.RecordButton.clicked.connect(self.on_RecordButton_click)
        self.ui.LoadButton.clicked.connect(self.on_LoadButton_click)

    def find_microphone_index(self):
        """Поиск индекса устройства микрофона, исключая виртуальные устройства."""
        num_devices = self.pyaudio_instance.get_device_count()
        for index in range(num_devices):
            device_info = self.pyaudio_instance.get_device_info_by_index(index)
            if device_info['maxInputChannels'] > 0:
                if 'mic' in device_info['name'].lower() or 'input' in device_info['name'].lower():
                    #print(f"Микрофон найден: {device_info['name']} на индексе {index}")
                    return index
        #print("Микрофон не найден, используется устройство по умолчанию.")
        return None

    def update_audio_duration(self):
        duration_seconds = len(self.final_audio) / 1000  # Получаем длительность в секундах
        duration_time = QTime(0, 0).addSecs(int(duration_seconds))  # Преобразуем секунды в QTime
        self.ui.EndTimeLabel.setText(duration_time.toString("mm:ss"))

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

    def on_ppb_click(self):
        if self.final_audio is None:
            self.UnloadedAudioWarning()
            return

        if self.ui.PlayPauseButton.text() == u"Play":
            self.ui.PlayPauseButton.setText(u"Stop")
            self.start_playing()
        else:
            self.ui.PlayPauseButton.setText(u"Play")
            self.stop_playing()

    def start_playing(self):
        self.audio_data = self.final_audio.raw_data
        self.num_channels = self.final_audio.channels
        self.bytes_per_sample = self.final_audio.sample_width
        self.sample_rate = self.final_audio.frame_rate

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
        self.ui.PlayPauseButton.setText(u"Play")

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

    def on_SaveButton_click(self):
        if self.final_audio is not None:
            # Открытие диалогового окна для выбора места сохранения файла
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Audio File", self.initial_dir,
                                                       "Audio Files (*.mp3 *.wav *.ogg *.flac)")

            if file_name:
                # Сохранение аудиозаписи
                self.final_audio.export(file_name, format=file_name.split('.')[-1])
                # Оповещение об успешном сохранении
                QMessageBox.information(self, "Information", "Audio saved successfully!")
        else:
            # Если аудио не записано, вывести предупреждение
            self.UnloadedAudioWarning()

    def on_LoadButton_click(self):
        # Открытие диалогового окна для выбора файла
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Audio File", self.initial_dir,
                                                   "Audio Files (*.mp3 *.wav *.ogg *.flac)")

        if file_name:
            # Загрузка и обработка аудиофайла с помощью pydub
            self.final_audio = AudioSegment.from_file(file_name)

            # Обновляем UI или выполняем дальнейшие действия
            self.ui.AudioStatusLabel.setText(u"Audio loaded")
            self.update_audio_duration()
        else:
            self.ui.RecordStatus.setText(u"Audio not found")

    def on_RecordButton_click(self):
        if not self.is_recording:
            self.ui.RecordStatus.setText(u"Record status: Active")
            self.start_recording()
        else:
            self.ui.RecordStatus.setText(u"Record status: Unactive")
            self.stop_recording()
            self.update_audio_duration()

    def start_recording(self):
        """Начать запись с выбранного микрофона."""
        self.stream = self.pyaudio_instance.open(format=self.audio_format,
                                                 channels=self.channels,
                                                 rate=self.rate,
                                                 input=True,
                                                 frames_per_buffer=self.chunk,
                                                 input_device_index=self.mic_index)  # Установка микрофона как устройства записи
        self.is_recording = True
        self.record()

    def stop_recording(self): # for on_RecordButton_click
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None

        # Создаем аудиофайл из захваченных данных
        audio_data = b''.join(self.recorded_frames)
        audio_segment = AudioSegment(data=audio_data, sample_width=2, frame_rate=self.rate, channels=self.channels)
        self.final_audio = audio_segment
        self.ui.AudioStatusLabel.setText(u"Audio recorded")

    def record(self):
        """Запись данных в фоновом потоке."""
        def record_thread():
            while self.is_recording:
                data = self.stream.read(self.chunk)
                self.recorded_frames.append(data)
        threading.Thread(target=record_thread).start()