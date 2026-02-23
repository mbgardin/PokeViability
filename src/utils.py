import os
import re
import requests

def ensure_dirs():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/cleaned", exist_ok=True)

def get_json(url: str) -> dict:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()

def normalize_name(name: str) -> str:
    # good enough baseline; add a manual fix dict later if needed
    s = name.strip().lower()
    s = s.replace(" ", "-")
    s = s.replace(".", "")
    s = s.replace("'", "")
    s = s.replace(":", "")
    s = re.sub(r"[^a-z0-9\-]", "", s)
    return s