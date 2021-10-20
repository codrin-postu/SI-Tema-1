import socket

from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES

HOST = socket.gethostname()
PORT = 25341

key_1 = b'1234567890abcdef'
key_2 = get_random_bytes(AES.block_size)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by ', addr)
        aes = AES.new(key_1, AES.MODE_ECB)
        while True:
            data = conn.recv(1024).decode()
            print(data)

            if not data:
                break

            if data == 'ECB':
                key_2 = get_random_bytes(AES.block_size)
                print(key_2)
                enc_key_2 = aes.encrypt(key_2)
                conn.sendall(enc_key_2)
            if data == 'CFB':
                print('Not yet done!')

        conn.close()



