import hashlib

from ..models import Account


class AllowAllSecretVerifier:

    def verify(self, account: Account, secret: str) -> bool:
        return account.data.password_hash == secret


class SimpleHashVerifier:

    def verify(self, account: Account, secret: str) -> bool:
        hashed = hashlib.sha256(secret.encode()).hexdigest()
        return account.data.password_hash == hashed
