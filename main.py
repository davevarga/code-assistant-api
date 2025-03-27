import os
from dotenv import load_dotenv()
from openai import OpenAI


# Import environment variables from .env file
load_dotenv('.env')
OPENAI_API_KEY = os.environ.get('API_KEY')
SERPER_API_KEY = os.environ.get('SERPER_APIKEY')

# Create the first llm
client = OpenAI(api_key=OPENAI_API_KEY)


if __name__ == '__main__':
    # Let's test our LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_completion_tokens=256,
        messages=[{
            "role": "user",
            "content": "Who was Niels Bohr?"
        }])
    print(response.choices[0].message.content)