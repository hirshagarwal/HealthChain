import base64
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives._serialization import PublicFormat, Encoding
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from records.record import Record, RecordType


class UserData(Record):
    def __init__(self, first_name, last_name, dob, public_key):
        super().__init__(record_type=RecordType.USER_DATA)
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.public_key: RSAPublicKey = public_key

    def __str__(self):
        return self.json_serialize()

    def json_serialize(self):
        data = {
            'record_type': self.record_type.name,
            'first_name': str(base64.b64encode(self.encrypt(self.first_name))),
            'last_name': self.last_name,
            'dob': self.dob,
            'public_key': self.public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
        }
        return json.dumps(data)

    def encrypt(self, data):
        return self.public_key.encrypt(data.encode('utf-8'),
                                       padding.OAEP(
                                           mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                           algorithm=hashes.SHA256(),
                                           label=None
                                       ))

    @staticmethod
    def json_deserialize_userdata(json_string):
        json_object = json.loads(json_string)
        return UserData(
            json_object['first_name'],
            json_object['last_name'],
            json_object['dob'],
            json_object['public_key']
        )
