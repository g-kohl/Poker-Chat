# Libraries:
import random

# Modules:
import variables as var

#=====================
# Initialize the game:
#=====================
def initPlayers():
    for i in range(var.playersQuantity):
        var.listPlayers.append(var.Player("player" + str(i+1), [var.NULLCARD, var.NULLCARD], 20*var.minimalBet, True, 0, 1, []))
    # Initializes the list of players with a standard name, null cards, 20 times the minimal bet as cash, a boolean indicating the activity of the player, 0 as the current bet, 1 as the value of the hand and a empty list for the best hand

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
        print("Your cards are: ")
    else:
        print("Player" + str(player+1) + "'s are: ")

    print(stringCards(var.listPlayers[player].cards[0].number, var.listPlayers[player].cards[0].suit) 
          + " " 
          + stringCards(var.listPlayers[player].cards[1].number, var.listPlayers[player].cards[1].suit))
    # Shows the hand of the current player

#===================
# Control the turns:
#===================
def nextPlayer(player):
    player += 1

    if player >= var.playersQuantity:
        return player - var.playersQuantity
    else:
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

    return flag
    # Returns false if it finds a player the still have to bet/pay, and true if that isn't the case

def countActivePlayers():
    activePlayers = 0

    for i in range(var.playersQuantity):
        if var.listPlayers[i].active:
            activePlayers += 1

    return activePlayers

#======================================
# Control the decisions of the players:
#======================================
def bettingRound():
    for i in range(var.playersQuantity):
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
            print("Player" + str(var.currentPlayer+1) + " folds")
            fold()
            
        case var.CHECK:
            if var.listPlayers[var.currentPlayer].currentBet < var.toPayBet:
                if var.currentPlayer == var.USER:
                    print("You can't check, to continue playing this hand you must either call or raise")

                playerDecision()
            else:
                print("Player" + str(var.currentPlayer+1) + " checks")

        case var.CALL:
            if var.toPayBet == 0:
                if var.currentPlayer == var.USER:
                    print("There is nothing to call, you can fold, check or raise")

                playerDecision() 
            else:
                isAllIn(var.CALL)

        case var.RAISE:
            if var.listPlayers[var.currentPlayer].cash < var.toPayBet:
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
            print("Player" + str(var.currentPlayer+1) + " calls")
        elif decision == var.RAISE:
            print("Player" + str(var.currentPlayer+1) + " raises to " + str(var.toPayBet))
    else:
        allIn()
    # Verifies if is an "all in" situation. If it isn't, just pays the bet

def allIn():
    print("Player" + str(var.currentPlayer+1) + " goes all in!")
    var.pot += var.listPlayers[var.currentPlayer].cash
    var.listPlayers[var.currentPlayer].currentBet += var.listPlayers[var.currentPlayer].cash
    var.listPlayers[var.currentPlayer].cash = 0
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

#=====================
# Control the results:
#=====================
def showdown():
    for i in range(var.playersQuantity):
        if var.listPlayers[i].active:
            var.listPlayers[i].handValue = calculateHand(i)

    bestHand = 0
    for i in range(var.playersQuantity):
        if var.listPlayers[i].active and var.listPlayers[i].handValue > bestHand:
            bestHand = var.listPlayers[i].handValue

    for i in range(var.playersQuantity):
        if var.listPlayers[i].active:
            if var.listPlayers[i].handValue == bestHand:
                print("player" + str(i+1) + " won!" + " (" + printHand(i) + ")")
            else:
                print("player" + str(i+1) + " lost..." + " (" + printHand(i) + ")")

            print(stringCards(var.listPlayers[i].cards[0].number, var.listPlayers[i].cards[0].suit)
                  + " "
                  + stringCards(var.listPlayers[i].cards[1].number, var.listPlayers[i].cards[1].suit))
    # Looks for the player with the best hand

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
        
def sortPossibleCards(possibleCards):
    for i in range(1, 7):
        key = possibleCards[i]
        j = i - 1

        while j >= 0 and key.number < possibleCards[j].number:
            possibleCards[j+i] = possibleCards[j]
            j -= 1

        possibleCards[j+1] = key

    for i in range(7):
        if possibleCards[i] == 1:
            possibleCards.append(possibleCards[i])
    
    return possibleCards
    # Sorts the 7 possible cards to make the hand (insertion sort)

def calculateHand(player):
    possibleCards = sortPossibleCards([var.listPlayers[player].cards[0], var.listPlayers[player].cards[1], var.communityCards[0], var.communityCards[1], var.communityCards[2], var.communityCards[3], var.communityCards[4]])

    if royalFlush(possibleCards, player):
        return var.ROYALFLUSH
    elif straightFlush(possibleCards, player):
        return var.STRAIGHTFLUSH
    elif equalNumber(possibleCards, 4, player):
        return var.FOUROFAKIND
    elif fullHouse(possibleCards, player):
        return var.FULLHOUSE
    elif flush(possibleCards, player):
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

    counter = 3

    for i in range(len(possibleCards)):
        if possibleCards[len(possibleCards)-1-i].number != var.lookForCard1:
            var.listPlayers[player].bestHand[2+i] = possibleCards[len(possibleCards)-1-i]
            counter -= 1

            if counter == 0:
                break
    # Gets the best hand (pair): Pair1, Pair2, Highcards in descending order
            
