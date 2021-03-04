NO_PLAYER = 0
PLAYER1 = 1
PLAYER2 = 2

class SmallBoard:
	
	def __init__(self, side_length):
		self.height = side_length
		self.width = side_length
		self.winner = NO_PLAYER
		self.playCount1 = 0
		self.playCount2 = 0
		self.board = [[NO_PLAYER for i in range(self.width)] for j in range(self.height)]
		self.currPlayer = NO_PLAYER
		self.moveHistory = []
	
	def play(self, r, c, player):
		if self.board[r][c] != NO_PLAYER:
			return (False, NO_PLAYER)

		if player != PLAYER1 and player != PLAYER2:
			return (False, NO_PLAYER)

		if self.winner != NO_PLAYER:
			return (False, self.winner)

		if player == PLAYER1:
			self.playCount1 += 1
		else:
			self.playCount2 += 1

		self.board[r][c] = player
		self.moveHistory.append((r, c))
		self.winner = self.checkWin(r, c, player)
		return (True, self.winner)

	def undoMove(self):
		if len(self.moveHistory) == 0:
			return
		
		r, c = self.moveHistory.pop()

		if self.board[r][c] == PLAYER1:
			self.playCount1 -= 1
		if self.board[r][c] == PLAYER2:
			self.playCount2 -= 1

		self.board[r][c] = NO_PLAYER
		self.winner = NO_PLAYER
		
		return (r, c)

	def validMoves(self, r, c):
		moves = []

		if self.winner != NO_PLAYER:
			return []

		for i in range(self.height):
			for j in range(self.width):
				if self.board[i][j] == NO_PLAYER:
					moves.append((i + r, j + c))

		return moves

	def checkWin(self, r, c, player):
		row = self.checkRow(r, player)
		column = self.checkColumn(c, player)
		diag = self.checkDiag(player)

		return player if row or column or diag else self.checkFill()

	def checkRow(self, r, player):
		for i in range(self.width):
			if self.board[r][i] != player:
				return False

		return True

	def checkColumn(self, c, player):
		for i in range(self.height):
			if self.board[i][c] != player:
				return False

		return True

	def checkDiag(self, player):
		if self.height != self.width:
			return False

		diag1 = True
		diag2 = True
		for i in range(self.height):
			if self.board[i][i] != player:
				diag1 = False

			if self.board[i][self.height - i - 1] != player:
				diag2 = False

		return diag1 or diag2

	def checkFill(self):
		if self.playCount1 + self.playCount2 == self.height * self.width:
			return PLAYER1 if self.playCount1 > self.playCount2 else PLAYER2
		else:
			return NO_PLAYER

class BigBoard:

	def __init__(self, side_length):
		self.height = side_length
		self.width = side_length
		self.playRow = side_length
		self.playColumn = side_length
		self.winner = NO_PLAYER
		self.currPlayer = PLAYER1
		self.wonBoard1 = 0
		self.wonBoard2 = 0
		self.board = [[SmallBoard(side_length) for i in range(side_length)] for j in range(side_length)]
		self.moveHistory = []

	def play(self, r, c):
		bbr = int(r / self.height)
		bbc = int(c / self.width)
		sbr = r % self.height
		sbc = c % self.width

		if self.winner != NO_PLAYER:
			return (False, NO_PLAYER, self.winner)

		# if (r, c) not in self.validMoves():
		# 	return (False, NO_PLAYER, NO_PLAYER)

		if bbr >= self.height or bbc >= self.width:
			return (False, NO_PLAYER, NO_PLAYER)

		if self.playRow != self.height and self.playColumn != self.width and (bbr != self.playRow or bbc != self.playColumn):
			return (False, NO_PLAYER, NO_PLAYER)

		success, winner = self.board[bbr][bbc].play(sbr, sbc, self.currPlayer)

		if not success:
			return (False, winner, NO_PLAYER)

		if winner != NO_PLAYER:
			if winner == PLAYER1:
				self.wonBoard1 += 1
			else:
				self.wonBoard2 += 1

			self.winner = self.checkWin(bbr, bbc)
		
		self.moveHistory.append((bbr, bbc, self.playRow, self.playColumn))
		self.playRow = sbr if self.board[sbr][sbc].winner == NO_PLAYER else self.height
		self.playColumn = sbc if self.board[sbr][sbc].winner == NO_PLAYER else self.width

		self.passTurn()

		return (True, winner, self.winner)

	def reset(self):
		self.playRow = self.height
		self.playColumn = self.width
		self.winner = NO_PLAYER
		self.currPlayer = PLAYER1
		self.wonBoard1 = 0
		self.wonBoard2 = 0
		self.board = [[SmallBoard(self.height) for i in range(self.width)] for j in range(self.height)]
		self.moveHistory = []

	def undoMove(self):
		if len(self.moveHistory) == 0:
			return

		bbr, bbc, self.playRow, self.playColumn  = self.moveHistory.pop()

		if self.board[bbr][bbc].winner == PLAYER1:
			self.wonBoard1 -= 1
		if self.board[bbr][bbc].winner == PLAYER2:
			self.wonBoard2 -= 1

		sbr, sbc= self.board[bbr][bbc].undoMove()
		self.winner = NO_PLAYER
		self.passTurn()

		return (bbr * self.height + sbr, bbc * self.width + sbc)

	def validMoves(self):
		moves = []

		if self.winner != NO_PLAYER:
			return []

		if self.playRow == self.height and self.playColumn == self.width:
			for i in range(self.height):
				for j in range(self.width):
					moves.extend(self.board[i][j].validMoves(i * self.height, j * self.width))
		elif self.playRow < self.height and self.playColumn < self.width:
			moves.extend(self.board[self.playRow][self.playColumn].validMoves(self.playRow * self.height, self.playColumn * self.width))

		return moves

	def passTurn(self):
		self.currPlayer = PLAYER1 if self.currPlayer == PLAYER2 else PLAYER2

	def checkWin(self, bbr, bbc):
		row = self.checkRow(bbr)
		column = self.checkColumn(bbc)
		diag = self.checkDiag()

		return self.currPlayer if row or column or diag else self.checkFill()

	def checkRow(self, bbr):
		for i in range(self.height):
			if self.board[bbr][i].winner != self.currPlayer:
				return False

		return True

	def checkColumn(self, bbc):
		for i in range(self.height):
			if i >= self.height or bbc >= self.width:
				print('It broke')
				print(i, bbc)
			if self.board[i][bbc].winner != self.currPlayer:
				return False

		return True

	def checkDiag(self):
		if self.height != self.width:
			return False

		diag1 = True
		diag2 = True
		for i in range(self.height):
			if self.board[i][i].winner != self.currPlayer:
				diag1 = False

			if self.board[i][self.height - i - 1].winner != self.currPlayer:
				diag2 = False

		return diag1 or diag2

	def checkFill(self):
		if self.wonBoard1 + self.wonBoard2 != self.height * self.width:
			return NO_PLAYER

		return PLAYER1 if self.wonBoard1 > self.wonBoard2 else PLAYER2