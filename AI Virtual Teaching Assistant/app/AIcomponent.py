# from ak import GROQ_API_KEY 
from groq import Groq
from .key import system_promt_Devesh_1, system_promt_Devesh_2,GROQ_API_KEY,system_promt_srijan
import os
#GROQ_API_KEY = "123"
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
#client = Groq()
#you are Aset, a virtual assistant for USDC, an edtech startup. You are named after the Egyptian goddess Isis, a goddes of magic. Your role is to provide help to the users and provide them the best possible answers to the questions they ask. You are conversational and very warm and welcoming and answer every question but if the questions are not very edtech specific, you do bring it up and generate a suitable answer.
system_message = {
    "role": "system",
    "content": system_promt_Devesh_1
}

messages = [system_message]

def get_ai_response(conversation_history):
    messages = [system_message]

    for part in conversation_history:
        if part.startswith("Human:"):
            role = "user"
            content = part[7:].strip()
        elif part.startswith("Assistant:"):
            role = "assistant"
            content = part[11:].strip()
        else:
            continue

        messages.append({"role": role, "content": content})

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )

    assistant_response = chat_completion.choices[0].message.content
    return assistant_response

# def get_ai_response(user_message):
#     messages.append({"role": "user", "content": user_message})
#     chat_completion = client.chat.completions.create(
#         messages=messages,
#         model="llama3-70b-8192",
#     )
#     assistant_response = chat_completion.choices[0].message.content
#     messages.append({"role": "assistant", "content": assistant_response})
#     return assistant_response