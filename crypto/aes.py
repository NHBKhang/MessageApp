import secrets


def generate_key(key_length):
    # Ensure the key length is compatible with AES (128, 192, or 256 bits)
    if key_length not in [128, 192, 256]:
        raise ValueError("Key length must be 128, 192, or 256 bits")

    # Calculate the number of bytes needed for the key
    num_bytes = key_length // 8

    # Generate a random sequence of bytes
    aes_key = secrets.token_bytes(num_bytes)

    return aes_key

if __name__ == "__main__":
    print(generate_key(256))