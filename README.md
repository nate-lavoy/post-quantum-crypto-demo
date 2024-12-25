# Post-Quantum Safe PKI Demonstration

This project implements quantum-safe cryptography using Open Quantum Safe's [implementation](https://openquantumsafe.org/liboqs/), providing secure encryption for sensitive HR data with standard state-of-the-art and post-quantum security algorithms.

## Features

- Hybrid post-quantum safe encryption using Kyber1024 and RSA KEM
- Secure handling of employee PII data
- Uses [liboqs-python](https://github.com/open-quantum-safe/liboqs-python) Python wrapper for liboqs

## Setup

### Install and activate a Python virtual environment

Execute in a Terminal/Console/Administrator Command Prompt

```shell
python3 -m venv venv
source venv/bin/activate
python3 -m ensurepip --upgrade
```

### Install Poetry

Execute in a Terminal/Console/Administrator Command Prompt

```shell
pip install poetry
```

### Install project dependencies

```shell
poetry install
```

## Cryptographic Operations

### Initial setup

```bash
python3 setup.py
```

This command initializes the workspace and generates two sets of public/private keypairs, one with Kyber and one with RSA. It simulates actions performed by the receiver of data (who would send the public keys to the sender).

### File encryption

```bash
python3 encrypt.py {plaintext file}
```

Encrypts the input file using the reciever's Kyber and RSA public keys for encapsulation, SHAH-256 for hashing and AES-256 for data encryption. Simulates actions performed by the sender of data (who would send back two encapsulated shared secrets: one for RSA and one for Kyber, and the encrypted message).

You can use the included "mock_data.txt" in place of {plaintext file} or use your own file.

### File decryption

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
