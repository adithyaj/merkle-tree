from utils import *
import math
from node import Node

from merkle_tree import MerkleTree

def merkle_proof(tx, merkle_tree):
    """Given a tx and a Merkle tree object, retrieve its list of tx's and
    parse through it to arrive at the minimum amount of information required
    to arrive at the correct block header. This does not include the tx
    itself.

    Return this data as a list; remember that order matters!
    """
    #### YOUR CODE HERE
    data = []
    tx_list = merkle_tree.leaves
    if len(tx_list) == 1 or tx not in tx_list:
        return data

    # construct a temporary merkle tree with the correct half of the
    # tx list and append the block header of the intermediate tree
    direction = ''
    while len(tx_list) > 2:
        tx_pos = tx_list.index(tx)
        half_size = int(len(tx_list)/2)
        if tx_pos < half_size:
            temp_merk = concat_and_hash_list(tx_list[half_size:])
            tx_list = tx_list[:half_size]
            direction = 'r'
        else:
            temp_merk = concat_and_hash_list(tx_list[:half_size])
            tx_list = tx_list[half_size:]
            direction = 'l'
        data.append(Node(direction, temp_merk))
    tx_pos = tx_list.index(tx)

    # add the last sibling pair to the list
    if tx_pos == 0:
        data.append(Node('r', tx_list[1]))
    else:
        data.append(Node('l', tx_list[0]))

    return data


def verify_proof(tx, merkle_proof):
    """Given a Merkle proof - constructed via `merkle_proof(...)` - verify
    that the correct block header can be retrieved by properly hashing the tx
    along with every other piece of data in the proof in the correct order
    """
    #### YOUR CODE HERE
    sibling_tx = merkle_proof.pop()
    if sibling_tx.direction == 'r':
        hash = hash_data(tx+sibling_tx.tx)
    else:
        hash = hash_data(sibling_tx.tx+tx)

    while len(merkle_proof) != 0:
        txHash = merkle_proof.pop()
        if txHash.direction == 'r':
            hash = hash_data(hash+txHash.tx)
        else:
            hash = hash_data(txHash.tx+hash)
            
    return hash


    
