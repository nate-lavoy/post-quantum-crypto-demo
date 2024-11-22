# Simulates the sender (the public key was shared by receiever)

import oqs
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

hr_file = "hr_original.txt"
encrypted_hr_file = "hr_encrypted.bin"

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
print("Symmetric Key:", symmetric_key.hex())


# Encrypt the HR file
with open(hr_file, "rb") as f:
    plaintext = f.read()

init_vec = os.urandom(16)  # Initialization vector for AES
cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(init_vec))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Save the IV and ciphertext to a file
with open(encrypted_hr_file, "wb") as f:
    f.write(init_vec + ciphertext)

print(f"File encrypted and saved as {encrypted_hr_file}.")
print("Encapsulated shared secret saved to 'shared_secret_ciphertext.bin'.")
