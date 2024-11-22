# Post-Quantum Safe PKI Demonstration

- Based on liboqs from the Linux Foundation's [Open Quantum Safe](https://openquantumsafe.org/liboqs/) project

- Demonstration is with mock employee records containing sensitive personally identifiable information (PII), but can be used to encrypt/decrypt any sensitive file

- Uses Kyber1024 for key encapsulation and AES-256 for encryption

- Need to have [liboqs-python](https://github.com/open-quantum-safe/liboqs-python) wrapper in your path

-python requirements: oqs, cryptography

## Usage

- run setup (cleans up workspace and creates requester's public/private keys)
'python3 setup.py'

- encrypt the file:
'python3 encrypt.py {plaintext file}'

the encrypted file will be saved as {plaintext file}.encrypted

- decrypt the file:
'python3 decrypt.py'

the decrypted file will be saved as {plaintext file}.decrypted

- clean up files (all secrets, keys, and encrypted/decrypted files)
'python3 cleanup.py'

this is also automatically run every time setup.py is run