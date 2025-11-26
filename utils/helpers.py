import os
import hashlib

def hash_file(path):
    try:
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        return sha256.hexdigest()
    except:
        return None

def check_path_exists(path):
    return os.path.exists(path)
