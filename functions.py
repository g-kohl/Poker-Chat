# Libraries:
import random
import time

# Modules:
import variables as var

#=====================
# Initialize the game:
#=====================
def initPlayers():
    for i in range(var.playersQuantity):
        var.listPlayers.append(var.Player("player" + str(i+1), [var.NULLCARD, var.NULLCARD], var.bbQuant*var.minimalBet, True, 0, 0, 0, [var.NULLCARD, var.NULLCARD, var.NULLCARD, var.NULLCARD, var.NULLCARD]))
    # Initializes the list of players with a standard name, null cards, var.bbQuant times the minimal bet as cash, a boolean indicating the activity of the player, 0 as the current bet, 0 as the value of the hand, 0 as tiebreak points and a empty list for the best hand

def getCard():
    while True:
        equalCard = False
        randomCard = var.Card(var.numbers[random.randrange(0, 13)], var.suits[random.randrange(0, 4)])

        for i in range(var.playersQuantity):
            if randomCard.number == var.listPlayers[i].cards[0].number and randomCard.suit == var.listPlayers[i].cards[0].suit:
                equalCard = True

            if randomCard.number == var.listPlayers[i].cards[1].number and randomCard.suit == var.listPlayers[i].cards[1].suit:
                equalCard = True

        for i in range(5):
            if randomCard.number == var.communityCards[i].number and randomCard.suit == var.communityCards[i].suit:
                equalCard = True

        if equalCard == False:
            return randomCard 
    # Generates a random card and verify if it was generated before
        
def distributeCards():
    for i in range(var.playersQuantity):
        var.listPlayers[i].cards[0] = getCard()
        var.listPlayers[i].cards[1] = getCard()
    # Generates two random cards (never generated before) for each player

def getCommunityCards():
    for i in range(5):
        var.communityCards[i] = getCard()
    # Generates the community cards

def emptyCurrentBet():
    var.toPayBet = 0

    for i in range(var.playersQuantity):
        var.listPlayers[i].currentBet = 0
    # Makes the current bet of all players be zero

def stringCards(cardNumber, cardSuit):
    match cardNumber:
        case var.ACE:
            return "A" + cardSuit
        case 10:
            return "T" + cardSuit
        case var.JACK:
            return "J" + cardSuit
        case var.QUEEN:
            return "Q" + cardSuit
        case var.KING:
            return "K" + cardSuit
        case _ :
            return str(cardNumber) + cardSuit
    # Generates a string for the card

def showPlayerCards(player):
    if player == var.USER:
        print("Your cards are: %s %s" % (stringCards(var.listPlayers[player].cards[0].number, var.listPlayers[player].cards[0].suit),
                                         stringCards(var.listPlayers[player].cards[1].number, var.listPlayers[player].cards[1].suit)))
    else:
        print("%s's cards are: %s %s" % (var.listPlayers[player].name,
                                         stringCards(var.listPlayers[player].cards[0].number, var.listPlayers[player].cards[0].suit),
                                         stringCards(var.listPlayers[player].cards[1].number, var.listPlayers[player].cards[1].suit)))
    # Shows the hand of the current player

def showPossibleCards(possibleCards):
    for i in range(len(possibleCards)):
        print(stringCards(possibleCards[i].number, possibleCards[i].suit))
    # Shows all possible cards of a player

#===================
# Control the turns:
#===================
def nextPlayer(player):
    player += 1

    if player >= var.playersQuantity:
        player -= var.playersQuantity
    
    return player
    # Gets the number of the next player of the table

def previousPlayer(player):
    player -= 1

    if player < 0:
        return var.playersQuantity
    else:
        return player
    # Gets the number of the previous player of the table

def isEndOfRound():
    flag = True

    for i in range(var.playersQuantity):
        if var.listPlayers[i].active and var.listPlayers[i].currentBet < var.toPayBet and var.listPlayers[i].cash > 0:
            flag = False
            # print("%s have to play" % var.listPlayers[i].name)

    return flag
    # Returns false if it finds a player the still have to bet/pay, and true if that isn't the case

