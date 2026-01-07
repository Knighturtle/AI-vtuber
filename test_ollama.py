import ollama
from config import OLLAMA_MODEL

print("Testing Ollama streaming...")

for chunk in ollama.chat(
    model=OLLAMA_MODEL,
    messages=[{"role": "user", "content": "Say a very short hello."}],
    stream=True,
):
    text = (chunk.get("message") or {}).get("content") or ""
    if text:
        print(text, end="", flush=True)

print()
