# from ak import GROQ_API_KEY 
from groq import Groq
from .key import system_promt_1,GROQ_API_KEY,system_promt_srijan,system_promt2
import os

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_message = {
    "role": "system",
    "content": system_promt_1
}

def get_ai_response(conversation_history):
    messages = []
    for i, part in enumerate(conversation_history):
        if i % 4 == 0:
            messages.append(system_message)
        
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
        model="llama3-70b-8192",
    )
    assistant_response = chat_completion.choices[0].message.content
    return assistant_response

