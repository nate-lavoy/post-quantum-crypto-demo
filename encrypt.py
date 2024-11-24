# Simulates the sender (the public key was shared by receiever)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import sys
import oqs
import os

# Check for a command-line argument
if len(sys.argv) != 2:
    print("Usage: python3 encrypt.py <file_to_encrypt>")
    sys.exit(1)

# Get the input file from the command-line argument
input_file = sys.argv[1]
# Ensure the file exists
if not os.path.exists(input_file):
    print(f"Error: File '{input_file}' does not exist.")
    sys.exit(1)

output_file = f"{input_file}.encrypted"

# Generate RSA keypair
rsa_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072  # NIST recommended size
)
rsa_public_key = rsa_private_key.public_key()

# Save RSA keys
with open("rsa_private_key.pem", "wb") as f:
    f.write(rsa_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("rsa_public_key.pem", "wb") as f:
    f.write(rsa_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

# Load the Kyber public key
with open("public_key.bin", "rb") as pub_key_file:
    kyber_public_key = pub_key_file.read()

# Generate shared secrets using both Kyber and RSA
post_quantum_algorithm = "Kyber1024"
with oqs.KeyEncapsulation(post_quantum_algorithm) as sender:
    kyber_ciphertext, kyber_shared_secret = sender.encap_secret(kyber_public_key)

    # Save the Kyber ciphertext
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

# Combine both shared secrets for the final symmetric key
combined_secret = kyber_shared_secret + rsa_shared_secret
hasher = hashes.Hash(hashes.SHA256())
hasher.update(combined_secret)
symmetric_key = hasher.finalize()

# Encrypt the HR file
with open(input_file, "rb") as f:
    plaintext = f.read()

init_vec = os.urandom(16) # Initialization vector for AES
cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(init_vec))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Save the IV and ciphertext to a file
with open(output_file, "wb") as f:
    f.write(init_vec + ciphertext)

print(f"File encrypted and saved as {output_file}.")
print("Kyber ciphertext saved to 'kyber_shared_secret_ciphertext.bin'")
print("RSA ciphertext saved to 'rsa_shared_secret_ciphertext.bin'")