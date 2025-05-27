import hashlib

def hash_pw(password:str) -> str:
    """Return a SHA-256 hash of the given password."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()