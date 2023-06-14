from blockchain import Block

# Mainly use this file for testing

if __name__ == '__main__':
    blockchain = [Block.genesis_block()]
    first_block = blockchain[0]
    blockchain.append(Block.new_block(blockchain[len(blockchain) - 1]))
