NO_PLAYER = 0
PLAYER1 = 1
PLAYER2 = 2

class SmallBoard:
		
	def __init__(self, width, height):
		self.height = height
		self.width = width
		self.winner = NO_PLAYER
		self.playCount1 = 0
		self.playCount2 = 0
		self.board = [[NO_PLAYER for i in range(self.width)] for j in range(self.height)]
		self.currPlayer = NO_PLAYER
		self.moveHistory = []

	