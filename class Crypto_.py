class Crypto:

    def generate_keys_RSA():
        key = RSA.generate(2048)
        __private_key = key.export_key()
        public_key = key.publickey().export_key()

        return __private_key, public_key

    def encrypt(message):
        pass
    def decrypt(message):
        pass

