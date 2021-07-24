# !?usr/bin/python3

import Crypto_funcs
import socket
import time


def message(text, pubkey_pem):
    aes_key = Crypto_funcs.aes_key_generate()
    ciphertext = Crypto_funcs.aes_encryption(text, aes_key)
    cipherkey = Crypto_funcs.rsa_encryption(pubkey_pem, aes_key)
    return [cipherkey, ciphertext]


def send_to_another(HOST, PORT, message):
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #   s.connect((HOST, PORT))
    #   s.sendall(message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    conn.send(message)
    conn.close()


def receive_from_another(HOST, PORT):
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #   s.bind((HOST, PORT))
    # s.listen()
    # conn, addr = s.accept()
    #    with conn:
    #       while True:
    #          data = conn.recv(1024)
    #         return data
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    data = (sock.recv(1024))
    sock.close()
    return data


def A_main(message, HOST='127.0.0.1', PORT=8000):
    your_message = message

    pubkey_pem = receive_from_another(HOST, PORT)
    time.sleep(1)

    finmes = message(your_message, pubkey_pem)
    send_to_another(HOST, PORT, finmes[0])
    time.sleep(1)

    send_to_another(HOST, PORT, finmes[1])
    print('Check input of Bob.py')


print('''This is the second program u need to start.
Write there a message, which u want to send (only latin letters).
''')
text = input('Type your text: ')

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

A_main(text, HOST, PORT)
