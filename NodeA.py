import socket

from Cryptodome.Cipher import AES


def client():
    key_1 = b'1234567890abcdef'

    host = socket.gethostname()  # We will connect to NodeB server and
    PORT_KM = 25341  # the KeyManager server for communication
    PORT_B = 25342
    keymanager_socket = socket.socket()
    node_b_socket = socket.socket()
    keymanager_socket.connect((host, PORT_KM))
    node_b_socket.connect((host, PORT_B))

    file_object = open("original_file.txt", "r")
    provided_text = file_object.read().encode()
    file_object.close()

    blocks_count = int(len(provided_text) / AES.block_size)
    curr_block = 0

    enc_mode = input("Encryption modes:\nECB\nCFB\nYour choice: ").upper()
    node_b_socket.sendall(enc_mode.encode())
    keymanager_socket.sendall(enc_mode.encode())

    key_2 = keymanager_socket.recv(1024)
    node_b_socket.sendall(key_2)

    aes = AES.new(key_1, AES.MODE_ECB)

    key_1 = aes.decrypt(key_2)

    ciphertext = bytearray()

    while curr_block < blocks_count:
        if enc_mode == 'ECB':
            aes = AES.new(key_1, AES.MODE_ECB)
            text_curr_block = provided_text[AES.block_size * curr_block:AES.block_size * (curr_block + 1)]
            cipher_curr_block = aes.encrypt(text_curr_block)
            print(cipher_curr_block)

            aes = AES.new(key_1, AES.MODE_ECB)
            print(aes.decrypt(cipher_curr_block))
            node_b_socket.sendall(cipher_curr_block)

            ciphertext.extend(cipher_curr_block)
        elif enc_mode == 'CFB':
            print("Not yet done big boye!")

        curr_block += 1

    node_b_socket.close()
    keymanager_socket.close()

    cipher_file = open("cipher_file.txt", "w")
    cipher_file.write(ciphertext.decode())
    cipher_file.close()


if __name__ == "__main__":
    client()
