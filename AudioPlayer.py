import time

import pyaudio, wave
import numpy as np
from TTS.api import TTS

tts = TTS(model_name='tts_models/en/ljspeech/glow-tts', progress_bar=False, gpu=False)


class AudioPlayer:
    def __init__(self):
        self.audio_format = pyaudio.paInt16
        self.audio_sample_rate = 22050
        self.frames_per_buffer = int(self.audio_sample_rate * 0.1)
        self.stream = None
        self.audio_data = None

    def play_blocking(self, text):
        self.audio_data = (np.array(tts.tts(text=text)) * (2 ** 15 - 1)).astype(np.int16)

        self.stream = pyaudio.PyAudio().open(
            format=self.audio_format,
            channels=1,
            rate=self.audio_sample_rate,
            output=True,
            frames_per_buffer=self.frames_per_buffer
        )

        num_frames = len(self.audio_data)
        frames_written = 0
        while frames_written < num_frames:
            frames_to_write = min(self.frames_per_buffer, num_frames - frames_written)
            self.stream.write(self.audio_data[frames_written:frames_written + frames_to_write])
            frames_written += frames_to_write

        self.stream.stop_stream()
        self.stream.close()
        self.stream = None

    def play_test(self, text):
        tts.tts_to_file(text=text, file_path="test.wav")
        with wave.open("test.wav", 'rb') as wf:
            # Instantiate PyAudio and initialize PortAudio system resources (1)
            p = pyaudio.PyAudio()

            # Open stream (2)
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            # Play samples from the wave file (3)
            while len(data := wf.readframes(512)):  # Requires Python 3.8+ for :=
                stream.write(data)

            # Close stream (4)
            stream.close()

            # Release PortAudio system resources (5)
            p.terminate()

    def play_nonblocking(self, text):
        tts.tts_to_file(text=text, file_path="sound.wav")
        with wave.open("sound.wav", 'rb') as wf:
            # Define callback for playback (1)
            def callback(in_data, frame_count, time_info, status):
                data = wf.readframes(frame_count)
                # If len(data) is less than requested frame_count, PyAudio automatically
                # assumes the stream is finished, and the stream stops.
                return (data, pyaudio.paContinue)

            # Instantiate PyAudio and initialize PortAudio system resources (2)
            p = pyaudio.PyAudio()

            # Open stream using callback (3)
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True,
                            stream_callback=callback)

            # Wait for stream to finish (4)
            while stream.is_active():
                time.sleep(0.05)

            # Close the stream (5)
            stream.close()

            # Release PortAudio system resources (6)
            p.terminate()

audio_player = AudioPlayer()
