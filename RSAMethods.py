from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


def encrypt(message):
    data = message.encode("utf-8")
    print(data)
    print(type(data))
    file_out = open("encrypted_data.txt", "wb")

    recipient_key = RSA.import_key(open("public.pem").read())
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [file_out.write(x) for x in (enc_session_key,
                                 cipher_aes.nonce, tag, ciphertext)]
    file_out.close()

def clean():
    open('encrypted_data.txt', 'w').close()