def isEndOfGame():
    count = 0

    for i in range(var.playersQuantity):
        if var.listPlayers[i].cash > 0:
            count += 1

    if count == 1:
        return True

    return False
    # Returns true if the game ended

def countActivePlayers():
    activePlayers = 0

    for i in range(var.playersQuantity):
        if var.listPlayers[i].active and var.listPlayers[i].cash > 0:
            activePlayers += 1

    return activePlayers
    # Returns the number of active players that still have cash

def prepareNextHand():
    var.pot = 0
    var.toPayBet = var.minimalBet
    var.communityCards = [var.NULLCARD, var.NULLCARD, var.NULLCARD, var.NULLCARD, var.NULLCARD]

    for i in range(var.playersQuantity):
        var.listPlayers[i].cards = [var.NULLCARD, var.NULLCARD]
        var.listPlayers[i].currentBet = 0
        var.listPlayers[i].handValue = 0
        var.listPlayers[i].tiebreakPoints = 0
        var.listPlayers[i].bestHand = [var.NULLCARD, var.NULLCARD, var.NULLCARD, var.NULLCARD, var.NULLCARD]

        if var.listPlayers[i].cash > 0:
            var.listPlayers[i].active = True
        else:
            var.listPlayers[i].active = False

    nextP = nextPlayer(var.dealer)
    while not var.listPlayers[nextP].active:
        nextP = nextPlayer(nextP)

    var.dealer = var.currentPlayer = nextP
    # Prepare configurations for the next hand

#======================================
# Control the decisions of the players:
#======================================
def bettingRound():
    for i in range(var.playersQuantity):
        if countActivePlayers() <= 1 and isEndOfRound():
            break

        if var.listPlayers[var.currentPlayer].active and var.listPlayers[var.currentPlayer].cash > 0:
            playerDecision()

        var.currentPlayer = nextPlayer(var.currentPlayer)
    # Every active player makes a decision

    while not isEndOfRound():
        for i in range(var.playersQuantity):
            if var.listPlayers[var.currentPlayer].active and var.listPlayers[var.currentPlayer].currentBet < var.toPayBet and var.listPlayers[var.currentPlayer].cash > 0:
                playerDecision()
                
            var.currentPlayer = nextPlayer(var.currentPlayer)
    # If there are players that still have to bet/pay, asks for the decisions  

def showDecisions():
    return input("Fold(1) | Check(2) | Call(3) | Raise(4)")
    # Shows the decisions a player can do

def playerDecision():
    if var.currentPlayer == var.USER:
        decision = int(showDecisions())
    else:
        decision = random.randrange(1, 5)

    match decision:
        case var.FOLD:
            sleep()
            print("%s folds (cash: %d)" % (var.listPlayers[var.currentPlayer].name, var.listPlayers[var.currentPlayer].cash))
            fold()
            
        case var.CHECK:
            if var.listPlayers[var.currentPlayer].currentBet < var.toPayBet:
                if var.currentPlayer == var.USER:
                    print("You can't check, to continue playing this hand you must either call or raise")

                playerDecision()
            else:
                sleep()
                print("%s checks (cash: %d)" % (var.listPlayers[var.currentPlayer].name, var.listPlayers[var.currentPlayer].cash))

        case var.CALL:
            if var.toPayBet == 0 or var.toPayBet == var.listPlayers[var.currentPlayer].currentBet:
                if var.currentPlayer == var.USER:
                    print("There is nothing to call, you can fold, check or raise")

                playerDecision() 
            else:
                isAllIn(var.CALL)

        case var.RAISE:
            if var.listPlayers[var.currentPlayer].cash <= var.toPayBet:
                if var.currentPlayer == var.USER:
                    print("You don't have enough cash to raise")

                playerDecision()
            else:
                raiseBet()
    # Redirect to the coresponding function based on the decision

