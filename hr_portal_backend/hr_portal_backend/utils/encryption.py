# utils/encryption.py
import oqs
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import json
import os
from ctypes import create_string_buffer

class EncryptionManager:
    def __init__(self):
        self.algorithm = "Kyber1024"
    
    def generate_keypair(self):
        with oqs.KeyEncapsulation(self.algorithm) as receiver:
            public_key = receiver.generate_keypair()
            private_key = receiver.secret_key
            return b64encode(public_key).decode(), b64encode(private_key).decode()
    
    def encrypt_data(self, data: dict, public_key: str):
        data_bytes = json.dumps(data).encode()
        
        with oqs.KeyEncapsulation(self.algorithm) as sender:
            public_key_bytes = b64decode(public_key)
            ciphertext, shared_secret = sender.encap_secret(public_key_bytes)
            
            symmetric_key = shared_secret[:32]
            init_vec = os.urandom(16)
            cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(init_vec))
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(data_bytes) + encryptor.finalize()
            
            return {
                "encrypted_data": b64encode(encrypted_data).decode(),
                "shared_secret_ciphertext": b64encode(ciphertext).decode(),
                "init_vector": b64encode(init_vec).decode()
            }
    
    def decrypt_data(self, encrypted_data: str, private_key: str, 
                    shared_secret_ciphertext: str, init_vector: str):
        try:
            with oqs.KeyEncapsulation(self.algorithm) as receiver:
                # Convert private key to ctypes buffer
                private_key_bytes = b64decode(private_key)
                private_key_buffer = create_string_buffer(private_key_bytes)
                
                # Decode other components
                ciphertext = b64decode(shared_secret_ciphertext)
                encrypted_data_bytes = b64decode(encrypted_data)
                init_vec = b64decode(init_vector)
                
                # Set private key and decrypt shared secret
                receiver.secret_key = private_key_buffer
                shared_secret = receiver.decap_secret(ciphertext)
                
                # Decrypt data with AES
                symmetric_key = shared_secret[:32]
                cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(init_vec))
                decryptor = cipher.decryptor()
                decrypted_data = decryptor.update(encrypted_data_bytes) + decryptor.finalize()
                
                return json.loads(decrypted_data.decode())
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")