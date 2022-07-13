import os
import openai
import re
openai.api_key = os.getenv("OPENAI_API_KEY")



def generate_question(prompt):
    response = openai.Completion.create(model="text-davinci-002",
                prompt=prompt,
                temperature=0.7,
                max_tokens=100,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0)
    return response['choices'][0]['text']

    