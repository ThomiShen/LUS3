import openai

class Evaluator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def get_evaluation(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()


