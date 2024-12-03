# Post-Quantum Safe PKI Demonstration

This project implements quantum-safe cryptography using liboqs, providing secure encryption for sensitive HR data with post-quantum security guarantees.

## Features

- Hybrid post-quantum safe encryption using Kyber1024 and RSA KEM
- Secure handling of employee PII data

## Prerequisites

- liboqs-python wrapper
- Python packages: oqs, cryptography

## Cryptographic Operations
#### (Can be run without running the frontend and backend just to check the encryption/decryption)

### Initial Setup

```bash
python3 setup.py
```

This command initializes the workspace and generates quantum-safe public/private keypairs.

### File Encryption

```bash
python3 encrypt.py {plaintext file}
```

Encrypts the input file using Kyber1024 KEM for key exchange and AES-256 for data encryption.

### File Decryption

```bash
python3 decrypt.py
```

Decrypts the encrypted file using the stored keys.

### Cleanup

```bash
python3 cleanup.py
```

Removes all generated keys, secrets, and encrypted/decrypted files.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License.
