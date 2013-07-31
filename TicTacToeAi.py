import os, sys, random
from LearningChooser import LearningChooser

class TicTacToeAi:
	def __init__(self, board, mark):
		self.board = board
		self.ai = LearningChooser([], 'tictactoe.bin', 75)
		self.currentHashes = []
		self.mark = mark

	def __str__(self): return self.__unicode__()
	def __unicode__(self): return '{{TicTacToeAi: {}}}'.format(self.ai)
	def __repr__(self): return self.__unicode__()

	def commitMove(self):
		board = self.board
		hashes = board.getAllPossibleNextMoves()

		for hash in hashes:
			if not self.ai.hasOption(hash): self.ai.addOption(hash)

		selectedHash = self.ai.chooseOptionFromSet(hashes)
		self.currentHashes.append(selectedHash)
		self.board.commitMove(self.mark, self.board.getMoveIndexFromHash(selectedHash))

	def win(self):
		for hash in self.currentHashes:
			self.ai.rewardOption(hash)

	def saveResults(self): self.ai.save()