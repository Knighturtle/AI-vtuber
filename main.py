import threading
import sys
import time

from config import VSEE_IP, VSEE_PORT
from brain import get_reply_and_emotion
from audio import speak_jp
from vseeface_osc import set_emotion, clear_all

# Exaggerated Expression Mapping (Visual Enhancement)
# Maps detected emotion -> visually distinct display emotion
# [VERIFICATION MODE] Strict 1:1 mapping
EMOTION_DISPLAY_MAP = {
    "Neutral": "Neutral",
    "Joy": "Joy",
    "Angry": "Angry",
    "Sorrow": "Sorrow",
    "Surprise": "Surprise",
    "Fun": "Fun"
}

def run_visual_test():
    """Cycle through all emotions for visual verification (2s hold)."""
    print("\n>>> STARTING VISUAL TEST SEQUENCE <<<")
    
    # Test sequence: Neutral -> Fun -> Joy -> Angry -> Sorrow -> Surprise (Mapped)
    test_emotions = ["Neutral", "Fun", "Joy", "Angry", "Sorrow", "Surprise"]
    
    for raw_emo in test_emotions:
        # Apply the mapping even in test to verify exactly what user sees
        display_emo = EMOTION_DISPLAY_MAP.get(raw_emo, "Neutral")
        print(f"[TEST] Raw: {raw_emo} -> Display: {display_emo}")
        
        if display_emo == "Neutral":
             clear_all()
             time.sleep(2.0)
        else:
             set_emotion(display_emo, 1.0, 2.0) # 2s hold for test
             
    print(">>> VISUAL TEST COMPLETE <<<\n")

def main():
    print("=== AI VTuber System Started ===")
    print(f"Target: VSeeFace @ {VSEE_IP}:{VSEE_PORT}")
    print("Commands: 'q', 'quit', 'exit' to stop.")
    print("Command:  '/test' to run visual expression test.")
    
    # Ensure clean state
    clear_all()

    while True:
        try:
            user_input = input("\nYou> ").strip()
        except EOFError:
            break
            
        if not user_input:
            continue
            
        if user_input.lower() in ["q", "quit", "exit"]:
            print("Exiting...")
            break

        if user_input.lower() == "/test":
            run_visual_test()
            continue

        # 1. Brain Processing
        print("...")
        reply, emotion = get_reply_and_emotion(user_input)
        
        # 2. Apply Visual Enhancement Mapping
        display_emotion = EMOTION_DISPLAY_MAP.get(emotion, "Neutral")
        
        print(f"[AI] Emotion: {emotion}")
        print(f"[DISPLAY] Emotion sent to VSeeFace: {display_emotion}")
        print(f"[AI] Reply:   {reply}")

        # 3. Parallel Actions
        # Thread 1: Face Expression
        # Increased hold time to 5.0s for better visibility
        t_face = threading.Thread(target=set_emotion, args=(display_emotion, 1.0, 5.0))
        
        # Thread 2: Audio
        print(f"[AUDIO] speaking: {reply}")
        t_audio = threading.Thread(target=speak_jp, args=(reply,))
        
        t_face.start()
        t_audio.start()
        
        # Wait for both to finish before accepting next input
        t_face.join()
        t_audio.join()
        
    print("=== System Shutdown ===")

if __name__ == "__main__":
    main()
