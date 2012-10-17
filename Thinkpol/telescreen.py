from gevent.monkey import patch_all; patch_all()
import gevent
from gevent import socket
from uuid import uuid1
from port import Port
import yajl as json

class Telescreen(object):
	monitoring = []

	def __init__(self):
		self.__dict__["_state"] = {}
		self.__dict__["_uuid"] = "%s_%s" % (self.__class__.__name__, (uuid1().hex)[:8])

	def __setattr__(self, attr, val):
		self.__dict__[attr] = val
		if attr in self.monitoring:
			self._state[attr] = val

	def _connect(self, addr):
		listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listen_sock.connect(addr)
		self._port = Port(listen_sock)
		self._observer = gevent.spawn(self._observe)

	def _observe(self):
		self._port.write(self._uuid)
		while True:
			msg = self._port.read()
			if not msg: 
				break
			elif msg == "P":
				self._port.write("P")
			else:
				self.fetch_trigger()
				if not self._port.write(json.dumps(self._state)):
					break

	def fetch_trigger(self):
		pass

	def _close_connection(self):
		self._port.close()
		self._observer.join()

	def __repr__(self):
		return self._uuid

if __name__ == '__main__':
	class T(Telescreen):
		def __init__(self):
			super(T, self).__init__()
			self.v1 = 1
			self.v2 = 2

	t = T()
	t._connect(("localhost", 10000))
	t.a = 1
	t.a = 1
	t.a = 2
	gevent.sleep(20)
	t.a = 6
	t._a = 7
	t._keep_alive()