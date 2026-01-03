from pathlib import Path

# ---------------------------
# SETTINGS
# ---------------------------
SYSTEM_PROMPT = """You are a cute anime VTuber.
You are friendly, slightly playful, and talk like a livestreamer.
Keep replies short and natural.
IMPORTANT:
- Use plain ASCII only (no emoji).
- If the user types a shell command, tell them to run it in PowerShell, not in chat.
"""

OLLAMA_MODEL = "gemma3:4b"

PIPER_DIR = Path(r"C:\piper")
PIPER_EXE = PIPER_DIR / "piper.exe"
MODEL = PIPER_DIR / "models" / "en_US-lessac-medium.onnx"
CONFIG = PIPER_DIR / "models" / "en_US-lessac-medium.onnx.json"
ESPEAK_DATA = PIPER_DIR / "espeak-ng-data"
OUT_WAV = PIPER_DIR / "out.wav"

# TTS tuning (optional): 1.0 = normal, >1.0 slower, <1.0 faster
LENGTH_SCALE = "1.2"

# ---------------------------
# LOGGING & IDLE TALK SETTINGS
# ---------------------------
LOG_DIR = Path("logs")
CONVERSATION_LOG = LOG_DIR / "conversation.log"
ERROR_LOG = LOG_DIR / "error.log"

# Autonomous self-talk master switch
AUTONOMOUS_MODE_ENABLED = True

# Seconds before VTuber starts talking when no user input (10–20 sec recommended)
IDLE_USER_TIMEOUT = 15
# Minimum seconds between automatic talks
IDLE_MIN_INTERVAL = 60
# Maximum number of automatic talks per session
IDLE_MAX_MESSAGES = 10
