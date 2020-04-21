import matplotlib.pyplot as plt
import numpy as np

class Player:
	def __init__(self, player_type):
		self.player_type = player_type 
		self.payoff = 0  
		self.grudge = False

	'''
		1 = cooperate, 0 = defect 
	'''
	def make_move(self, round, lastMoveOther):
		if (self.player_type == "AC"):
			return 1
		elif (self.player_type == "AD"): 
			return 0 
		elif(self.player_type == "t4t"):
			if (round == 0):
				return 1 
			else:
				return lastMoveOther
		else:
			if (self.grudge):
				return 0
			else:
				return 1 

		# if (otherPlayer == 0):
		# 	self.grudge = True 

	def resetPayoff(self):
		self.payoff = 0 

	def resetGrudge(self):
		self.grudge = False 

	def printPlayer(self):
		print(self.player_type + " " + str(self.payoff))

class Game:
	def __init__(self, n, m, p, k):
		self.players = [] 
		self.n = n
		self.m = m 
		self.p = p 
		self.k = k 
		self.AC_payoff = []
		self.AD_payoff = [] 
		self.t4t_payoff = []
		self.G_payoff = []
		self.AC_number = []
		self.AD_number = []
		self.t4t_number = []
		self.G_number = []
		self.total = [] 
		self.setUpPlayers()

	def setUpPlayers(self):
		eachPlayer = int(self.n / 4)

		for i in range(eachPlayer):
			p = Player("AC")
			self.players.append(p)

		for i in range(eachPlayer):
			p = Player("AD")
			self.players.append(p)

		for i in range(eachPlayer):
			p = Player("t4t")
			self.players.append(p)

		for i in range(eachPlayer):
			p = Player("G")
			self.players.append(p)

	def play_game(self):
		for i in range(self.k):
			self.generation()
			self.getDistribution()
			self.getTotalPayOffs()
			if i != self.k-1:
				self.subPlayers()
				self.resetPayoffs()
		self.plot_payoff()
		self.plot_number()
		self.plot_total()
		self.plot_avg_payoff()
			
	def subPlayers(self):
		temp = self.players[100-self.p:]

		for i in range(self.p):
			self.players[i] = Player(temp[i].player_type)

	def generation(self):
		for one in range(self.n):
			for two in range(one+1, self.n):
				playerOne = self.players[one]
				playerTwo = self.players[two]
				self.repeatedGame(playerOne, playerTwo)
		self.players.sort(key = lambda x: x.payoff)

	def repeatedGame(self, playerOne, playerTwo):
		playerOneMove = 0 
		playerTwoMove = 0 
		lastPlayerOne = 0 
		lastPlayerTwo = 0 
		for i in range(self.m):
			playerOneMove = playerOne.make_move(i, lastPlayerTwo)
			playerTwoMove = playerTwo.make_move(i, lastPlayerOne)

			lastPlayerOne = playerOneMove
			lastPlayerTwo = playerTwoMove

			if (playerOneMove == 0):
				playerTwo.grudge = True 

			if (playerTwoMove == 0):
				playerOne.grudge = True

			playerOnePayoff, playerTwoPayoff = self.getPayoff(playerOneMove, playerTwoMove)

			playerOne.payoff += playerOnePayoff
			playerTwo.payoff += playerTwoPayoff

		playerOne.grudge = False 
		playerTwo.grudge = False 


	def getPayoff(self, playerOne, playerTwo):
		if playerOne == 1 and playerTwo == 1:
			return 3, 3 
		elif playerOne == 0 and playerTwo == 0:
			return 1, 1 
		elif playerOne == 1 and playerTwo == 0:
			return 0, 5 
		else:
			return 5, 0 

	def resetPayoffs(self):
		for p in self.players:
			p.resetPayoff()

	def printPlayers(self):
		for p in self.players:
			p.printPlayer()

	def getDistribution(self):
		AC = 0 
		t4t = 0 
		AD = 0 
		G = 0
		for p in self.players:
			if p.player_type == "AC":
				AC += 1 
			elif p.player_type == "AD":
				AD += 1
			elif p.player_type == "t4t":
				t4t += 1 
			else:
				G += 1

		self.AC_number.append(AC)
		self.AD_number.append(AD)
		self.t4t_number.append(t4t)
		self.G_number.append(G)

		# print("AC: " + str(AC) + " AD: " + str(AD) + " t4t: " + str(t4t) + " G: " + str(G))

	def getTotalPayOffs(self):
		AC = 0 
		t4t = 0 
		AD = 0 
		G = 0
		for p in self.players:
			if p.player_type == "AC":
				AC += p.payoff
			elif p.player_type == "AD":
				AD += p.payoff
			elif p.player_type == "t4t":
				t4t += p.payoff  
			else:
				G += p.payoff

		total = AC + t4t + AD + G

		self.AC_payoff.append(AC)
		self.AD_payoff.append(AD)
		self.t4t_payoff.append(t4t)
		self.G_payoff.append(G)
		self.total.append(total)

		# print("AC: " + str(AC) + " AD: " + str(AD) + " t4t: " + str(t4t) + " G: " + str(G) + " total: " + str(total))

	def plot_payoff(self):
		plt.plot(range(self.k), self.AC_payoff)
		plt.plot(range(self.k), self.AD_payoff)
		plt.plot(range(self.k), self.G_payoff)
		plt.plot(range(self.k), self.t4t_payoff)

		plt.xlabel('Generation')
		plt.ylabel('Payoff')

		plt.legend(['Always Cooperate', 'Always Defect', 'Grudge', 'Tit for Tat'])
		plt.title('Payoffs for each type of player')
		plt.show()

	def plot_number(self):
		plt.plot(range(self.k), self.AC_number)
		plt.plot(range(self.k), self.AD_number)
		plt.plot(range(self.k), self.G_number)
		plt.plot(range(self.k), self.t4t_number)

		plt.xlabel('Generation')
		plt.ylabel('Quantity of player')

		plt.legend(['Always Cooperate', 'Always Defect', 'Grudge', 'Tit for Tat'])
		plt.title('Percentage of each type of player')
		plt.show()

	def plot_total(self):
		plt.plot(range(self.k), self.total)
		plt.xlabel('Generation')
		plt.ylabel('Total Payoff')

		# plt.legend(['Always Cooperate', 'Always Defect', 'Grudge', 'Tit for Tat'])
		plt.title('Total Payoff')
		plt.show()

	def plot_avg_payoff(self):
		AC_avg = np.array(self.AC_payoff) / np.array(self.AC_number)
		AD_avg = np.array(self.AD_payoff) / np.array(self.AD_number)
		G_avg = np.array(self.G_payoff) / np.array(self.G_number)
		t4t_avg = np.array(self.t4t_payoff) / np.array(self.t4t_number)

		plt.plot(range(self.k), AC_avg)
		plt.plot(range(self.k), AD_avg)
		plt.plot(range(self.k), G_avg)
		plt.plot(range(self.k), t4t_avg)

		plt.xlabel('Generation')
		plt.ylabel('AVG Payoff')

		plt.legend(['Always Cooperate', 'Always Defect', 'Grudge', 'Tit for Tat'])
		plt.title('Avg payoff of each type of player')
		plt.show()

g = Game(100, 5, 50, 20)

g.play_game()

# for p in g.players:
# 	p.printPlayer()



















