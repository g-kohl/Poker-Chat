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
var.bbQuant = int(input("How many big blinds as starting cash?"))
var.dealer = var.currentPlayer = random.randrange(0, var.playersQuantity)

print("You're player1")

f.initPlayers()

while f.countActivePlayers() > 1:
    f.distributeCards()
    f.getCommunityCards()

    # for i in range(var.playersQuantity):
    #    f.showPlayerCards(i)

    #==========
    # Pre-Flop:
    #==========

    f.sleep()
    print("The dealer is %s" % var.listPlayers[var.dealer].name)

    if var.listPlayers[var.USER].active:
        f.sleep()
        f.showPlayerCards(var.USER)

    f.sleep()
    nextP = f.nextPlayer(var.currentPlayer)
    while not var.listPlayers[nextP].active:
        nextP = f.nextPlayer(nextP)

    var.currentPlayer = nextP

    if var.listPlayers[var.currentPlayer].cash <= int(var.minimalBet/2):
        var.listPlayers[var.currentPlayer].currentBet = var.listPlayers[var.currentPlayer].cash
        var.pot += var.listPlayers[var.currentPlayer].cash
        var.listPlayers[var.currentPlayer].cash = 0
        print("%s is the small blind and goes all in (cash: %d)" % (var.listPlayers[var.currentPlayer].name, var.listPlayers[var.currentPlayer].cash))
    else:
        var.listPlayers[var.currentPlayer].cash -= int(var.minimalBet/2)
        var.listPlayers[var.currentPlayer].currentBet += int(var.minimalBet/2)
        var.pot += int(var.minimalBet/2)
        print("%s is the small blind and bets %d chip(s) (cash: %d)" % (var.listPlayers[var.currentPlayer].name, int(var.minimalBet/2), var.listPlayers[var.currentPlayer].cash))

    f.sleep()
    nextP = f.nextPlayer(var.currentPlayer)
    while not var.listPlayers[nextP].active:
        nextP = f.nextPlayer(nextP)

    var.currentPlayer = nextP

    if var.listPlayers[var.currentPlayer].cash <= var.minimalBet:
        var.listPlayers[var.currentPlayer].currentBet = var.listPlayers[var.currentPlayer].cash
        var.pot += var.listPlayers[var.currentPlayer].cash
        var.listPlayers[var.currentPlayer].cash = 0
        print("%s is the small blind and goes all in (cash: %d)" % (var.listPlayers[var.currentPlayer].name, var.listPlayers[var.currentPlayer].cash))
    else:
        var.listPlayers[var.currentPlayer].cash -= var.minimalBet
        var.listPlayers[var.currentPlayer].currentBet += var.minimalBet
        var.pot += var.minimalBet
        print("%s is the big blind and bets %d chip(s) (cash: %d)" % (var.listPlayers[var.currentPlayer].name, var.minimalBet, var.listPlayers[var.currentPlayer].cash))

    firstOfRound = var.currentPlayer = f.nextPlayer(var.currentPlayer)
    lastOfRound = f.previousPlayer(var.currentPlayer)

    f.bettingRound()          

    f.sleep()
    print("End of Pre-Flop")
    print("The pot has %d chips" % var.pot)

    #======
    # Flop:
    #======
    print("The flop is: %s %s %s" % (f.stringCards(var.communityCards[0].number, var.communityCards[0].suit),
                                    f.stringCards(var.communityCards[1].number, var.communityCards[1].suit),
                                    f.stringCards(var.communityCards[2].number, var.communityCards[2].suit)))

    f.emptyCurrentBet()
    var.currentPlayer = f.nextPlayer(var.dealer)

    f.bettingRound()

    f.sleep()
    print("End of Flop")
    print("The pot has %d chips" % var.pot)

    #======
    # Turn:
    #======
    print("The turn is: %s" % f.stringCards(var.communityCards[3].number, var.communityCards[3].suit))

    f.emptyCurrentBet()
    var.currentPlayer = f.nextPlayer(var.dealer)

    f.bettingRound()

    f.sleep()
    print("End of Turn")
    print("The pot has %d chips" % var.pot)

    #=======
    # River:
    #=======
    print("The river is: %s" % f.stringCards(var.communityCards[4].number, var.communityCards[4].suit))

    f.emptyCurrentBet()
    var.currentPlayer = f.nextPlayer(var.dealer)

    f.bettingRound()

    f.sleep()
    print("End of River")
    print("The pot has %d chips" % var.pot)

    #==========
    # Showdown:
    #==========
    f.sleep()
    winners = f.showdown()
    f.distributePot(winners)

    if not f.isEndOfGame():
        f.prepareNextHand()
        print("Next Hand...\n")

for i in range(var.playersQuantity):
    if var.listPlayers[i].active:
        print("%s won the game!" % var.listPlayers[i].name)
        break