def isAllIn(decision):
    if var.listPlayers[var.currentPlayer].cash > var.toPayBet - var.listPlayers[var.currentPlayer].currentBet:
        var.pot += var.toPayBet - var.listPlayers[var.currentPlayer].currentBet
        var.listPlayers[var.currentPlayer].cash -= var.toPayBet - var.listPlayers[var.currentPlayer].currentBet
        var.listPlayers[var.currentPlayer].currentBet = var.toPayBet

        if decision == var.CALL:
            sleep()
            print("%s calls (cash: %d)" % (var.listPlayers[var.currentPlayer].name, var.listPlayers[var.currentPlayer].cash))
        elif decision == var.RAISE:
            sleep()
            print("%s raises to %d (cash: %d)" % (var.listPlayers[var.currentPlayer].name, var.toPayBet, var.listPlayers[var.currentPlayer].cash))
    else:
        allIn()
    # Verifies if is an "all in" situation. If it isn't, just pays the bet

def allIn():
    sleep()
    var.pot += var.listPlayers[var.currentPlayer].cash
    var.listPlayers[var.currentPlayer].currentBet += var.listPlayers[var.currentPlayer].cash
    var.listPlayers[var.currentPlayer].cash = 0
    print("%s goes all in! (cash: %d)" % (var.listPlayers[var.currentPlayer].name, var.listPlayers[var.currentPlayer].cash))
    # Prints the "all in" message and empties the player's cash

def fold():
    var.listPlayers[var.currentPlayer].active = False
    # Makes the player inactive

def raiseBet():
    if var.currentPlayer == var.USER:
        bet = input("How much do you want to raise the previous bet?")
    else:
        bet = random.randrange(1, var.listPlayers[var.currentPlayer].cash - var.toPayBet + 1)

    var.toPayBet += int(bet)
    isAllIn(var.RAISE)
    # If it is the user turn, asks how much will be the raise
    # If it isn't, generate a random number that will be the raise

def sleep():
    time.sleep(1.5)

#=====================
# Control the results:
#=====================
def showdown():
    winners = []

    for i in range(var.playersQuantity):
        if var.listPlayers[i].active:
            var.listPlayers[i].handValue = calculateHand(i)

    bestHand = 0
    for i in range(var.playersQuantity):
        if var.listPlayers[i].active and var.listPlayers[i].handValue > bestHand:
            bestHand = var.listPlayers[i].handValue

    tiebreakValue = tiebreak(bestHand)
    print("Best hand: %d" % bestHand)
    print("TB: %d" % tiebreakValue)

    for i in range(var.playersQuantity):
        if var.listPlayers[i].active:
            if var.listPlayers[i].handValue == bestHand and var.listPlayers[i].tiebreakPoints == tiebreakValue:
                print("%s won! (%s) TB: %d" % (var.listPlayers[i].name, printHand(i), var.listPlayers[i].tiebreakPoints))
                winners.append(i)
            else:
                print("%s lost... (%s) TB: %d" % (var.listPlayers[i].name, printHand(i), var.listPlayers[i].tiebreakPoints))
            
            print("%s %s" % (stringCards(var.listPlayers[i].cards[0].number, var.listPlayers[i].cards[0].suit),
                             stringCards(var.listPlayers[i].cards[1].number, var.listPlayers[i].cards[1].suit)))
            
            print("%s %s %s %s %s" % (stringCards(var.listPlayers[i].bestHand[0].number, var.listPlayers[i].bestHand[0].suit),
                                      stringCards(var.listPlayers[i].bestHand[1].number, var.listPlayers[i].bestHand[1].suit),
                                      stringCards(var.listPlayers[i].bestHand[2].number, var.listPlayers[i].bestHand[2].suit),
                                      stringCards(var.listPlayers[i].bestHand[3].number, var.listPlayers[i].bestHand[3].suit),
                                      stringCards(var.listPlayers[i].bestHand[4].number, var.listPlayers[i].bestHand[4].suit)))
            
    return winners
    # Looks for the player with the best hand and returns a list of the winners

