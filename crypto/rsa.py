from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


# https://stackoverflow.com/questions/2466401/how-to-generate-ssh-key-pairs-with-python
def generate_rsa_key_pair(return_as_bytes: bool = True):
    private_key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=4096)
    public_key = private_key.public_key()
    private_key_bytes: bytes = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                         format=serialization.PrivateFormat.PKCS8,
                                                         encryption_algorithm=serialization.NoEncryption())
    public_key_bytes: bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                      format=serialization.PublicFormat.SubjectPublicKeyInfo)
    if return_as_bytes:
        return private_key_bytes, public_key_bytes

    return private_key_bytes.decode('utf-8'), public_key_bytes.decode('utf-8')