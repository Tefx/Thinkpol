import socket
from port import Port

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 9999))
port = Port(sock)

print port.read()