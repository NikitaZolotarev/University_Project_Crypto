from Cryptodome.PublicKey import RSA

# Generate a new RSA key pair for alice
key = RSA.generate(2048)

# Save the private key to a file
private_key = key.export_key()
with open('private_Alice.pem', 'wb') as f:
    f.write(private_key)

# Save the public key to a file
public_key = key.publickey().export_key()
with open('public_Alice.pem', 'wb') as f:
    f.write(public_key)


#for bob
# Generate a new RSA key pair
key = RSA.generate(2048)

# Save the private key to a file
private_key = key.export_key()
with open('private_Bob.pem', 'wb') as f:
    f.write(private_key)

# Save the public key to a file
public_key = key.publickey().export_key()
with open('public_Bob.pem', 'wb') as f:
    f.write(public_key)