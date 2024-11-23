import os
import glob

# cleanup
generated_files = [
    # Original Kyber files
    "public_key.bin",
    "private_key.bin",
    "shared_secret_ciphertext.bin",
    "hr_encrypted.bin",
    "hr_decrypted.txt",
    # New RSA and hybrid files
    "rsa_private_key.pem",
    "rsa_public_key.pem",
    "kyber_shared_secret_ciphertext.bin",
    "rsa_shared_secret_ciphertext.bin"
]

enc_dec = [
    "*.encrypted",  # All encrypted files
    "*.decrypted",  # All decrypted files
]

def cleanup():
    print("Cleaning up files...")
    
    # Remove specific files
    for file in generated_files:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"Removed {file}")
        except Exception as e:
            print(f"Error removing {file}: {e}")

    # Remove files matching patterns
    for pattern in enc_dec:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                print(f"Removed {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")
    
    print("Cleanup completed.")

if __name__ == "__main__":
    cleanup()