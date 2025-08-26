# core/i18n.py
from deep_translator import GoogleTranslator

supported_langs = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
}

def translate_text(text: str, target_lang: str = "en") -> str:
    try:
        if not text or target_lang == "en":
            return text
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception:
        return text