def getTwoPairs(possibleCards, player):
    highPair = max([var.lookForCard1, var.lookForCard2])
    lowPair = min([var.lookForCard1, var.lookForCard2])

    for i in range(7):
        if possibleCards[i].number == highPair:
            var.listPlayers[player].bestHand[0] = possibleCards[i]
            var.listPlayers[player].bestHand[1] = possibleCards[i+1]
            break

    for i in range(7):
        if possibleCards[i].number == lowPair:
            var.listPlayers[player].bestHand[2] = possibleCards[i]
            var.listPlayers[player].bestHand[3] = possibleCards[i]
            break

    for i in range(7):
        if possibleCards[len(possibleCards)-1-i].number != var.lookForCard1 and possibleCards[len(possibleCards)-1-i].number != var.lookForCard2:
            var.listPlayers[player].bestHand[4] = possibleCards[len(possibleCards)-1-i]
    # Gets the best hand (two pairs): HighPair1, HighPair2, LowPair1, LowPair2, Highcard
            
def getThreeOfAKind(possibleCards, player):
    for i in range(7):
        if possibleCards[i].number == var.lookForCard1:
            var.listPlayers[player].bestHand[0] = possibleCards[i]
            var.listPlayers[player].bestHand[1] = possibleCards[i+1]
            var.listPlayers[player].bestHand[2] = possibleCards[i+2]
            break

    counter = 2

    for i in range(len(possibleCards)):
        if possibleCards[len(possibleCards)-1-i].number != var.lookForCard1:
            var.listPlayers[player].bestHand[3+i] = possibleCards[len(possibleCards)-1-i]
            counter -= 1

            if counter == 0:
                break
    # Gets the best hand (three of a kind): Trio1, Trio2, Trio3, highcards in descending order
            
def getStraight(possibleCards, player):
    for i in range(5):
        for j in range(7):
            if var.lookForCard1 - i == 14:
                if possibleCards[j].number == 1:
                    var.listPlayers[player].bestHand[i] = possibleCards[j]
                    break
            elif var.lookForCard1 - i == possibleCards[j].number:
                var.listPlayers[player].bestHand[i] = possibleCards[j]
                break
    # Gets the best hand (straight): ascending order
            
def getFlush(possibleCards, player):
    cardCount = 0

    for i in range(7):
        if possibleCards[len(possibleCards)-1-i].suit == var.lookForSuit:
            var.listPlayers[player].bestHand[i] = possibleCards[len(possibleCards)-1-i]
            cardCount += 1

            if cardCount == 5:
                break
    # Gets the best hand (flush): descending order
    
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
            if possibleCards[i].number == possibleCards[6-j].number and possibleCards[i].suit != possibleCards[6-j].suit:
                if var.lookForCard1 == 0:
                    var.lookForCard1 = possibleCards[i].number
                else:
                    var.lookForCard2 = possibleCards[i].number

                pairs += 1
                break

    if pairs >= 2:
        return True
    else:
        return False
    # Returns True if the player has two pairs

def straight(possibleCards):
    cardCount = 0

    for i in range(1, 6):
        if isThereNumber(i, possibleCards):
            cardCount += 1

            if cardCount == 5:
                var.lookForCard1 = 5
                return True
        else:
            break

    for i in range(3):
        cardCount = 0

        if possibleCards[len(possibleCards)-1-i].number == 1:
            firstStraightCard = 14
        else:
            firstStraightCard = possibleCards[len(possibleCards)-1-i].number

        for j in range(1, 5):
            if firstStraightCard - j == possibleCards[len(possibleCards)-1-i-j].number:
                cardCount += 1

                if cardCount == 4:
                    var.lookForCard1 = firstStraightCard
                    return True
            else:
                break
    
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

def fullHouse(possibleCards): #ARRUMAR
    if not equalNumber(possibleCards, 3):
        return False

    equalNumbers = 0

    for i in range(7):
        for j in range(6-i):
            if possibleCards[i].number == possibleCards[j].number:
                equalNumbers += 1
                if equalNumbers == 3:
                    numberOfTrio = possibleCards[i].number
                    break
        equalNumbers = 0

    for i in range(7):
        if possibleCards[i].number == numberOfTrio:
            possibleCards[i] == var.NULLCARD

    if equalNumber(possibleCards, 2):
        return True
    else: 
        return False

def straightFlush(possibleCards): # VER QUAL É O MAIOR STRAIGHT FLUSH
    nextCard = 0

    for i in range(7):
        currentSuit = possibleCards[i].suit
        for j in range(4):
            if possibleCards[i].number + j + 1 == 14:
                if isThereCard(var.ACE, currentSuit, possibleCards):
                    nextCard += 1
            elif isThereCard(possibleCards[i].number + j + 1, currentSuit, possibleCards):
                nextCard += 1

        if nextCard == 4:
            return True
        else:
            nextCard = 0
    
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