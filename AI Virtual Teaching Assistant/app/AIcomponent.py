# AIcomponent.py

from groq import Groq
from groq import RateLimitError
from .key import system_prompt_1, GROQ_API_KEY, UNSPLASH_ACCESS_KEY
import os
import requests

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["UNSPLASH_ACCESS_KEY"] = UNSPLASH_ACCESS_KEY

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

system_message = {
    "role": "system",
    "content": system_prompt_1
}

def get_image_from_unsplash(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={os.environ['UNSPLASH_ACCESS_KEY']}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']
        return image_url
    else:
        return None

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
    
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192",
        )
        assistant_response = chat_completion.choices[0].message.content
        
        if "image of" in assistant_response.lower() or "photo of" in assistant_response.lower():
            query = assistant_response.split("image of")[-1].strip() if "image of" in assistant_response.lower() else assistant_response.split("photo of")[-1].strip()
            image_url = get_image_from_unsplash(query)
            if image_url:
                return {
                    "message": f"Here is an image related to {query}:",
                    "imageUrl": image_url
                }
            else:
                return {
                    "message": f"Sorry, I couldn't find an image for {query}."
                }
        
        return {
            "message": assistant_response
        }
    except RateLimitError as e:
        error_message = "Sorry, you've reached your token limit. Please try again later."
        print(f"Error: {e}")
        return {
            "message": error_message
        }
    except Exception as e:
        error_message = "I apologize, but I'm experiencing technical difficulties. Please try again later."
        print(f"Error: {e}")
        return {
            "message": error_message
        }
