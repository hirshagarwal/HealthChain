# Overview
HealthChain is an open source Python based blockchain specifically designed to store health record data.

It is designed to be anonymous, but not fully encrypted, making it possible to easily run analysis on population wide
data.

## Runtime Instruction
Python environment should be activated with `source venv/bin/activate`

# Technical Overview
## BlockChain
The blockchain is simply a list of `Block` objects. Each block contains some metadata, as well as a `data` field, 
which contains the core content stored as JSON. `data` must be stored as a `Record` type object to ensure proper 
serialization/deserialization.

The blockchain will always generate a genesis block when it is created. All this does is signify the start of the 
blockchain and provide a root hash for all subsequent block.

As will all blockchains the data is permanent and can not be altered after being written. In the context of healthcare 
data this means that if a mistake is made it will need to be corrected with a block that negates the erroneous one, 
and then another block to insert new data (this system has not yet been built).

## Users
A user must be created by inserting a `USER_DATA` type block. Once a user is created with a specific `id` its private 
key will need to be retained. The initial user block contains some basic user information, as well as their public key.
The public key from this block should be used to validate all subsequent transactions associated with the user. In order
to allow write access from other users we might need to use some sort of symmetric encryption.