#!?usr/bin/python3

import minecraft
import socket
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)


def message(text, pubkey_pem):
    aes_key = minecraft.aes_key_generate()
    ciphertext = minecraft.aes_encryption(text, aes_key)
    cipherkey = minecraft.rsa_encryption(pubkey_pem, aes_key)
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


your_message = input()

pubkey_pem = receive_from_another(HOST, PORT)
time.sleep(1)

finmes = message(your_message, pubkey_pem)
send_to_another(HOST, PORT, finmes[0])
time.sleep(1)

send_to_another(HOST, PORT, finmes[1])
