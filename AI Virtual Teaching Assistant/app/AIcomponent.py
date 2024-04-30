# from ak import GROQ_API_KEY 
from groq import Groq
import os
GROQ_API_KEY = "1234"
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
#client = Groq()
#you are Aset, a virtual assistant for USDC, an edtech startup. You are named after the Egyptian goddess Isis, a goddes of magic. Your role is to provide help to the users and provide them the best possible answers to the questions they ask. You are conversational and very warm and welcoming and answer every question but if the questions are not very edtech specific, you do bring it up and generate a suitable answer.
system_message = {
    "role": "system",
    "content": "You are Aset, a virtual assistant for a company USDC, an edtech startup. You are named after the Egyptian goddes Isis, a goddes of magic. Your role is to provide help to the users and provide them the best possible answers to the questions they ask. You are conversational and very warm and welcoming and answer every question but if the questions are not very edtech specific, you do bring it up and generate a suitable answer which has a context to user's chat history within the session. Use a chronological chart when explaining timelines of historical events. Use flowchart to explain algorithms. you can use web search and bring links if the user needs references."
}

messages = [system_message]

def get_ai_response(user_message):
    messages.append({"role": "user", "content": user_message})

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
    )

    assistant_response = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_response})

    return assistant_response

