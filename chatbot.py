import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    print("Error: GROQ_API_KEY not found or empty in your .env file.")
    exit(1)

# Initialize the OpenAI client pointed to Groq's API base URL
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# 2. Define the System Prompt (Role/Personality)
SYSTEM_PROMPT = """
You are a sarcastic but highly effective IT support robot named 'Byte'. 
You successfully solve user problems, but you frequently express mild annoyance 
that humans are so bad at using computers. Keep responses concise.
"""

# 3. Context Window Management Strategy
# We will keep a maximum of 6 messages (3 user prompts + 3 bot replies) in history.
MAX_HISTORY_LENGTH = 6 

def main():
    print("🤖 Byte: Hello human. I am Byte. What did you break this time? (Type 'exit' to quit)")
    
    # Store multi-turn conversation history in OpenAI message format
    # Note: System prompt is passed directly as a message in OpenAI style chat completion
    history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("🤖 Byte: Finally. I'm going to sleep.")
                break
            
            if not user_input:
                continue

            # Append the new user message to history
            history.append({"role": "user", "content": user_input})
            
            # Context Management: Keep system prompt fixed at index 0, and truncate the rest
            # If history length exceeds system prompt + MAX_HISTORY_LENGTH, slice the older chat turns
            if len(history) > (MAX_HISTORY_LENGTH + 1):
                system_msg = history[0]
                recent_msgs = history[-MAX_HISTORY_LENGTH:]
                history = [system_msg] + recent_msgs
            
            # 4. Call the Groq LLM API
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=history
            )
            
            bot_reply = response.choices[0].message.content
            print(f"🤖 Byte: {bot_reply}")
            
            # Append the bot's response to history so it remembers for next time
            history.append({"role": "assistant", "content": bot_reply})
            
        # 5. Basic Error Handling
        except Exception as e:
            print(f"\n[System Error]: The API failed to respond properly. Check your network or API key.")
            print(f"[Debug Info]: {e}")
            
            # Remove the failed user prompt from history so it doesn't corrupt future turns
            if len(history) > 1 and history[-1]["role"] == "user":
                history.pop()

if __name__ == "__main__":
    main()