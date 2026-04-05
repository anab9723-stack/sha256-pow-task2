import hashlib
import json
import time


def sha256_hex(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hex_to_bin(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(256)


def has_leading_zero_bits(hash_hex, starting_zeros):
    hash_bin = hex_to_bin(hash_hex)
    return hash_bin.startswith("0" * starting_zeros)


def mine_block(data, starting_zeros):
    nonce_number = 0
    start_time = time.time()

    while True:
        pow_nonce = f"NONCE-{nonce_number}"   # власний формат nonce
        combined = data + pow_nonce
        block_hash = sha256_hex(combined)

        if has_leading_zero_bits(block_hash, starting_zeros):
            end_time = time.time()
            return {
                "block_hash": block_hash,
                "data": data,
                "pow_nonce": pow_nonce,
                "starting_zeros": starting_zeros,
                "time_seconds": round(end_time - start_time, 4)
            }

        nonce_number += 1


def save_block_to_file(block, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(block, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    data = input("Enter block data: ")
    starting_zeros = int(input("Enter number of starting zero bits (at least 16): "))

    if starting_zeros < 16:
        print("StartingZeros must be at least 16.")
    else:
        print("Mining block, please wait...")
        block = mine_block(data, starting_zeros)

        save_block_to_file(block, "block.json")

        print("\nBlock created successfully.")
        print("Block hash:", block["block_hash"])
        print("Data:", block["data"])
        print("PoW nonce:", block["pow_nonce"])
        print("Starting zeros:", block["starting_zeros"])
        print("Time (seconds):", block["time_seconds"])
        print("Block saved to block.json")