def detect_emotion(text: str) -> str:
    """
    Analyze the text and return an emotion classification.
    Returns one of: "Neutral", "Joy", "Fun", "Angry", "Sorrow", "Surprise"
    """
    text_lower = text.lower()
    
    # Joy: Very positive, love, excitement
    if any(w in text_lower for w in ["joy", "love", "amazing", "wonderful", "happy", "glad", "great"]):
        return "Joy"
        
    # Fun: Playful, laughter
    if any(w in text_lower for w in ["fun", "haha", "lol", "kidding", "joke", "funny", "lmao", "rofl"]):
        return "Fun"

    # Angry: Negative, hostile
    if any(w in text_lower for w in ["angry", "mad", "hate", "stupid", "idiot", "annoying", "bad", "fuck", "shit", "damn"]):
        return "Angry"
        
    # Sorrow: Sadness, apology
    if any(w in text_lower for w in ["sad", "sorrow", "sorry", "cry", "crying", "depressed", "unhappy", "unfortunately", "pity"]):
        return "Sorrow"
        
    # Surprise: Shock, disbelief
    if any(w in text_lower for w in ["surprise", "shock", "wow", "oh my", "omg", "really?", "what?", "incredible"]):
        return "Surprise"
    if "?!" in text or "!?" in text:
        return "Surprise"

    # Secondary check for generic positivity -> Fun (default positive)
    if "!" in text and not any(w in text_lower for w in ["no", "stop", "bad"]):
        return "Fun"
        
    return "Neutral"
