import time
try:
    import sounddevice as sd
except ImportError:
    sd = None # Fallback if not installed, though requirements include it.

import pyttsx3
import threading

from vtuber_brain import VtuberBrain
from vsee_face_osc import set_emotion, clear_all

def main():
    print("Initializing AI VTuber...")
    
    # Setup Logic
    brain = VtuberBrain()
    
    # Setup TTS
    engine = pyttsx3.init()
    # Configure voice if possible (first available)
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id) 
    engine.setProperty('rate', 150) # Speed

    print("VTuber Started. Type 'exit' to quit.")
    print("Listening for input... (Text-based for now)")

    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                break
                
            # 1. AI Processing
            reply_text, emotion = brain.generate_response(user_input)
            print(f"VTuber ({emotion}): {reply_text}")
            
            # 2. Set Emotion
            set_emotion(emotion)
            
            # 3. Speak (This blocks until finished in simple pyttsx3 usage)
            # If using VSeeFace Audio Lip Sync, verify VSeeFace is listening to output device.
            engine.say(reply_text)
            engine.runAndWait()
            
            # 4. Wait 2 seconds then clear emotion
            time.sleep(2.0)
            clear_all()
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        clear_all()
        print("Done.")

if __name__ == "__main__":
    main()
