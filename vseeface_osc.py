from pythonosc import udp_client
import time
from config import VSEE_IP, VSEE_PORT, EMOTION_PARAMS

# Setup OSC client for VSeeFace VMC Receiver
client = udp_client.SimpleUDPClient(VSEE_IP, VSEE_PORT)

def send_vmc_blend(name: str, value: float):
    """
    Send VMC protocol message for BlendShape.
    Address: /VMC/Ext/Blend/Val
    Payload: [name, value]
    """
    client.send_message("/VMC/Ext/Blend/Val", [name, float(value)])
    print(f"[OSC] Sent {name} = {value}")

def clear_all():
    """Reset all registered emotions (except Neutral) to 0.0"""
    print("[OSC] Clearing all emotions...")
    for emo in EMOTION_PARAMS:
        if emo == "Neutral":
            continue
        send_vmc_blend(emo, 0.0)

def set_emotion(name: str, strength: float = 1.0, hold_sec: float = 0.8):
    """
    Set a specific emotion using VMC protocol.
    Defaults: strength=1.0, hold_sec=0.8
    """
    if name not in EMOTION_PARAMS:
        print(f"[WARN] Unknown emotion: {name}, ignored.")
        return

    # 1. Clear others (always done first)
    clear_all()
    
    # Neutral is just "all cleared"
    if name == "Neutral":
        return
    
    # 2. Set new emotion
    send_vmc_blend(name, strength)
    
    # 3. Hold if requested
    if hold_sec > 0:
        time.sleep(hold_sec)
        # Reset this specific emotion
        send_vmc_blend(name, 0.0)

if __name__ == "__main__":
    print(f"Connecting to {VSEE_IP}:{VSEE_PORT}...")
    
    # Demo Sequence
    print(">>> Triggering Neutral")
    set_emotion("Neutral")
    time.sleep(1)

    for emo in ["Fun", "Joy", "Angry", "Sorrow", "Surprise"]:
        print(f">>> Triggering {emo}")
        set_emotion(emo, 1.0, 2.0)
    
    print("DONE")
