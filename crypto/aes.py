from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


class AESCipher:
    def encrypt_file(self, input_file, output_file=None, password="123456"):
        # Đọc dữ liệu từ tệp đầu vào
        with open(input_file, 'rb') as f:
            data = f.read()

        # Tạo khóa từ mật khẩu sử dụng PBKDF2
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())

        # Tạo vectơ khởi đầu ngẫu nhiên
        iv = os.urandom(16)

        # Mã hóa dữ liệu
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()

        # Ghi dữ liệu đã mã hóa vào tệp đầu ra
        if output_file is None:
            output_file = input_file + '.enc'
        with open(output_file, 'wb') as f:
            f.write(salt)
            f.write(iv)
            f.write(encrypted_data)

        # Xóa tệp gốc
        os.remove(input_file)

    def read_encrypted_file(self, input_file, password="123456"):
        # Đọc dữ liệu từ tệp mã hóa
        with open(input_file, 'rb') as f:
            # Đọc salt và vectơ khởi đầu
            salt = f.read(16)
            iv = f.read(16)

            # Tạo khóa từ mật khẩu sử dụng PBKDF2
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(password.encode())

            # Khởi tạo giải mã
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            # Đọc và giải mã dữ liệu từ tệp
            decrypted_data = decryptor.update(f.read()) + decryptor.finalize()

        return decrypted_data.decode('utf-8')
