import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: GEMINI_API_KEY not found. Please check your .env file.")
    exit(1)

# Configure the API
genai.configure(api_key=API_KEY)

# 2. Define the System Prompt (Role/Personality)
SYSTEM_PROMPT = """
You are a sarcastic but highly effective IT support robot named 'Byte'. 
You successfully solve user problems, but you frequently express mild annoyance 
that humans are so bad at using computers. Keep responses concise.
"""

# Initialize the model with the system instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# 3. Context Window Management Strategy
# We will keep a maximum of 6 messages (3 user prompts + 3 bot replies) in history.
MAX_HISTORY_LENGTH = 6 

def main():
    print("🤖 Byte: Hello human. I am Byte. What did you break this time? (Type 'exit' to quit)")
    
    # Store multi-turn conversation history
    history = []
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("🤖 Byte: Finally. I'm going to sleep.")
                break
            
            if not user_input:
                continue

            # Append the new user message to the history array
            history.append({"role": "user", "parts": [user_input]})
            
            # Truncate history to enforce context window limits
            # If the history exceeds MAX_HISTORY_LENGTH, slice the array to keep only the newest messages
            if len(history) > MAX_HISTORY_LENGTH:
                history = history[-MAX_HISTORY_LENGTH:]
            
            # 4. Call the LLM API
            response = model.generate_content(history)
            bot_reply = response.text
            
            print(f"🤖 Byte: {bot_reply}")
            
            # Append the bot's response to the history so it remembers for next time
            history.append({"role": "model", "parts": [bot_reply]})
            
        # 5. Basic Error Handling
        except Exception as e:
            print(f"\n[System Error]: The API failed to respond properly. Check your network or API key.")
            print(f"[Debug Info]: {e}")
            
            # Remove the failed user prompt from history so it doesn't corrupt future turns
            if history and history[-1]["role"] == "user":
                history.pop()

if __name__ == "__main__":
    main()