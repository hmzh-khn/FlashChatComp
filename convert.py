import re
import random

skip = [0b101010, 0b010101, 0b000000, 0b111111];
values = ["{:06b}".format(x) for x in range(0, 2**6) if not x in skip]

lowChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./ "
highChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>? '

SHIFT_VAL = values[-1]

SENTINEL = "00010101010101000"

def encode(s):
	res = []
	for c in s:
		if c in lowChars:
			idx = lowChars.index(c)
			res.append(values[idx])
		elif c in highChars:
			idx = highChars.index(c)
			res.append(SHIFT_VAL)
			res.append(values[idx])
	return ''.join(res)

def decode(bits):
	res = []
	wasShift = False
	for b in re.findall(".{6}",bits):
		try:
			if b == SHIFT_VAL:
				wasShift = True
			else:
				idx = values.index(b)
				if wasShift:
					res.append(highChars[idx])
				else:
					res.append(lowChars[idx])
				wasShift = False
		except:
			pass
	return ''.join(res)

def checksum(bits):
	sum = 0
	for b in re.findall(".{6}",bits):
		sum += int(b,2)
	csidx = sum % len(values)
	return values[csidx]

def makeMessage(type,body):
	t = values[lowChars.index(type)]
	encoded = encode(body)
	datasize = len(encoded)/6
	if(datasize >= len(values)**2):
		raise Exception("Message is too long.")
	cs = checksum(encoded)

	print t,datasize, cs

	sizeBit1 = datasize / len(values)
	sizeBit2 = datasize % len(values)

	msg = [SENTINEL]
	msg.append(t)
	msg.append(values[sizeBit1])
	msg.append(values[sizeBit2])
	msg.append(cs)
	msg.append(encoded)

	#print msg

	return ''.join(msg)

class MessageDecoder:
	state = "scanning"
	bits = ""
	message = {}
	counter = 0
	data = ""

	def __init__(self):
		pass

	def reset(self):
		self.state = "scanning"
		self.bits = ""
		self.message = {}
		self.counter = 0
		self.data = ""

	def consume(self, bit):
		try:
			self.bits += "1" if bit else "0"
			#print self.state, self.bits
			if self.state == "scanning":
				if self.bits == SENTINEL:
					self.state = "header_type"
					self.bits = ""
				while not SENTINEL.startswith(self.bits):
					self.bits = self.bits[1:]
			elif len(self.bits) == 6:
				if self.state == "header_type":
					self.message['type'] = decode(self.bits)
					self.state = "header_size"
				elif self.state == "header_size":
					if self.counter == 0:
						self.message['size'] = values.index(self.bits)
						self.counter += 1
					elif self.counter == 1:
						self.message['size'] = self.message['size']*len(values) + values.index(self.bits)
						self.counter = 0
						self.state = "header_checksum"
				elif self.state == "header_checksum":
					self.message['checksum'] = self.bits
					self.state = "body"
					print self.message
				elif self.state == "body":
					self.data += self.bits
					self.counter += 1
					if self.counter >= self.message['size']:
						cs = checksum(self.data)
						if cs == self.message['checksum']:
							self.message['body'] = decode(self.data)
							result = self.message
							self.reset()
							return result
						else:
							print "Invalid checksum!"
							self.reset()
				self.bits = ""
				return None
		except ValueError, e:
			print "BAD LOOKUP"
			print e
			reset()
			return None


# def decodeMessage():
# 	decoder = MessageDecoder();
# 	while True:
# 		bit = yield None
# 		val = decoder.consume(bit)
# 		if val != None:
# 			yield val
# 			raise StopIteration()

if __name__ == '__main__':
	e =  '{:b}'.format(random.randint(0,2**random.randint(3,20))) \
		+ makeMessage('m',"If you pass the optional framerate argument the function will delay to keep the game running slower than the given ticks per second. This can be used to help limit the runtime speed of a game. By calling Clock.tick_busy_loop(40) once per frame, the program will never run at more than 40 frames per second.") \
		+ '{:b}'.format(random.randint(0,2**random.randint(3,20))) \
		+ makeMessage('m',"Potato salad!") \
		+ '{:b}'.format(random.randint(0,2**random.randint(3,20)))
	print(e)

	decoder = MessageDecoder();
	for bit in e:
		value = decoder.consume(bit == '1')
		if value != None:
			print value
