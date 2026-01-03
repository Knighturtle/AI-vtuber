# AI VTuber (Streaming LLM + Real-time TTS)

A Python-based AI VTuber prototype that integrates **streaming large language model (LLM) responses** with **real-time text-to-speech (TTS)** output.  
This project focuses on **modular architecture**, **low-latency interaction**, and **extensibility** toward autonomous and long-running operation.

---

## Overview

This project demonstrates how a conversational AI system can:

- Generate **token-streamed responses** from a local LLM
- Convert responses into **real-time speech output**
- Maintain short-term conversational memory
- Separate concerns cleanly across modules for future scalability

The system is designed as a **foundation** for interactive agents, virtual assistants, or VTuber-style applications.

---

## Key Features

- **Streaming text generation**
  - Incremental token output from a local LLM (via Ollama)
- **Real-time voice synthesis**
  - Sentence-by-sentence speech playback using Piper TTS
- **Low-latency interaction**
  - Text is printed and spoken while the model is still generating
- **Simple conversation memory**
  - Short rolling chat history for contextual responses
- **Command-like input detection**
  - Prevents accidental shell commands from being treated as chat input
- **Modular architecture**
  - Clear separation of I/O, reasoning, audio, and configuration layers
- **Designed for future autonomy**
  - Structure supports expansion toward 24/7 or self-driven operation

---

## Project Structure
├─ main.py        # Application entry point and main I/O loop

├─ brain.py       # LLM interaction, streaming logic, and memory

├─ audio.py       # Text-to-speech pipeline (Piper)

├─ config.py      # Configuration, paths, and model settings

├─ vtuber_brain.py# Original single-file prototype (reference)

├─ requirements.txt

└─ README.md

Requirements / Installation / Running
## Requirements
- OS: Windows
- Python 3.10+
- Local LLM backend (Ollama)
- Local TTS engine (Piper)

## Installation
pip install -r requirements.txt

## Running
python main.py

LICENSE

MIT License

Copyright (c) 2026 Knighturtle

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

