import base64
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives._serialization import PublicFormat, Encoding
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey

from records.record import Record, RecordType


class UserData(Record):
    def __init__(self, first_name, last_name, dob, public_key: RSAPublicKey):
        super().__init__(record_type=RecordType.USER_DATA)
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.public_key: RSAPublicKey = public_key

    def __str__(self):
        data = {
            'record_type': self.record_type.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob,
            'public_key': self.public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
        }
        return json.dumps(data)

    def json_serialize(self):
        first_name_encrypted = self.encrypt(self.first_name)
        last_name_encrypted = self.encrypt(self.last_name)
        data = {
            'record_type': self.record_type.name,
            'first_name': first_name_encrypted,
            'last_name': last_name_encrypted,
            'dob': self.dob,
            'public_key': self.public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
        }
        return json.dumps(data)

    def encrypt(self, data):
        encrypted_bytes = self.public_key.encrypt(data.encode('utf-8'),
                                                  padding.OAEP(
                                                      mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                      algorithm=hashes.SHA256(),
                                                      label=None
                                                  ))
        return base64.b64encode(encrypted_bytes).decode('ASCII')

    @staticmethod
    def decrypt_user_data_block(block_json, private_key: RSAPrivateKey):
        first_name_encrypted = block_json['first_name']
        last_name_encrypted = block_json['last_name']
        first_name = UserData.decrypt_string(first_name_encrypted, private_key)
        last_name = UserData.decrypt_string(last_name_encrypted, private_key)

        return UserData(
            first_name,
            last_name,
            block_json['dob'],
            private_key.public_key()
        )

    @staticmethod
    def decrypt_string(encrypted_string, private_key: RSAPrivateKey):
        decoded_bytes = base64.b64decode(encrypted_string.encode('ASCII'))
        return private_key.decrypt(
            decoded_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode('utf-8')

    @staticmethod
    def json_deserialize_userdata(json_string):
        json_object = json.loads(json_string)
        return UserData(
            json_object['first_name'],
            json_object['last_name'],
            json_object['dob'],
            json_object['public_key']
        )
