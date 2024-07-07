from Cryptodome.Random import get_random_bytes

def generate_keys():
    key = get_random_bytes(32)
    with open('/Users/nikitazolotarev/Downloads/crypto/AES_key.txt','wb') as f:
        f.write(key)
generate_keys()