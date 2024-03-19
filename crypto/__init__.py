import os


secret_path = os.path.dirname(os.path.abspath(__file__)) + '\enc\\'

from crypto.chacha20 import ChaCha20
from crypto.rsa import RSA

chacha20 = ChaCha20()
rsa = RSA()

# p, k = rsa.generate_keypair()
# aes.encrypt_file(rsa.save_private_key('kha', k))
# print(aes.read_encrypted_file(os.path.dirname(os.path.abspath(__file__)) + '\enc\kha_config.ini.enc'))