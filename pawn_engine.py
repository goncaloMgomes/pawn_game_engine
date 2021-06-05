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
		bg_gray = "\u001b[48;5;239m"

		print("  ♟ -> BLACK PAWN \n  ♙ -> WHITE PAWN")
		print(tx_cyan + "  0 1 2 3 4 5 6 7" + reset)
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
					tx_color = tx_white
					#if self.board[l,c] == constants.WHITE: tx_color = tx_green
					#if self.board[l,c] == constants.BLACK: tx_color = tx_red
					if(self.board[l,c] != 0):
						pawn = w_pawn if (self.board[l,c] == 2) else b_pawn
						print(bg_gray + tx_color + pawn + " " + reset, end='')
					else:
						print(bg_gray + tx_color + "  " + reset, end='')
				if(c == 7): print(tx_cyan + " " +str(l) + reset)
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
		input_move = input_move.split(",")
		if(len(input_move) != 2):
			return False
		try:
			int(input_move[0])
			int(input_move[1])
		except ValueError:
			return False

		return True


	def run(self):
		legal_move = True
		valid_src = True
		valid_dst = True
		while(self.gameover == 0):
			self.clear()
			self.print_side_to_move()
			self.print_board()
			if(self.colour_to_move == self.human_colour):
				if(not legal_move):
					legal_move = True
					print("Illegal move, try again.")
				if(not valid_src or not valid_dst):
					valid_src = True
					valid_dst = True
					print("Input error, try again.")
				#USER INPUT
				src_square = input("Src square: ")
				valid_src = self.is_input_valid(src_square)
				src_square = src_square.split(",")
				dst_square = input("Dst square: ")
				valid_dst = self.is_input_valid(dst_square)
				dst_square = dst_square.split(",")


				if(valid_src and valid_dst):
					move = Move(int(src_square[0]),int(src_square[1]),int(dst_square[0]),int(dst_square[1]))
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
			self.is_game_over()
			if(self.gameover == constants.WHITE):
				print("Congratulations WHITE wins the game!")
			elif(self.gameover == constants.BLACK):
				print("Congratulations BLACK wins the game!")


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
	board.run()
