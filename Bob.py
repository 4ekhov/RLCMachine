import Crypto_funcs
import socket
import time
from requests import get


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


try:
    server = get('http://api.ipify.org').text
    print('Your ip in network is:', server)
    print('Recommended port: 8000 or other >1023'
          'Use Hamachi or other VPN to create local network')
except Exception:
    SENDING_HOST = socket.gethostname()
    print('Your name in local network is:', SENDING_HOST)
    RECEIVING_HOST = input("Type server's ip/name: ")
    PORT = 8000  # The port used by the server

    print('''
    Run this program before Alice.py
    Here will be message from second program, ypu are welcome.
    
    The message: ''', end='')
    B_communication()
input('type enter to close')
