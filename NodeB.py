import socket

from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES


def server():
    HOST = socket.gethostname()
    PORT = 25342

    # key = get_random_bytes(AES.block_size)
    key_1 = b'1234567890abcdef'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Client connected: ', addr)

            aes = AES.new(key_1, AES.MODE_ECB)

            enc_mode = conn.recv(1024).decode()
            key_2 = conn.recv(1024)
            key_1 = aes.decrypt(key_2)

            print('Received encryption mode: ', enc_mode)
            print('Will take each block of 16 bytes and decrypt it')

            conn.sendall('READY'.encode())
            decrypted_text = bytearray()

            while True:
                data = conn.recv(16)
                print(data)

                if data == b'':
                    break

                if enc_mode == 'ECB':
                    aes = AES.new(key_1, AES.MODE_ECB)
                    decrypted_curr_block = aes.decrypt(data)
                    decrypted_text.extend(decrypted_curr_block)

            conn.close()
            decrypted_file = open("decrypted_file.txt", "w")
            decrypted_file.write(decrypted_text.decode())
            print("Decrypted text has been saved in file!")


if __name__ == '__main__':
    server()
