# Simulates receiver's pub/priv key generation
import oqs
import cleanup

cleanup.cleanup()

post_quantum_algorithm = "Kyber1024"

# Generate keypair
with oqs.KeyEncapsulation(post_quantum_algorithm) as receiver:
    public_key = receiver.generate_keypair() 

    # Save the public key to share
    with open("public_key.bin", "wb") as pub_key_file:
        pub_key_file.write(public_key)

    # Save the private key (decryption only)
    with open("private_key.bin", "wb") as priv_key_file:
        priv_key_file.write(receiver.secret_key)

print("Keypair generated.")
print("Receiver's public key saved as 'public_key.bin'.")
print("Receiver's private key saved as 'private_key.bin'.")
