from pythonosc import udp_client
import time

# VSeeFace OSC Settings
VSEE_IP = "127.0.0.1"
VSEE_PORT = 39539
EMOTION_PARAMS = ["Neutral", "Joy", "Fun", "Angry", "Sorrow", "Surprise"]

client = udp_client.SimpleUDPClient(VSEE_IP, VSEE_PORT)

def clear_all():
    """Reset all registered emotions to 0.0"""
    for emo in EMOTION_PARAMS:
        if emo == "Neutral": continue # Neutral isn't a blendshape usually, but the state.
        client.send_message(f"/avatar/parameters/{emo}", 0.0)

def set_emotion(name: str, strength: float = 1.0):
    """
    Set a specific emotion. 
    1. Clears other emotions.
    2. Sets 'name' to 'strength'.
    """
    # Normalize name if needed (e.g. capitalizing)
    if name not in EMOTION_PARAMS:
        # Fallback or ignore
        if name != "Neutral":
             print(f"[WARN] Unknown emotion: {name}")
        clear_all()
        return

    if name == "Neutral":
        clear_all()
        return

    # Clear first ensures 'Toggle' behavior (only one active)
    clear_all()
    
    # Send new emotion
    client.send_message(f"/avatar/parameters/{name}", float(strength))
