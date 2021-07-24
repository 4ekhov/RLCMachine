import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8080))

sock.listen(1)

conn, addr = sock.accept()
conn.send(b'qwerty')
conn.close()