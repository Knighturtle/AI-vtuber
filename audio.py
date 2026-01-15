import traceback
import pyttsx3
import time

def _pick_jp_voice(eng):
    try:
        voices = eng.getProperty("voices") or []
        for v in voices:
            name = (getattr(v, "name", "") or "")
            vid  = (getattr(v, "id", "") or "")
            if ("Haruka" in name) or ("JA-JP" in vid) or ("ja-JP" in vid):
                eng.setProperty("voice", v.id)
                print(f"[AUDIO] using voice: {name}")
                return
        if voices:
            # Fallback
            default_name = getattr(voices[0], "name", "Default")
            print(f"[AUDIO] using default voice: {default_name}")
    except Exception as e:
        print("[AUDIO][WARN] voice select failed:", e)

def speak_jp(text: str):
    """
    Speak text using a fresh pyttsx3 engine instance every time.
    This prevents audio driver freeze issues on some Windows environments.
    """
    text = str(text or "").strip()
    if not text:
        return
    
    eng = None
    try:
        # Explicitly use sapi5 on Windows
        eng = pyttsx3.init(driverName="sapi5")
        eng.setProperty("rate", 170)
        eng.setProperty("volume", 1.0)
        
        _pick_jp_voice(eng)
        
        # print(f"[AUDIO] saying: {text[:20]}...")
        eng.say(text)
        eng.runAndWait()
        
    except Exception as e:
        print(f"[AUDIO][ERROR] speak failed: {e}")
        traceback.print_exc()
    finally:
        if eng:
            try:
                eng.stop()
                # Deliberately remove reference to aid GC
                del eng
            except Exception:
                pass

# Alias for compatibility
speak = speak_jp
