# Simulates the receiver (keys were generated in setup.py)

import oqs
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from ctypes import create_string_buffer

decrypted_hr_file = "hr_decrypted.txt"
encrypted_hr_file = "hr_encrypted.bin"

post_quantum_algorithm = "Kyber1024" 

# Load the private key
with open("private_key.bin", "rb") as priv_key_file:
    private_key = priv_key_file.read()

# Load the ciphertext (encapsulated shared secret)
with open("shared_secret_ciphertext.bin", "rb") as cipher_file:
    ciphertext = cipher_file.read()

with oqs.KeyEncapsulation(post_quantum_algorithm) as receiver:
    receiver.secret_key = create_string_buffer(private_key)
    shared_secret_dec = receiver.decap_secret(ciphertext)

symmetric_key = shared_secret_dec[:32]  # Use first 256 bits for AES-256
print("Symmetric Key:", symmetric_key.hex())

# Decrypt the HR file
with open(encrypted_hr_file, "rb") as f:
    init_vec = f.read(16) # we saved the iv as first 16 bytes of the file
    encrypted_data = f.read() # the rest is the ciphertext

cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(init_vec))
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

with open(decrypted_hr_file, "wb") as f:
    f.write(decrypted_data)

print(f"File decrypted and saved as {decrypted_hr_file}.")
