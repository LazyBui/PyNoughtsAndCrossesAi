import os, sys, random
from BinaryFileReader import BinaryFileReader
from BinaryFileWriter import BinaryFileWriter
from LearningMetric import LearningMetric

class LearningChooser:
	def __init__(self, options, metricsFile, explorationTolerance):
		if explorationTolerance < 0 or explorationTolerance > 100: raise ArgumentException('explorationTolerance should be expressed as an integer between 0 and 100 inclusive')
		explorationTolerance = int(explorationTolerance)

		self.options = []
		self.metrics = {}
		self.metricsFile = metricsFile
		self.explorationTolerance = explorationTolerance

		try:
			with BinaryFileReader(metricsFile) as f:
				entries = f.readInt32()
				for i in range(entries):
					entry = LearningMetric()
					entry.load(f)
					self.metrics[entry.getIdentifier()] = entry
					self.options.append(entry.getIdentifier())

		except IOError as e:
			for i in range(len(options)):
				self.addOption(options[i])

	def __str__(self): return self.__unicode__()
	def __unicode__(self):
		l = sorted(list(self.metrics.values()), key = lambda m: m.getIdentifier())
		s = '\n'.join('{}'.format(n) for n in l)
		return '{{LearningChooser ({}): \n{}}}'.format(len(self.metrics.values()), s)
	def __repr__(self): return self.__unicode__()

	def chooseOption(self):
		option = None
		if random.randint(0, 100) < self.explorationTolerance:
			option = self.options[random.randint(0, len(self.options) - 1)]
		else:
			sortedMetrics = sorted(self.metrics.values(), key = lambda v: v.getChance(), reverse = True)
			option = sortedMetrics[0].getIdentifier()

		self.metrics[option].choose()
		return option

	def chooseOptionFromSet(self, options):
		option = None

		# No point even bothering
		if len(options) == 1: option = options[0]
		elif random.randint(0, 100) < self.explorationTolerance:
			while option is None or option not in options:
				option = self.options[random.randint(0, len(self.options) - 1)]
		else:
			sortedMetrics = sorted(self.metrics.values(), key = lambda v: v.getChance(), reverse = True)
			i = 0
			while option is None or option not in options:
				option = sortedMetrics[i].getIdentifier()
				i += 1

		self.metrics[option].choose()
		return option

	def addOption(self, option):
		self.options.append(option)
		self.metrics[option] = LearningMetric(identifier = option, rewards = 1, totalTests = 1)

	def hasOption(self, option): return option in self.options
	def rewardIndex(self, index): self.rewardOption(self.options[index])
	def rewardOption(self, option): self.metrics[option].reward()

	def save(self):
		with BinaryFileWriter(self.metricsFile) as f:
			keys = self.metrics.keys()
			f.writeInt32(len(keys))
			for key in keys:
				self.metrics[key].save(f)