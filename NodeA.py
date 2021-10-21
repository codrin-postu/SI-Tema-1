import socket

from Cryptodome.Cipher import AES


# Source: https://nitratine.net/blog/post/xor-python-byte-strings/
def xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def client():
    block_size = 16  # 16 / 32 bytes

    key_1 = b'1234567890abcdef'
    iv = b'Iaammmagrooot012'

    host = socket.gethostname()  # We will connect to NodeB server and
    port_km = 25341  # the KeyManager server for communication
    port_b = 25342
    keymanager_socket = socket.socket()
    node_b_socket = socket.socket()
    keymanager_socket.connect((host, port_km))
    node_b_socket.connect((host, port_b))

    file_object = open("original_file.txt", "r")
    provided_text = file_object.read().encode()
    provided_text = provided_text.ljust(len(provided_text) + (len(provided_text) % block_size))
    file_object.close()

    blocks_count = int(len(provided_text) / block_size)
    curr_block = 0

    enc_mode = input("Encryption modes:\nECB\nCFB\nYour choice: ").upper()
    node_b_socket.sendall(enc_mode.encode())
    keymanager_socket.sendall(enc_mode.encode())

    enc_key_2 = keymanager_socket.recv(1024)
    node_b_socket.sendall(enc_key_2)

    aes = AES.new(key_1, AES.MODE_ECB)
    key_2 = aes.decrypt(enc_key_2)

    # iv = bytearray()
    # if enc_mode == 'CFB':
    #     enc_iv = keymanager_socket.recv(1024)
    #     node_b_socket.sendall(enc_iv)
    #     iv = aes.decrypt(enc_iv)

    message = node_b_socket.recv(1024).decode()
    if message != 'READY':
        exit(0)

    ciphertext = bytearray()

    while curr_block < blocks_count:
        aes = AES.new(key_2, AES.MODE_ECB)
        text_curr_block = provided_text[block_size * curr_block:block_size * (curr_block + 1)]

        if enc_mode == 'ECB':
            cipher_curr_block = aes.encrypt(text_curr_block)
            node_b_socket.sendall(cipher_curr_block)

        elif enc_mode == 'CFB':
            cipher_curr_block = aes.encrypt(iv)
            cipher_curr_block = xor(cipher_curr_block, text_curr_block)
            iv = cipher_curr_block  # the current ciphertext becomes the iv for next block
            node_b_socket.sendall(cipher_curr_block)

        print('Sending block', curr_block)
        ciphertext.extend(cipher_curr_block)

        curr_block += 1

    node_b_socket.close()
    keymanager_socket.close()
    print('Contents of the file have been delivered!')
    # print(ciphertext)


if __name__ == "__main__":
    client()
