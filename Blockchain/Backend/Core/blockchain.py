from Blockchain.Backend.Core.blockheader import BlockHeader
from Blockchain.Backend.Core.block import Block
from Blockchain.Backend.Core.Database.database import BlockchainDB
from Blockchain.Backend.Util.util import hash256
from Blockchain.config import VERSION, ZERO_HASH, TARGET, DIFFICULTY_TARGET, BLOCK_SIZE
import time
import json
import hashlib


class Blockchain:
    def __init__(self):
        # self.chain = []
        self.blockchainDB = BlockchainDB()

        if self.blockchainDB.fileExists():
            print("file already exists")
        else:
            self.create_genesis_block()

    def write_on_disk(self, block):
        self.blockchainDB.write(block)

    def read_from_disk(self):
        return self.blockchainDB.read()

    def get_last_block(self):
        return self.blockchainDB.lastBlock()

    def create_genesis_block(self):
        self.add_block(1, ZERO_HASH)

    def add_block(self, blockHeight, prevBlockHash):

        # Create a new block header
        version = VERSION
        timestamp = int(time.time())
        bits = DIFFICULTY_TARGET # Placeholder for the actual difficulty target

        # transactions = []  # Placeholder for actual transactions
        Txs = [f"A is sending {blockHeight} coins to B"]  # Placeholder for actual transactions

        merkle_root = hash256(json.dumps(Txs).encode('utf-8'))

        block_header = BlockHeader(version, prevBlockHash, merkle_root, timestamp, bits)

        block_header.mine(TARGET)

        # Create a new block
        new_block = Block(blockHeight, BLOCK_SIZE, block_header.__dict__, Txs).__dict__

        # Add the new block to the blockchain
        # self.chain.append(new_block)
        self.write_on_disk([new_block])

        print(f"Block {blockHeight} added to the blockchain with hash: {block_header.blockHash}")


    def add_next_block(self):
        last_block = self.get_last_block()
        new_block_height = last_block["Height"] + 1
        new_prev_hash = last_block["BlockHeader"]["blockHash"]
        self.add_block(new_block_height, new_prev_hash)

    def print(self):
        print(json.dumps(self.read_from_disk(), indent=4))



    def validate_chain(self, blocks=None):
        if blocks is None:
            blocks = self.read_from_disk()

        # 1. Empty chain is invalid
        if not blocks:
            return False

        prev_hash = ZERO_HASH
        for i, block in enumerate(blocks):
            header = block['BlockHeader']

            # 2 & 3. Correct height and previous hash
            if block['Height'] != i + 1:
                return False
            if header['prev_block_hash'] != prev_hash:
                return False

            # 4. Recalculate the hash and compare
            data = (str(header['version']) + header['prev_block_hash'] +
                    header['merkle_root'] + str(header['timestamp']) +
                    header['bits'] + str(header['nonce']))
            if hashlib.sha256(data.encode()).hexdigest() != header['blockHash']:
                return False

            # 5. Hash must meet the target ("0000")
            if not header['blockHash'].startswith(TARGET):
                return False

            prev_hash = header['blockHash']

        return True