from Cryptodome.Cipher import AES
key = b'Sixteen byte key'
obj = AES.new(key, AES.MODE_CBC)
message = "The answer is no"
ciphertext = obj.encrypt(message.encode('utf-8'))

obj2 = AES.new(key, AES.MODE_CBC)
text = obj2.decrypt(ciphertext)
print(text)
'The answer is no'