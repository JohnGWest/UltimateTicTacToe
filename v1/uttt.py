import tkinter as tk
import random
import uttt_board as ttt

BOARD_HEIGHT = 3
BOARD_WIDTH = BOARD_HEIGHT

BUTTON_HEIGHT = 3
BUTTON_WIDTH = BUTTON_HEIGHT * 2

LINE_THICKNESS = 6

USE_UTILS = False

def main():
	root = tk.Tk()
	root.title('Ultimate Tic Tac Toe')
	root.config(bg='Black')
	root.resizable(False, False)

	gameboard = ttt.BigBoard(BOARD_HEIGHT)
	button_board = [[0 for i in range(BOARD_WIDTH * BOARD_WIDTH)] for j in range(BOARD_HEIGHT * BOARD_HEIGHT)]

	for i in range(BOARD_HEIGHT * BOARD_HEIGHT):
		for j in range(BOARD_WIDTH * BOARD_WIDTH):
			button_board[i][j] = tk.Button(root, height=BUTTON_HEIGHT, width=BUTTON_WIDTH, command=lambda r=i, c=j: button_press(r, c, gameboard, button_board, text))
			button_board[i][j].config(bg='Yellow')
			button_board[i][j].grid(row=i + int(i / BOARD_HEIGHT), column=j + int(j / BOARD_WIDTH))

	c_columns = [0 for i in range(BOARD_WIDTH - 1)]
	for i in range(len(c_columns)):
		c_columns[i] = tk.Canvas(root, height=0, width=LINE_THICKNESS, bd=0, highlightthickness=0, bg='Black')
		c_columns[i].grid(row=0, column=BOARD_WIDTH*(i + 1) + i)
	c_rows = [0 for i in range(BOARD_HEIGHT - 1)]
	for i in range(len(c_columns)):
		c_columns[i] = tk.Canvas(root, height=LINE_THICKNESS, width=0, bd=0, highlightthickness=0, bg='Black')
		c_columns[i].grid(row=BOARD_HEIGHT * (i + 1) + i, column=0)

	text = tk.StringVar()
	text.set('Red turn')
	label = tk.Label(root, textvariable=text)
	label.config(bg='Black', fg='White')
	label.grid(row=BOARD_HEIGHT * BOARD_HEIGHT + BOARD_HEIGHT, column=0, columnspan=BOARD_WIDTH)

	if USE_UTILS:
		utils_panel = tk.Toplevel(root)
		utils_panel.geometry('+800+300')

		random_button = tk.Button(utils_panel, text='Random Play', command=lambda: random_play(gameboard, button_board, text))
		random_button.pack()

		random_game_button = tk.Button(utils_panel, text='Random Game', command=lambda: random_game(gameboard, button_board, text))
		random_game_button.pack()

		reset_button = tk.Button(utils_panel, text='Reset Game', command=lambda: reset(gameboard, button_board, text))
		reset_button.pack()

		undo_button = tk.Button(utils_panel, text='Undo', command=lambda: undo(gameboard, button_board, text))
		undo_button.pack()

	root.mainloop()

def button_press(r, c, gameboard, button_board, text):
	moves = gameboard.validMoves()
	player = gameboard.currPlayer

	success, small_winner, big_winner = gameboard.play(r, c)

	if not success:
		return

	for i, j in moves:
		button_board[i][j].config(bg='White')

	button_board[r][c].config(bg='Red' if player == ttt.PLAYER1 else 'Blue')

	bbr = int(r / BOARD_HEIGHT)
	bbc = int(c / BOARD_WIDTH)
	if small_winner != ttt.NO_PLAYER:
		for i in range(bbr * BOARD_HEIGHT, bbr * BOARD_HEIGHT + BOARD_HEIGHT):
			for j in range(bbc * BOARD_WIDTH, bbc * BOARD_WIDTH + BOARD_WIDTH):
				button_board[i][j].config(bg='Red' if small_winner == ttt.PLAYER1 else 'Blue')

	if big_winner != ttt.NO_PLAYER:
		text.set('{} wins!'.format('Red' if big_winner == ttt.PLAYER1 else 'Blue'))
	else:
		text.set('{} turn'.format('Red' if gameboard.currPlayer == ttt.PLAYER1 else 'Blue'))
		for r, c in gameboard.validMoves():
			button_board[r][c].config(bg='Yellow')

def random_play(gameboard, button_board, text):
	moves = gameboard.validMoves()
	r, c = random.choice(moves)
	button_press(r, c, gameboard, button_board, text)

def random_game(gameboard, button_board, text):
	if gameboard.winner != ttt.NO_PLAYER:
		reset(gameboard, button_board, text)

	while gameboard.winner == ttt.NO_PLAYER:
		random_play(gameboard, button_board, text)

def reset(gameboard, button_board, text):
	gameboard.reset()
	for i in range(BOARD_HEIGHT * BOARD_HEIGHT):
		for j in range(BOARD_WIDTH * BOARD_WIDTH):
			button_board[i][j].config(bg='Yellow')
	
	text.set('Red turn')

def undo(gameboard, button_board, text):
	if len(gameboard.moveHistory) == 0:
		return

	for r, c in gameboard.validMoves():
		button_board[r][c].config(bg='White')

	r, c = gameboard.undoMove()

	bbr = int(r / BOARD_HEIGHT)
	bbc = int(c / BOARD_WIDTH)

	for i in range(BOARD_HEIGHT):
		for j in range(BOARD_WIDTH):
			if gameboard.board[bbr][bbc].board[i][j] == ttt.NO_PLAYER:
				button_board[bbr * BOARD_HEIGHT + i][bbc * BOARD_WIDTH + j].config(bg='White')
			elif gameboard.board[bbr][bbc].board[i][j] == ttt.PLAYER1:
				button_board[bbr * BOARD_HEIGHT + i][bbc * BOARD_WIDTH + j].config(bg='Red')
			elif gameboard.board[bbr][bbc].board[i][j] == ttt.PLAYER2:
				button_board[bbr * BOARD_HEIGHT + i][bbc * BOARD_WIDTH + j].config(bg='Blue')

	button_board[r][c].config(bg='White')
	text.set('Red turn' if gameboard.currPlayer == ttt.PLAYER1 else 'Blue turn')
	
	for r, c in gameboard.validMoves():
		button_board[r][c].config(bg='Yellow')

main()