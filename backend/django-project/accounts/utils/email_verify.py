import secrets
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

def generate_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"

def make_code_hash(code: str) -> str:
    return make_password(code)

def verify_code(code: str, code_hash: str) -> bool:
    return check_password(code, code_hash)

def expires_at(minutes=10):
    return timezone.now() + timedelta(minutes=minutes)

