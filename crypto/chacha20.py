from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets
import base64


class ChaCha20:
    def bytes_to_base64(self, byte_data):
        """
        Chuyển đổi dữ liệu byte thành chuỗi Base64.
        """
        base64_data = base64.b64encode(byte_data).decode('utf-8')
        return base64_data

    def base64_to_bytes(self, base64_string):
        """
        Chuyển đổi chuỗi Base64 thành dữ liệu byte.
        """
        byte_data = base64.b64decode(base64_string)
        return byte_data

    def generate_key(self):
        random_bytes = secrets.token_bytes(32)
        return self.__bytes_to_base64(random_bytes)

    def generate_nonce(self):
        random_bytes = secrets.token_bytes(16)
        return random_bytes

    def __shorten_bytes_to_hex(self, byte_data):
        """
        Chuyển đổi dữ liệu byte thành chuỗi hex.
        """
        hex_data = byte_data.hex()
        return hex_data

    def __restore_bytes_from_hex(self, hex_data):
        """
        Chuyển đổi chuỗi hex trở lại dữ liệu byte.
        """
        byte_data = bytes.fromhex(hex_data)
        return byte_data

    def encrypt(self, key, nonce, message):
        """
        Mã hóa một chuỗi sử dụng ChaCha20-Poly1305.
        """
        # Chuyển đổi chuỗi thành dạng byte
        message_bytes = message.encode('utf-8')

        # Khởi tạo đối tượng mã hóa
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())

        # Tạo đối tượng mã hóa
        encryptor = cipher.encryptor()

        # Mã hóa dữ liệu
        ciphertext_bytes = encryptor.update(message_bytes) + encryptor.finalize()

        return self.__shorten_bytes_to_hex(ciphertext_bytes)

    def decrypt(self, key, nonce, cipher_message):
        """
        Giải mã một chuỗi sử dụng ChaCha20-Poly1305.
        """
        # Khởi tạo đối tượng giải mã
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())

        # Tạo đối tượng giải mã
        decryptor = cipher.decryptor()

        # Giải mã dữ liệu
        decrypted_bytes = decryptor.update(self.__restore_bytes_from_hex(cipher_message)) + decryptor.finalize()

        # Chuyển đổi dữ liệu từ byte thành chuỗi
        decrypted_text = decrypted_bytes.decode('utf-8')

        return decrypted_text
