from jwt import InvalidSignatureError, decode


def verify_signature(token: str, signature_secret: str = None) -> bool:
    """
    Method to verify that an incoming JWT was sent by Vonage.
    """

    try:
        decode(token, signature_secret, algorithms='HS256')
        return True
    except InvalidSignatureError:
        return False
    except Exception as e:
        raise VonageVerifyJwtError(repr(e))


class VonageVerifyJwtError(Exception):
    """The signature could not be verified."""
