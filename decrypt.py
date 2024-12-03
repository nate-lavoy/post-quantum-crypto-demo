# decrypt.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import oqs
import os
import glob
from ctypes import create_string_buffer

# Pattern to match encrypted files
encrypted_file_pattern = "*.encrypted"

# Find encrypted files dynamically
encrypted_files = glob.glob(encrypted_file_pattern)

if not encrypted_files:
    print(f"No encrypted files found matching pattern '{encrypted_file_pattern}'.")
    exit(1)

# Use the first matching encrypted file
encrypted_file = encrypted_files[0]
decrypted_file = encrypted_file.replace(".encrypted", ".decrypted")

post_quantum_algorithm = "Kyber1024"

# Load the Kyber private key
if not os.path.exists("kyber_private_key.bin"):
    print("Error: Kyber private key file 'kyber_private_key.bin' not found.")
    exit(1)

with open("kyber_private_key.bin", "rb") as priv_key_file:
    kyber_private_key = priv_key_file.read()

# Load the RSA private key
if not os.path.exists("rsa_private_key.pem"):
    print("Error: RSA private key file 'rsa_private_key.pem' not found.")
    exit(1)

with open("rsa_private_key.pem", "rb") as f:
    rsa_private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Load both ciphertexts
if not os.path.exists("kyber_shared_secret_ciphertext.bin"):
    print("Error: Kyber ciphertext file 'kyber_shared_secret_ciphertext.bin' not found.")
    exit(1)

with open("kyber_shared_secret_ciphertext.bin", "rb") as cipher_file:
    kyber_ciphertext = cipher_file.read()

if not os.path.exists("rsa_shared_secret_ciphertext.bin"):
    print("Error: RSA ciphertext file 'rsa_shared_secret_ciphertext.bin' not found.")
    exit(1)

with open("rsa_shared_secret_ciphertext.bin", "rb") as f:
    rsa_ciphertext = f.read()

# Decrypt Kyber shared secret
with oqs.KeyEncapsulation(post_quantum_algorithm) as receiver:
    receiver.secret_key = create_string_buffer(kyber_private_key)
    kyber_shared_secret = receiver.decap_secret(kyber_ciphertext)

# Decrypt RSA shared secret
rsa_shared_secret = rsa_private_key.decrypt(
    rsa_ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Combine both shared secrets
combined_secret = kyber_shared_secret + rsa_shared_secret
hasher = hashes.Hash(hashes.SHA256())
hasher.update(combined_secret)
symmetric_key = hasher.finalize()

# Decrypt the encrypted file
if not os.path.exists(encrypted_file):
    print(f"Error: Encrypted file '{encrypted_file}' not found.")
    exit(1)

with open(encrypted_file, "rb") as f:
    init_vec = f.read(16)  # Read the IV (first 16 bytes)
    encrypted_data = f.read()  # Read the remaining ciphertext

cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(init_vec))
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

# Save the decrypted content
with open(decrypted_file, "wb") as f:
    f.write(decrypted_data)

print(f"File decrypted and saved as {decrypted_file}.")