#!/usr/bin/env python
#  blitzavi89
# ----------------------------------------------------------------
# SIMPLE 5x5 BATTLE SHAPE GAME WITH GUI
# ----------------------------------------------------------------

import webbrowser
import urllib
import base64
import Tkinter
from Tkinter import *
import math
import tkMessageBox
import random

# GUI INTERFACE AND EVENT HANDLING FOR BATTLESHIP GAME
class BattleShip_App(Tkinter.Tk) :
	def __init__(self, parent) :
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.Initialize()
	button = []
	side_button = { "quit": None , "view_hint": None, "score": None , "turns" : None}
	counter = 0
	win_lose = False
	turns = 5
#URL Image List
	img_list = ["http://alfa.gifs-planet.com/new3/5013.gif", "http://alfa.gifs-planet.com/new/1024.gif", "http://alfa.gifs-planet.com/new3/4966.gif", "http://alfa.gifs-planet.com/new/1015.gif", "http://alfa.gifs-planet.com/new/4059.gif", "http://alfa.gifs-planet.com/new3/4976.gif", "http://alfa.gifs-planet.com/new3/5015.gif" ] 

# Game GUI initialized
	def Initialize(self) :		
		self.grid()
# All buttons layed out for guessing ship
		for i in range (5) :
			self.button.append([])
		        for j in range (5) :
 	                  	self.button[i].append(Tkinter.Button(self,text="0",fg = "Black", activebackground="Red", command = lambda x=i,y=j : self.OnButtonClick(x,y)))
				self.button[i][j].configure(width = 10, height = 8)
			        self.button[i][j].grid(column=i, row=j)

# Define the side buttons
		self.side_button["quit"] = Tkinter.Button(self, text="Quit Game", fg = "Blue", bg = "Yellow", command = self.OnClickQuit)
		self.side_button["quit"].grid(column = 20, row = 2)
		self.side_button["view_hint"] = Tkinter.Button(self, text="View Hint", fg = "Blue", bg = "Yellow", command = self.OnClickHint)
		self.side_button["view_hint"].grid(column = 25, row = 2)
		self.side_button["score"] = Tkinter.Button(self, text="View Score", fg = "Blue", bg = "Yellow", command = self.OnClickScore)
		self.side_button["score"].grid(column = 30, row = 2)
		self.side_button["turns"] = Tkinter.Button(self, text="5 Turns Left", fg = "Brown", bg = "Yellow")
		self.side_button["turns"].grid(column = 25, row = 7)

# What to do when button is clicked on the game	
	def OnButtonClick(self,x,y) :
		if self.CheckClickValidity(x,y) :		
			print "BattleShip_App:OnButtonClick(): User Button Clicked = X-- ", x+1," Y--", y+1
			self.counter = self.counter + 1
			print "BattleShip_App:OnButtonClick(): Counter = ",self.counter
			self.win_lose = BattleShip_Win_Or_Lose(x,y)
			print "BattleShip_App:OnButtonClick(): win_lose = ",self.win_lose
			if self.win_lose == True :
				self.button[x][y].configure(text="X", bg="Green")
				URL = random.choice(self.img_list)
				u = urllib.urlopen(URL)
				webbrowser.open(URL, new = 2)
			else :
				self.button[x][y].configure(text="X", bg="Black")
			self.turns -=1			
			self.side_button["turns"].configure(text= str(self.turns) + " Turns Left", fg = "Brown", bg = "Yellow")
			BattleShip_Score_Counter(self.win_lose)		
			Check_Win_Before_Five(x,y)
			if self.counter >= 5:
				BattleShip_App_Destroy()
			else :
				pass
		else :
			print "BattleShip_App:OnButtonClick(): Same button being clicked!"
			pass

# Checks validity of a button click during game
	def CheckClickValidity(self,X_Cor,Y_Cor) :
		if self.button[X_Cor][Y_Cor]["bg"] == "Black" or self.button[X_Cor][Y_Cor]["bg"] == "Green" :
			return False
		else :
			return True
	def OnClickQuit(self) :
		BattleShip_App_Destroy()
	def OnClickHint(self) :
		Past_Hints()
	def OnClickScore(self) :
		Score_App()

# GUI Class for Score App
class Score_App_Disp(Tkinter.Tk) :
	def __init__(self, parent) :
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.Display()
	button_quit = None
	text = None
	def Display(self) :
		self.grid()
		self.text = Tkinter.Text(self)
		self.text.insert(INSERT, "Hello\n")
		self.text.insert(INSERT, "User vs Computer Scores \n")
		self.text.grid(column = 0, row = 0)
		self.button_quit = Tkinter.Button(self, bg = "Yellow", fg = "Blue", text = "Quit Score", width = 8, height = 6, command = self.OnClickQuit)
		self.button_quit.grid(column = 4, row = 5)
	def OnClickQuit(self) :
		Score_App_Destroy()
		
