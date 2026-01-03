from audio import speak_piper, ascii_only
from brain import (
    is_probably_shell_command,
    add_memory,
    talk_stream,
    stream_speak,
)


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