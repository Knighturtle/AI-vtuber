import re
from ollama import chat
from config import SYSTEM_PROMPT, OLLAMA_MODEL, EMOTION_PARAMS

def normalize_emotion(raw_emo: str) -> str:
    """Normalize emotion string to one of the allowed params or Neutral."""
    raw = raw_emo.strip().lower()
    valid_map = {e.lower(): e for e in EMOTION_PARAMS}
    
    if raw in valid_map:
        return valid_map[raw]
    return "Neutral"

def get_reply_and_emotion(user_text: str):
    """
    Send text to Ollama and robustly parse response.
    Returns: (reply_text, emotion_label)
    """
    
    # 1. Angry Override Check (Pre-LLM or Post-LLM? User implies override result)
    # We will check this at the end to overwrite LLM's emotion if needed.
    angry_keywords = ["ふざけるな", "ムカつく", "怒る", "舐めるな", "馬鹿"]
    is_angry_input = any(k in user_text for k in angry_keywords)

    # 2. Strict Prompt
    prompt = f"""
User says: "{user_text}"

Instructions:
1. Decide emotion from: {', '.join(EMOTION_PARAMS)}
2. Write a short Japanese reply.
3. ABSOLUTELY NO MARKDOWN. NO **bold**. NO QUOTES.
4. Output format must be EXACTLY two lines:
EMOTION: <Emotion>
REPLY: <Reply text>
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    try:
        response = chat(model=OLLAMA_MODEL, messages=messages)
        content = response['message']['content'].strip()
        
        # Requirement 3: Raw Log
        print(f"[LLM RAW] {content}")

        # Requirement 2: Robust Parsing
        emotion = "Neutral"
        reply = content 

        # Find EMOTION (Case insensitive, lenient separator)
        # Matches: "EMOTION: Joy", "EMOTION=Joy", "**EMOTION**: Joy", "Emotion Joy"
        emo_match = re.search(r"(?:EMOTION|Emotion)[\s:=]+([a-zA-Z]+)", content)
        if emo_match:
            emotion = normalize_emotion(emo_match.group(1))
        
        # Find REPLY
        # Look for "REPLY:" etc, and take everything after.
        reply_match = re.search(r"(?:REPLY|Reply)[\s:=]+(.*)", content, re.DOTALL)
        if reply_match:
            reply = reply_match.group(1).strip()
            
            # Inner cleanup if potential double prefix
            inner_match = re.match(r"^(?:REPLY|Reply)[\s:=「]+", reply, re.IGNORECASE)
            if inner_match:
                reply = reply[inner_match.end():].strip()
        else:
            # Fallback: remove emotion line from content
            lines = content.split('\n')
            clean_lines = []
            for line in lines:
                # If line looks like EMOTION header, skip
                if re.match(r"^\s*(?:EMOTION|Emotion)[\s:=]+", line):
                    continue
                # If line is just empty or symbols
                if not line.strip():
                    continue
                clean_lines.append(line)
            if clean_lines:
                reply = "\n".join(clean_lines).strip()

        # Final Cleanup of Reply
        reply = reply.strip('"\'')
        reply = re.sub(r"^(?:REPLY|Reply)[\s:=]+", "", reply, flags=re.IGNORECASE).strip()

        # 4. Apply Angry Override
        if is_angry_input:
            print("[LOGIC] Angry keyword detected -> Forcing Angry")
            emotion = "Angry"

        return reply, emotion

    except Exception as e:
        print(f"[ERROR] Ollama failed: {e}")
        return "エラーが発生しました。", "Sorrow"