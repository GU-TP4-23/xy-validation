import pigpio
import struct
import time
import rasp_opencv

import random

BUS_NUM = 1
XY_ADDR = 0x57
header_mv = '\x61'
header_ok = '\x76'

def handler(gpio, level, tick):
	global pi
	print("interrupt received")
	time.sleep(0.5);
	(count, data) = pi.i2c_read_device(xy, 8)
	print(f"read {count} bytes of raw data:\t", data)
	x = struct.unpack_from('f', data, 0)
	y = struct.unpack_from('f', data, 4)
	print("x:\t", x)
	print("y:\t", y)
	
	
	"""
	CV stuff
	
	# used to track progress
	team = 0
	component = 0
	new_x, new_y = rasp_opencv.call_CV(x,y,team, component)
	# case when it is in position
	if (new_x is None and new_y is None):
		pass
	"""

	time.sleep(5)
	
	if random.choice([True, False]):
		print("writing confirmation...")
		msg_ok = ord(header_ok)
		pi.i2c_write_byte(xy, msg_ok)
	else:
		print("writing adjustment...")
		new_x = 20000.0
		new_y = 40000.0
		msg_adj = bytearray(struct.pack(
			"<cff",
			bytes(header_mv, 'ascii'),
			new_x,
			new_y
		))
		pi.i2c_write_device(xy, msg_adj)

if __name__ == "__main__":
	print("initialising GPIO")
	pi = pigpio.pi()
	if not pi.connected:
		print("failed to initialise GPIO")
		exit()
	print("GPIO initialised")
	
	print("intialising I2C slave device at ", XY_ADDR)
	xy = pi.i2c_open(BUS_NUM, XY_ADDR)
	if not xy:
		print("failed to initialise I2C device")
		exit()
	irq = pi.callback(21, pigpio.RISING_EDGE, handler)
	print("I2C device initialised")
	
	print("waiting for interrupt")
	while True:
		print(".", end="", flush=True)
		time.sleep(0.5)
