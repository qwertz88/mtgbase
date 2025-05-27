import hashlib

def hash_pw(password: str) -> str:
    """
    Generates a SHA-256 hash of the given password.

    Parameters
    ----------
    password : str
        The password string to be hashed.

    Returns
    -------
    str
        The hexadecimal representation of the SHA-256 hash.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()