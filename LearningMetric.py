import sys

class LearningMetric:
	def __init__(self, identifier = None, rewards = None, totalTests = None):
		self.identifier = identifier
		self.rewards = rewards
		self.totalTests = totalTests

	def __str__(self): return self.__unicode__()
	def __unicode__(self): return '{{LearningMetric "{}": {}/{} ({}%)}}'.format(self.identifier, self.rewards, self.totalTests, self.getChance())
	def __repr__(self): return self.__unicode__()

	def reward(self): self.rewards += 1
	def choose(self): self.totalTests += 1

	def load(self, fileStream):
		self.identifier = fileStream.readNullTerminatedString()
		self.rewards = fileStream.readInt32()
		self.totalTests = fileStream.readInt32()

	def save(self, fileStream):
		fileStream.writeNullTerminatedString(self.identifier)
		fileStream.writeInt32(self.rewards)
		fileStream.writeInt32(self.totalTests)

	def getIdentifier(self): return self.identifier
	def getChance(self): return self.rewards / self.totalTests * 100
