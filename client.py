import uuid

import requests as requests
from requests import Response

from blockchain import Block
from clienthelper import ClientHelper
from records.userdata import UserData
from user import User


class HealthChainClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.helper = ClientHelper(host, port)

    def add_block(self, new_block: Block):
        request_response = requests.post("http://{}:{}/add_block".format(
            self.host,
            self.port),
            data=new_block.get_json())
        return request_response.json()

    def get_blockchain(self) -> Response:
        return requests.get("http://{}:{}/get_blockchain"
                            .format(self.host, self.port)).json()


def create_user_demo():
    demo_client = HealthChainClient('localhost', '8080')
    demo_user = User(uuid.uuid4())
    demo_block = demo_client.helper.build_user_block('Hirsh', 'Agarwal', '16/08/1997', demo_user)
    demo_response = demo_client.add_block(demo_block)
    print(demo_response)
    decrypted_block = UserData.decrypt_user_data_block(demo_response['block_data'], demo_user.private_key)
    print(decrypted_block)


if __name__ == '__main__':
    client = HealthChainClient('localhost', '8081')
    user = User(uuid.uuid4())
    block = client.helper.build_user_block('Hirsh', 'Agarwal', '16/08/1997', user)
    response = client.add_block(block)

    note_block = client.helper.build_note_block("Patient attended clinic today...", user)
    note_block.signed_hash = user.sign_message(note_block.hash.encode('utf-8'))
    # response_note = client.add_block(note_block)
    # response_note2 = client.add_block(note_block)
    print(client.get_blockchain())

