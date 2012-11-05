from gevent.monkey import patch_all; patch_all()
import gevent
from gevent import socket
from uuid import uuid1
from Corellia import ObjPort

class Telescreen(object):
	monitoring = []

	def __init__(self):
		self._state = {}
		self._uuid = "%s_%s" % (self.__class__.__name__, (uuid1().hex)[:8])
		for name in self.monitoring:
			setattr(self, name, None)

	def _connect(self, addr):
		listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listen_sock.connect(addr)
		self._port = ObjPort(listen_sock)
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
				self._state = {k:getattr(self, k) for k in self.monitoring}
				if not self._port.write(self._state):
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