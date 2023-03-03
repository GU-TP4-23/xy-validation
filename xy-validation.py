import pigpio
import struct
import time

BUS_NUM = 1
XY_ADDR = 0x57
header_mv = 0x61;
header_ok = 0x76;

def handler(gpio, level, tick):
	global pi
	print("interrupt received")
	(count, data) = pi.i2c_read_device(xy, 8)
	print(f"read {count} bytes of raw data:\t", data)
	x = struct.unpack_from('f', data, 0)
	y = struct.unpack_from('f', data, 4)
	print("x:\t", x)
	print("y:\t", y)
	
	"""
	CV stuff
	"""
	time.sleep(5);
	
	print("writing confirmation...")
	pi.i2c_write_byte(xy, header_ok)

if __name__ == "__main__":
	print("initialising GPIO")
	pi = pigpio.pi()
	if not pi.connected:
		print("failed to initialise GPIO")
		exit()
	print("GPIO initialised")
	
	print("intialising I2C slave device at ", XY_ADDR)
	xy = pi.i2c_open(BUS_NUM, XY_ADDR);
	if not xy:
		print("failed to initialise I2C device")
		exit()
	irq = pi.callback(21, pigpio.RISING_EDGE, handler)
	print("I2C device initialised")
	
	print("waiting for interrupt")
	while True:
		print(".", end="", flush=True)
		time.sleep(0.5);
