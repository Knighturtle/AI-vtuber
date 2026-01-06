import logging
import queue
import threading
import time

from audio import speak_piper, ascii_only
from brain import (
    is_probably_shell_command,
    add_memory,
    talk_stream,
    stream_speak,
)
from config import (
    LOG_DIR,
    CONVERSATION_LOG,
    ERROR_LOG,
    AUTONOMOUS_MODE_ENABLED,
    IDLE_USER_TIMEOUT,
    IDLE_MIN_INTERVAL,
    IDLE_MAX_MESSAGES,
)


conversation_logger = logging.getLogger("conversation")
error_logger = logging.getLogger("error")


def setup_logging() -> None:
    """Set up file loggers for conversation and errors."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Avoid adding handlers multiple times (e.g., if main() is re-run)
    if conversation_logger.handlers or error_logger.handlers:
        return

    formatter = logging.Formatter("%(asctime)s - %(message)s")

    conv_handler = logging.FileHandler(CONVERSATION_LOG, encoding="utf-8")
    conv_handler.setFormatter(formatter)
    conversation_logger.setLevel(logging.INFO)
    conversation_logger.addHandler(conv_handler)
    conversation_logger.propagate = False

    err_handler = logging.FileHandler(ERROR_LOG, encoding="utf-8")
    err_handler.setFormatter(formatter)
    error_logger.setLevel(logging.INFO)
    error_logger.addHandler(err_handler)
    error_logger.propagate = False


def input_worker(input_queue: "queue.Queue[str]", stop_event: threading.Event) -> None:
    """Read user input lines in a separate thread and push them to a queue."""
    while not stop_event.is_set():
        try:
            user_text = input("You: ")
        except EOFError:
            break
        input_queue.put(user_text)
        if user_text.strip().lower() in ("exit", "quit"):
            break


def maybe_idle_talk(
    last_user_time: float,
    last_idle_talk_time: float,
    idle_talk_count: int,
) -> tuple[float, int]:
    """If enough time has passed with no user input, have the VTuber talk once."""
    now = time.time()
    if (
        AUTONOMOUS_MODE_ENABLED
        and now - last_user_time >= IDLE_USER_TIMEOUT
        and idle_talk_count < IDLE_MAX_MESSAGES
        and now - last_idle_talk_time >= IDLE_MIN_INTERVAL
    ):
        prompt = (
            "It's quiet in chat. As a VTuber, say a short, natural monologue or question "
            "to the viewers. Keep it friendly and brief, like a real streamer talking to viewers."
        )
        print("VTuber: ", end="", flush=True)
        try:
            reply = stream_speak(talk_stream(prompt))
            reply = ascii_only(reply)
            conversation_logger.info("ASSISTANT_IDLE: %s", reply)
            add_memory("assistant", reply)
        except Exception as e:  # noqa: F841 - logged below
            print(f"\n[ERROR] Idle talk failed: {e}")
            error_logger.exception("Idle talk failed")
            return last_idle_talk_time, idle_talk_count
        return now, idle_talk_count + 1

    return last_idle_talk_time, idle_talk_count


# ---------------------------
# MAIN LOOP
# ---------------------------
def main() -> None:
    setup_logging()

    print("VTuber is online! Type 'exit' to quit.")
    conversation_logger.info("SYSTEM: VTuber started")
    speak_piper("VTuber is online.")

    input_queue: "queue.Queue[str]" = queue.Queue()
    stop_event = threading.Event()
    thread = threading.Thread(
        target=input_worker,
        args=(input_queue, stop_event),
        daemon=True,
    )
    thread.start()

    last_user_time = time.time()
    last_idle_talk_time = 0.0
    idle_talk_count = 0

    try:
        while True:
            try:
                # Wait for user input with timeout so we can trigger idle talk
                user_raw = input_queue.get(timeout=1.0)
            except queue.Empty:
                last_idle_talk_time, idle_talk_count = maybe_idle_talk(
                    last_user_time, last_idle_talk_time, idle_talk_count
                )
                continue

            user_text = user_raw.strip()

            # 空行は「入力があった」とみなしてアイドルタイマーだけリセット
            if not user_text:
                last_user_time = time.time()
                continue

            last_user_time = time.time()

            if user_text.lower() in ("exit", "quit"):
                conversation_logger.info("USER: %s", user_text)
                break

            conversation_logger.info("USER: %s", user_text)

            # Stop accidental shell commands being treated as chat
            if is_probably_shell_command(user_text):
                msg = "That looks like a command. Run it in PowerShell, not in chat."
                print(f"VTuber: {msg}")
                conversation_logger.info("ASSISTANT: %s", msg)
                speak_piper(msg)
                continue

            # Memory: store user
            add_memory("user", user_text)

            # Stream reply: print + speak as it streams
            print("VTuber: ", end="", flush=True)
            try:
                final_reply = stream_speak(talk_stream(user_text))
            except Exception as e:  # noqa: F841 - logged below
                print(f"\n[ERROR] Failed to talk: {e}")
                error_logger.exception("Failed to talk to user")
                fallback = "Sorry, I had a problem replying just now."
                speak_piper(fallback)
                final_reply = fallback

            final_reply = ascii_only(final_reply)
            conversation_logger.info("ASSISTANT: %s", final_reply)

            # Memory: store assistant
            add_memory("assistant", final_reply)
    finally:
        stop_event.set()
        conversation_logger.info("SYSTEM: VTuber stopped")


if __name__ == "__main__":
    main()
    from pythonosc.udp_client import SimpleUDPClient
