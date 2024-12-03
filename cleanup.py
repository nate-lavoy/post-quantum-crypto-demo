import os
import glob

# List of specifically generated files to remove
generated_files = [
    # Kyber files
    "kyber_public_key.bin",
    "kyber_private_key.bin",
    # RSA files
    "rsa_private_key.pem",
    "rsa_public_key.pem",
    # Hybrid encryption-related files
    "kyber_shared_secret_ciphertext.bin",
    "rsa_shared_secret_ciphertext.bin",
]

# Patterns for dynamically generated encrypted and decrypted files
enc_dec_patterns = [
    "*.encrypted",  # All encrypted files
    "*.decrypted",  # All decrypted files
]

def cleanup():
    print("Starting cleanup...")

    # Remove specifically listed files
    for file in generated_files:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"Removed: {file}")
        except Exception as e:
            print(f"Error removing {file}: {e}")

    # Remove files matching glob patterns
    for pattern in enc_dec_patterns:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                print(f"Removed: {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")

    print("Cleanup completed.")

if __name__ == "__main__":
    print("Cleaning up old files...")
    cleanup()
