import socket
from port import ObjPort

class Agent(object):
	def __init__(self, addr):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(addr)
		self.port = ObjPort(sock)

	def list(self):
		self.port.write("?")
		return self.port.read()

	def fetch(self, want="*"):
		if want == "*":
			req = "*"
		else:
			req = want
		self.port.write(req)
		return self.port.read()

if __name__ == '__main__':
	Smith = Agent(("localhost", 10001))
	print Smith.list()
	print Smith.fetch()