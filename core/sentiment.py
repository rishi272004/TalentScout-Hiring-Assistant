# core/sentiment.py
from textblob import TextBlob
from langdetect import detect
from deep_translator import GoogleTranslator

def analyze_sentiment(text: str) -> dict:
    if not text:
        return {"lang": None, "polarity": 0.0, "subjectivity": 0.0, "label": "neutral"}
    try:
        lang = detect(text)
    except Exception:
        lang = "en"
    if lang != "en":
        try:
            text_en = GoogleTranslator(source='auto', target='en').translate(text)
        except Exception:
            text_en = text
    else:
        text_en = text
    tb = TextBlob(text_en)
    polarity = tb.sentiment.polarity
    subjectivity = tb.sentiment.subjectivity
    label = "positive" if polarity > 0.1 else ("negative" if polarity < -0.1 else "neutral")
    return {"lang": lang, "polarity": polarity, "subjectivity": subjectivity, "label": label}
