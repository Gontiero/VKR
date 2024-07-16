class AudioDatabase:
    def __init__(self):
        self.audio_file = None

    def set_audio_file(self, audio):
        self.audio_file = audio

    def get_audio_file(self):
        return self.audio_file

    def clear_audio_file(self):
        self.audio_file = None