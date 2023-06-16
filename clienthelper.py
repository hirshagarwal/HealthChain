import requests

from blockchain import Block
from records.note import Note
from records.userdata import UserData
from user import User


class ClientHelper:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def build_user_block(self, first_name, last_name, dob, user_object: User) -> Block:
        tail_block = self.get_tail_block()
        init_user_block = UserData(
            first_name,
            last_name,
            dob,
            user_object.public_key
        )
        return Block.new_block(tail_block, user_object.user_id, init_user_block.get_data_encrypted())

    def build_note_block(self, note, user_object: User) -> Block:
        tail_block = self.get_tail_block()
        init_note_data = Note(note)
        return Block.new_block(tail_block, user_object.user_id, init_note_data)

    def get_tail_block(self) -> Block:
        return Block.from_json(requests.get("http://{}:{}/get_tail_block"
                                            .format(self.host, self.port)).json())
