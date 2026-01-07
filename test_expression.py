import time
from vseeface_osc import set_emotion, clear_all
from config import EMOTION_PARAMS

def run_test():
    print("Starting VSeeFace Expression Test...")
    
    # Ensure clean slate
    clear_all()
    time.sleep(1)

    for emo in EMOTION_PARAMS:
        print(f"Testing: {emo}")
        set_emotion(emo, strength=1.0)
        time.sleep(2)
        
    print("Returning to Neutral (Clear)")
    clear_all()
    print("Test Complete.")

if __name__ == "__main__":
    run_test()
