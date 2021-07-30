import Crypto_funcs
import paho.mqtt.client as mqtt 
import time
import uuid

# NOTE: to add a third party, Eve, to eavesdrop on the communication, use:
#   mosquitto_sub -t "/slon/2021-summer/4ekhov_crypto_project/#" -h $BROKER_URL -u $USERNAME -P $PASSWORD

MAIN_TOPIC = '/slon/2021-summer/4ekhov_crypto_project/'

my_name = input('Your name: ')
try:
    pub = open(my_name+'.pub', 'rb').read()
    priv = open(my_name+'.priv', 'rb').read()
    print('Keys loaded OK')
except FileNotFoundError:
    print('Keys not found, generating')
    priv, pub = Crypto_funcs.rsa_keys_generate()
    with open(name+'.pub', 'wb') as o: o.write(pub)
    with open(name+'.priv', 'wb') as o: o.write(priv)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MAIN_TOPIC+'#')

peer_name = None
peer_key = None

def on_message(client, userdata, msg):
    global peer_name
    global peer_key
    global my_name
    if msg.topic == MAIN_TOPIC + 'pubkey/requests':
        if msg.payload.decode() == my_name:
            print("Received request for my public key")
            client.publish(MAIN_TOPIC + 'pubkey/responses', bytes(my_name, 'utf-8') + b':' + pub)
    elif peer_name is not None:
        if msg.topic == MAIN_TOPIC + 'pubkey/responses':
            payload = msg.payload.decode()
            name, data = payload.split(':', 1)
            if name == peer_name:
               peer_key = data 
    elif msg.topic == MAIN_TOPIC + 'messages':
        target_name, key, data = msg.payload.decode().split(':')
        if target_name == my_name:
            key = bytes.fromhex(key)
            data = bytes.fromhex(data)
            data_key = Crypto_funcs.rsa_decryption(priv, key)
            dec_data = Crypto_funcs.aes_decryption(data, data_key)
            print('Received data:', dec_data)
        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_start()

while True:
    peer_name = input('Peer name: ')
    peer_key = None
    client.publish(MAIN_TOPIC+'pubkey/requests', peer_name)
    i = 0
    while peer_key is None:
        print('Waiting for response... (',i, '/ 10)')
        i += 1
        time.sleep(1)
        if i > 10:
            print('Timeout!')
            break
    if peer_key == None:
        peer_name = None
        continue

    message = input('> ')
    symm_key = Crypto_funcs.aes_key_generate()
    symm_data = Crypto_funcs.aes_encryption(message, symm_key)
    enc_key = Crypto_funcs.rsa_encryption(peer_key, symm_key)

    client.publish(MAIN_TOPIC+'messages', peer_name + ':' + enc_key.hex() + ':' + symm_data.hex())
