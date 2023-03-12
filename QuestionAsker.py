import openai

class QuestionAsker:
    def __init__(self):
        pass

    def ask(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "system", "content": "If you don't know an answer, reply 'Sorry I don't know that'"},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {f"role": "user", "content": prompt}
            ]
        )
        print(response)
        return response.choices[0].message.content
