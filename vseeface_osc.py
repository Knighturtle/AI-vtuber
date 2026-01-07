from pythonosc import udp_client
import time
from config import VSEE_IP, VSEE_PORT, EMOTION_PARAMS

client = udp_client.SimpleUDPClient(VSEE_IP, VSEE_PORT)

def clear_all():
    """Reset all registered emotions to 0.0"""
    for emo in EMOTION_PARAMS:
        client.send_message(f"/avatar/parameters/{emo}", 0.0)

def set_emotion(name: str, strength: float = 1.0, hold_sec: float = 0.0):
    """
    Set a specific emotion. 
    1. Clears other emotions.
    2. Sets 'name' to 'strength'.
    3. If hold_sec > 0, waits and then clears it (blocking).
       Usually we don't want to block main thread, so use hold_sec=0 for immediate return.
    """
    if name == "Neutral":
        clear_all()
        return

    # Check if valid to avoid sending garbage
    if name not in EMOTION_PARAMS:
        print(f"[WARN] Unknown emotion: {name}, ignored.")
        return

    # Clear others first to ensure single expression (optional, depends on model)
    clear_all()
    
    # Send new emotion
    client.send_message(f"/avatar/parameters/{name}", float(strength))
    
    if hold_sec > 0:
        time.sleep(hold_sec)
        client.send_message(f"/avatar/parameters/{name}", 0.0)
