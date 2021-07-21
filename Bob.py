#!/usr/bin/env python3

import minecraft
import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8000  # The port used by the server


def decryption(cipherkey, ciphertext, privkey_pem):
    aes_key = minecraft.rsa_decryption(privkey_pem, cipherkey)
    plaintext = minecraft.aes_decryption(ciphertext, aes_key)
    return plaintext


def send_to_another(HOST, PORT, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message)


def receive_from_another(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                return data


privkey_pem, pubkey_pem = minecraft.rsa_keys_generate()

send_to_another(HOST, PORT, pubkey_pem)
time.sleep(1)

cipherkey = receive_from_another(HOST, PORT)
time.sleep(1)

ciphertext = receive_from_another(HOST, PORT)

print(decryption(cipherkey, ciphertext, privkey_pem))
