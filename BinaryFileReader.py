import struct, os

class BinaryFileReader:
	readAbsolute = os.SEEK_SET
	readRelative = os.SEEK_CUR
	readFromEnd = os.SEEK_END

	def __init__(self, filename):
		self.m_filename = filename
		self.m_handle = open(filename, 'rb')
		self.m_pos = 0

	def __enter__(self): return self
	def __exit__(self, type, value, traceback): self.close()

	def _read(self, s, b):
		ret = struct.unpack(s, self.m_handle.read(b))[0]
		self.m_pos += b
		return ret

	def close(self):
		self.m_pos = -1
		self.m_handle.close()

	def peekBytes(self, bytes):
		ret = self.m_handle.read(bytes)
		self.m_handle.seek(-bytes, self.readRelative)
		return ret

	def tell(self): return self.m_pos

	def seekAbsolute(self, bytePosition): return self.seek(bytePosition, readAbsolute)
	def seekRelative(self, bytes): return self.seek(bytes, readRelative)
	def seekFromEnd(self, bytes): return self.seek(bytes, readFromEnd)

	def seek(self, bytes, whence = readRelative):
		self.m_handle.seek(bytes, whence)
		self.m_pos = self.m_handle.tell()
		return self.m_pos

	def reset(self):
		self.m_handle.seek(0, readAbsolute)
		self.m_pos = 0

	def readBool(self): return self._read('?', 1)
	def readInt8(self): return self._read('b', 1)
	def readInt16(self): return self._read('h', 2)
	def readInt32(self): return self._read('i', 4)
	def readInt64(self): return self._read('q', 8)
	def readUInt8(self): return self._read('B', 1)
	def readUInt16(self): return self._read('H', 2)
	def readUInt32(self): return self._read('I', 4)
	def readUInt64(self): return self._read('Q', 8)
	def readFloat32(self): return self._read('f', 4)
	def readFloat64(self): return self._read('d', 8)
	def readString(self, byteSize, encoding = 'utf-8'): return self._read('{}s'.format(byteSize), byteSize).decode(encoding)
	def readNullTerminatedString(self, byteSize = None, encoding = 'utf-8'):
		if not byteSize is None: return self._read('{}s'.format(byteSize), byteSize).decode(encoding)[:-1]
		bArr = b''
		tByte = self._read('1s', 1)
		while tByte != b'\x00':
			bArr += tByte
			tByte = self._read('1s', 1)
		return bArr.decode(encoding)

	def readBytes(self, bytes):
		ret = self.m_handle.read(bytes)
		self.m_pos += bytes
		return ret

	# Aliases
	def skip(self, bytes): return self.seek(bytes, self.readRelative)
	def readByte(self): return self.readInt8()
	def readShort(self): return self.readInt16()
	def readInt(self): return self.readInt32()
	def readLong(self): return self.readInt64()
	def readUByte(self): return self.readUInt8()
	def readUShort(self): return self.readUInt16()
	def readUInt(self): return self.readUInt32()
	def readULong(self): return self.readUInt64()
	def readFloat(self): return self.readFloat32()
	def readDouble(self): return self.readFloat64()
