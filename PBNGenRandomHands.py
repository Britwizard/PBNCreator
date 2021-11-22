# PBNGenerateRandomHands.py
# version 1 - Initial version
# version 2 - Change to implement option to reject boards if no hand is greater than 11 points
# This is part of the PBN_Generator app
# This module generates a random deal of 52 cards and divides them in 4.
# The passed parameter, Dealer, is one of N,E,W or S.  The returned result has the cards sorted into 4 hands with each suit sorted in order.
# The order of the suits is spades,hearts,diamonds,clubs.  The order of the 4 hands starts with the dealer and goes clockwise.

import random
convert_card={"A":14,"K":13,"Q":12,"J":11,"T":10}
convert_back={"14":"A","13":"K","12":"Q","11":"J","10":"T"}
# This function sorts a suit in the order AKQJT98765432 returning a string.
# If no cards in suit return empty string 
def sortsuit(suitlist):
    sortedsuit = ""
    if len(suitlist) > 0:
        suitlist.sort(reverse=True)  # Sort cards into descending order
# Converts high numbers back into honour cards       
        for i in suitlist:
            if i > 9:
                den=convert_back[str(i)]
            else:
                den=str(i)
            sortedsuit=sortedsuit+den
    return(sortedsuit)        

# This function sorts the cards in a random hand into suits in the order S,H,D,C and sorts each 
# suit in the order AKQJT9876542. Convert honour cards into numbers so that they can be sorted.
def sorthand(hand):
    handspades = []
    handhearts = []
    handdiamonds=[]
    handclubs=[]
    for card in hand:
        den = card[0:1]
        suit = card[1:2]
        
        if den.isalpha():
            num=convert_card[den] 
        else:
            num=int(den)
        if suit=="S":
            handspades.append(num)
            continue
        if suit=="H":
            handhearts.append(num)
            continue
        if suit=="D":
            handdiamonds.append(num)
            continue
        handclubs.append(num)
# The following code is better, but match/case is a new feature in Python 3.10
# and pyinstaller does not seem to handle it - it generate a 'module PBNGenRandomHands
# not found' error at run time.
        # match suit:
        #     case 'S': handspades.append(num)
        #     case 'H': handhearts.append(num)
        #     case 'D': handdiamonds.append(num)
        #     case 'C': handclubs.append(num)

    # Sort each of the suits into descending order and concatenate them with a '.' between each suit
    sortedspades = sortsuit(handspades)
    sortedhearts = sortsuit(handhearts)
    sorteddiamonds = sortsuit(handdiamonds)
    sortedclubs = sortsuit(handclubs)
    sortedhand = sortedspades + "." + sortedhearts +"." + sorteddiamonds + "." + sortedclubs 
    return sortedhand

# This is the function that is called in this module.  
# It generates a board with random hands but if the 'passedout' option is set to '1' it will check that at least one
# hand has more than 11 points otherwise it will reject the board and generate a new one. 
def GenerateRandomHand(Dealer,passedout):
#Shuffle a pack of 52 playing cards
    Lessthan11= True
    
    while Lessthan11:    
        spades = ["AS","KS","QS","JS","TS","9S","8S","7S","6S","5S","4S","3S","2S"]
        hearts = ["AH","KH","QH","JH","TH","9H","8H","7H","6H","5H","4H","3H","2H"]
        diamonds= ["AD","KD","QD","JD","TD","9D","8D","7D","6D","5D","4D","3D","2D"]
        clubs = ["AC","KC","QC","JC","TC","9C","8C","7C","6C","5C","4C","3C","2C"]
        cards = spades.copy()
        for i in hearts:
            cards.append(i)
        for i in diamonds:
            cards.append(i)
        for i in clubs:
            cards.append(i)

        random.shuffle(cards)

        # Divide shuffled into 4 hands
        NorthHand = cards[0:13]
        EastHand = cards[13:26]
        SouthHand = cards[26:39]
        WestHand = cards[39:52]
        if passedout == '1':
            Lessthan11 = Checkpassedouthand(NorthHand,EastHand,SouthHand,WestHand)
        else:
            Lessthan11=False
    #Sort the hands
    N=sorthand(NorthHand)
    E=sorthand(EastHand)
    S=sorthand(SouthHand)
    W=sorthand(WestHand)
    
    if Dealer == "N":
        result =  Dealer+":" + N + " " + E + " " + S + " " + W 
    if Dealer == "E":
        result =  Dealer+":" + E + " " + S + " " + W + " " + N 
    if Dealer == "S":
        result =  Dealer+":" + S + " " + W + " " + N + " " + E 
    if Dealer == "W":
       result =   Dealer+":" + W + " " + N + " " + E +  " " + S
    return result
# check hands to make sure one has at least 11 HCP.
def Checkpassedouthand(NorthHand,EastHand,SouthHand,WestHand):
    if HCPcount(NorthHand) > 11: return False
    if HCPcount(EastHand) > 11: return False
    if HCPcount(SouthHand) > 11: return False
    if HCPcount(WestHand) > 11: return False
    return True

def HCPcount(Hand):
    HCP=0
    for Card in Hand:
        Value = Card[:1]
        if Value=='A': 
            HCP+=4
            continue
        if Value=='K':
            HCP+=3
            continue
        if Value=='Q':
            HCP+=2
            continue
        if Value=='J':
            HCP+=1
            continue
# The following code is better, but match/case is a new feature in Python 3.10
# and pyinstaller does not seem to handle it - it generate a 'module PBNGenRandomHands
# not found' error at run time.
        # match Value:
        #     case 'A': HCP+=4
        #     case 'K': HCP+=3
        #     case 'Q': HCP+=2
        #     case 'J': HCP+=1
    return HCP
        
