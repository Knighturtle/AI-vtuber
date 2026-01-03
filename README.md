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
.
├─ main.py        # Application entry point and main I/O loop

├─ brain.py       # LLM interaction, streaming logic, and memory

├─ audio.py       # Text-to-speech pipeline (Piper)

├─ config.py      # Configuration, paths, and model settings

├─ vtuber_brain.py# Original single-file prototype (reference)

├─ requirements.txt

└─ README.md

