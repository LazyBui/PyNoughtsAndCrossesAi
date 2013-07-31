import array, sys, os, re, random
from TicTacToeBasics import *

class Board:
	def __init__(self, columnCount, rowCount, solutionSequenceCount):
		self.board = []
		self.columnCount = columnCount
		self.rowCount = rowCount
		self.solutionSequenceCount = solutionSequenceCount

	def __str__(self): return self.__unicode__()
	def __repr__(self): return self.__unicode__()
	def __unicode__(self):
		reprStr = ''
		lastRow = 0
		lastColumn = 0
		boardSize = self.columnCount * self.rowCount
		maxPadding = len('{}'.format(boardSize))
		formatString = '{{0:0{}}}'.format(maxPadding)
		padding = ' ' * maxPadding
		lineBreak = '-' * ((self.columnCount * maxPadding) + (self.columnCount - 1) * 3)
		for i in range(boardSize):
			row = i // self.columnCount
			column = i % self.columnCount

			if row != lastRow:
				reprStr += '\n' + lineBreak + '\n'
				lastRow = row
				lastColumn = 0

			if column != lastColumn:
				reprStr += ' | '
				lastColumn = column

			t = Mark.getText(self.board[i])
			if t == '': reprStr += formatString.format(i + 1)
			else: reprStr += padding[0:maxPadding - len(t)] + t

		return reprStr

	def generate(self, fillInRandomGame = False):
		boardSize = self.columnCount * self.rowCount
		currentPlayer = 0
		if random.randint(0, 1) == 1: currentPlayer = Mark.o
		else: currentPlayer = Mark.x

		self.startingPlayer = currentPlayer
		self.board = [0] * boardSize

		if fillInRandomGame:
			done = False
			addedMoves = 0

			# 3x3 = 9 -> 30
			# 5x5 = 25 -> 20
			# 10x10 = 100 -> 10
			chanceToExit = max(100 - boardSize, 10)
			# Alternate moves until we either hit a random event or fill the table			
			while not done and addedMoves < boardSize:
				moveIndex = -1
				while moveIndex == -1 or self.board[moveIndex] != 0:
					moveIndex = random.randint(0, boardSize - 1)

				self.board[moveIndex] = currentPlayer
				if currentPlayer == Mark.x: currentPlayer = Mark.o
				else: currentPlayer = Mark.x

				done = random.randint(0, 100) < chanceToExit
				addedMoves += 1

	def getRaw(self): return list(self.board)

	def commitMove(self, mark, index):
		currentPlayer = self._impl_currentPlayer(self.getMoveCounts())
		if mark != currentPlayer: raise Exception
		if index < 0 or index > self.columnCount * self.rowCount: raise Exception
		if self.board[index] != 0: raise Exception
		self.board[index] = mark

	def getCurrentPlayer(self): return self._impl_currentPlayer(self.getMoveCounts())

	def _impl_currentPlayer(self, moveCounts):
		oMoves = moveCounts['o']
		xMoves = moveCounts['x']
		firstPlayer = moveCounts['first']

		currentPlayer = None
		if oMoves < xMoves: currentPlayer = Mark.o
		elif oMoves > xMoves: currentPlayer = Mark.x
		elif firstPlayer == 'x': currentPlayer = Mark.x
		elif firstPlayer == 'o': currentPlayer = Mark.o
		else: raise Exception

		return currentPlayer

	def _impl_isGameResolved(self, board, columnCount, rowCount, solutionSequenceCount):
		victoryType = None

		boardSize = columnCount * rowCount
		length = solutionSequenceCount - 1
		columnRightLength = columnCount - length
		columnLeftLength = length - 1
		rowLength = rowCount - length

		def testSolution(i, indexFunction):
			nums = []
			nums.append(board[i])
			for j in range(length):
				idx = indexFunction(i, j)
				nums.append(board[idx])

			total = sum(nums)
			if total == -solutionSequenceCount: return Victory.o
			if total == solutionSequenceCount: return Victory.x
			return None

		hasBlank = False
		for i in range(boardSize):
			row = i // columnCount
			column = i % columnCount
			hasRightDiagonal = column < columnRightLength and row < rowLength
			hasLeftDiagonal = column > columnLeftLength and row < rowLength
			hasHorizontal = column < rowLength
			hasVertical = row < columnRightLength
			if board[i] == 0: hasBlank = True

			if hasRightDiagonal:
				victoryType = testSolution(i, lambda i, j: i + (j  * columnCount) + columnCount + j + 1)
				if not victoryType is None: break
			if hasLeftDiagonal:
				victoryType = testSolution(i, lambda i, j: i + (j  * columnCount) - j + length)
				if not victoryType is None: break
			if hasHorizontal:
				victoryType = testSolution(i, lambda i, j: i + j + 1)
				if not victoryType is None: break
			if hasVertical:
				victoryType = testSolution(i, lambda i, j: i + (j + 1) * rowCount)
				if not victoryType is None: break

		# Victory was undecided, could be a tie or simply in progress
		if victoryType is None and not hasBlank: victoryType = Victory.tie

		return victoryType

	def projectedGameHash(self, board):
		hash = 0
		for i in range(self.columnCount * self.rowCount):
			e = board[i]
			# We don't factor this into the hash, aka a clean board should have a hash of 0
			if e == 0: continue

			# We use these to compute the hash
			row = (i // self.columnCount) + 1
			column = (i % self.columnCount) + 1

			# The hash is a function of the game state, so in our case, the positions of the marks (and by extension, the marks)
			hash ^= (column << 2) | (row << 2 << self.columnCount)

			if e == Mark.o: hash ^= 2
			elif e == Mark.x: hash ^= 1

		return '{0:016X}'.format(hash)

	def currentGameHash(self): return self.projectedGameHash(self.board)

	def getMoveCounts(self):
		movesLeft = 0
		oMoves = 0
		xMoves = 0
		for i in range(self.columnCount * self.rowCount):
			e = self.board[i]
			if e == 0: movesLeft += 1
			elif e == Mark.o: oMoves += 1
			elif e == Mark.x: xMoves += 1

		firstPlayer = 'o'
		if self.startingPlayer == Mark.x: firstPlayer = 'x'
		return {'remaining': movesLeft, 'o': oMoves, 'x': xMoves, 'first': firstPlayer, 'executed': xMoves + oMoves}

	def getAllPossibleNextMoves(self):
		hashes = []
		currentPlayer = self._impl_currentPlayer(self.getMoveCounts())
		for i in range(self.columnCount * self.rowCount):
			e = self.board[i]
			if e != 0: continue

			# We only care about empty columns
			board = list(self.board)
			board[i] = currentPlayer
			hashes.append(self.projectedGameHash(board))

		return hashes

	def getMoveIndexFromHash(self, hash):
		currentPlayer = self._impl_currentPlayer(self.getMoveCounts())
		idx = -1
		for i in range(self.columnCount * self.rowCount):
			e = self.board[i]
			if e != 0: continue

			# We only care about empty columns
			board = list(self.board)
			board[i] = currentPlayer
			testHash = self.projectedGameHash(board)
			if testHash == hash:
				idx = i
				break

		return idx

	def getEndings(self):
		moveCounts = self.getMoveCounts()
		possibleGames = []
		startingPlayer = self._impl_currentPlayer(moveCounts)
		movesLeft = moveCounts['remaining']

		#def findEnding(movesLeft, boardState):
		#	for i in reversed(range(movesLeft)):
		#		findEnding(movesLeft, boardState)

		#findEnding(moveCounts['remaining'], self.board)
		return possibleGames

	def isGameResolved(self):
		return self._impl_isGameResolved(self.board, self.columnCount, self.rowCount, self.solutionSequenceCount)