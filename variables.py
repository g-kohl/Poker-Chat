# Libraries:
from dataclasses import dataclass

# Classes:
@dataclass
class Card:
    number: int
    suit: str

@dataclass
class Player:
    name : str
    cards: [] # List of Data Class 'Cards'
    cash: int
    active: bool
    currentBet: int
    handValue: int
    bestHand: [] # List of Data Class 'Cards'

# Constants:
ACE = 1
JACK = 11
QUEEN = 12
KING = 13

FOLD = 1
CHECK = 2
CALL = 3
RAISE = 4

USER = 0

HIGHCARD = 1
PAIR = 2
TWOPAIRS = 3
THREEOFAKIND = 4
STRAIGHT = 5
FLUSH = 6
FULLHOUSE = 7
FOUROFAKIND = 8
STRAIGHTFLUSH = 9
ROYALFLUSH = 10

NULLCARD = Card(0, "")

numbers = [ACE, 2, 3, 4, 5, 6, 7, 8, 9, 10, JACK, QUEEN, KING]
suits = ["♦", "♣", "♥", "♠"]

# Global Variables:
playersQuantity = 0
minimalBet = 0
currentPlayer = 0
dealer = 0
pot = 0
toPayBet = 0
lookForCard = 0
listPlayers = [] # List of Data Class 'Player'
communityCards = [NULLCARD, NULLCARD, NULLCARD, NULLCARD, NULLCARD] # List of Data Class 'Cards'
