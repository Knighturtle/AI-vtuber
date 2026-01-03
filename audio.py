import subprocess
import winsound

from config import PIPER_EXE, MODEL, CONFIG, ESPEAK_DATA, OUT_WAV, LENGTH_SCALE, PIPER_DIR


def ascii_only(text: str) -> str:
    """Remove any non-ASCII chars (prevents cp1252 UnicodeEncodeError)."""
    return text.encode("ascii", errors="ignore").decode()


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
    try:
        subprocess.run(
            cmd,
            input=text + "\n",
            text=True,
            check=True,
            cwd=str(PIPER_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        # Do not crash the whole VTuber if TTS fails; just warn and skip.
        print(f"[WARN] Piper TTS failed: {e}")
        return

    winsound.PlaySound(str(OUT_WAV), winsound.SND_FILENAME)
