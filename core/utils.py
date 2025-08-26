# core/utils.py
import os, json, hashlib
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "sample_data", "simulated_db.json")
KEY_PATH = os.path.join(os.path.dirname(__file__), "..", ".fernet_key")

def ensure_dir(path):
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def ensure_key():
    key = os.getenv("FERNET_KEY")
    if key:
        return key
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as f:
            key = f.read()
            return key.decode()
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    return key.decode()

def _get_fernet():
    return Fernet(ensure_key().encode())

def anonymize_candidate_record(candidate: dict) -> dict:
    email = candidate.get("email", "").lower()
    phone = candidate.get("phone", "")
    email_hash = hashlib.sha256(email.encode()).hexdigest()
    phone_hash = hashlib.sha256(phone.encode()).hexdigest() if phone else ""
    summary = {
        "name_masked": (candidate.get("full_name", "").split(" ")[0] + "***") if candidate.get("full_name") else "anon",
        "years_exp": candidate.get("years_exp"),
        "role": candidate.get("role"),
        "skills": candidate.get("skills"),
    }
    f = _get_fernet()
    token = f.encrypt(json.dumps(candidate).encode()).decode()
    return {"email_hash": email_hash, "phone_hash": phone_hash, "payload_enc": token, "summary": summary}

def save_candidate_record(candidate: dict) -> str:
    ensure_dir(DB_PATH)
    record = anonymize_candidate_record(candidate)
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            try: db = json.load(f)
            except json.JSONDecodeError: db = {}
    else:
        db = {}
    import time
    rid = f"c_{int(time.time())}"
    db[rid] = record
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)
    return rid

def load_all_records() -> dict:
    if not os.path.exists(DB_PATH): return {}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        try: return json.load(f)
        except json.JSONDecodeError: return {}

def decrypt_payload(token: str) -> dict:
    return json.loads(_get_fernet().decrypt(token.encode()).decode())
