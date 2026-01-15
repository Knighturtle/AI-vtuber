# AI-Vtuber "Full Start" Guide

This repository contains a simple AI VTuber system that connects Ollama (Brain), Piper (TTS), and VSeeFace (Avatar/Emotions).

## Prerequisites

- **Windows OS**
- **Python 3.10+**
- **Ollama** installed and running (Model: `gemma3:4b` or change in `config.py`)
- **Piper TTS** configured (paths in `config.py`)
- **VSeeFace** installed

## Setup Instructions

### 1. VSeeFace Configuration

1. Open VSeeFace.
2. Go to **Settings > General**.
3. Enable **OSC Receiver** (if applicable, but mainly we use VRChat format).
4. Go to **Settings > Advanced**.
5. Enable **"Send VRChat OSC data (experimental)"** (Actually we are *sending* TO VSeeFace, so ensure **"Listen for VRChat OSC data"** is ON).
   - Receiver Port: **39539** (Default)
   - *Note: VSeeFace listens on 39539 by default for VRChat-params.*
6. Ensure your avatar has BlendShapes named:
   - `Joy`
   - `Angry`
   - `Sad`
   - `Surprised`
   - *If your avatar uses different names (e.g. `Fun`, `Sorrow`), update `EMOTION_PARAMS` in `config.py`.*

### 2. Python Environment

Open PowerShell in this folder:

```powershell
# Create venv (if not exists)
python -m venv .venv

# Activate venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Test Expressions

Check if the avatar's face moves:

```powershell
python test_expression.py
```

*You should see the avatar cycle through Joy, Angry, Sad, Surprised.*
*If it doesn't move:*

- Check VSeeFace port (39539).
- Check IP (127.0.0.1).
- Check BlendShape names in VSeeFace vs `config.py`.

### 4. Run the VTuber

```powershell
python main.py
```

- Type in the console to talk to the VTuber.
- The VTuber will reply (Ollama), speak (Piper), and change expression (OSC).
- Use `Ctrl+C` or type `exit` to quit.

## Troubleshooting

- **No Audio**: Check `PIPER_DIR` path in `config.py`.
- **No Emotions**: Run `test_expression.py`. If fails, disable firewall or check VSeeFace OSC settings.
- **Ollama Error**: Ensure `ollama serve` is running and you have pulled the model (`ollama pull gemma3:4b`).
