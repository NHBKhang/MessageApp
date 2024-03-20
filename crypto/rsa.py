from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
from crypto import secret_path
from djangochat import settings


class RSA:
    def generate_keypair(self):
        """
        Tạo một cặp khóa RSA và trả về khóa công khai và khóa riêng tư.
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        return public_key, private_key

    def encrypt(self, message, public_key):
        """
        Mã hóa một chuỗi sử dụng khóa công khai RSA.
        """
        message_bytes = message.encode('utf-8')
        encrypted_data = public_key.encrypt(
            message_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_data

    def decrypt(self, encrypted_data, private_key):
        """
        Giải mã dữ liệu sử dụng khóa riêng tư RSA.
        """
        decrypted_bytes = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        decrypted_message = decrypted_bytes.decode('utf-8')
        return decrypted_message

    def save_private_key(self, username, key):
        # Export the private key to PEM format
        private_key_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Convert the PEM formatted key to string
        private_key = private_key_pem.decode('utf-8')

        import configparser

        # Tạo một đối tượng ConfigParser
        config = configparser.ConfigParser()

        # Thêm một section mới vào file .ini
        config.add_section('PRIVATE_KEY')

        # Thêm các khóa và giá trị tương ứng
        config.set('PRIVATE_KEY', 'SECRET_KEY', private_key)
        # config.set('PRIVATE_KEYS', 'DATABASE_PASSWORD', 'your_database_password')

        if not os.path.exists(secret_path):
            os.makedirs(secret_path)

        with open(secret_path + username + '_config.ini', 'w') as configfile:
            config.write(configfile)

        from crypto.aes import AESCipher
        aes = AESCipher()
        aes.encrypt_file(secret_path + username + '_config.ini', password=settings.FILE_SECRET_KEY)

        return secret_path + username + '_config.ini'

    def read_private_key(self, username):
        import configparser
        from crypto.aes import AESCipher

        # Đường dẫn đến file .ini
        path = secret_path + username + '_config.ini.enc'
        if not os.path.exists(path):
            return None

        aes = AESCipher()
        decrypted_data = aes.read_encrypted_file(path, password=settings.FILE_SECRET_KEY)

        # Tạo một đối tượng ConfigParser
        config = configparser.ConfigParser()

        # Đọc file .ini
        config.read_string(decrypted_data)

        key = config.get('PRIVATE_KEY', 'SECRET_KEY')

        # Chuyển chuỗi về lại dạng bytes
        private_key_pem = key.encode('utf-8')

        # Tải private key từ PEM format
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,  # If the private key is not password-protected
            backend=default_backend()
        )

        return private_key

    def public_key_to_string(self, public_key):
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Chuyển đổi PEM formatted public key thành chuỗi
        public_key_string = public_key_pem.decode('utf-8')

        return public_key_string

    def string_to_public_key(self, public_key_string):
        public_key_bytes = public_key_string.encode('utf-8')

        # Tải khóa công khai từ PEM format
        public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=default_backend()
        )

        return public_key
