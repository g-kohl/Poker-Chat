# Libraries:
#from dataclasses import dataclass
import random

# Modules:
import variables as var
import functions as f

#==========
# Pre-Game:
#==========
var.playersQuantity = int(input("How many players(2-10)?"))
var.toPayBet = var.minimalBet = int(input("How much will be the minimal bet?"))
var.dealer = var.currentPlayer = random.randrange(0, var.playersQuantity)

print("You're always player number 1")

f.initPlayers()
f.distributeCards()
f.getCommunityCards()

#for i in range(var.playersQuantity):
#    f.showPlayerCards(i)

#==========
# Pre-Flop:
#==========

print("The dealer will be player" + str(var.dealer+1))

f.showPlayerCards(var.USER)

var.currentPlayer = f.nextPlayer(var.currentPlayer)
print("Player" + str(var.currentPlayer+1) + " is the small blind and bets " + str(int(var.minimalBet/2)) + " chip(s)")
var.listPlayers[var.currentPlayer].cash -= int(var.minimalBet/2)
var.listPlayers[var.currentPlayer].currentBet += int(var.minimalBet/2)

var.currentPlayer = f.nextPlayer(var.currentPlayer)
print("Player" + str(var.currentPlayer+1) + " is the big blind and bets " + str(var.minimalBet) + " chips")
var.listPlayers[var.currentPlayer].cash -= var.minimalBet
var.listPlayers[var.currentPlayer].currentBet += var.minimalBet

var.pot += int((3*var.minimalBet)/2)

firstOfRound = var.currentPlayer = f.nextPlayer(var.currentPlayer)
lastOfRound = f.previousPlayer(var.currentPlayer)

f.bettingRound()          

print("End of Pre-Flop")
print("The pot has " + str(var.pot) + " chips")

#======
# Flop:
#======
print("The flop is:")
print(f.stringCards(var.communityCards[0].number, var.communityCards[0].suit)
      + " "
      + f.stringCards(var.communityCards[1].number, var.communityCards[1].suit)
      + " "
      + f.stringCards(var.communityCards[2].number, var.communityCards[2].suit))

f.emptyCurrentBet()
var.currentPlayer = f.nextPlayer(var.dealer)

f.bettingRound()

print("End of Flop")
print("The pot has " + str(var.pot) + " chips")

#======
# Turn:
#======
print("The turn is:")
print(f.stringCards(var.communityCards[3].number, var.communityCards[3].suit))

f.emptyCurrentBet()
var.currentPlayer = f.nextPlayer(var.dealer)

f.bettingRound()

print("End of Turn")
print("The pot has " + str(var.pot) + " chips")

#=======
# River:
#=======
print("The river is:")
print(f.stringCards(var.communityCards[4].number, var.communityCards[4].suit))

f.emptyCurrentBet()
var.currentPlayer = f.nextPlayer(var.dealer)

f.bettingRound()

print("End of River")
print("The pot has " + str(var.pot) + " chips")

#==========
# Showdown:
#==========
f.showdown()
