import base64
import datetime as dt
import hashlib as hl
import json
from base64 import b64encode

from records import record
from records.genesis import Genesis
from records.note import Note
from records.record import RecordType
from records.userdata import UserData
from user import User


class Block:
    def __init__(self, index, timestamp, data, prev_hash, user_id):
        self.index = index
        self.timestamp = timestamp
        self.data: record = data
        self.prev_hash = prev_hash
        self.user_id = user_id
        self.hash = self.hash_block()
        self.signed_hash = None

    def __str__(self):
        string_builder = "Index: " + str(self.index) + "\n"
        string_builder += "User Id: " + str(self.user_id) + "\n"
        string_builder += "Timestamp: " + str(self.timestamp) + "\n"
        string_builder += "Previous Hash: " + str(self.prev_hash) + "\n"
        string_builder += "Hash: " + str(self.hash_block()) + "\n"
        if self.signed_hash is not None:
            string_builder += "Signed Hash: " + str(b64encode(self.signed_hash)) + "\n"
        string_builder += "Data: " + str(self.data)
        return string_builder

    def hash_block(self):
        block_encryption = hl.sha256()
        encoded_block = (str(self.index)
                         + str(self.timestamp)
                         + str(self.data)
                         + str(self.prev_hash)
                         ).encode('utf-8')
        block_encryption.update(encoded_block)
        return block_encryption.hexdigest()

    def get_dict(self):
        return {
            'index': self.index,
            'timestamp': str(self.timestamp),
            'block_data': self.data.get_dict(),
            'prev_hash': self.prev_hash,
            'user_id': str(self.user_id),
            'hash': self.hash,
            'signed_hash': self.signed_hash
        }

    def get_json(self):
        serializable_dict: record = self.get_dict()
        serializable_dict['block_data'] = self.data.get_dict()
        if self.signed_hash is not None:
            serializable_dict['signed_hash'] = base64.b64encode(self.signed_hash).decode('utf-8')
        return json.dumps(serializable_dict)

    @staticmethod
    def genesis_block():
        return Block(0, dt.datetime.now(), Genesis(), " ", "root")

    @staticmethod
    def new_block(last_block, user_id, block_data: record):
        # TODO: Assert json string
        index = last_block.index + 1
        timestamp = dt.datetime.now()
        hash_block = last_block.hash
        return Block(index, timestamp, block_data, hash_block, user_id)

    @staticmethod
    def get_b64_string(message):
        if message is not None:
            return str(b64encode(message))
        return None

    @staticmethod
    def from_json(json_block):
        block = Block(json_block['index'],
                      json_block['timestamp'],
                      Block.record_from_json(json.dumps(json_block['block_data'])),
                      json_block['prev_hash'],
                      json_block['user_id']
                      )
        if json_block['signed_hash'] is not None:
            block.signed_hash = json_block['signed_hash']
        block.hash = json_block['hash']
        return block

    @staticmethod
    def record_from_json(json_string):
        json_object = json.loads(json_string)
        if json_object['record_type'] == RecordType.USER_DATA.name:
            return UserData.json_deserialize_userdata(json_string)
        elif json_object['record_type'] == RecordType.NOTE.name:
            return Note.json_deserialize_note(json_string)
        elif json_object['record_type'] == RecordType.GENESIS.name:
            return Genesis.deserialize_genesis(json_string)


class Chain:
    def __init__(self):
        self.blockchain = [Block.genesis_block()]

    def __str__(self):
        sb = ""
        for block in self.blockchain:
            sb += str(block)
            sb += "\n"
        return sb

    def add_block(self, new_block: Block):
        user_index = self.find_user_exist(new_block.user_id)
        if user_index == -1:
            assert new_block.data.record_type == RecordType.USER_DATA
            self.blockchain.append(new_block)
        else:
            user_origin_block = self.blockchain[user_index]

            assert new_block.data.record_type != RecordType.USER_DATA, "For now you can't overwrite your user block"
            assert new_block.signed_hash is not None, "A new block must have a signed hash"

            self.verify_transaction(user_origin_block, new_block)
            self.blockchain.append(new_block)

    def read_tail_block(self) -> Block:
        return self.blockchain[len(self.blockchain) - 1]

    def find_user_exist(self, user_id) -> int:
        for block in self.blockchain:
            if block.user_id == user_id:
                return block.index
        return -1

    def get_json(self):
        dict_array = []
        for block_dict in self.blockchain:
            dict_array.append(block_dict.get_dict())
        return json.dumps(dict_array)

    @staticmethod
    def verify_transaction(user_origin_block, new_block):
        user_data = user_origin_block.data
        User.verify_message(
            new_block.signed_hash,
            new_block.hash,
            user_data.public_key)
