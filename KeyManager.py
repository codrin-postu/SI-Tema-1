import socket

from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES

HOST = socket.gethostname()
PORT = 25341

key = get_random_bytes(AES.block_size)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by ', addr)
        while True:
            data = conn.recv(1024).decode()
            print(data)


