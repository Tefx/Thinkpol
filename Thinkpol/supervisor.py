import psutil
from subprocess import PIPE
from telescreen import Telescreen
import gevent
import signal

class Worker(Telescreen):
	def __init__(self, cmd):
		super(Worker, self).__init__()
		self._keeplet = gevent.spawn(self.keep_alive)
		self.cmd = cmd

	def keep_alive(self):
		self._p = psutil.Popen(self.cmd, shell=False, stdout=PIPE)
		self._running = True
		while self._running:
			if not self._p.is_running():
				self._p = psutil.Popen(self.cmd, shell=False, stdout=PIPE)
			gevent.sleep(5)

	def stop(self):
		self._running = False
		self._p.terminate()
		try:
			self._p.wait(3)
		except TimeoutExpired:
			self._p.kill()

	def info(self):
		return {'cpu_percent'	:	self._p.get_cpu_percent(),
				'memory_percent':	self._p.get_memory_percent(),
				'status'		:	str(self._p.status),
				'usertimes'		:	self._p.get_cpu_times().user,
				'systimes'		:	self._p.get_cpu_times().system}


class Node(Telescreen):
	def start(self, cmd, num):
		print num
		self._workers = [Worker(cmd) for i in xrange(num)]
		self.cpu_num = psutil.NUM_CPUS
		self.boot_time = psutil.BOOT_TIME
		self.pmem_total = psutil.TOTAL_PHYMEM

	def stop(self):
		for worker in self._workers:
			worker.stop()

	def connect(self, addr, conn_workers=False):
		self._connect(addr)
		if conn_workers:
			for worker in self._workers:
				worker._connect(addr)

	def fetch_trigger(self):
		self.pmem_used = psutil.used_phymem()
		self.worker_info = {str(w):w.info() for w in self._workers}


if __name__ == '__main__':
	sv = Node()
	sv.start("yes", 2)
	sv.connect(("localhost", 10000))

	gevent.signal(signal.SIGTERM, sv.stop)
	gevent.signal(signal.SIGQUIT, sv.stop)
	gevent.signal(signal.SIGINT, sv.stop)

	gevent.sleep(100)