def distributePot(winners):
    value = var.pot / len(winners)

    for i in range(len(winners)):
        var.listPlayers[winners[i]].cash += value
        print("%s received: %d chips" % (var.listPlayers[winners[i]].name, value))
    # Distributes the money among the winners

def tiebreak(bestHand):
    match bestHand:
        case var.HIGHCARD | var.FLUSH:
            for i in range(5):
                highestCard = findHighestCard(bestHand, i, i)

                for j in range(var.playersQuantity):
                    if var.listPlayers[j].tiebreakPoints == i and var.listPlayers[j].bestHand[i].number == highestCard:
                        var.listPlayers[j].tiebreakPoints = i+1

            return 5
            
        case var.PAIR:
            highestHighPair = findHighestCard(bestHand, 0, 0)

            for i in range(var.playersQuantity):
                if var.listPlayers[i].active and var.listPlayers[i].handValue == bestHand and var.listPlayers[i].bestHand[0].number == highestHighPair:
                    var.listPlayers[i].tiebreakPoints = 1

            for i in range(3):
                highestCard = findHighestCard(bestHand, i+2, i+1)

                for j in range(var.playersQuantity):
                    if var.listPlayers[j].tiebreakPoints == i+1 and var.listPlayers[j].bestHand[i+2].number == highestCard:
                        var.listPlayers[j].tiebreakPoints = i+2
            
            return 4

        case var.TWOPAIRS:
            highestHighPair = findHighestCard(bestHand, 0, 0)

            for i in range(var.playersQuantity):
                if var.listPlayers[i].active and var.listPlayers[i].handValue == bestHand and var.listPlayers[i].bestHand[0].number == highestHighPair:
                    var.listPlayers[i].tiebreakPoints = 1

            highestLowPair = findHighestCard(bestHand, 2, 1)

            for i in range(var.playersQuantity):
                if var.listPlayers[i].tiebreakPoints == 1 and var.listPlayers[i].bestHand[2].number == highestLowPair:
                    var.listPlayers[i].tiebreakPoints = 2

            highestCard = findHighestCard(bestHand, 4, 2)

            for i in range(var.playersQuantity):
                if var.listPlayers[i].tiebreakPoints == 2 and var.listPlayers[i].bestHand[4].number == highestCard:
                    var.listPlayers[i].tiebreakPoints = 3
        
            return 3

        case var.THREEOFAKIND:
            highestTrio = findHighestCard(bestHand, 0, 0)

            for i in range(var.playersQuantity):
                if var.listPlayers[i].active and var.listPlayers[i].handValue == bestHand and var.listPlayers[i].bestHand[0].number == highestTrio:
                    var.listPlayers[i].tiebreakPoints = 1

            for i in range(2):
                highestCard = findHighestCard(bestHand, i+3, i+1)

                for j in range(var.playersQuantity):
                    if var.listPlayers[j].tiebreakPoints == i+1 and var.listPlayers[j].bestHand[i+3].number == highestCard:
                        var.listPlayers[j].tiebreakPoints = i+2
            
            return 3

        case var.FULLHOUSE:
            highestTrio = findHighestCard(bestHand, 0, 0)

            for i in range(var.playersQuantity):
                if var.listPlayers[i].active and var.listPlayers[i].handValue == bestHand and var.listPlayers[i].bestHand[0].number == highestTrio:
                    var.listPlayers[i].tiebreakPoints = 1

            highestPair = findHighestCard(bestHand, 3, 1)

            for i in range(var.playersQuantity):
                if var.listPlayers[i].tiebreakPoints == 1 and var.listPlayers[i].bestHand[3].number == highestPair:
                    var.listPlayers[i].tiebreakPoints = 2

            return 2
        
        case var.ROYALFLUSH:
            return 0
        
        case _: # Straight, Straight Flush or Four Of A Kind
            highestCard = findHighestCard(bestHand, 0, 0)

            for i in range(var.playersQuantity):
                if var.listPlayers[i].active and var.listPlayers[i].handValue == bestHand and var.listPlayers[i].bestHand[0].number == highestCard:
                    var.listPlayers[i].tiebreakPoints = 1

            return 1
    # Tiebreak

