import socket

from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES


# Source: https://nitratine.net/blog/post/xor-python-byte-strings/
def xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def server():
    HOST = socket.gethostname()
    PORT = 25342

    block_size = 16

    # key = get_random_bytes(AES.block_size)
    key_1 = b'1234567890abcdef'
    iv = b'Iaammmagrooot012'                    # For block of 16 bytes

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Client connected: ', addr)

            aes = AES.new(key_1, AES.MODE_ECB)

            enc_mode = conn.recv(1024).decode()
            enc_key_2 = conn.recv(1024)
            key_2 = aes.decrypt(enc_key_2)

            # enc_iv = conn.recv(1024)
            # iv = aes.decrypt(enc_iv)

            print('Received encryption mode: ', enc_mode)
            print('Will take each block of', block_size, 'bytes and decrypt it')
            print('._______________________________________________')

            conn.sendall('READY'.encode())
            decrypted_text = bytearray()

            while True:
                data = conn.recv(block_size)
                if data == b'':
                    break

                print("|   ", data)

                aes = AES.new(key_2, AES.MODE_ECB)

                if enc_mode == 'ECB':
                    decrypted_curr_block = aes.decrypt(data)

                if enc_mode == 'CFB':
                    cipher_curr_block = aes.encrypt(iv)
                    decrypted_curr_block = xor(cipher_curr_block, data)
                    iv = data

                decrypted_text.extend(decrypted_curr_block)

            conn.close()
            print('|_______________________________________________')

            decrypted_file = open("decrypted_file.txt", "w")
            decrypted_file.write(decrypted_text.decode())
            print("Decrypted text has been saved in file!")


if __name__ == '__main__':
    server()
