import os 
from dotenv import load_dotenv
import anthropic

load_dotenv()

def generate_response(chat):
    message = []
    
    for msg in chat:
        sender = msg.get("sender")
        text = msg.get("text", "")
        
        role = 'user' if sender == 'user' else 'assistant'
        
        message.append({
            "role": role,
            "content": text
        })
    
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=message
    )
    
    return response.content[0].text