def findHighestCard(bestHand, index, tiebreakValue):
    highestCard = 0

    for i in range(var.playersQuantity):
        if var.listPlayers[i].active and var.listPlayers[i].handValue == bestHand and var.listPlayers[i].tiebreakPoints == tiebreakValue:
            if var.listPlayers[i].bestHand[index].number == var.ACE:
                highestCard = var.ACE
                break
            elif var.listPlayers[i].bestHand[index].number > highestCard:
                highestCard = var.listPlayers[i].bestHand[index].number
    
    return highestCard
    # Finds the highest "index-th" card from the players with the best hand and best current tiebreak points

def printHand(player):
    match var.listPlayers[player].handValue:
        case var.HIGHCARD: return "high card"
        case var.PAIR: return "pair"
        case var.TWOPAIRS: return "two pairs"
        case var.THREEOFAKIND: return "three of a kind"
        case var.STRAIGHT: return "straight"
        case var.FLUSH: return "flush"
        case var.FULLHOUSE: return "full house"
        case var.FOUROFAKIND: return "four of a kind"
        case var.STRAIGHTFLUSH: return "straight flush"
        case var.ROYALFLUSH: return "royal flush"
    # Prints the hand
        
def printBestHand(player):
    for i in range(5):
        print(stringCards(var.listPlayers[player].bestHand[i].number, var.listPlayers[player].bestHand[i].suit))
    # Prints the best hand
        
def sortPossibleCards(possibleCards):
    for i in range(1, 7):
        key = possibleCards[i]
        j = i - 1

        while j >= 0 and key.number < possibleCards[j].number:
            possibleCards[j+1] = possibleCards[j]
            j -= 1

        possibleCards[j+1] = key

    for i in range(7):
        if possibleCards[i].number == 1:
            possibleCards.append(possibleCards[i])
    
    return possibleCards
    # Sorts the 7 possible cards to make the hand (insertion sort)

def calculateHand(player):
    possibleCards = sortPossibleCards([var.listPlayers[player].cards[0], var.listPlayers[player].cards[1], var.communityCards[0], var.communityCards[1], var.communityCards[2], var.communityCards[3], var.communityCards[4]])

    if royalFlush(possibleCards, player):
        return var.ROYALFLUSH
    elif straightFlush(possibleCards):
        getStraightFlush(possibleCards, player)
        return var.STRAIGHTFLUSH
    elif equalNumber(possibleCards, 4):
        getFourOfAKind(possibleCards, player)
        return var.FOUROFAKIND
    elif fullHouse(possibleCards):
        getFullHouse(possibleCards, player)
        return var.FULLHOUSE
    elif flush(possibleCards):
        getFlush(possibleCards, player)
        return var.FLUSH
    elif straight(possibleCards):
        getStraight(possibleCards, player)
        return var.STRAIGHT
    elif equalNumber(possibleCards, 3):
        getThreeOfAKind(possibleCards, player)
        return var.THREEOFAKIND
    elif twoPairs(possibleCards):
        getTwoPairs(possibleCards, player)
        return var.TWOPAIRS
    elif equalNumber(possibleCards, 2):
        getPair(possibleCards, player)
        return var.PAIR
    else:
        getHighCard(possibleCards, player)
        return var.HIGHCARD
    # Calculates the value of the player's hand

def isThereNumber(number, cards):
    for i in range(len(cards)):
        if cards[i].number == number:
            return True
        
    return False
    # Verifies if a number is in a list of cards

def isThereCard(number, suit, cards):
    for i in range(len(cards)):
        if cards[i].number == number and cards[i].suit == suit:
            return True
        
    return False
    # Verifies if a card is in a list of cards

