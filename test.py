import socket
import select
import errno
import sys
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

with open('public.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())
with open('private.pem', 'rb') as f:
    private_key = RSA.import_key(f.read())
cipher_rsa = PKCS1_OAEP.new(public_key)
decipher_rsa = PKCS1_OAEP.new(private_key)
message = input()

encrypted_message = cipher_rsa.encrypt(message.encode('utf-8'))
print("encrypt:", encrypted_message)
decrypted_message = decipher_rsa.decrypt(encrypted_message)
print(decrypted_message.decode('utf-8'))