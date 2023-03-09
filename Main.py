import deepspeech
import numpy as np
import openai
import pyaudio
from TTS.api import TTS

tts = TTS(model_name='tts_models/en/ljspeech/glow-tts', progress_bar=False, gpu=False)

model_path = "deepspeech-0.9.3-models.pbmm"
scorer_path = "deepspeech-0.9.3-models.scorer"
QUESTION_LENGTH_SECONDS = 5
key_phrase = "quick question"


class QuestionAsker:
    def __init__(self):
        pass

    def ask(self, prompt):
        context = f"""You are a butler called Jeeves.\n
                  You answer questions factually and in a polite manner, like a Victorian era butler would.\n
                  If you don't know an answer, reply 'Sorry I don't know that'.\n
                  The master has asked the following question. Please reply accordingly:\n
                  {prompt}""",

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=context,
            temperature=0.7,
            max_tokens=50,
            n=1,
            stop=None,
            frequency_penalty=0.25,
            presence_penalty=0.6
        )

        print(response)
        return response.choices[0].text.strip()

class QuestionListener:

    def __init__(self):
        self.model = deepspeech.Model(model_path)
        self.model.enableExternalScorer(scorer_path)
        self.audio_chunk_size = 1024
        self.audio_sample_rate = 16000
        self.audio_format = pyaudio.paInt16

        self.stream = self.model.createStream()
        self.recording = False
        self.frames = []
        self.processed = False

    def process_audio_frame(self, audio_frame) -> bool:
        self.stream.feedAudioContent(audio_frame)
        text = self.stream.intermediateDecode()
        if key_phrase in text.lower() and not self.recording:
            print("Key phrase detected! Recording started.")
            return True
        return False

    def process_response(self, audio_frame):
        self.stream.feedAudioContent(audio_frame)
        text = self.stream.intermediateDecode()
        return text

    def listen(self):
        audio_input = pyaudio.PyAudio().open(
            format=self.audio_format,
            channels=1,
            rate=self.audio_sample_rate,
            input=True,
            frames_per_buffer=self.audio_chunk_size
        )

        # Listen for phrase
        while not self.processed:
            audio_data = audio_input.read(self.audio_chunk_size)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            self.processed = self.process_audio_frame(audio_array)

        audio_input.stop_stream()

        self.play_speech("I'm listening...")
        print("say question now")

        audio_input.start_stream()

        # Listen for question
        frames = []
        while len(frames) * self.audio_chunk_size <= self.audio_sample_rate * QUESTION_LENGTH_SECONDS:
            audio_data = audio_input.read(self.audio_chunk_size)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            frames.append(audio_array)

        audio_input.stop_stream()
        audio_data = b''.join(frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        text = self.model.stt(audio_array)
        print(f"Question: {text}")
        self.play_speech(text=f"Was your question: {text}?")

        responded = False
        response = ""
        audio_input.start_stream()
        while not responded:
            audio_data = audio_input.read(self.audio_chunk_size)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            response = self.process_response(audio_array)
            if "yes" in response.lower() or "no" in response.lower():
                responded = True

        if "yes" in response.lower():
            print("ok, thinking...")
            self.stream.freeStream()
            return text
        else:
            return ""

    def play_speech(self, text):
        wav = tts.tts(text=text)
        stream = pyaudio.PyAudio().open(
            format=self.audio_format,
            channels=1,
            rate=self.audio_sample_rate,
            output=True
        )
        audio_bytes = (np.array(wav) * (2 ** 15 - 1)).astype(np.int16).tobytes()
        stream.write(audio_bytes)
        stream.close()


question_listener = QuestionListener()
question_asker = QuestionAsker()

question = question_listener.listen()
response = question_asker.ask(question)

wav = tts.tts(text=response)
stream = pyaudio.PyAudio().open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    output=True
)
audio_bytes = (np.array(wav) * (2 ** 15 - 1)).astype(np.int16).tobytes()
stream.write(audio_bytes)
stream.close()
