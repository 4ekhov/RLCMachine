#!?usr/bin/python3

import Crypto_funcs
import socket
import time


def message(text, pubkey_pem):
    aes_key = Crypto_funcs.aes_key_generate()
    ciphertext = Crypto_funcs.aes_encryption(text, aes_key)
    cipherkey = Crypto_funcs.rsa_encryption(pubkey_pem, aes_key)
    return [cipherkey, ciphertext]


def receive_from_another(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                return data


def send_to_another(HOST, PORT, text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(text)


def A_main(massage, HOST='127.0.0.1', PORT=8000):
    your_message = massage

    pubkey_pem = receive_from_another(HOST, PORT)
    time.sleep(1)

    finmes = message(your_message, pubkey_pem)
    send_to_another(HOST, PORT, finmes[0])
    time.sleep(1)

    send_to_another(HOST, PORT, finmes[1])


print('''
This is the first u program u need to start. Write there a massage, which u want do send (only latin letters).
Run second program (Bob.py) after typed ur massage.
''')
text = input('Type your text: ')

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

A_main(text, HOST, PORT)
