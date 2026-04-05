import hashlib
import json
import sys


def sha256_hex(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hex_to_bin(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(256)


def has_leading_zero_bits(hash_hex, starting_zeros):
    hash_bin = hex_to_bin(hash_hex)
    return hash_bin.startswith("0" * starting_zeros)


def verify_block(filename):
    with open(filename, "r", encoding="utf-8") as f:
        block = json.load(f)

    data = block["data"]
    pow_nonce = block["pow_nonce"]
    stored_hash = block["block_hash"]
    starting_zeros = block["starting_zeros"]

    recalculated_hash = sha256_hex(data + pow_nonce)

    if recalculated_hash != stored_hash:
        print("Block is invalid: hash does not match.")
        return

    if not has_leading_zero_bits(recalculated_hash, starting_zeros):
        print("Block is invalid: insufficient number of starting zero bits.")
        return

    print("Block is valid.")
    print("Stored hash:      ", stored_hash)
    print("Recalculated hash:", recalculated_hash)
    print("Data:             ", data)
    print("PoW nonce:        ", pow_nonce)
    print("Starting zeros:   ", starting_zeros)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_block.py block.json")
    else:
        verify_block(sys.argv[1])