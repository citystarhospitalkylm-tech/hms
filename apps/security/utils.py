import jwt
from django.conf import settings
from ipaddress import ip_address


def get_client_ip(request):
    """
    Retrieves client IP from X-Forwarded-For or REMOTE_ADDR.
    """
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        # take first IP in the list
        ip = xff.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    try:
        return str(ip_address(ip))
    except ValueError:
        return None


def decode_jwt_token(token: str) -> dict:
    """
    Decodes a JWT using the project’s secret key and algorithm settings.
    """
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": True},
        )
    except jwt.PyJWTError as exc:
        raise ValueError(f"Invalid token: {exc}") from exc


def encrypt_data(plaintext: bytes) -> bytes:
    """
    Placeholder for AES-GCM or similar encryption.
    Integrate your KMS or key-management here.
    """
    raise NotImplementedError("Plug in your encryption backend")