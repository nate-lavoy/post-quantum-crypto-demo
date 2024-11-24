# Post-Quantum Safe PKI Demonstration

- Based on liboqs from the Linux Foundation's [Open Quantum Safe](https://openquantumsafe.org/liboqs/) project

- Demonstration is with mock employee records containing sensitive personally identifiable information (PII), but can be used to encrypt/decrypt any sensitive file

- Implements hybrid encryption using:
  - Kyber1024 (post-quantum) for quantum-resistant key encapsulation
  - RSA-3072 (classical) for traditional security
  - AES-256 for symmetric encryption
  - SHA-256 for key combination

- This hybrid approach provides protection against both classical and quantum attacks

- Need to have [liboqs-python](https://github.com/open-quantum-safe/liboqs-python) wrapper in your path

- Python requirements: oqs, cryptography

## Usage

### 1) Run setup

```bash
python3 setup.py
```

  Cleans up workspace and creates Kyber public/private keys

### 2) Encrypt the file:

```bash
python3 encrypt.py {plaintext file}
```

  - Generates RSA key pair
  - Creates hybrid encryption using both Kyber and RSA
  - Saves encrypted file as {plaintext file}.encrypted
  - Generates necessary key encapsulation files:
    - kyber_shared_secret_ciphertext.bin
    - rsa_shared_secret_ciphertext.bin

### 3) Decrypt the file:

```bash
python3 decrypt.py
```

  - Uses both Kyber and RSA keys for decryption
  - Combines shared secrets securely
  - Saves decrypted file as {plaintext file}.decrypted

### 4) Clean up files (all secrets, keys, and encrypted/decrypted files)

```bash
python3 cleanup.py
```

  - Removes all generated keys (Kyber and RSA)
  - Removes all ciphertexts and shared secrets
  - Removes encrypted/decrypted files
  - This is also automatically run every time setup.py is run

## Security Notes

- RSA-3072 matches NIST's recommended security level
- Kyber1024 provides post-quantum security
- Keys are combined using SHA-256 for enhanced security
- Each encryption generates unique session keys
- All sensitive files are properly cleaned up after use