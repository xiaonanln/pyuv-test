import socket
import pyuv
import time

TEST_DATA = 'A' * (1024 * 1024 * 20)
WRITE_INTERVAL = 0.2

class Client(object):
	def __init__(self):
		self.loop = pyuv.Loop.default_loop()
		self.tcp = pyuv.TCP(self.loop)
		self.tcp.connect(("127.0.0.1", 1234), self.on_connect)
		self.total_read = 0
		self.total_write = 0
		self.start_time = time.time()

	def on_connect(self, tcp, error):
		print 'on_connect', tcp, error
		tcp.start_read(self.on_read)
		tcp.write(TEST_DATA, self.on_write)

	def on_read(self, tcp, data, error):
		# print 'on_read', tcp, len(data), error
		self.total_read += len(data)

	def on_write(self, tcp, error):
		# print 'on_write', tcp, error

		self.total_write += len(TEST_DATA)
		pyuv.Timer(self.loop).start(self.on_timer, WRITE_INTERVAL, 0)

	def on_timer(self, timer):
		# print 'on_timer', timer
		dt = time.time() - self.start_time
		print self.total_write / dt, self.total_read / dt
		self.tcp.write(TEST_DATA, self.on_write)

client = Client()
client.loop.run()
