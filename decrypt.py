# Simulates the receiver (keys were generated in setup.py)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import oqs
import os
import glob
from ctypes import create_string_buffer

encrypted_file_pattern = "*.encrypted"  # Match any file ending with .encrypted

# Find the encrypted file dynamically
encrypted_files = glob.glob(encrypted_file_pattern)

if not encrypted_files:
    print(f"No encrypted files found matching pattern '{encrypted_file_pattern}'.")
    exit(1)

# Use the first matching encrypted file
encrypted_file = encrypted_files[0]
decrypted_file = encrypted_file.replace(".encrypted", ".decrypted")

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
#print("Symmetric Key:", symmetric_key.hex())

# Decrypt the HR file
with open(encrypted_file, "rb") as f:
    init_vec = f.read(16) # we saved the iv as first 16 bytes of the file
    encrypted_data = f.read() # the rest is the ciphertext

cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(init_vec))
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

with open(decrypted_file, "wb") as f:
    f.write(decrypted_data)

print(f"File decrypted and saved as {decrypted_file}.")
