import numpy as np
import pyaudio, wave
from TTS.api import TTS

# Initialize TTS engine
tts = TTS(model_name='tts_models/en/ljspeech/glow-tts', progress_bar=False, gpu=False)
p = pyaudio.PyAudio()
chunk_size = 1024

# Generate audio
text = "Hello, how are you?"
audio = tts.tts_to_file(text, file_path="audio.wav")

wf = wave.open("audio.wav", 'rb')
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(chunk_size)

while data:
    stream.write(data)
    data = wf.readframes(chunk_size)

stream.stop_stream()
stream.close()

p.terminate()