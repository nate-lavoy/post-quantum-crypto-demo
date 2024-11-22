# Simulates the sender (the public key was shared by receiever)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
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

post_quantum_algorithm = "Kyber1024" 

# Load the public key
with open("public_key.bin", "rb") as pub_key_file:
    public_key = pub_key_file.read()

# Generate a shared secret using the public key
post_quantum_algorithm = "Kyber1024"
with oqs.KeyEncapsulation(post_quantum_algorithm) as sender:
    ciphertext, shared_secret = sender.encap_secret(public_key) #the ciphertext is the encapsulated shared_secret

    # Save the ciphertext (encapsulated key)
    with open("shared_secret_ciphertext.bin", "wb") as cipher_file:
        cipher_file.write(ciphertext)

# Symmetric key derived from shared secret
symmetric_key = shared_secret[:32]  # AES requires a 256-bit key
#print("Symmetric Key:", symmetric_key.hex())


# Encrypt the HR file
with open(input_file, "rb") as f:
    plaintext = f.read()

init_vec = os.urandom(16)  # Initialization vector for AES
cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(init_vec))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Save the IV and ciphertext to a file
with open(output_file, "wb") as f:
    f.write(init_vec + ciphertext)

print(f"File encrypted and saved as {output_file}.")
print("Encapsulated shared secret saved to 'shared_secret_ciphertext.bin'.")
