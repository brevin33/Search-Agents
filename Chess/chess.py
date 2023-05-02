import copy


# this game is not exactly the same as chess differences below 
#
# game allows castling even if king has moved as long as in original position
# game does not allow en passant
# pawns only promote into queens
class Chess:

	def __init__(self):
		self.board = [["rb","kb","bb","qb","Kb","bb","kb","rb"],["pb","pb","pb","pb","pb","pb","pb","pb"],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],["pw","pw","pw","pw","pw","pw","pw","pw"],["rw","kw","bw","qw","Kw","bw","kw","rw"]]
		self.legalMoves = {"w": [], "b": []}
		self.color = "w"
		self.check = {"w": False , "b": False}
		self.king = {"w": (4,7) , "b": (4,0)}
		self.done = False
		self.updatePotentialMoves()
		self.validateMoves()

	def getLegalActions():
		return self.legalMoves[self.color]

	def movePeice(self,move):
		self.legalMoves["w"] = []
		self.legalMoves["b"] = []
		if move == "castleKw":
			self.board[7][4] = 0
			self.board[7][7] = 0
			self.board[7][5] = "rw"
			self.board[7][6] = "Kw"
		elif move == "castleKb":
			self.board[0][4] = 0
			self.board[0][7] = 0
			self.board[0][5] = "rb"
			self.board[0][6] = "Kb"
		elif move == "castleqw":
			self.board[7][4] = 0
			self.board[7][0] = 0
			self.board[7][3] = "rw"
			self.board[7][2] = "Kw"
		elif move == "castleqb":
			self.board[0][4] = 0
			self.board[0][0] = 0
			self.board[0][3] = "rb"
			self.board[0][2] = "Kb"
		else:
			if self.board[move[1]][move[0]] == "Kw":
				self.king["w"] = (move[2],move[3])
			if self.board[move[1]][move[0]] == "Kb":
				self.king["b"] = (move[2],move[3])
			self.board[move[3]][move[2]] = self.board[move[1]][move[0]]
			self.board[move[1]][move[0]] = 0
		self.promotePawns()
		self.updatePotentialMoves()
		self.findChecksW()
		self.findChecksB()
		self.validateMoves()

		if self.color == "w":
			self.color = "b"
		else:
			self.color = "w"
		self.validateMoves()
		if len(self.legalMoves[self.color]) == 0 and self.check[self.color]:
			if self.color == "w":
				self.done = "b"
			else:
				self.done = "w"
		elif len(self.legalMoves[self.color]) == 0:
			self.done = "draw"
		return True

	def printBoard(self):
		for row in self.board:
			for p in row:
				if p == 0:
					p = "--"
				print(p + " ",end="")
			print("")
		print("")

	def updatePotentialMoves(self):
		self.legalMoves["w"] = []
		self.legalMoves["b"] = []
		for y in range(len(self.board)):
			for x in range(len(self.board[y])):
				peice = self.board[y][x]
				if peice == "rb":
					self.addRookMoves(x,y,"b")
				elif peice == "kb":
					self.addKnightMoves(x,y,"b")
				elif peice == "bb":
					self.addBishopMoves(x,y,"b")
				elif peice == "qb":
					self.addRookMoves(x,y,"b")
					self.addBishopMoves(x,y,"b")
				elif peice == "Kb":
					self.addKingMoves(x,y,"b")
					self.king["b"] = (x,y)
				elif peice == "pb":
					self.addPawnMoves(x,y,"b")
				elif peice == "rw":
					self.addRookMoves(x,y,"w")
				elif peice == "kw":
					self.addKnightMoves(x,y,"w")
				elif peice == "bw":
					self.addBishopMoves(x,y,"w")
				elif peice == "qw":
					self.addRookMoves(x,y,"w")
					self.addBishopMoves(x,y,"w")
				elif peice == "Kw":
					self.addKingMoves(x,y,"w")
					self.king["w"] = (x,y)
				elif peice == "pw":
					self.addPawnMoves(x,y,"w")

	def validateMoves(self):
		i = 0
		moveLoopLength = len(self.legalMoves[self.color])
		while i < moveLoopLength:
			move = self.legalMoves[self.color][i]
			oldboard = copy.deepcopy(self.board)
			oldmoves = copy.deepcopy(self.legalMoves)
			oldking = copy.deepcopy(self.king)	
			oldcheck = copy.deepcopy(self.check)
			if move == "castleKw":
				self.board[7][4] = 0
				self.board[7][7] = 0
				self.board[7][5] = "rw"
				self.board[7][6] = "Kw"
			elif move == "castleKb":
				self.board[0][4] = 0
				self.board[0][7] = 0
				self.board[0][5] = "rb"
				self.board[0][6] = "Kb"
			elif move == "castleqw":
				self.board[7][4] = 0
				self.board[7][0] = 0
				self.board[7][3] = "rw"
				self.board[7][2] = "Kw"
			elif move == "castleqb":
				self.board[0][4] = 0
				self.board[0][0] = 0
				self.board[0][3] = "rb"
				self.board[0][2] = "Kb"
			else:
				if self.board[move[1]][move[0]] == "Kw":
					self.king["w"] = (move[2],move[3])
				elif self.board[move[1]][move[0]] == "Kb":
					self.king["b"] = (move[2],move[3])
				self.board[move[3]][move[2]] = self.board[move[1]][move[0]]
				self.board[move[1]][move[0]] = 0
			if self.color == "w":
				self.findChecksW()
			else:
				self.findChecksB()
			if self.check[self.color]:
				self.board = copy.deepcopy(oldboard)
				self.check = copy.deepcopy(oldcheck)
				self.legalMoves = copy.deepcopy(oldmoves)
				self.king = copy.deepcopy(oldking)
				del self.legalMoves[self.color][i]
				i -= 1
				moveLoopLength -= 1
			else:
				self.check = copy.deepcopy(oldcheck)
				self.board = copy.deepcopy(oldboard)
				self.legalMoves = copy.deepcopy(oldmoves)
				self.king = oldking
			i += 1

	def addKingMoves(self,x,y,c):
		if c == "w":
			if self.board[7][4] == "Kw" and self.board[7][7] == "rw" and self.board[7][5] == 0 and self.board[7][6] == 0:
				self.legalMoves[c].append("castleKw")
			elif self.board[7][4] == "Kw" and self.board[7][0] == "rw" and self.board[7][3] == 0 and self.board[7][2] == 0 and self.board[7][1] == 0:
				self.legalMoves[c].append("castleqw")
		else:
			if self.board[0][4] == "Kb" and self.board[0][7] == "rb" and self.board[0][5] == 0 and self.board[0][6] == 0:
				self.legalMoves[c].append("castleKb")
			elif self.board[7][4] == "Kb" and self.board[0][0] == "rb" and self.board[0][3] == 0 and self.board[0][2] == 0 and self.board[0][1] == 0:
				self.legalMoves[c].append("castleqb")
		moves = [(x,y,x,y+1),(x,y,x+1,y+1),(x,y,x-1,y+1),(x,y,x-1,y),(x,y,x+1,y),(x,y,x,y-1),(x,y,x-1,y-1),(x,y,x+1,y-1)]
		for move in moves:
			if ((move[2] >= 8 or move[2] < 0 or move[3] >= 8 or move[3] < 0) == False) and (self.board[move[3]][move[2]] == 0 or self.board[move[3]][move[2]][1] != c):
				self.legalMoves[c].append(move)

	def findChecksW(self):
		x = self.king["w"][0]
		y = self.king["w"][1]

		#check for kings
		moves = [(x,y,x,y+1),(x,y,x+1,y+1),(x,y,x-1,y+1),(x,y,x-1,y),(x,y,x+1,y),(x,y,x,y-1),(x,y,x-1,y-1),(x,y,x+1,y-1)]
		for move in moves:
			if ((move[2] >= 8 or move[2] < 0 or move[3] >= 8 or move[3] < 0) == False) and (self.board[move[3]][move[2]] == "Kb"):
				self.check["w"] = True
				return

		#check for knights
		moves = [(x,y,x+2,y+1),(x,y,x+2,y-1),(x,y,x-2,y+1),(x,y,x-2,y-1),(x,y,x+1,y+2),(x,y,x+1,y-2),(x,y,x-1,y+2),(x,y,x-1,y-2)]
		for move in moves:
			if ((move[2] >= 8 or move[2] < 0 or move[3] >= 8 or move[3] < 0) == False) and (self.board[move[3]][move[2]] == "kb"):
				self.check["w"] = True
				return

		#check for pawns
		moves = [(x,y,x-1,y-1),(x,y,x+1,y-1)]
		for move in moves:
			if ((move[2] >= 8 or move[2] < 0 or move[3] >= 8 or move[3] < 0) == False) and (self.board[move[3]][move[2]] == "pb"):
				self.check["w"] = True
				return

		#check for rook/queen
		hit = False
		move = [x,y,x,y]
		move[2] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qb" or self.board[move[3]][move[2]] == "rb":
					self.check["w"] = True
					return
			move[2] -= 1
		hit = False
		move = [x,y,x,y]
		move[2] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qb" or self.board[move[3]][move[2]] == "rb":
					self.check["w"] = True
					return
			move[2] += 1
		hit = False
		move = [x,y,x,y]
		move[3] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qb" or self.board[move[3]][move[2]] == "rb":
					self.check["w"] = True
					return
			move[3] -= 1
		hit = False
		move = [x,y,x,y]
		move[3] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qb" or self.board[move[3]][move[2]] == "rb":
					self.check["w"] = True
					return
			move[3] += 1

		# check for bishop/queen
		hit = False
		move = [x,y,x,y]
		move[2] -= 1
		move[3] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qb" or self.board[move[3]][move[2]] == "bb":
					self.check["w"] = True
					return
			move[2] -= 1
			move[3] -= 1
		hit = False
		move = [x,y,x,y]
		move[2] += 1
		move[3] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qb" or self.board[move[3]][move[2]] == "bb":
					self.check["w"] = True
					return
			move[2] += 1
			move[3] -= 1
		hit = False
		move = [x,y,x,y]
		move[2] -= 1
		move[3] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qb" or self.board[move[3]][move[2]] == "bb":
					self.check["w"] = True
					return
			move[2] -= 1
			move[3] += 1
		hit = False
		move = [x,y,x,y]
		move[2] += 1
		move[3] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qb" or self.board[move[3]][move[2]] == "bb":
					self.check["w"] = True
					return
			move[2] += 1
			move[3] += 1
		self.check["w"] = False
		return

	def findChecksB(self):
		x = self.king["b"][0]
		y = self.king["b"][1]

		#check for kings
		moves = [(x,y,x,y+1),(x,y,x+1,y+1),(x,y,x-1,y+1),(x,y,x-1,y),(x,y,x+1,y),(x,y,x,y-1),(x,y,x-1,y-1),(x,y,x+1,y-1)]
		for move in moves:
			if ((move[2] >= 8 or move[2] < 0 or move[3] >= 8 or move[3] < 0) == False) and (self.board[move[3]][move[2]] == "Kw"):
				self.check["b"] = True
				return

		#check for knights
		moves = [(x,y,x+2,y+1),(x,y,x+2,y-1),(x,y,x-2,y+1),(x,y,x-2,y-1),(x,y,x+1,y+2),(x,y,x+1,y-2),(x,y,x-1,y+2),(x,y,x-1,y-2)]
		for move in moves:
			if ((move[2] >= 8 or move[2] < 0 or move[3] >= 8 or move[3] < 0) == False) and (self.board[move[3]][move[2]] == "kw"):
				self.check["b"] = True
				return

		#check for pawns
		moves = [(x,y,x-1,y+1),(x,y,x+1,y+1)]
		for move in moves:
			if ((move[2] >= 8 or move[2] < 0 or move[3] >= 8 or move[3] < 0) == False) and (self.board[move[3]][move[2]] == "pw"):
				self.check["b"] = True
				return

		#check for rook/queen
		hit = False
		move = [x,y,x,y]
		move[2] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qw" or self.board[move[3]][move[2]] == "rw":
					self.check["b"] = True
					return
			move[2] -= 1
		hit = False
		move = [x,y,x,y]
		move[2] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qw" or self.board[move[3]][move[2]] == "rw":
					self.check["b"] = True
					return
			move[2] += 1
		hit = False
		move = [x,y,x,y]
		move[3] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qw" or self.board[move[3]][move[2]] == "rw":
					self.check["b"] = True
					return
			move[3] -= 1
		hit = False
		move = [x,y,x,y]
		move[3] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qw" or self.board[move[3]][move[2]] == "rw":
					self.check["b"] = True
					return
			move[3] += 1

		# check for bishop/queen
		hit = False
		move = [x,y,x,y]
		move[2] -= 1
		move[3] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qw" or self.board[move[3]][move[2]] == "bw":
					self.check["b"] = True
					return
			move[2] -= 1
			move[3] -= 1
		hit = False
		move = [x,y,x,y]
		move[2] += 1
		move[3] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qw" or self.board[move[3]][move[2]] == "bw":
					self.check["b"] = True
					return
			move[2] += 1
			move[3] -= 1
		hit = False
		move = [x,y,x,y]
		move[2] -= 1
		move[3] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qw" or self.board[move[3]][move[2]] == "bw":
					self.check["b"] = True
					return
			move[2] -= 1
			move[3] += 1
		hit = False
		move = [x,y,x,y]
		move[2] += 1
		move[3] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]] == "qw" or self.board[move[3]][move[2]] == "bw":
					self.check["b"] = True
					return
			move[2] += 1
			move[3] += 1
		self.check["b"] = False
		return

	def addKnightMoves(self,x,y,c):
		moves = [(x,y,x+2,y+1),(x,y,x+2,y-1),(x,y,x-2,y+1),(x,y,x-2,y-1),(x,y,x+1,y+2),(x,y,x+1,y-2),(x,y,x-1,y+2),(x,y,x-1,y-2)]
		for move in moves:
			if ((move[2] >= 8 or move[2] < 0 or move[3] >= 8 or move[3] < 0) == False) and (self.board[move[3]][move[2]] == 0 or self.board[move[3]][move[2]][1] != c):
				self.legalMoves[c].append(move)

	def addPawnMoves(self,x,y,c):
		if c == "b":
			if ((y+1 >= 8 or y+1 < 0 or x >= 8 or x < 0) == False) and self.board[y+1][x] == 0:
				self.legalMoves[c].append((x,y,x,y+1))
			if ((y+2 >= 8 or y+2 < 0 or x >= 8 or x < 0) == False) and y == 1 and self.board[y+1][x] == 0 and self.board[y+2][x] == 0:
				self.legalMoves[c].append((x,y,x,y+2))
			if ((y+1 >= 8 or y+1 < 0 or x-1 >= 8 or x-1 < 0) == False) and str(self.board[y+1][x-1])[-1] == "w":
				self.legalMoves[c].append((x,y,x-1,y+1))
			if ((y+1 >= 8 or y+1 < 0 or x+1 >= 8 or x+1 < 0) == False) and str(self.board[y+1][x+1])[-1] == "w":
				self.legalMoves[c].append((x,y,x+1,y+1))
		if c == "w":
			if ((y-1 >= 8 or y-1 < 0 or x >= 8 or x < 0) == False) and self.board[y-1][x] == 0:
				self.legalMoves[c].append((x,y,x,y-1))
			if ((y-2 >= 8 or y-2 < 0 or x >= 8 or x < 0) == False) and y == 6 and self.board[y-1][x] == 0 and self.board[y-2][x] == 0:
				self.legalMoves[c].append((x,y,x,y-2))
			if ((y-1 >= 8 or y-1 < 0 or x-1 >= 8 or x-1 < 0) == False) and str(self.board[y-1][x-1])[-1] == "b":
				self.legalMoves[c].append((x,y,x-1,y-1))
			if ((y-1 >= 8 or y-1 < 0 or x+1 >= 8 or x+1 < 0) == False) and str(self.board[y-1][x+1])[-1] == "b":
				self.legalMoves[c].append((x,y,x+1,y-1))

	def promotePawns(self):
		for x in range(len(self.board[0])):
			if self.board[0][x] == "pw":
				self.board[0][x] = "qw"
		for x in range(len(self.board[7])):
			if self.board[7][x] == "pb":
				self.board[7][x] = "qb"

	def addRookMoves(self,x,y,c):
		hit = False
		move = [x,y,x,y]
		move[2] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]][1] != c:
					self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			else:
				self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			move[2] -= 1
		hit = False
		move = [x,y,x,y]
		move[2] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]][1] != c:
					self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			else:
				self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			move[2] += 1
		hit = False
		move = [x,y,x,y]
		move[3] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]][1] != c:
					self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			else:
				self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			move[3] -= 1
		hit = False
		move = [x,y,x,y]
		move[3] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]][1] != c:
					self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			else:
				self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			move[3] += 1

	def addBishopMoves(self,x,y,c):
		hit = False
		move = [x,y,x,y]
		move[2] -= 1
		move[3] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]][1] != c:
					self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			else:
				self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			move[2] -= 1
			move[3] -= 1
		hit = False
		move = [x,y,x,y]
		move[2] += 1
		move[3] -= 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]][1] != c:
					self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			else:
				self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			move[2] += 1
			move[3] -= 1
		hit = False
		move = [x,y,x,y]
		move[2] -= 1
		move[3] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]][1] != c:
					self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			else:
				self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			move[2] -= 1
			move[3] += 1
		hit = False
		move = [x,y,x,y]
		move[2] += 1
		move[3] += 1
		while hit == False and move[2] >= 0 and move[2] <= 7 and move[3] >= 0 and move[3] <= 7:
			if self.board[move[3]][move[2]] != 0:
				hit = True
				if self.board[move[3]][move[2]][1] != c:
					self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			else:
				self.legalMoves[c].append(tuple(copy.deepcopy(move)))
			move[2] += 1
			move[3] += 1