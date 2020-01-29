import random

suits = ("Hearts","Diamonds","Spades","Clubs")
ranks = ("Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace")
values = {"Two":2, "Three":3,"Four":4,"Five":5,"Six":6,"Seven":7,"Eight":8,"Nine":9,"Ten":10,"Jack":10,
          "Queen":10,"King":10,"Ace":11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))  # build Card objects and add them to the list
    
    def __str__(self):
        deck_comp = ''  
        for card in self.deck:
            deck_comp += '\n ' + card.__str__() 
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card              

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self,card):
        #card is actually the card from Deck.deal() --> single Card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]
        
        #track our aces
        if card.rank == "Ace":
            self.aces += 1
        
    def adjust_for_ace(self):
        
        #if total value of hand > 21 and there is an ACE in the hand
        #Then treat the value of ace to be 1 instead of 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
        
class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
        
def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input("How many chips would you like to bet? : "))
        except ValueError:
            return "Sorry, the bet must be an integer!"
        else:
            if chips.bet > chips.total:
                print(f"Sorry, your bet can't exceed {chips.total}.")
            else:
                break

def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing
    
    while True:
        x = input("Would you like to hit or stand? Enter 'h' for hit and 's' for stand: ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)
            
        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False
            
        else:
            print("Sorry,try again.")
            continue
            
        break    

def show_some(player,dealer):
    #show 1 of dealer's cards
    print("\nDealer's Hand: ")
    print("<card hidden>")
    print('',dealer.cards[1])
    
    #show all of player's cards
    print("\nPlayer's Hand: ", *player.cards, sep = '\n')
    
    
def show_all(player,dealer):
    #show allof player and dealer's cards as well as their values
    print("\nDealer's Hand: ",*dealer.cards, sep = '\n')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand: ",*player.cards,sep = '\n')
    print("Player's Hand =",player.value)


#player got >21 so he loses the hand and also the bet
def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

#player got 21 so he wins the hand and the bet
def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

#dealer got >21 so he loses the hand and also the bet
def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()

#dealer got 21 so he wins the hand and the bet
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()

#both player and dealer got 21
def push(player,dealer):
    print("Player and Dealer tie. It's a push!")    

while True:
    
    print("Welcome to BlackJack. Get as close to 21 as you can without going over.\nDealer hits until he reaches 17. Aces are counted as 1 or 11.")
    
    #create and shuffle the deck.
    deck = Deck()
    deck.shuffle()
    
    #create a player and deal 2 cards to that player
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    #create a dealer and deal 2 cards to the dealer
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    #set up player's chips and take his bet
    player_chips = Chips()
    take_bet(player_chips)
    
    #show both of player's cards and one of the dealer's --> show_some()
    show_some(player_hand,dealer_hand)
    
    #start the game , recall variable from the hit_or_stand() function
    while playing:
        
        #prompt for player to hit or stand
        hit_or_stand(deck,player_hand)
        
        #show cards after player hits/stands but keep one dealer card hidden
        show_some(player_hand,dealer_hand)
        
        #if player's hand >21 call player_busts and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break
            
    #if player has not busted play dealer's hand until dealer reaches 17
    if player_hand.value <= 21:
            
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)
                
        #show all cards
        show_all(player_hand,dealer_hand)
            
        #run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
                
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
                
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
                
        else:
            push(player_hand,dealer_hand)
                
    #inform player of their total chips
    print(f"\n Player's winning stand at {player_chips.total}")
        
    #ask to play again
    new_game = input("Would you like to start a new game? Enter 'y' or 'n': ")
        
    if new_game[0].lower() =='y':
        playing = True
        continue
            
    else:
        print("Thanks for playing!")
        break
        