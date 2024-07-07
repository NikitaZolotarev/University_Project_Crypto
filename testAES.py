from Cryptodome.Cipher import AES, DES
from Cryptodome.Util.Padding import pad, unpad

BLOCK_SIZE = 32
key = b'Sixteen byte key'
cipher = AES.new(key, AES.MODE_ECB)
data = "emories broken the truth go unspoken i even forgotten my name i dont know the reason or what is the season"
ciphertext = cipher.encrypt(pad(data.encode("utf-8"), BLOCK_SIZE))
#oh no there will be bloooodsheeed

#key = b'Sixteen byte key'
decipher = AES.new(key, AES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)

print("The message is authentic:", plaintext.decode('utf-8'))
