# Simulates receiver's pub/priv key generation
import oqs
import cleanup
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

cleanup.cleanup()

# Generate Kyber keypair
post_quantum_algorithm = "Kyber1024"
with oqs.KeyEncapsulation(post_quantum_algorithm) as receiver:
    kyber_public_key = receiver.generate_keypair()
    kyber_private_key = receiver.secret_key

    # Save Kyber keys
    with open("kyber_public_key.bin", "wb") as pub_key_file:
        pub_key_file.write(kyber_public_key)
    with open("kyber_private_key.bin", "wb") as priv_key_file:
        priv_key_file.write(kyber_private_key)

# Generate RSA keypair
rsa_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072
)
rsa_public_key = rsa_private_key.public_key()

# Save RSA keys
with open("rsa_private_key.pem", "wb") as priv_key_file:
    priv_key_file.write(
        rsa_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )
with open("rsa_public_key.pem", "wb") as pub_key_file:
    pub_key_file.write(
        rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Kyber and RSA keypairs generated and saved.")