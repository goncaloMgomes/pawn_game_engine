import numpy as np
import constants
from collections import namedtuple
import os
import math
from time import sleep

Move = namedtuple('Move', ['src_l','src_c','dst_l','dst_c'])

class Board:
	def __init__(self):
		self.board = np.zeros((8,8),dtype=int)

		self.colour_to_move = constants.WHITE

		self.gameover = 0 #0 means that no one has yet won the game
		self.last_move = Move(None,None,None,None)
		self.engine_colour = constants.BLACK
		self.human_colour = constants.WHITE
		self.search_depth = 5
		self.init_board()
		self.label_to_coordinate= {
			"a8":( 0,0 ), "b8":( 0,1 ), "c8":( 0,2 ), "d8":( 0,3 ), "e8":( 0,4 ), "f8":( 0,5 ),"g8":( 0,6 ), "h8":( 0,7 ),
			"a7":( 1,0 ), "b7":( 1,1 ), "c7":( 1,2 ), "d7":( 1,3 ), "e7":( 1,4 ), "f7":( 1,5 ),"g7":( 1,6 ), "h7":( 1,7 ),
			"a6":( 2,0 ), "b6":( 2,1 ), "c6":( 2,2 ), "d6":( 2,3 ), "e6":( 2,4 ), "f6":( 2,5 ),"g6":( 2,6 ), "h6":( 2,7 ),
			"a5":( 3,0 ), "b5":( 3,1 ), "c5":( 3,2 ), "d5":( 3,3 ), "e5":( 3,4 ), "f5":( 3,5 ),"g5":( 3,6 ), "h5":( 3,7 ),
			"a4":( 4,0 ), "b4":( 4,1 ), "c4":( 4,2 ), "d4":( 4,3 ), "e4":( 4,4 ), "f4":( 4,5 ),"g4":( 4,6 ), "h4":( 4,7 ),
			"a3":( 5,0 ), "b3":( 5,1 ), "c3":( 5,2 ), "d3":( 5,3 ), "e3":( 5,4 ), "f3":( 5,5 ),"g3":( 5,6 ), "h3":( 5,7 ),
			"a2":( 6,0 ), "b2":( 6,1 ), "c2":( 6,2 ), "d2":( 6,3 ), "e2":( 6,4 ), "f2":( 6,5 ),"g2":( 6,6 ), "h2":( 6,7 ),
			"a1":( 7,0 ), "b1":( 7,1 ), "c1":( 7,2 ), "d1":( 7,3 ), "e1":( 7,4 ), "f1":( 7,5 ),"g1":( 7,6 ), "h1":( 7,7 )
			}


	def init_board(self):

		#black_pawn = 1 -> BLACK
		#white_pawn = 2 -> WHITE
		for c in range(8):
			self.board[6,c] = constants.WHITE
			self.board[1,c] = constants.BLACK


	def print_board(self):

		bg_white = "\u001b[47m"
		tx_black = "\u001b[30m"
		tx_white = "\u001b[37m"
		tx_green = "\u001b[32m"
		tx_red = "\u001b[31m"
		tx_cyan = "\u001b[36;1m"
		reset = "\u001b[0m"
		w_pawn = "♙"
		b_pawn = "♟"
		bg_gray = "\u001b[48;5;240m"

		print("  ♟ -> BLACK PAWN \n  ♙ -> WHITE PAWN\n\n")
		for l in range(8):
			print(str(8-l)+" ",end='')
			for c in range(8):
				if(((c % 2 == 0) and (l % 2 == 0)) or (c % 2 != 0) and (l % 2 != 0)): #white square
					tx_color = tx_black
					#if self.board[l,c] == constants.WHITE: tx_color = tx_green
					#if self.board[l,c] == constants.BLACK: tx_color = tx_red
					if(self.board[l,c] != 0):
						pawn = w_pawn if self.board[l,c] == 2 else b_pawn
						print(bg_white  + tx_color + pawn + " " + reset , end='')
					else:
						print(bg_white  + tx_color + "  " + reset, end='')
				else:#black square
					tx_color = tx_black
					#if self.board[l,c] == constants.WHITE: tx_color = tx_green
					#if self.board[l,c] == constants.BLACK: tx_color = tx_red
					if(self.board[l,c] != 0):
						pawn = w_pawn if (self.board[l,c] == 2) else b_pawn
						print(bg_gray + tx_color + pawn + " " + reset, end='')
					else:
						print(bg_gray + tx_color + "  " + reset, end='')
				if(c == 7): print()
			if(l == 7):
				print("  a b c d e f g h")



	def print_side_to_move(self):

		print("WHITE TO MOVE" if self.colour_to_move == constants.WHITE else "BLACK TO MOVE")


	def get_moves(self,board,side_to_move,last_move):

		moves = []
		for l in range(8):
			for c in range(8):
				piece = board[l,c]
				if(piece == side_to_move and piece == constants.WHITE):
					#WHITE moves in the direction where l reduces value
					if(l == 6):#first position for WHITE
						if(board[l-2,c] == 0): #empty square
							moves.append(Move(l,c,l-2,c))
					if(self.last_move.src_l == 1 and last_move.dst_l == 3 and l == 3):#en passant available
						if(c == last_move.dst_c - 1):
							moves.append(Move(l,c,l-1,c+1))
						if(c == last_move.dst_c + 1):
							moves.append(Move(l,c,l-1,c-1))
					if(l >= 1):
						if(board[l-1,c] == 0): #empty square
							moves.append(Move(l,c,l-1,c))
						if(c >= 1):
							if(board[l-1,c-1] == constants.BLACK): #square with a BLACK pawn
								moves.append(Move(l,c,l-1,c-1))
						if(c <= 6):
							if(board[l-1,c+1] == constants.BLACK): #square with a BLACK pawn
								moves.append(Move(l,c,l-1,c+1))
				elif(piece == side_to_move and piece == constants.BLACK):
					#BLACK moves in the direction where l increases value
					if(l == 1):#first position for BLACK
						if(board[l+2,c] == 0): #empty square
							moves.append(Move(l,c,l+2,c))
					if(last_move.src_l == 6 and last_move.dst_l == 4 and l == 4):#en passant available
						if(c == last_move.dst_c - 1):
							moves.append(Move(l,c,l+1,c+1))
						if(c == last_move.dst_c + 1):
							moves.append(Move(l,c,l+1,c-1))
					if(l <= 6):
						if(board[l+1,c] == 0): #empty square
							moves.append(Move(l,c,l+1,c))
						if(c >= 1):
							if(board[l+1,c-1] == constants.WHITE): #square with a BLACK pawn
								moves.append(Move(l,c,l+1,c-1))
						if(c <= 6):
							if(board[l+1,c+1] == constants.WHITE): #square with a BLACK pawn
								moves.append(Move(l,c,l+1,c+1))
		return moves


	def determine_board_position(self):

		board_position = ""
		if(self.colour_to_move == constants.BLACK):
			board_position  = "B:"
		else:
			board_position  = "W:"

		board_position += "W"
		for l in range(8):
			for c in range(8):
				piece = self.board[l,c]
				if(piece == constants.WHITE):
					board_position += self.get_label_from_coordinates((l,c)) + ','

		board_position = board_position[:-1]
		board_position += ":B"
		for l in range(8):
			for c in range(8):
				piece = self.board[l,c]
				if(piece == constants.BLACK):
					board_position += self.get_label_from_coordinates((l,c)) + ','
		board_position = board_position[:-1]
		board_position += '.'

		return board_position


	def do_move(self,move):

		moves = self.get_moves(self.board,self.colour_to_move,self.last_move)
		if(move in moves):
			#if there is a change in columns and the destiny square is empty
			#then a move en passant was performed and it is needed to remove the eaten piece from the square
			if(move.dst_c != move.src_c and self.board[move.dst_l,move.dst_c] == 0):
				# remove eaten  piece
				self.board[move.src_l,move.dst_c] = 0
			# move piece to new square
			self.board[move.dst_l,move.dst_c] = self.board[move.src_l,move.src_c]
			# remove piece from origin square
			self.board[move.src_l,move.src_c] = 0
			# toggle player to move
			self.colour_to_move = constants.WHITE if self.colour_to_move == constants.BLACK else constants.BLACK
			#return True if the move is legal
			return True
		else:
			return False

	def do_cmove(self,move):

		if(move.dst_c != move.src_c and self.board[move.dst_l,move.dst_c] == 0):
			# remove eaten  piece
			self.board[move.src_l,move.dst_c] = 0
		# move piece to new square
		self.board[move.dst_l,move.dst_c] = self.board[move.src_l,move.src_c]
		# remove piece from origin square
		self.board[move.src_l,move.src_c] = 0
		# toggle player to move
		self.colour_to_move = constants.WHITE if self.colour_to_move == constants.BLACK else constants.BLACK

	def clear(self):

		os.system('cls' if os.name=='nt' else 'clear')

	def is_input_valid(self,input_move):

		return (input_move in self.label_to_coordinate.keys())


	def get_coordinates_from_label(self,input_move):

		return self.label_to_coordinate[input_move]


	def get_label_from_coordinates(self,label):

		return list(self.label_to_coordinate.keys())[list(self.label_to_coordinate.values()).index(label)]

	def set_players_colours(self):

		colours = {
			'1': constants.BLACK,
			'2': constants.WHITE,
			'default': constants.WHITE
		}
		print("Human plays with the colour: ")
		print("[1]-Black")
		print("[2]-White")
		option = str(input("Option: "))
		colour = colours.get(option,colours.get('default'))
		self.clear()
		print("The human plays with the colour %s." % ("white" if colour == constants.WHITE else "black"))
		self.human_colour = colour
		self.engine_colour = constants.WHITE if self.human_colour == constants.BLACK else constants.BLACK


	def set_starting_player(self):

		starting_players = {
			'1': "human",
			'2': "computer",
			'default': "human"
		}
		print("Choose the starting player:")
		print("[1]-Human")
		print("[2]-Computer")
		option = str(input("Option: "))
		starting_player = starting_players.get(option,starting_players.get('default'))
		self.clear()
		print("The starting player is %s." % (starting_player))
		self.colour_to_move = self.human_colour if starting_player == "human" else self.engine_colour



	def set_board_position(self):
		board_position = self.determine_board_position()
		board_position = str(input("Board position: "))
		if(len(board_position) > 0):
			self.board = np.zeros((8,8),dtype=int)
			if(board_position[0] == "B"):
				self.colour_to_move = constants.BLACK
			if(board_position[0] == "W"):
				self.colour_to_move = constants.WHITE
			slices = board_position.split(":")
			if(len(slices) == 3):
				if(slices[1][0] == "W"):
					aux = slices[1][1:]
					white_pieces = aux.split(',')
					aux = slices[2][1:-1]
					black_pieces = aux.split(',')
				elif(slices[1][0] == "B"):
					aux = slices[1][1:]
					black_pieces = aux.split(',')
					aux = slices[2][1:-1]
					white_pieces = aux.split(',')
				if(len(white_pieces) > 0 and len(black_pieces) > 0):
					for piece in white_pieces:
						(l,c) = self.get_coordinates_from_label(piece)
						self.board[l,c] = constants.WHITE
					for piece in black_pieces:
						(l,c) = self.get_coordinates_from_label(piece)
						self.board[l,c] = constants.BLACK






	def print_board_position(self):

		print(self.determine_board_position())



	def print_invalid(self):

		print("Invalid option, please try again!")



	def menu(self):
		print("      ♟♟♟   PAWN GAME   ♙♙♙\n")
		print("[1] - Select human colour  - (%s)" % ("white" if self.human_colour == constants.WHITE else "black"))
		print("[2] - Set board position   -")
		print("[3] - Get board position   -")
		print("[4] - Set starting player  - (%s)" % ("human" if self.colour_to_move == self.human_colour else "computer"))
		print("[5] - Start game           -")


	def run_menu(self):
		menu_functions = {
			1: self.set_players_colours,
			2: self.set_board_position,
			3: self.print_board_position,
			4: self.set_starting_player,
			5: self.run_game,
			'default':self.print_invalid
		}
		self.clear()
		while(True):
			self.menu()
			option = int(input("Option: "))
			self.clear()
			menu_functions.get(option,menu_functions.get('default'))()


	def run_game(self):

		tx_green = "\u001b[32m"
		tx_cyan = "\u001b[36;1m"
		reset = "\u001b[0m"
		legal_move = True
		valid_src = True
		valid_dst = True
		if(self.gameover != 0):
			print("Game already won, to play again please set the board again.")

		while(self.gameover == 0):
			try:
				self.clear()
				self.is_game_over()
				if(self.gameover == constants.WHITE):
					print("Congratulations WHITE wins the game!")
				elif(self.gameover == constants.BLACK):
					print("Congratulations BLACK wins the game!")
				if(self.gameover == 0):
					self.print_side_to_move()
				self.print_board()
				if(self.gameover == 0):
					if(self.colour_to_move == self.human_colour):
						if(not legal_move):
							legal_move = True
							print("Illegal move, try again.")
						if(not valid_src or not valid_dst):
							valid_src = True
							valid_dst = True
							print("Input error, try again.")
						#USER INPUT
						print("\n\nUsage: letter followed by row number.Ex: a1")
						src_label = input("Src square: ")
						valid_src = self.is_input_valid(src_label)
						dst_label = input("Dst square: ")
						valid_dst = self.is_input_valid(dst_label)

						if(valid_src and valid_dst):
							src_square = self.get_coordinates_from_label(src_label)
							dst_square = self.get_coordinates_from_label(dst_label)

							move = Move(src_square[0],src_square[1],dst_square[0],dst_square[1])
							legal_move = self.do_move(move)
							if(legal_move):
								self.last_move = move
					else:
						print("Computer thinking....")
						#sleep(1)
						cmove = self.get_cmove()
						self.do_cmove(cmove)
						self.last_move = cmove
						#print(self.get_hmove())#human hint move
			except KeyboardInterrupt:
				self.clear()
				break



	#Function to determine if the current game has finished
	def is_game_over(self):

		if(self.colour_to_move == self.engine_colour):
			moves = self.get_moves(self.board,self.engine_colour,self.last_move)
			if(len(moves) == 0):
				self.gameover = self.human_colour
		else:
			moves = self.get_moves(self.board,self.human_colour,self.last_move)
			if(len(moves) == 0):
				self.gameover = self.engine_colour
		for c in range(8):
			#WHITE wins when a white pawn gets to the row 0
			if(self.colour_to_move == constants.BLACK):
				if(self.board[0,c] == constants.WHITE):
					self.gameover = constants.WHITE
					break
			#BLACK wins when a black pawn gets to the row 7
			else:
				if(self.board[7,c] == constants.BLACK):
					self.gameover = constants.BLACK
					break
	#Function to determine if a child in minimax has reached a game over position
	def is_game_over_in_position(self,position,maximizingPlayer,last_move):

		if(maximizingPlayer):
			moves = self.get_moves(position,self.engine_colour,last_move)
			if(len(moves) == 0):
				return self.human_colour
		else:
			moves = self.get_moves(position,self.human_colour,last_move)
			if(len(moves) == 0):
				return self.engine_colour
		#If there are moves to be made we have to check then if a piece has reached the other side
		#This function follows the same logic of is_game_over()
		for c in range(8):
			#if maximizingPlayer is the current player to play we need to check if the
			#minimizingPlayer won in the last state before proceeding
			#WHITE wins when a white pawn gets to the row 0
			if(maximizingPlayer):
				if(position[0,c] == constants.WHITE):
					return constants.WHITE
			#BLACK wins when a black pawn gets to the row 7
			else:
				if(position[7,c] == constants.BLACK):
					return constants.BLACK
		return 0

	def get_static_evaluation_of_position(self,position,maximizingPlayer,last_move):

		#each pawn has a value of 1, all pawns are the same
		#a win has a value of 100 a loss -100
		evaluation = 0
		winner = self.is_game_over_in_position(position,maximizingPlayer,last_move)
		if(winner == self.engine_colour):
			evaluation = 100
			return evaluation
		elif(winner == self.human_colour):
			evaluation = -100
			return evaluation
		for l in range(8):
			for c in range(8):
				if(position[l,c] == self.engine_colour):
					evaluation += 1
				if(position[l,c] == self.human_colour):
					evaluation -= 1
		return evaluation

	def get_child_positions(self,position,side_to_move,last_move):

		positions = []
		moves = self.get_moves(position,side_to_move,last_move)
		for move in moves:
			child = np.copy(position)
			if(move.dst_c != move.src_c and child[move.dst_l,move.dst_c] == 0):
				child[move.src_l,move.dst_c] = 0
			# move piece to new square
			child[move.dst_l,move.dst_c] = child[move.src_l,move.src_c]
			# remove piece from origin square
			child[move.src_l,move.src_c] = 0
			positions.append((child,move))
		return positions




	def minimax(self, position, last_move, depth, alpha, beta, maximizingPlayer):

		best_move = Move(None,None,None,None)
		is_game_over = self.is_game_over_in_position(position,maximizingPlayer,last_move)
		if((depth == 0) or (is_game_over != 0)):
			eval = self.get_static_evaluation_of_position(position,maximizingPlayer,last_move)
			if(is_game_over == self.engine_colour):
				eval += depth #the higher the depth the less moves it is required to achieve a good position
			elif(is_game_over == self.engine_colour):
				eval -= depth
			return eval,best_move

		if(maximizingPlayer):
			child_positions = self.get_child_positions(position,self.engine_colour,last_move)
			#print(child_positions)
			maxEval = -math.inf
			for child in child_positions:
				eval,_ = self.minimax(child[0],child[1], depth - 1, alpha, beta, False)
				if(eval > maxEval):
					maxEval = eval
					best_move = child[1]
				alpha = max(alpha, eval)
				if (beta <= alpha):
					break
			return maxEval,best_move
		else:
			child_positions = self.get_child_positions(position,self.human_colour,last_move)
			minEval = math.inf
			for child in child_positions:
				eval,_ = self.minimax(child[0],child[1], depth - 1, alpha, beta, True)
				#minEval = min(eval,minEval)
				if(eval < minEval):
					minEval = eval
					best_move = child[1]
				beta = min(beta, eval)
				if (beta <= alpha):
					break
			return minEval,best_move


	def get_cmove(self):

		_,best_move = self.minimax(self.board,self.last_move, self.search_depth, -math.inf, math.inf, True)
		return best_move


	def get_hmove(self):

		_,best_move = self.minimax(self.board,self.last_move, self.search_depth, -math.inf, math.inf, False)
		return best_move

if __name__ == "__main__":
	board = Board()
	board.run_menu()
