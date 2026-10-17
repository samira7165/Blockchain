import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Blockchain.Backend.Core.blockchain import Blockchain

if __name__ == "__main__":
    print("Initializing Blockchain...")
    blockchain = Blockchain()

    blockchain.add_next_block()
    blockchain.add_next_block()

    blockchain.print()

     # Case 1: original chain
    print("Case 1 - Blockchain Valid:", blockchain.validate_chain())

    # Case 2: tamper with a nonce
    blocks = blockchain.read_from_disk()
    blocks[0]['BlockHeader']['nonce'] += 1
    print("Case 2 - Blockchain Valid:", blockchain.validate_chain(blocks))

    #In the VS Code terminal (**Ctrl + **), make sure you're in the "FULL ..." folder, the one that contains requirements.txt`. Then:

#pip install pycryptodome
#ppython Blockchain\main.py