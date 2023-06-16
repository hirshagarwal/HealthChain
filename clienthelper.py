import requests

from blockchain import Block
from records.userdata import UserData
from user import User


class ClientHelper:
    def __init__(self, host, port):
        self.host = host
        self.port = port

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
        return Block.new_block(tail_block, user_object.user_id, init_user_block)
