from ollama import chat
from emotion import detect_emotion
import time

# Config
OLLAMA_MODEL = "gemma3:4b"

class VtuberBrain:
    def __init__(self):
        self.memory = []
        self.system_prompt = (
            "You are a cute anime VTuber. "
            "Talk like a livestreamer. Keep it short. "
            "Use ASCII only."
        )

    def generate_response(self, user_text: str):
        # Add user to memory
        self.memory.append({"role": "user", "content": user_text})
        
        try:
            # Generate
            response = chat(
                model=OLLAMA_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *self.memory
                ]
            )
            reply_text = response['message']['content']
            
            # Add assistant to memory
            self.memory.append({"role": "assistant", "content": reply_text})
            
            # Detect emotion
            emo = detect_emotion(reply_text)
            
            return reply_text, emo
            
        except Exception as e:
            print(f"Error in brain: {e}")
            return "Sorry, I blanked out!", "Sorrow"

# Simple instance for easy import if needed, 
# but main.py will likely instantiate this.
brain_instance = VtuberBrain()
