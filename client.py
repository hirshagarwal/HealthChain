import json
import uuid

import requests as requests
from requests import Response

from blockchain import Block
from records.userdata import UserData
from user import User


class HealthChainClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def add_block(self, new_block: Block):
        pass

    def build_user_block(self, first_name, last_name, dob, user_object: User) -> Block:
        tail_block_json = requests.get("http://{}:{}/get_tail_block"
                                       .format(self.host, self.port)).json()
        tail_block = Block.from_json(tail_block_json)
        init_user_block = UserData(
            first_name,
            last_name,
            dob,
            user_object.public_key
        )
        user_block_serialized = init_user_block.json_serialize()
        return Block.new_block(tail_block, user.user_id, user_block_serialized)

    def get_blockchain(self) -> Response:
        return requests.get("http://{}:{}/get_blockchain"
                            .format(self.host, self.port))


if __name__ == '__main__':
    client = HealthChainClient('localhost', '8080')
    user = User(uuid.uuid4())
    block = client.build_user_block('Hirsh', 'Agarwal', '16/08/1997', user)
    block_data = json.loads(block.data)
    print(block_data)
    decrypted_block = UserData.decrypt_user_data_block(block_data, user.private_key)
    print(decrypted_block)
