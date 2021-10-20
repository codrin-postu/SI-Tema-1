import socket

from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES


def server():
    HOST = socket.gethostname()
    PORT = 25341

    key_1 = b'1234567890abcdef'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Client connected: ', addr)

            aes = AES.new(key_1, AES.MODE_ECB)

            while True:
                data = conn.recv(1024).decode()

                if not data:
                    break

                print('Received mode: ', data)

                if data == 'ECB':
                    key_2 = get_random_bytes(16)
                    print("Generated key: ", key_2, '\nEncrypting key!')
                    enc_key_2 = aes.encrypt(key_2)
                    conn.sendall(enc_key_2)
                if data == 'CFB':
                    print('Not yet done!')

            conn.close()


if __name__ == '__main__':
    server()
