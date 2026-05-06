import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096
)

# Private key in PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Public key in OpenSSH format
public_key = private_key.public_key()
public_openssh = public_key.public_bytes(
    encoding=serialization.Encoding.OpenSSH,
    format=serialization.PublicFormat.OpenSSH
)

# Save files
with open("stocklive_key", "wb") as f:
    f.write(private_pem)

with open("stocklive_key.pub", "wb") as f:
    f.write(public_openssh)

print("Keys generated successfully.")
