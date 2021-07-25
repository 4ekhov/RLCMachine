import Crypto_funcs
import socket
import time


def gen_message(text, pubkey_pem):
    aes_key = Crypto_funcs.aes_key_generate()
    ciphertext = Crypto_funcs.aes_encryption(text, aes_key)
    cipherkey = Crypto_funcs.rsa_encryption(pubkey_pem, aes_key)
    return [cipherkey, ciphertext]


def send_to_another(HOST, PORT, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    conn.send(message)
    conn.close()


def receive_from_another(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    data = (sock.recv(1024))
    sock.close()
    return data


def A_communication(message):
    your_message = message

    pubkey_pem = receive_from_another(RECEIVING_HOST, PORT)
    time.sleep(0.05)

    finmes = gen_message(your_message, pubkey_pem)
    send_to_another(SENDING_HOST, PORT, finmes[0])
    time.sleep(0.05)

    send_to_another(SENDING_HOST, PORT, finmes[1])
    print('Check input of Bob.py')


RECEIVING_HOST = input("Type server's ip: ")
SENDING_HOST = socket.gethostname()
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

print('''This is the second program u need to start.
    Write there a message, which u want to send (only latin letters).
    ''')

text = input('Type your text: ')
A_communication(text)
