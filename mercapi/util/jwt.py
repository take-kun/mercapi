import random
from time import time
from typing import Dict, Optional
from uuid import UUID

from ecdsa import SigningKey
from jose import jws
from jose.backends.ecdsa_backend import ECDSAECKey
from jose.constants import ALGORITHMS


def generate_dpop(
    url: str,
    method: str,
    key: SigningKey,
    extra_payload: Optional[Dict[str, str]] = None,
) -> str:
    payload = {
        "iat": int(time()),
        "jti": str(UUID(int=random.getrandbits(128))),
        "htu": url,
        "htm": method,
        **extra_payload,
    }

    ec_key = ECDSAECKey(key, ALGORITHMS.ES256)
    headers = {
        "typ": "dpop+jwt",
        "alg": "ES256",
        "jwk": {k: ec_key.to_dict()[k] for k in ["crv", "kty", "x", "y"]},
    }

    return jws.sign(payload, key, headers, ALGORITHMS.ES256)
