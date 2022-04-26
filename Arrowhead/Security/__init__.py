from asyncio.windows_events import NULL
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class SecurityManager:
    generated = False

    @staticmethod
    def generateKeys():
        if not SecurityManager.generated:
            SecurityManager.private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048,)
            SecurityManager.generated = True

    @staticmethod
    def getSignature(message):
        signature = SecurityManager.private_key.sign(message,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
        return signature

    @staticmethod
    def getPublicKey():
        pub = {}
        pub_key = SecurityManager.private_key.public_key()
        pub["n"] = pub_key.public_numbers().n
        pub["e"] = pub_key.public_numbers().e
        return pub
