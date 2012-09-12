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

	def fetch_trigger(self):
		self.cpu_percent = self._p.get_cpu_percent()
		self.memory_percent = self._p.get_memory_percent()
		self.status = str(self._p.status)
		self.usertimes = self._p.get_cpu_times().user
		self.systimes = self._p.get_cpu_times().system


class Node(Telescreen):
	def start(self, cmd, num):
		print num
		self.workers = [Worker(cmd) for i in xrange(num)]
		self.cpu_num = psutil.NUM_CPUS
		self.vmem_total = psutil.total_virtmem()
		self.boot_time = psutil.BOOT_TIME
		self.pmem_total = psutil.TOTAL_PHYMEM

	def stop(self):
		for worker in self.workers:
			worker.stop()

	def connect(self, addr):
		self._connect(addr)
		for worker in self.workers:
			worker._connect(addr)

	def fetch_trigger(self):
		self.vmem_usage = psutil.virtmem_usage()
		self.vmem_avail = psutil.avail_virtmem()
		self.vmem_used = psutil.used_virtmem()

		self.pmem_usage = psutil.phymem_usage()
		self.pmem_avail = psutil.avail_phymem()
		self.pmem_used = psutil.used_phymem()


if __name__ == '__main__':
	sv = Node()
	sv.start("yes", 2)
	sv.connect(("localhost", 10000))

	gevent.signal(signal.SIGTERM, sv.stop)
	gevent.signal(signal.SIGQUIT, sv.stop)
	gevent.signal(signal.SIGINT, sv.stop)

	gevent.sleep(100)
