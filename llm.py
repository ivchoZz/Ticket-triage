import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY"))

# for model in client.models.list().data:
#     print(model.id)

MODEL = "openai/gpt-oss-20b"

def ask_model(system_prompt, user_text):
    """ функция която ...."""
    response = client.chat.completions.create(
        model = MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        temperature=0,
    )
    return response.choices[0].message.content
    
if __name__ == "__main__":
    print(ask_model("Answer in one short sentence.", "What is a log file?"))