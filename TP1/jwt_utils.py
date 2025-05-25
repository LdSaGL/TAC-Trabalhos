import json
import base64
import hmac
import hashlib
import hmac_key
from datetime import datetime, timedelta, timezone

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key, load_pem_public_key
)

# Secret used for HMAC (HS256)
SECRET_KEY = hmac_key.SECRET_KEY

# RSA key files (same as used for HTTPS)
PRIVATE_KEY_FILE = "key.pem"
PUBLIC_KEY_FILE = "cert.pem"

# Encodes data in Base64 URL format without padding
def base64url_encode(data: bytes) -> bytes:
    return base64.urlsafe_b64encode(data).rstrip(b'=')

# Decodes Base64 URL format, adding necessary padding
def base64url_decode(input_str: str) -> bytes:
    padding_len = (4 - len(input_str) % 4) % 4
    return base64.urlsafe_b64decode(input_str + ("=" * padding_len))

# Loads the RSA private key from file
def load_private_key():
    with open(PRIVATE_KEY_FILE, "rb") as f:
        return load_pem_private_key(f.read(), password=None)

# Loads the RSA public key from file
def load_public_key():
    with open(PUBLIC_KEY_FILE, "rb") as f:
        return load_pem_public_key(f.read())

# Generates a JWT using either HS256 (HMAC) or RS256 (RSA)
def generate_jwt(payload: dict, exp_minutes: int = 30, alg: str = "HS256") -> str:
    # Create header and expiration time
    header = {"alg": alg, "typ": "JWT"}
    payload = payload.copy()
    payload["exp"] = int((datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)).timestamp())

    # Encode header and payload in Base64 URL format
    header_b64 = base64url_encode(json.dumps(header).encode())
    payload_b64 = base64url_encode(json.dumps(payload).encode())
    to_sign = header_b64 + b"." + payload_b64

    # Sign with HMAC or RSA depending on the algorithm
    if alg == "HS256":
        signature = hmac.new(SECRET_KEY, to_sign, hashlib.sha256).digest()
    elif alg == "RS256":
        private_key = load_private_key()
        signature = private_key.sign(
            to_sign,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    else:
        raise ValueError("Unsupported algorithm")

    # Encode signature and return final token
    signature_b64 = base64url_encode(signature)
    return b".".join([header_b64, payload_b64, signature_b64]).decode()

# Verifies a JWT and returns the payload if valid, or None if invalid
def verify_jwt(token: str) -> dict | None:
    try:
        # Split token into parts
        header_b64, payload_b64, signature_b64 = token.split(".")
        to_verify = f"{header_b64}.{payload_b64}".encode()
        signature = base64url_decode(signature_b64)

        # Decode and read header to check algorithm
        header = json.loads(base64url_decode(header_b64))
        alg = header.get("alg")

        # Verify using the correct method
        if alg == "HS256":
            expected = hmac.new(SECRET_KEY, to_verify, hashlib.sha256).digest()
            if not hmac.compare_digest(expected, signature):
                return None  # Invalid HMAC signature
        elif alg == "RS256":
            public_key = load_public_key()
            public_key.verify(
                signature,
                to_verify,
                padding.PKCS1v15(),
                hashes.SHA256()
            )  # Raises exception if invalid
        else:
            return None  # Unsupported algorithm

        # Decode payload and check expiration
        payload = json.loads(base64url_decode(payload_b64))
        exp = payload.get("exp")
        if exp is None or datetime.now(timezone.utc).timestamp() > exp:
            return None  # Token expired

        return payload  # Token is valid

    except Exception:
        return None  # Any error means the token is invalid
