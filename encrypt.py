# Simulates sender encrypting data with receiver's public keys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import sys
import oqs
import os

if len(sys.argv) != 2:
    print("Usage: python3 encrypt.py <file_to_encrypt>")
    sys.exit(1)

input_file = sys.argv[1]
if not os.path.exists(input_file):
    print(f"Error: File '{input_file}' does not exist.")
    sys.exit(1)

output_file = f"{input_file}.encrypted"

# Load RSA public key
with open("rsa_public_key.pem", "rb") as f:
    rsa_public_key = serialization.load_pem_public_key(f.read())

# Load Kyber public key
with open("kyber_public_key.bin", "rb") as pub_key_file:
    kyber_public_key = pub_key_file.read()

# Generate shared secrets
post_quantum_algorithm = "Kyber1024"
with oqs.KeyEncapsulation(post_quantum_algorithm) as sender:
    kyber_ciphertext, kyber_shared_secret = sender.encap_secret(kyber_public_key)

    # Save Kyber ciphertext
    with open("kyber_shared_secret_ciphertext.bin", "wb") as cipher_file:
        cipher_file.write(kyber_ciphertext)

# Generate a random key for RSA
rsa_shared_secret = os.urandom(32)

# Encrypt the RSA shared secret
rsa_ciphertext = rsa_public_key.encrypt(
    rsa_shared_secret,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Save the RSA ciphertext
with open("rsa_shared_secret_ciphertext.bin", "wb") as f:
    f.write(rsa_ciphertext)

# Combine Kyber and RSA shared secrets for the symmetric key
combined_secret = kyber_shared_secret + rsa_shared_secret
hasher = hashes.Hash(hashes.SHA256())
hasher.update(combined_secret)
symmetric_key = hasher.finalize()

# Encrypt the file
with open(input_file, "rb") as f:
    plaintext = f.read()

init_vec = os.urandom(16)  # Initialization vector for AES
cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(init_vec))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Save IV and ciphertext
with open(output_file, "wb") as f:
    f.write(init_vec + ciphertext)

print(f"File encrypted and saved as {output_file}.")
