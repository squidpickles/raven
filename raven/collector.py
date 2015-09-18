import serial
import asyncore
import logging
import threading
import raven.parser
from ConfigParser import RawConfigParser

kRecvBufferSize = 8192
kLoopTimeout = 5

serial.Serial.recv = serial.Serial.read
serial.Serial.send = serial.Serial.write

kLog = logging.getLogger(__name__)

class SerialClient(object, asyncore.dispatcher):
	def __init__(self, device='/dev/ttyUSB0', speed=115200):
		asyncore.dispatcher.__init__(self)
		self.create_socket(device, speed)
		self.send_buffer = b''
		self.send_lock = threading.RLock()
		self.looper = threading.Thread(target=asyncore.loop, name='Asyncore loop', kwargs={'timeout': kLoopTimeout})
		self.looper.daemon = True

	def start(self):
		self.looper.start()

	def stop(self):
		self.close()
		self.looper.join()

	def create_socket(self, device, speed):
		ser = serial.Serial(device, speed, serial.EIGHTBITS, serial.PARITY_NONE, timeout=0.5)
		ser.nonblocking()
		ser.flushInput()
		ser.flushOutput()
		self.set_socket(ser)

	def handle_read(self):
		raw = self.recv(kRecvBufferSize)
		kLog.debug("Received {}".format(raw))
		return raw

	def writable(self):
		return (len(self.send_buffer) > 0)

	def handle_write(self):
		bytes_sent = self.send(self.send_buffer)
		kLog.debug("Sent {}".format(self.send_buffer[:bytes_sent]))
		self.send_buffer = self.send_buffer[bytes_sent:]

	def send_message(self, raw):
		with self.send_lock.acquire():
			self.send_buffer += raw

class Collector(SerialClient):
	def __init__(self, config_path, read_callback=None):
		self.config = RawConfigParser()
		self.config.read(config_path)
		self.recv_buffer = b''
		device = self.config.get('serial', 'device')
		speed = self.config.getint('serial', 'speed')
		super(Collector, self).__init__(device, speed)
		self.read_callback = read_callback

	def handle_read(self):
		raw = super(Collector, self).handle_read()
		self.recv_buffer += raw
		try:
			self.read_callback(raven.parser.RavenMessageParser.parse(self.recv_buffer.strip(b'\x00')))
		except Exception:
			pass
		else:
			self.recv_buffer = b''

	def send_command(self, command):
		raw = raven.parser.RavenCommand.dump(command)
		self.send_message(raw)

if __name__ == '__main__':
	import time
	logging.basicConfig(level=logging.DEBUG)
	client = SerialClient()
	kLog.info("Starting")
	client.start()
	kLog.info("Waiting 10 seconds")
	try:
		time.sleep(10)
	except KeyboardInterrupt:
		pass
	kLog.info("Stopping")
	client.stop()
	kLog.info("Exiting")
