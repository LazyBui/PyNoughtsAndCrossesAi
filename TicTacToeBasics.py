class Mark:
	o = -1
	x = 1

	@staticmethod
	def getText(mark):
		if mark == Mark.o: return 'o'
		if mark == Mark.x: return 'x'
		return ''

class Victory:
	o = 1
	x = 2
	tie = 3

	@staticmethod
	def getText(victoryState):
		if victoryState == Victory.o: return 'o'
		if victoryState == Victory.x: return 'x'
		if victoryState == Victory.tie: return 'tie'
		return 'undecided'