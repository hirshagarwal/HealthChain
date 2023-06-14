import datetime as dt
import hashlib as hl


class Block:
    def __init__(self, index, timestamp, data, prevhash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prevhash
        self.hash = self.hash_block()

    def __str__(self):
        string_builder = "Index: " + str(self.index) + "\n"
        string_builder += "Timestamp: " + str(self.timestamp) + "\n"
        string_builder += "Previous Hash: " + str(self.prev_hash) + "\n"
        string_builder += "Hash: " + str(self.hash_block()) + "\n"
        string_builder += "Data: " + self.data
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
        return Block(0, dt.datetime.now(), "Genesis block transaction", " ")

    @staticmethod
    def new_block(last_block):
        index = last_block.index + 1
        timestamp = dt.datetime.now()
        data = "Transaction " + str(index)
        hash_block = last_block.hash
        return Block(index, timestamp, data, hash_block)


class Chain:
    def __init__(self):
        self.blockchain = [Block.genesis_block()]

    def add_block(self, new_block):
        pass
