# AI VTuber (Neuro-sama–inspired)

A Python-based AI VTuber prototype that combines:
- LLM streaming responses (Ollama)
- Real-time TTS output (Piper)
- Modular architecture (main/brain/audio/config)

## Features
- Streaming text output
- Voice output (TTS)
- Simple chat memory
- Command-like input detection
- Modular structure for future autonomy / 24-7 operation

## Project Structure
- `main.py` : main loop (I/O)
- `brain.py`: LLM + streaming logic + memory
- `audio.py`: TTS pipeline (Piper)
- `config.py`: settings / paths

## Requirements
- Windows
- Python 3.10+
- Ollama installed and running
- Piper installed (local)

## Run
```powershell
pip install -r requirements.txt
python main.py
