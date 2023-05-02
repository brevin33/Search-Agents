import random
class Tetris:
	#moves by block then by rotation
	#allowedMoves["I"][90] gives (0,6) a tuple for the allowed range of x
	#if the range is (0,0) it is the same as a prior rotation
	allowedMoves = {"I": {0: (0,9), 90: (0,6), 180: (-1,-1), 270: (-1,-1)}, "L": {0: (0,7), 90: (0,8), 180: (0,7), 270: (1,9)}, "J": {0: (0,7), 90: (1,9), 180: (0,7), 270: (0,8)}, "S": {0: (1,9), 90: (0,7), 180: (-1,-1), 270: (-1,-1)}, "Z": {0: (0,8), 90: (2,9), 180: (-1,-1), 270: (-1,-1)}, "T": {0: (0,7), 90: (0,8), 180: (1,8), 270: (1,9)}, "O": {0: (0,8), 90: (-1,-1), 180: (-1,-1), 270: (-1,-1)}}
	def __init__(self,visibleBlocks):
		self.board = []
		self.blocks = []
		self.blockNames = ["L","T","I","J","O","S","Z"]
		self.alteredRows = []
		self.score = 0
		self.done = False
		for i in range(20):
			self.board.append([0,0,0,0,0,0,0,0,0,0]);
		for i in range(visibleBlocks):
			r = random.randrange(7)
			self.blocks.append(self.blockNames[r]);

	def generateBlock(self):
		self.blocks.append(self.blockNames[random.randrange(7)]);

	def GameOver(self):
		self.done = True;

	def dropAtLocation(self,x,rotation):
		block = self.blocks[0]
		if block == "L":
			self.dropL(x,rotation)
		elif block == "T":
			self.dropT(x,rotation)
		elif block == "I":
			self.dropI(x,rotation)
		elif block == "J":
			self.dropJ(x,rotation)
		elif block == "O":
			self.dropO(x,rotation)
		elif block == "S":
			self.dropS(x,rotation)
		elif block == "Z":
			self.dropZ(x,rotation)


	def update_board(self):
		self.blocks.pop(0)
		rowscleared = 0
		for index in self.alteredRows:
			clearedRow = True
			for block in self.board[index]:
				if block == 0:
					clearedRow = False
			if clearedRow == True:
				del self.board[index]
				self.board.append([0,0,0,0,0,0,0,0,0,0]);
				rowscleared += 1
		self.alteredRows = []
		#self.drawboard()
		if rowscleared == 1:
			self.score += 100
		elif rowscleared == 2:
			self.score += 300
		elif rowscleared == 3:
			self.score += 500
		elif rowscleared == 4:
			self.score += 800

	def drawboard(self):
		for index in [19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]:
			for spot in self.board[index]:
				if spot == 0:
					print("-",end="")
				else:
					print("x",end="")
			print("");
		print("_____________________________");

	#"I": {0: (0,9), 90: (0,6), 180: (0,9), 270: (0,6)}
	def dropI(self,x,rotation):
		positionY = 19 # postion to place new block at
		while positionY >= 0: # finding positionY
			if self.board[positionY][x] != 0:
				break
			if rotation == 90 or rotation == 270:
				if self.board[positionY][x+1] != 0 or self.board[positionY][x+2] != 0 or self.board[positionY][x+3] != 0:
					break
			positionY -= 1
		positionY += 1
		# Placing Piece
		if rotation == 90 or rotation == 270:
			if (positionY + 0) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY][x+1] = 1;
			self.board[positionY][x+2] = 1;
			self.board[positionY][x+3] = 1;
			self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		else:
			if (positionY + 3) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY+1][x] = 1;
			self.board[positionY+2][x] = 1;
			self.board[positionY+3][x] = 1;
			self.alteredRows.append(positionY+3) #alteredRows must be put in highest index first
			self.alteredRows.append(positionY+2)
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY+0)
		self.update_board()
		return

	#"L": {0: (0,7), 90: (0,8), 180: (0,7), 270: (1,9)}
	def dropL(self,x,rotation):
		positionY = 19 # postion to place new block at
		while positionY >= 0: # finding positionY
			if self.board[positionY][x] != 0:
				break
			if rotation == 0:
				if positionY != 0 and self.board[positionY-1][x] != 0 or self.board[positionY][x+1] != 0 or self.board[positionY][x+2] != 0:
					break
			elif rotation == 90:
				if self.board[positionY][x+1] != 0:
					break
			elif rotation == 180:
				if self.board[positionY][x+1] != 0 or self.board[positionY][x+2] != 0:
					break
			elif rotation == 270:
				if positionY+2 <= 19 and self.board[positionY+2][x-1] != 0:
					break
			positionY -= 1
		positionY += 1
		# Placing Piece
		if rotation == 0:
			if positionY == 0:
				positionY = 1
			if (positionY + 0) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY][x+1] = 1;
			self.board[positionY][x+2] = 1;
			self.board[positionY-1][x] = 1;
			self.alteredRows.append(positionY);
			self.alteredRows.append(positionY - 1); #alteredRows must be put in highest index first
				# Placing Piece
		elif rotation == 90:
			if (positionY + 2) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY][x+1] = 1;
			self.board[positionY+1][x] = 1;
			self.board[positionY+2][x] = 1;
			self.alteredRows.append(positionY+2)
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		elif rotation == 180:
			if (positionY + 1) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY][x+1] = 1;
			self.board[positionY][x+2] = 1;
			self.board[positionY+1][x+2] = 1;
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		else:
			if (positionY + 2) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY+1][x] = 1;
			self.board[positionY+2][x] = 1;
			self.board[positionY+2][x-1] = 1;
			self.alteredRows.append(positionY+2)
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY+0)
		self.update_board()
		return

	#"J": {0: (0,7), 90: (1,9), 180: (0,7), 270: (0,8)}
	def dropJ(self,x,rotation):
		positionY = 19 # postion to place new block at
		while positionY >= 0: # finding positionY
			if self.board[positionY][x] != 0:
				break
			if rotation == 0:
				if self.board[positionY-1][x+2] != 0 or self.board[positionY][x+1] != 0 or self.board[positionY][x+2] != 0:
					break
			elif rotation == 90:
				if self.board[positionY][x-1] != 0:
					break
			elif rotation == 180:
				if self.board[positionY][x+1] != 0 or self.board[positionY][x+2] != 0:
					break
			elif rotation == 270:
				if positionY+2 <= 19 and self.board[positionY+2][x+1] != 0:
					break
			positionY -= 1
		positionY += 1
		# Placing Piece
		if rotation == 0:
			if positionY == 0:
				positionY = 1
			if (positionY + 0) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY][x+1] = 1;
			self.board[positionY][x+2] = 1;
			self.board[positionY-1][x+2] = 1;
			self.alteredRows.append(positionY);
			self.alteredRows.append(positionY - 1); #alteredRows must be put in highest index first
				# Placing Piece
		elif rotation == 90:
			if (positionY + 2) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY][x-1] = 1;
			self.board[positionY+1][x] = 1;
			self.board[positionY+2][x] = 1;
			self.alteredRows.append(positionY+2)
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		elif rotation == 180:
			if (positionY + 1) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY][x+1] = 1;
			self.board[positionY][x+2] = 1;
			self.board[positionY+1][x] = 1;
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		else:
			if (positionY + 2) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY+1][x] = 1;
			self.board[positionY+2][x] = 1;
			self.board[positionY+2][x+1] = 1;
			self.alteredRows.append(positionY+2)
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY+0)
		self.update_board()
		return

	#"S": {0: (1,9), 90: (0,7), 180: (1,9), 270: (0,7)}
	def dropS(self,x,rotation):
		positionY = 19 # postion to place new block at
		while positionY >= 0: # finding positionY
			if self.board[positionY][x] != 0:
				break
			if rotation == 90 or rotation == 270:
				if self.board[positionY][x+1] != 0 or (positionY <= 18 and self.board[positionY+1][x+2] != 0):
					break
			else:
				if positionY <= 18 and self.board[positionY+1][x-1] != 0:
					break
			positionY -= 1
		positionY += 1
		# Placing Piece
		if rotation == 90 or rotation == 270:
			if (positionY + 1) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY][x+1] = 1;
			self.board[positionY+1][x+1] = 1;
			self.board[positionY+1][x+2] = 1;
			self.alteredRows.append(positionY+1);
			self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		else:
			if (positionY + 3) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY+1][x] = 1;
			self.board[positionY+1][x-1] = 1;
			self.board[positionY+2][x-1] = 1;
			self.alteredRows.append(positionY+2)
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY+0)
		self.update_board()
		return

	#"Z": {0: (0,8), 90: (2,9), 180: (0,8), 270: (2,9)}
	def dropZ(self,x,rotation):
		positionY = 19 # postion to place new block at
		while positionY >= 0: # finding positionY
			if self.board[positionY][x] != 0:
				break
			if rotation == 90 or rotation == 270:
				if self.board[positionY][x-1] != 0 or (positionY <= 18 and self.board[positionY+1][x-2] != 0):
					break
			else:
				if positionY <= 18 and self.board[positionY+1][x+1] != 0:
					break
			positionY -= 1
		positionY += 1
		# Placing Piece
		if rotation == 90 or rotation == 270:
			if (positionY + 1) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY][x-1] = 1;
			self.board[positionY+1][x-1] = 1;
			self.board[positionY+1][x-2] = 1;
			self.alteredRows.append(positionY+1);
			self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		else:
			if (positionY + 3) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY+1][x] = 1;
			self.board[positionY+1][x+1] = 1;
			self.board[positionY+2][x+1] = 1;
			self.alteredRows.append(positionY+2)
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY+0)
		self.update_board()
		return

	#"T": {0: (0,7), 90: (0,8), 180: (1,8), 270: (1,9)}
	def dropT(self,x,rotation):
		positionY = 19 # postion to place new block at
		while positionY >= 0: # finding positionY
			if self.board[positionY][x] != 0:
				break
			if rotation == 0:
				if self.board[positionY][x+1] != 0 or self.board[positionY][x+2] != 0:
					break
			elif rotation == 90:
				if positionY <= 18 and self.board[positionY+1][x+1] != 0:
					break
			elif rotation == 180:
				if positionY <= 18 and (self.board[positionY+1][x+1] != 0 or self.board[positionY+1][x-1] != 0):
					break
			elif rotation == 270:
				if positionY <= 18 and self.board[positionY+1][x-1] != 0:
					break
			positionY -= 1
		positionY += 1
		# Placing Piece
		if rotation == 0:
			if (positionY + 1) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY][x+1] = 1;
			self.board[positionY][x+2] = 1;
			self.board[positionY+1][x+1] = 1;
			self.alteredRows.append(positionY);
			self.alteredRows.append(positionY - 1); #alteredRows must be put in highest index first
				# Placing Piece
		elif rotation == 90:
			if (positionY + 2) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY+1][x+1] = 1;
			self.board[positionY+1][x] = 1;
			self.board[positionY+2][x] = 1;
			self.alteredRows.append(positionY+2)
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		elif rotation == 180:
			if (positionY + 1) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY+1][x] = 1;
			self.board[positionY+1][x+1] = 1;
			self.board[positionY+1][x-1] = 1;
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		else:
			if (positionY + 2) >= 20:
				self.GameOver()
				return
			self.board[positionY][x] = 1;
			self.board[positionY+1][x-1] = 1;
			self.board[positionY+1][x] = 1;
			self.board[positionY+2][x] = 1;
			self.alteredRows.append(positionY+2)
			self.alteredRows.append(positionY+1)
			self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		self.update_board()
		return


	#"O": {0: (0,8), 90: (0,8), 180: (0,8), 270: (0,8)}
	def dropO(self,x,rotation):
		positionY = 19 # postion to place new block at
		while positionY >= 0: # finding positionY
			if self.board[positionY][x] != 0 or self.board[positionY][x+1] != 0:
				break
			positionY -= 1
		positionY += 1
		# Placing Piece
		if (positionY + 1) >= 20:
			self.GameOver()
			return
		self.board[positionY][x] = 1;
		self.board[positionY][x+1] = 1;
		self.board[positionY+1][x+1] = 1;
		self.board[positionY+1][x] = 1;
		self.alteredRows.append(positionY+1); #alteredRows must be put in highest index first
		self.alteredRows.append(positionY); #alteredRows must be put in highest index first
		self.update_board()
		return
