import re

from ollama import chat

from audio import speak_piper, ascii_only
from config import SYSTEM_PROMPT, OLLAMA_MODEL


# ---------------------------
# HELPERS
# ---------------------------
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


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