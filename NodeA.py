import socket

from Cryptodome.Cipher import AES

def client():
    key = b'Random key known!'

    HOST = socket.gethostname()                                                 # We will connect to NodeB server and
    PORT_KM = 25341                                                             # the KeyManager server for communication
    PORT_B = 25342
    km_socket = socket.socket()
    node_b_socket = socket.socket()
    km_socket.connect((HOST, PORT_KM))
    node_b_socket.connect((HOST, PORT_B))

    file_object = open("original_file.txt", "r")
    plain_text = file_object.read().encode()

    blocks_count = int(len(plain_text) / AES.block_size)
    curr_block = 0

    enc_mode = input("Encryption modes:\nECB\nCFB\nYour choice: ")
    node_b_socket.sendall(enc_mode.encode())
    km_socket.sendall(enc_mode.encode())

    key_2 = km_socket.recv(1024)
    node_b_socket.send(key_2)


    while curr_block < blocks_count:
        print(enc_mode)
        curr_block += 1


if __name__ == "__main__":
    client()