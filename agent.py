import json
import socket
from port import Port

class Agent(object):
	def __init__(self, addr):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(addr)
		self.port = Port(sock)

	def list(self):
		self.port.write("?")
		return json.loads(self.port.read())

	def fetch(self, want="*"):
		if want == "*":
			req = "*"
		else:
			req = json.dumps(want)
		self.port.write(req)
		return json.loads(self.port.read())

if __name__ == '__main__':
	Smith = Agent(("localhost", 10001))
	print Smith.list()
	print Smith.fetch(["Worker_8056ddbafca911e1a1f2109add559973"])