def getHighCard(possibleCards, player):
    for i in range(5):
        var.listPlayers[player].bestHand[i] = possibleCards[len(possibleCards)-1-i]
    # Gets the best hand (high card): descending order
        
def getPair(possibleCards, player):
    for i in range(7):
        if possibleCards[i].number == var.lookForCard1:
            var.listPlayers[player].bestHand[0] = possibleCards[i]
            var.listPlayers[player].bestHand[1] = possibleCards[i+1]
            break

    counter = 0

    for i in range(len(possibleCards)):
        if possibleCards[len(possibleCards)-1-i].number != var.lookForCard1:
            var.listPlayers[player].bestHand[2+counter] = possibleCards[len(possibleCards)-1-i]
            counter += 1

            if counter == 3:
                break
    # Gets the best hand (pair): Pair1, Pair2, Highcards in descending order
            
def getTwoPairs(possibleCards, player):
    highPair = max([var.lookForCard1, var.lookForCard2])
    lowPair = min([var.lookForCard1, var.lookForCard2])

    if lowPair == 1:
        highPair, lowPair = lowPair, highPair

    for i in range(7):
        if possibleCards[i].number == highPair:
            var.listPlayers[player].bestHand[0] = possibleCards[i]
            var.listPlayers[player].bestHand[1] = possibleCards[i+1]
            break

    for i in range(7):
        if possibleCards[i].number == lowPair:
            var.listPlayers[player].bestHand[2] = possibleCards[i]
            var.listPlayers[player].bestHand[3] = possibleCards[i+1]
            break

    for i in range(7):
        if possibleCards[len(possibleCards)-1-i].number != highPair and possibleCards[len(possibleCards)-1-i].number != lowPair:
            var.listPlayers[player].bestHand[4] = possibleCards[len(possibleCards)-1-i]
            break
    # Gets the best hand (two pairs): HighPair1, HighPair2, LowPair1, LowPair2, Highcard
            
def getThreeOfAKind(possibleCards, player):
    for i in range(7):
        if possibleCards[i].number == var.lookForCard1:
            var.listPlayers[player].bestHand[0] = possibleCards[i]
            var.listPlayers[player].bestHand[1] = possibleCards[i+1]
            var.listPlayers[player].bestHand[2] = possibleCards[i+2]
            break

    counter = 0

    for i in range(len(possibleCards)):
        if possibleCards[len(possibleCards)-1-i].number != var.lookForCard1:
            var.listPlayers[player].bestHand[3+counter] = possibleCards[len(possibleCards)-1-i]
            counter += 1

            if counter == 2:
                break
    # Gets the best hand (three of a kind): Trio1, Trio2, Trio3, highcards in descending order
            
def getStraight(possibleCards, player):
    for i in range(5):
        for j in range(7):
            if var.lookForCard1 - i == 14:
                if possibleCards[j].number == 1:
                    var.listPlayers[player].bestHand[4-i] = possibleCards[j]
                    break
            elif var.lookForCard1 - i == possibleCards[j].number:
                var.listPlayers[player].bestHand[4-i] = possibleCards[j]
                break
    # Gets the best hand (straight): ascending order
            
def getFlush(possibleCards, player):
    cardCount = 0

    for i in range(7):
        if possibleCards[len(possibleCards)-1-i].suit == var.lookForSuit:
            var.listPlayers[player].bestHand[cardCount] = possibleCards[len(possibleCards)-1-i]
            cardCount += 1

            if cardCount == 5:
                break
    # Gets the best hand (flush): descending order
            
def getFullHouse(possibleCards, player):
    for i in range(7):
        if possibleCards[i].number == var.lookForCard1:
            var.listPlayers[player].bestHand[0] = possibleCards[i]
            var.listPlayers[player].bestHand[1] = possibleCards[i+1]
            var.listPlayers[player].bestHand[2] = possibleCards[i+2]
            break

    for i in range(7):
        if possibleCards[i].number == var.lookForCard2:
            var.listPlayers[player].bestHand[3] = possibleCards[i]
            var.listPlayers[player].bestHand[4] = possibleCards[i+1]
            break
    # Gets the best hand (full house): Trio1, Trio2, Trio3, Pair1, Pair2
        
