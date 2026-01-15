from ollama import chat
from emotion import detect_emotion
import time
import random
from config import OLLAMA_MODEL, SYSTEM_PROMPT, BOUNCE_EXIT_PHRASES

class VtuberBrain:
    def __init__(self):
        self.memory = []
        # State tracking
        self.bounce_mode = False
        self.bounce_counter = 0

    def generate_response(self, user_text: str):
        # Add user to memory
        self.memory.append({"role": "user", "content": user_text})
        
        # 1. Determine State / Dynamic Instruction
        if not self.bounce_mode:
            # 25% chance to trigger Bounce Mode if not active
            if random.random() < 0.25:
                self.bounce_mode = True
                self.bounce_counter = random.randint(1, 3) # 1 to 3 utterances
        
        # Prepare dynamic system instruction
        if self.bounce_mode:
            # Active Bounce Mode
            current_instruction = (
                "【現在：跳ねる状態】"
                "皮肉・論理的指摘・毒舌を許可する。"
                "感情は乗せずに、鋭く切り込め。"
                "最大3文まで。"
            )
            self.bounce_counter -= 1
        else:
            # Normal Mode
            current_instruction = (
                "【現在：通常状態】"
                "静かに、淡々と、観察せよ。"
                "皮肉は弱めに、事実は正確に。"
                "感情を表に出すな。"
            )

        try:
            # Generate response
            # We inject the permanent System Prompt + History + Current State Instruction
            messages_payload = [
                {"role": "system", "content": SYSTEM_PROMPT},
                *self.memory,
                {"role": "system", "content": current_instruction}
            ]
            
            response = chat(
                model=OLLAMA_MODEL,
                messages=messages_payload
            )
            reply_text = response['message']['content']
            
            # 2. Check for Mode Exit
            if self.bounce_mode and self.bounce_counter <= 0:
                # This was the last bounce message. Ensure exit phrase exists.
                has_exit_phrase = any(phrase in reply_text for phrase in BOUNCE_EXIT_PHRASES)
                if not has_exit_phrase:
                    # Force append a random exit phrase
                    exit_phrase = random.choice(BOUNCE_EXIT_PHRASES)
                    # Ensure minimal spacing
                    reply_text = f"{reply_text.rstrip()} {exit_phrase}"
                
                # Turn off mode
                self.bounce_mode = False

            # Add assistant to memory
            self.memory.append({"role": "assistant", "content": reply_text})
            
            # Detect emotion
            # In Observer mode, 'expression' might differ from 'text sentiment'.
            # We still let the detector run, but the config rules say "Don't show emotion".
            # The user might want the avatar to REMAIN neutral physically.
            # However, the prompt says "Cuteness exists in voice and expression only".
            # So we SHOULD return the detected emotion to drive the avatar.
            emo = detect_emotion(reply_text)
            
            return reply_text, emo
            
        except Exception as e:
            print(f"Error in brain: {e}")
            return "通信エラー。観測を中断します。", "Sad"

# Simple instance
brain_instance = VtuberBrain()
