import array, sys, os, re, random
from TicTacToeBasics import *
from TicTacToeBoard import *
from LearningChooser import *
from TicTacToeAi import *

exit = False
while not exit:
	board = Board(3, 3, 3)
	board.generate(False)
	boardSize = 3 * 3

	gameComplete = False
	firstMark = board.getCurrentPlayer()
	currentMark = firstMark
	playerMark = None
	aiMark = None
	vType = None
	if random.randint(0, 100) < 50:
		playerMark = firstMark
		if firstMark == Mark.o: aiMark = Mark.x
		elif firstMark == Mark.x: aiMark = Mark.o
	else:
		aiMark = firstMark
		if firstMark == Mark.o: playerMark = Mark.x
		elif firstMark == Mark.x: playerMark = Mark.o

	print('Player [{}]'.format(Mark.getText(playerMark)))
	print('AI [{}]'.format(Mark.getText(aiMark)))
	print('{} goes first'.format(Mark.getText(firstMark)))
	print('')

	ai = TicTacToeAi(board, aiMark)
	inputQuestion = 'Board index to place mark [1-{}]? '.format(boardSize)

	while not gameComplete:
		print('TURN: {}'.format(Mark.getText(currentMark)))
		print('Board: \n{}'.format(board))
		#print('GameHash: {}'.format(board.currentGameHash()))
		print('')

		if currentMark == aiMark: ai.commitMove()
		else:
			moveValid = False
			while not moveValid:
				try:
					moveIndex = input(inputQuestion)
					if moveIndex == 'secret':
						print(ai)
						raise Exception
					moveIndex = int(moveIndex)
					moveIndex -= 1
					board.commitMove(playerMark, moveIndex)
					moveValid = True
				except Exception as e:
					print('{}'.format(e))

		vType = board.isGameResolved()
		gameComplete = not vType is None
		if currentMark == playerMark: currentMark = aiMark
		elif currentMark == aiMark: currentMark = playerMark

	if vType == Victory.tie: print('Tie')
	else: print('Victory: {}!'.format(Victory.getText(vType)))

	if (vType == Victory.o and aiMark == Mark.o) or (vType == Victory.x and aiMark == Mark.x): ai.win()
	ai.saveResults()

	answer = None
	while answer is None or answer not in ['y', 'Y', 'yes', 'Yes', 'quit', 'Quit', 'exit', 'Exit', 'n', 'N', 'no', 'No']:
		answer = input('Exit [y/n]? ')
		if answer in ['y', 'Y', 'yes', 'Yes', 'quit', 'Quit', 'exit', 'Exit']: exit = True