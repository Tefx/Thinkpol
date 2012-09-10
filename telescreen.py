import gevent
from gevent.queue import Queue
from gevent import socket
from uuid import uuid1
from port import Port
import yajl as json
import sys

LISTEN_PORT = 9999

class Telescreen(object):
	def __init__(self):
		self.__dict__["cq"] = Queue()
		self.__dict__["observer"] = gevent.spawn(self.observe)
		self.__dict__["state"] = {}
		self.uuid = uuid1().hex

	def __setattr__(self, attr, val):
		 self.state[attr] = val

	def observe(self):
		listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listen_sock.bind(("", LISTEN_PORT))
		listen_sock.listen(20)
		while True:
			sock, _ = listen_sock.accept()
			port = Port(sock)
			port.write(json.dumps(self.state))
			port.close()

	def keep_alive(self):
		self.observer.join()


if __name__ == '__main__':
	class T(Telescreen):
		def __init__(self):
			super(T, self).__init__()
			self.v1 = 1
			self.v2 = 2

	t = T()
	t.a = 1
	t.a = 1
	t.a = 2
	gevent.sleep(20)
	t.a = 6
	t.keep_alive()