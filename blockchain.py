import datetime as dt
import hashlib as hl

from cryptography.hazmat.primitives.serialization import load_pem_public_key

from records.userdata import UserData
from user import User


class Block:
    def __init__(self, index, timestamp, data, prev_hash, user_id):
        self.index = index
        self.timestamp = timestamp
        self.data = data
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
        string_builder += "Signed Hash: " + str(self.signed_hash) + "\n"
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

    @staticmethod
    def genesis_block():
        return Block(0, dt.datetime.now(), "Genesis block transaction", " ", "root")

    @staticmethod
    def new_block(last_block, user_id, json_block_data):
        # TODO: Assert json string
        index = last_block.index + 1
        timestamp = dt.datetime.now()
        hash_block = last_block.hash
        return Block(index, timestamp, json_block_data, hash_block, user_id)


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
        # TODO: Run consensus mechanism
        user_index = self.find_user_exist(new_block.user_id)
        if user_index == -1:
            self.blockchain.append(new_block)
        else:
            user_origin_block = self.blockchain[user_index]
            self.verify_transaction(user_origin_block, new_block)
            self.blockchain.append(new_block)

    def read_tail_block(self) -> Block:
        return self.blockchain[len(self.blockchain) - 1]

    def find_user_exist(self, user_id) -> int:
        for block in self.blockchain:
            if block.user_id == user_id:
                return block.index
        return -1

    @staticmethod
    def verify_transaction(user_origin_block, new_block):
        user_data = UserData.json_deserialize_userdata(user_origin_block.data)
        public_key = load_pem_public_key(user_data.public_key.encode('utf-8'))
        User.verify_message(
            new_block.signed_hash,
            new_block.hash_block().encode('utf-8'),
            public_key)
