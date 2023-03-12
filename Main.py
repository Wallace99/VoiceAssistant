from AudioPlayer import AudioPlayer
from QuestionAsker import QuestionAsker
from Listener import listen_for_question, listen_for_phrase, verify_question

key_phrase = "question"


audio_player = AudioPlayer()
question_asker = QuestionAsker()

while True:
    print("Waiting for key phrase")
    listen_for_phrase(key_phrase)
    audio_player.play_nonblocking("I'm listening")
    print("say question now")
    question = listen_for_question()
    audio_player.play_test(text=f"Was your question: {question}?")
    if verify_question():
        answer = question_asker.ask(question)
        audio_player.play_test(answer)