def getFourOfAKind(possibleCards, player):
    for i in range(7):
        if possibleCards[i].number == var.lookForCard1:
            var.listPlayers[player].bestHand[0] = possibleCards[i]
            var.listPlayers[player].bestHand[1] = possibleCards[i+1]
            var.listPlayers[player].bestHand[2] = possibleCards[i+2]
            var.listPlayers[player].bestHand[3] = possibleCards[i+3]
            break

    for i in range(7):
        if possibleCards[len(possibleCards)-1-i].number != var.lookForCard1:
            var.listPlayers[player].bestHand[4] = possibleCards[len(possibleCards)-1-i]
    # Gets the best hand (four of a kind): Quad1, Quad2, Quad3, Quad4, Highcard
            
def getStraightFlush(possibleCards, player):
    for i in range(5):
        for j in range(7):
            if possibleCards[j].suit == var.lookForSuit:
                if var.lookForCard1 - i == 14:
                    if possibleCards[j].number == 1:
                        var.listPlayers[player].bestHand[4-i] = possibleCards[j]
                        break
                elif var.lookForCard1 - i == possibleCards[j].number:
                    var.listPlayers[player].bestHand[4-i] = possibleCards[j]
                    break
    # Gets the best hand (straight flush): ascending order
    
def equalNumber(possibleCards, occurrence):
    for i in range(7):
        equalNumbers = 0

        for j in range(7):
            if possibleCards[i].number == possibleCards[j].number:
                equalNumbers += 1

            if equalNumbers == occurrence:
                var.lookForCard1 = possibleCards[i].number
                return True

    return False
    # Returns True if the player has cards with the same number, based on the number of desired occurrences

def twoPairs(possibleCards):
    pairs = 0
    var.lookForCard1 = 0
    var.lookForCard2 = 0

    for i in range(7):
        for j in range(7-i):
            if possibleCards[len(possibleCards)-1-i].number == possibleCards[len(possibleCards)-1-i-j].number and possibleCards[len(possibleCards)-1-i].suit != possibleCards[len(possibleCards)-1-i-j].suit:
                if var.lookForCard1 == 0:
                    var.lookForCard1 = possibleCards[len(possibleCards)-1-i].number
                else:
                    var.lookForCard2 = possibleCards[len(possibleCards)-1-i].number

                pairs += 1
                break

    if pairs >= 2:
        return True
    else:
        return False
    # Returns True if the player has two pairs

def straight(possibleCards):
    if isThereNumber(var.ACE, possibleCards) and isThereNumber(10, possibleCards) and isThereNumber(var.JACK, possibleCards) and isThereNumber(var.QUEEN, possibleCards) and isThereNumber(var.KING, possibleCards):
        var.lookForCard1 = 1
        return True
    
    counter = 0
    i = len(possibleCards) - 1
    while counter < 3:
        if possibleCards[i].number != var.ACE:
            if (isThereNumber(possibleCards[i].number-1, possibleCards) and 
                isThereNumber(possibleCards[i].number-2, possibleCards) and
                isThereNumber(possibleCards[i].number-3, possibleCards) and
                isThereNumber(possibleCards[i].number-4, possibleCards)):

                var.lookForCard1 = possibleCards[i].number
                return True
            
            counter += 1

        i -= 1

    return False
    # Returns True if the player has a straight

def flush(possibleCards):
    for i in range(7):
        equalSuits = 0

        for j in range(7):
            if possibleCards[i].suit == possibleCards[j].suit:
                equalSuits += 1

            if equalSuits == 5:
                var.lookForSuit = possibleCards[i].suit
                return True

    return False
    # Returns True if the player has a flush