# Opens the Score App
def Score_App() :
	global score_app, User_Score_Lst, Computer_Score_Lst, game
	print User_Score_Lst, Computer_Score_Lst
	score_app = Score_App_Disp(None)
	score_app.title('BattleShip Score Window')
	for i in range (len(User_Score_Lst)) :
		score_app.text.insert(INSERT, str(User_Score_Lst[i]) + " vs " + str(Computer_Score_Lst[i]) + "\n")
	if len(User_Score_Lst) == 5 :
		score_app.text.insert(INSERT, "\n\n\nTOTAL SCORES\n\n\n User = " + str(User_Score) + "\n\n\n Computer = " + str(Computer_Score))
	if User_Score >=1 :
		score_app.text.insert(INSERT, "\n\n YOU WIN! :D")
	elif game.turns == 5 :
		score_app.text.insert(INSERT, "\n\n GAME HAS NOT YET STARTED! :O")
	else :
		score_app.text.insert(INSERT, "\n\n YOU LOSE! :(")	
	score_app.mainloop()

def Score_App_Destroy() :
	score_app.destroy()
	print "Score_App_Destroy(): Score App is destroyed!"

# Function that calculates win/lose for each round
def BattleShip_Win_Or_Lose(xCor, yCor) :		
	global computer_turn_x, computer_turn_y
	print "BattleShip_Win_Or_Lose(): Computer Choice = X-- ",computer_turn_x + 1," Y-- ",computer_turn_y + 1
	if xCor == computer_turn_x and yCor == computer_turn_y :
		return True
	else :
		return False

# Function that keeps score count for computer and user
def BattleShip_Score_Counter(score_check):
	global Computer_Score, User_Score, User_Score_Lst, Computer_Score_Lst	
	if score_check == True :
		User_Score +=1
		User_Score_Lst.append(1)
		Computer_Score_Lst.append(0)
		print "BattleShip_Score_Counter() List Update: User =", User_Score_Lst, " Computer = ",Computer_Score_Lst
	elif score_check == False :
		Computer_Score +=1
		User_Score_Lst.append(0)
		Computer_Score_Lst.append(1)
		print "BattleShip_Score_Counter() List Update: User =", User_Score_Lst, " Computer = ",Computer_Score_Lst
	print "BattleShip_Score_Counter(): Updated Score: USER = %d COMPUTER = %d" %(User_Score, Computer_Score)

# Check for win before number of turns = 5
def Check_Win_Before_Five(xCor, yCor) :
	if game.button[xCor][yCor]["bg"] == "Green" :
		Score_App()
	else :
		pass
		
# Hint generator
def Past_Hints() :
	global computer_turn_x, computer_turn_y, choice_list_x, choice_list_y, helper_x, helper_y, hint_count
	new_x = random.choice (choice_list_x)
	new_y = random.choice (choice_list_y)
	if hint_count <=4 :
		if game.button[new_x][new_y]["bg"] == "Black" or game.button[new_x][new_y]["bg"] == "Green" or game.button[new_x][new_y]["bg"] == "Yellow" :
			Past_Hints()
		else :
			hint_count = hint_count + 1			
			tkMessageBox.showinfo("HINT BOX", "The ship is not in row = " + str(new_x+1) + " column = " + str(new_y+1))
			game.button[new_x][new_y].configure(text = "NOT HERE", bg = "Yellow")			
	else :
		tkMessageBox.showinfo("HINT BOX", "No More Hints! Proceed to Play...")

# BATTLESHIP GAME DESTROYER
def BattleShip_App_Destroy() :
	print "BattleShip_App_Destroy(): Called"	
	game.destroy()
	Score_App()

# BATTLESHIP GAME STARTER
def BattleShip_Start() :
	print "BattleShip_Start(): Game Started"
	game.mainloop()	

User_Score_Lst = []
Computer_Score_Lst = []
User_Score = 0
Computer_Score = 0
choice_list_x = [0,1,2,3,4]
choice_list_y = [0,1,2,3,4]
computer_turn_x = random.choice(choice_list_x)
computer_turn_y = random.choice(choice_list_y)
helper_x = choice_list_x
helper_x.remove(computer_turn_x)
helper_y = choice_list_y
helper_y.remove(computer_turn_y)
score_app = None
print helper_x, helper_y
hint_count = 0
game = BattleShip_App(None)
game.title('BattleShip Game')
BattleShip_Start()



