import deepspeech
import numpy as np
import pyaudio

# Create a DeepSpeech model object
model_path = "deepspeech-0.9.3-models.pbmm"
scorer_path = "deepspeech-0.9.3-models.scorer"
model = deepspeech.Model(model_path)
model.enableExternalScorer(scorer_path)


# Set up PyAudio stream
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

# Record audio from microphone
print("Say something...")
frames = []
for i in range(int(RATE / CHUNK_SIZE * 5)):
    data = stream.read(CHUNK_SIZE)
    frames.append(data)
audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

# Transcribe audio data
text = model.stt(audio_data)
print("Transcribed text:", text)

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()