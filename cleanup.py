import os

#cleanup
generated_files = [
    "public_key.bin",
    "private_key.bin",
    "shared_secret_ciphertext.bin",
    "hr_encrypted.bin",
    "hr_decrypted.txt",
]

def cleanup():
    for file in generated_files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception as e:
            print(f"Error removing {file}: {e}")

if __name__ == "__main__":
    print("Cleaning up old files.")
    cleanup()