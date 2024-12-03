# Post-Quantum Safe PKI Demonstration

This project implements quantum-safe cryptography using liboqs, providing secure encryption for sensitive HR data with standard state-of-the-art and post-quantum security algorithms.

## Features

- Hybrid post-quantum safe encryption using Kyber1024 and RSA KEM
- Secure handling of employee PII data

## Prerequisites

- liboqs-python wrapper
- Python packages: oqs, cryptography

## Cryptographic Operations

### Initial Setup

```bash
python3 setup.py
```

This command initializes the workspace and generates two sets of public/private keypairs, one with Kyber and one with RSA. It simulates actions performed by the receiver of data (who would send the public keys to the sender).

### File Encryption

```bash
python3 encrypt.py {plaintext file}
```

Encrypts the input file using the reciever's Kyber and RSA public keys for encapsulation, SHAH-256 for hashing and AES-256 for data encryption. Simulates actions performed by the sender of data (who would send back two encapsulated shared secrets: one for RSA and one for Kyber, and the encrypted message).

### File Decryption

```bash
python3 decrypt.py
```

Decrypts the encrypted file using the stored private keys and encapsulated shared secrets. Simulates actions performed by the receiver of data.

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
