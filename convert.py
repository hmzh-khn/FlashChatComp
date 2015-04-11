import re
import random
import rs

skip = [0b101010, 0b010101, 0b000000, 0b111111];
values = ["{:06b}".format(x) for x in range(0, 2**6) if not x in skip]

lowChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./ "
highChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>? '

SHIFT_VAL = values[-1]

SENTINEL = "00010101010101000"


rsEncoder = rs.RSCoder(len(values),len(values)-1)

def changeListBase(arr, oldbase, newbase):
	temp = reduce(lambda a, val: a*oldbase + val, arr, 0)
	res = []
	while temp > 0:
		res.append(int(temp % newbase))
		temp /= newbase
	res.reverse()
	return res

def encode(s):
	rsenc = rsEncoder.encode(s)
	indices = changeListBase(rsenc, 256, len(values))
	return ''.join(values[i] for i in indices)

	# for c in s:
	# 	if c in lowChars:
	# 		idx = lowChars.index(c)
	# 		res.append(values[idx])
	# 	elif c in highChars:
	# 		idx = highChars.index(c)
	# 		res.append(SHIFT_VAL)
	# 		res.append(values[idx])
	# return ''.join(res)

def decode(bits):
	parts = re.findall(".{6}",bits)
	indices = [values.index(seq) for seq in parts]
	rsenc = changeListBase(indices, len(values), 256)
	result = rsEncoder.decode(rsenc)
	return result

	# res = []
	# wasShift = False
	# for b in re.findall(".{6}",bits):
	# 	try:
	# 		if b == SHIFT_VAL:
	# 			wasShift = True
	# 		else:
	# 			idx = values.index(b)
	# 			if wasShift:
	# 				res.append(highChars[idx])
	# 			else:
	# 				res.append(lowChars[idx])
	# 			wasShift = False
	# 	except:
	# 		pass
	# return ''.join(res)

# def checksum(bits):
# 	sum = 0
# 	for b in re.findall(".{6}",bits):
# 		sum += int(b,2)
# 	csidx = sum % len(values)
# 	return values[csidx]

def makeMessage(type,body):
	t = values[lowChars.index(type)]
	encoded = encode(body)
	datasize = len(encoded)/6
	if(datasize >= len(values)):
		raise Exception("Message is too long.")
	# cs = checksum(encoded)

	print t,datasize

	# sizeBit1 = datasize / len(values)
	# sizeBit2 = datasize % len(values)

	msg = [SENTINEL]
	msg.append(t)
	msg.append(values[datasize])
	# msg.append(cs)
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
					print "FOUND SENTINEL!"
					self.state = "header_type"
					self.bits = ""
				while not SENTINEL.startswith(self.bits):
					self.bits = self.bits[1:]
			elif len(self.bits) == 6:
				if self.state == "header_type":
					self.message['type'] = lowChars[values.index(self.bits)]
					self.state = "header_size"
					print "Got header type {}".format(self.message['type'])
				elif self.state == "header_size":
					if self.counter == 0:
						self.message['size'] = values.index(self.bits)
						self.state = "body"
						print "Got header size {}".format(self.message['size'])
				# elif self.state == "header_checksum":
				# 	self.message['checksum'] = self.bits
				# 	self.state = "body"
				# 	print "Got header checksum {}".format(self.message['checksum'])
				elif self.state == "body":
					self.data += self.bits
					self.counter += 1
					if self.counter >= self.message['size']:
						self.message['body'] = decode(self.data)
						result = self.message
						print "Got message body! {}".format(self.message['body'])
						self.reset()
						return result
				self.bits = ""
				return None
		except ValueError, e:
			print "VALUE ERROR"
			print e
			self.reset()
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
		+ makeMessage('m',"Ice cream") \
		+ '{:b}'.format(random.randint(0,2**random.randint(3,20))) \
		+ makeMessage('m',"Potato salad!") \
		+ '{:b}'.format(random.randint(0,2**random.randint(3,20)))
	print(e)

	decoder = MessageDecoder();
	for bit in e:
		value = decoder.consume(bit == '1')
		if value != None:
			print value
