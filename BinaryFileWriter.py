import struct, os

class BinaryFileWriter:
	def __init__(self, filename):
		self.m_filename = filename
		self.m_handle = open(filename, 'wb')
		self.m_pos = 0

	def __enter__(self): return self
	def __exit__(self, type, value, traceback): self.close()

	def _write(self, s, val, b):
		ret = struct.pack(s, val)
		self.m_handle.write(ret)
		self.m_pos += b
		return ret

	def close(self):
		self.m_pos = -1
		self.m_handle.close()

	def tell(self): return self.m_pos

	def writeBool(self, val): return self._write('?', val, 1)
	def writeInt8(self, val): return self._write('b', val, 1)
	def writeInt16(self, val): return self._write('h', val, 2)
	def writeInt32(self, val): return self._write('i', val, 4)
	def writeInt64(self, val): return self._write('q', val, 8)
	def writeUInt8(self, val): return self._write('B', val, 1)
	def writeUInt16(self, val): return self._write('H', val, 2)
	def writeUInt32(self, val): return self._write('I', val, 4)
	def writeUInt64(self, val): return self._write('Q', val, 8)
	def writeFloat32(self, val): return self._write('f', val, 4)
	def writeFloat64(self, val): return self._write('d', val, 8)
	def writeString(self, val, encoding = 'utf-8'): return self._write('{}s'.format(len(val)), bytes(val, encoding), len(val))
	def writeNullTerminatedString(self, val, encoding = 'utf-8'):
		self.writeString(val, encoding)
		self.writeInt8(0x00)

	# Aliases
	def writeByte(self): return self.writeInt8()
	def writeShort(self): return self.writeInt16()
	def writeInt(self): return self.writeInt32()
	def writeLong(self): return self.writeInt64()
	def writeUByte(self): return self.writeUInt8()
	def writeUShort(self): return self.writeUInt16()
	def writeUInt(self): return self.writeUInt32()
	def writeULong(self): return self.writeUInt64()
	def writeFloat(self): return self.writeFloat32()
	def writeDouble(self): return self.writeFloat64()
