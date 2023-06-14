import uuid

from blockchain import Block, Chain
from records.note import Note
from records.userdata import UserData

from user import User

if __name__ == '__main__':
    blockchain = Chain()
    first_block = blockchain.read_tail_block()

    # Make virtual user
    user = User(uuid.uuid4())
    user2 = User(uuid.uuid4())
    init_user_block = UserData(
        'Hirsh',
        'Agarwal',
        '16-08-1997',
        user.public_key
    )

    # Persist user
    new_block = Block.new_block(first_block, user.user_id, init_user_block.json_serialize())
    blockchain.add_block(new_block)

    # Make first note block
    first_note_block = Note(
        "Patient attended clinic today for visit..."
    )
    recent_block = blockchain.read_tail_block()
    new_block_note = Block.new_block(recent_block,
                                     user.user_id,
                                     first_note_block.json_serialize())
    new_block_note.signed_hash = user.sign_message(new_block_note.hash.encode('utf-8'))
    blockchain.add_block(new_block_note)
    print(blockchain)
