from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


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
