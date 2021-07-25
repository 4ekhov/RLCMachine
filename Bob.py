import Crypto_funcs
import socket
import time


def decryption(cipherkey, ciphertext, privkey_pem):
    aes_key = Crypto_funcs.rsa_decryption(privkey_pem, cipherkey)
    plaintext = Crypto_funcs.aes_decryption(ciphertext, aes_key)
    return plaintext


def send_to_another(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SENDING_HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    conn.send(message)
    conn.close()


def receive_from_another():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((RECEIVING_HOST, PORT))
    data = (sock.recv(1024))
    sock.close()
    return data


def B_communication():
    privkey_pem, pubkey_pem = Crypto_funcs.rsa_keys_generate()

    send_to_another(pubkey_pem)
    time.sleep(0.05)

    cipherkey = receive_from_another()
    time.sleep(0.05)

    ciphertext = receive_from_another()

    print(decryption(cipherkey, ciphertext, privkey_pem))


RECEIVING_HOST = input("Type client's ip: ")
SENDING_HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 8000  # The port used by the server

print('''Run this program before Alice.py
Here will be ur message from second program, u are welcome.

Your message: ''', end='')
B_communication()