def fullHouse(possibleCards):
    if not equalNumber(possibleCards, 3):
        return False
    
    for i in range(7):
        equalNumbers = 0

        if possibleCards[i].number != var.lookForCard1:
            for j in range(7):
                if possibleCards[i].number == possibleCards[j].number:
                    equalNumbers += 1

                if equalNumbers == 2:
                    var.lookForCard2 = possibleCards[i].number
                    return True

    return False
    # Returns True if the player has a full house

def straightFlush(possibleCards):
    if not flush(possibleCards):
        return False
    
    if isThereCard(var.ACE, var.lookForSuit, possibleCards) and isThereCard(10, var.lookForSuit, possibleCards) and isThereCard(var.JACK, var.lookForSuit, possibleCards) and isThereCard(var.QUEEN, var.lookForSuit, possibleCards) and isThereCard(var.KING, var.lookForSuit, possibleCards):
        var.lookForCard1 = 1
        return True
    
    for i in range(3):
        cardCount = 0

        if possibleCards[len(possibleCards)-1-i].number != 1 and possibleCards[len(possibleCards)-1-i].suit == var.lookForSuit:
            lastStraightCard = possibleCards[len(possibleCards)-1-i].number

            j = counter = 1
            while counter < 5:
                if possibleCards[len(possibleCards)-1-i-j].number != possibleCards[len(possibleCards)-2-i-j].number:
                    counter += 1

                    if lastStraightCard - j == possibleCards[len(possibleCards)-1-i-j].number:
                        cardCount += 1

                        if cardCount == 4:
                            var.lookForCard1 = lastStraightCard
                            return True
                    else:
                        break
                
                j += 1
        
    return False
    # Returns True if the player has a straight flush

def royalFlush(possibleCards, player):
    if isThereCard(10, "♦", possibleCards) and isThereCard(var.JACK, "♦", possibleCards) and isThereCard(var.QUEEN, "♦", possibleCards) and isThereCard(var.KING, "♦", possibleCards) and isThereCard(var.ACE, "♦", possibleCards):
        var.listPlayers[player].bestHand = [var.Card(10, "♦"), var.Card(var.JACK, "♦"), var.Card(var.QUEEN, "♦"), var.Card(var.KING, "♦"), var.Card(var.ACE, "♦")]
        return True
    if isThereCard(10, "♣", possibleCards) and isThereCard(var.JACK, "♣", possibleCards) and isThereCard(var.QUEEN, "♣", possibleCards) and isThereCard(var.KING, "♣", possibleCards) and isThereCard(var.ACE, "♣", possibleCards):
        var.listPlayers[player].bestHand = [var.Card(10, "♣"), var.Card(var.JACK, "♣"), var.Card(var.QUEEN, "♣"), var.Card(var.KING, "♣"), var.Card(var.ACE, "♣")]
        return True
    if isThereCard(10, "♥", possibleCards) and isThereCard(var.JACK, "♥", possibleCards) and isThereCard(var.QUEEN, "♥", possibleCards) and isThereCard(var.KING, "♥", possibleCards) and isThereCard(var.ACE, "♥", possibleCards):
        var.listPlayers[player].bestHand = [var.Card(10, "♥"), var.Card(var.JACK, "♥"), var.Card(var.QUEEN, "♥"), var.Card(var.KING, "♥"), var.Card(var.ACE, "♥")]
        return True
    if isThereCard(10, "♠", possibleCards) and isThereCard(var.JACK, "♠", possibleCards) and isThereCard(var.QUEEN, "♠", possibleCards) and isThereCard(var.KING, "♠", possibleCards) and isThereCard(var.ACE, "♠", possibleCards):
        var.listPlayers[player].bestHand = [var.Card(10, "♠"), var.Card(var.JACK, "♠"), var.Card(var.QUEEN, "♠"), var.Card(var.KING, "♠"), var.Card(var.ACE, "♠")]
        return True
    return False
    # Returns True if the playes has a royal flush