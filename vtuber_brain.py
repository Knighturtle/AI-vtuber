# vtuber_brain.py
# Real-time VTuber reply: Ollama streaming + Piper TTS (sentence-by-sentence)
# Windows paths assumed: C:\piper\piper.exe, C:\piper\models\..., C:\piper\espeak-ng-data

from pathlib import Path
import subprocess
import winsound
import re

from ollama import chat


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
# HELPERS
# ---------------------------
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def ascii_only(text: str) -> str:
    """Remove any non-ASCII chars (prevents cp1252 UnicodeEncodeError)."""
    return text.encode("ascii", errors="ignore").decode()


def is_probably_shell_command(s: str) -> bool:
    """Very simple detection to stop accidental commands being treated as chat."""
    s = s.strip()
    if not s:
        return False
    starters = ("cd ", "dir", "ls", "python", "pip", "ollama", "chcp", "git", "cls", "start ", "code ")
    if s.lower().startswith(starters):
        return True
    if s.startswith((".", "..", ".\\", "C:\\", "D:\\")):
        return True
    return False


# ---------------------------
# PIPER TTS
# ---------------------------
def speak_piper(text: str) -> None:
    """Speak one chunk using Piper. ASCII-only to avoid Windows console encoding issues."""
    text = ascii_only(text.strip())
    if not text:
        return

    cmd = [
        str(PIPER_EXE),
        "--model", str(MODEL),
        "--config", str(CONFIG),
        "--espeak_data", str(ESPEAK_DATA),
        "--output_file", str(OUT_WAV),
        "--length_scale", str(LENGTH_SCALE),
    ]

    # Silence Piper logs (optional). Remove stdout/stderr if you want logs.
    subprocess.run(
        cmd,
        input=text + "\n",
        text=True,
        check=True,
        cwd=str(PIPER_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    winsound.PlaySound(str(OUT_WAV), winsound.SND_FILENAME)


# ---------------------------
# OLLAMA STREAMING
# ---------------------------
CHAT_MEMORY = []  # list of {"role": "user"/"assistant", "content": "..."}
MEMORY_LIMIT = 10


def add_memory(role: str, text: str) -> None:
    """Keep last N user/assistant messages."""
    global CHAT_MEMORY
    text = ascii_only(text.strip())
    if not text:
        return
    CHAT_MEMORY.append({"role": role, "content": text})
    if len(CHAT_MEMORY) > MEMORY_LIMIT:
        CHAT_MEMORY.pop(0)


def talk_stream(user_text: str):
    """Yield streamed tokens from Ollama (already ASCII-only)."""
    user_text = ascii_only(user_text)

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + CHAT_MEMORY
        + [{"role": "user", "content": user_text}]
    )

    stream = chat(
        model=OLLAMA_MODEL,
        messages=messages,
        stream=True,
    )

    for part in stream:
        chunk = part.get("message", {}).get("content", "")
        chunk = ascii_only(chunk)
        if chunk:
            yield chunk


def stream_speak(token_iter) -> str:
    """
    Print streaming text immediately, and speak sentence-by-sentence.
    Returns full final assistant reply (ASCII-only).
    """
    buf = ""
    full = ""
    spoken_any = False

    for token in token_iter:
        print(token, end="", flush=True)
        full += token
        buf += token

        parts = SENT_SPLIT.split(buf)
        # Speak all complete sentences; keep the last partial in buf
        for sent in parts[:-1]:
            sent = sent.strip()
            if sent:
                speak_piper(sent)
                spoken_any = True

        buf = parts[-1] if parts else ""

        # prevent buffer from growing too large
        if spoken_any and len(buf) > 500:
            buf = buf[-500:]

    # Speak leftover tail
    tail = buf.strip()
    if tail:
        speak_piper(tail)

    print()  # newline after reply
    return full.strip()


# ---------------------------
# MAIN LOOP
# ---------------------------
def main():
    print("VTuber is online! Type 'exit' to quit.")
    speak_piper("VTuber is online.")

    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue

        if user_text.lower() in ("exit", "quit"):
            break

        # Stop accidental shell commands being treated as chat
        if is_probably_shell_command(user_text):
            msg = "That looks like a command. Run it in PowerShell, not in chat."
            print(f"VTuber: {msg}")
            speak_piper(msg)
            continue

        # Memory: store user
        add_memory("user", user_text)

        # Stream reply: print + speak as it streams
        print("VTuber: ", end="", flush=True)
        final_reply = stream_speak(talk_stream(user_text))
        final_reply = ascii_only(final_reply)

        # Memory: store assistant
        add_memory("assistant", final_reply)


if __name__ == "__main__":
    main()
