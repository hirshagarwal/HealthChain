import uuid

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def sign_message(self, message_bytes):
        return self.private_key.sign(
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    @staticmethod
    def verify_message(signed_message, expected_message, public_key):
        public_key.verify(
            signed_message,
            expected_message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )


if __name__ == '__main__':
    user = User(uuid.uuid4())
    input_text = "H2 Micro".encode('utf-8')
    message = user.sign_message(input_text)
    user.verify_message(message, input_text, user.public_key)