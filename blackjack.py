# Problem Set 4
# Name: Katherine Kostecki
# Collaborators: Aaron Zhu
# Time Spent: 4:30
# Late Days Used: (only if you are using any)

import random
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import random
from ps4_classes import BlackJackCard, CardDecks, Busted


#############
# PROBLEM 1 #
#############
class BlackJackHand:
    """
    A class representing a game of Blackjack.   
    """

    # Do not modify these three lines, they provide an interface for the tester!
    HIT = 'hit'
    STAND = 'stand'
    DS = 'double-stand'
    #########################

    def __init__(self, deck, init_bet=1.0):
        """
        Parameters:
        deck - An instance of CardDeck that represents the starting shuffled
               card deck (this deck itself contains one or more standard card decks)
        init_bet - float, represents the init bet/wager of the hand

        Attributes:
        self.deck - CardDeck, represents the shuffled card deck for this game of BlackJack
        self.current_bet - float, represents the current bet/wager of the hand
        self.player - list, initialized with the first 2 cards dealt to the player
                      and updated as the player is dealt more cards from the deck
        self.dealer - list, initialized with the first 2 cards dealt to the dealer
                      and updated as the dealer is dealt more cards from the deck

        Important: You MUST deal out the first four cards in the following order:
            player, dealer, player, dealer
            
            You may find the deal_card function (and others) in ps4_classes.py helpful.
        """
        self.deck = deck
        self.current_bet = init_bet
        self.player = []
        self.dealer = []
        
        self.player.append(deck.deal_card())
        self.dealer.append(deck.deal_card())
        self.player.append(deck.deal_card())
        self.dealer.append(deck.deal_card())

    # Do not modify!
    def set_bet(self, new_bet):
        """
        Sets the player's current wager in the game.

        Parameters:
        new_bet - the floating point number representing the new wager for the game.

        Do not modify!
        """
        self.current_bet = new_bet

    # Do not modify!
    def get_bet(self):
        """
        Returns the player's current wager in the game.

        Returns:
        self.current_bet, the floating point number representing the current wager for the game

        Do not modify!
        """
        return self.current_bet
        
    # Do not modify this function!
    def set_initial_cards(self, player_cards, dealer_cards):
        """
        Sets the initial cards of the game.
        player_cards - list, containing the inital player cards
        dealer_cards - list, containing the inital dealer cards

        used for testing, DO NOT MODIFY
        """
        self.player = player_cards[:]
        self.dealer = dealer_cards[:]

    # You can call the method below like this:
    #   BlackJackHand.best_value(cards)
    @staticmethod
    def best_value(cards):
        """
        Finds the total value of the cards. All cards must contribute to the
        best sum; however, an Ace may contribute a value of 1 or 11.

        The best sum is the highest point total not exceeding 21 if possible.
        If it is not possible to keep the total value from exceeding 21, then
        the best sum is the lowest total value of the cards.

        Hint: If you have one Ace, give it a value of 11 by default. If the sum
        point total exceeds 21, then give it a value of 1. What should you do
        if cards has more than one Ace?

        Parameters:
        cards - a list of BlackJackCard instances.

        Returns:
        int, best sum of point values of the cards  
        """
        value = 0
        num_aces = 0
        
        for card in cards: #add value of all cards
            value += card.get_val()
            if card.get_val() == 11: #count number of aces
                num_aces += 1
                
        
        if value > 21: #if above 21, turn aces from 11 to 1 until value is below 21 or out of aces
            for ace in range(num_aces):
                if value > 21:
                    value -= 10
                    
        return value
        
            
    def get_player_cards(self):
        """
        Returns:
        list, a copy of the player's cards 
        """
        return self.player.copy()

    def get_dealer_cards(self):
        """
        Returns:
        list, a copy of the dealer's cards 
        """
        return self.dealer.copy()

    def get_dealer_upcard(self):
        """
        Returns the dealer's face up card. We define the dealer's face up card
        as the first card in their hand.

        Returns:
        BlackJackCard instance, the dealer's face-up card 
        """
        return self.dealer[0]

    # Strategy 1
    def copy_dealer_strategy(self):
        """
        A playing strategy in which the player uses the same metric as the
        dealer to determine their next move.

        The player will:
            - hit if the best value of their cards is less than 17
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision  
        """
        #hit if under 17, otherwise stand
        if self.best_value(self.get_player_cards()) < 17:
            return "hit"
        else:
            return "stand"

    # Strategy 2
    def cheating_strategy(self):
        """
        A playing strategy in which the player knows the best value of the
        dealer's cards.

        The player will:
            - hit if the best value of their hand is less than that of the dealer's
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision
        """
        #hit if lower than dealer, otherwise stand
        if self.best_value(self.get_player_cards()) < self.best_value(self.get_dealer_cards()):
            return "hit"
        else:
            return "stand"

    # Strategy 3
    def basic_strategy(self):
        """
        A playing strategy in which the player will
            - stand if one of the following is true:
                - the best value of player's hand is greater than or equal to 17
                - the best value of player's hand is between 12 and 16 (inclusive)
                  AND the dealer's up card is between 2 and 6 (inclusive)  
            - hit otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision 
        """
        
        #stand if above/equal to 17
        if self.best_value(self.get_player_cards()) >= 17:
            return "stand"
        
        #stand if between 12&16 and dealer upcard is between 2&6, otherwise hit
        elif (self.best_value(self.get_player_cards()) >= 12) and (self.best_value(self.get_player_cards()) <= 16) and (self.get_dealer_upcard().get_val() >= 2) and (self.get_dealer_upcard().get_val() <= 6):
            return "stand"
        else:
            return "hit"

    # Strategy 4
    def double_stand_strategy(self):
        """
        A playing strategy in which the player will
            - double-stand (DS) if the following is true:
                - the best value of the player's cards is 11
            - else they will fall back to using basic_strategy

        In our game, we allow "doubling stand" (DS) on any turn, rather than just the first turn.

        The double stand action indicates a special, somewhat risky, but possibly rewarding player
        action. It means the player wishes to double the current bet of the hand, hit one more time,
        and then immediately stand, ending their turn with whatever cards result. 

        This strategy simply consists of signaling to that the calling function with the action
        BlackJackHand.DS when the sum of the players cards is 11, which is a very good
        position in which to try to double one's bet while getting only one more card. Otherwise,
        the strategy falls back to using the basic_strategy to play normally.
        
        NOTE: This function should not double your bet.

        Returns:
        str, "double-stand" if player_best_score == 11,
             otherwise the return value of calling basic_strategy to play in the default way
        """
        #double stand when at 11
        if self.best_value(self.get_player_cards()) == 11:
            return "double-stand"
        
        #stand when above 17 (or equal to)
        elif self.best_value(self.get_player_cards()) >= 17:
            return "stand"
        
        #if between 12&16 and dealer upcard is between 2&6, stand, otherwise hit
        elif (self.best_value(self.get_player_cards()) >= 12) and (self.best_value(self.get_player_cards()) <= 16) and (self.get_dealer_upcard().get_val() >= 2) and (self.get_dealer_upcard().get_val() <= 6):
            return "stand"
        else:
            return "hit"

    # Strategy 5
    def random_strategy(self):
        """
        A playing strategy in which the player will
            - stand if the following is true:
                - the best value of player's hand is greater than or equal to 16
            - hit if the following is true:
                - the best value of player's hand is less than or equal to 12
            - otherwise:
                - toss a coin and hit if the result of the coin toss is a head, stand otherwise
                  (the 'random' library is already imported for you - think of ways to mimic a coin toss through it).

        Returns:
        str, "hit" or "stand" representing the player's decision
        """
        #stand when above/equal to 16
        if self.best_value(self.get_player_cards()) >= 16: 
            return "stand"
        
        #hit if below/equal to 12
        elif self.best_value(self.get_player_cards()) <= 12:
            return "hit"
        
        #randomly choose when between 12 and 16
        else:
            if random.randint(0,1) == 1:
                return "hit"
            else:
                return "stand"

    def play_player_turn(self, strategy):
        """
        Plays a full round of the player's turn and updates the player's hand
        to include new cards that have been dealt to the player (a hit). The player
        will be dealt a new card until they stand, bust, or double-stand.

        With double-stand, the player doubles their bet, receive one final hit, and
        then they stand. The hit with double-stand strategy (like any hit) can cause the player to
        go bust.

        The following will guide you through some design requirements for this function. 

        This function must _repeatedly_ query the strategy for the next action, until the action
        is to stand, or until their hand's best value is over 21, which should then raise a Busted
        exception (imported from ps4_classes.py) to signal this sad outcome to the caller.

        Remember, receiving the double-stand action from a strategy indicates:
            - the player wishes to double their current bet,
            - the player receives one last hit,
            - the player then immediately stands, ending their turn

        Remember, 
            - Whenever hitting, always signal to the caller if the best value of the 
              player's hand becomes greater than 21 (because the player has busted).

        Parameter:
        strategy - function, one of the the 4 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.copy_dealer_strategy, BlackJackHand.double_stand_strategy)

        Returns:          
        This function does not return anything.

        """
        next_move = ""
        next_move = strategy(self)
   
        #play hand until they stand
        while next_move != "stand":
            if next_move == "hit": #when 'hit', get a new card and check if player is still under 21
                self.player.append(self.deck.deal_card())
                if self.best_value(self.get_player_cards()) > 21: #bust if card puts them over 21
                    raise Busted
                else:
                    next_move = strategy(self)
                    
            elif next_move == "double-stand": #double stand changes the bet and ends the round for the player even if they don't bust
                self.set_bet(2*self.current_bet)
                self.player.append(self.deck.deal_card())
                if self.best_value(self.get_player_cards()) > 21: #bust if card puts them over 21
                    raise Busted
                    
                else: #game ends after double-stand so stand if cards are under 21
                    next_move = "stand"

    def play_dealer_turn(self):
        """
        Plays a full round of the dealer's turn and updates the dealer's hand
        to include new cards that have been dealt to the dealer. The dealer
        will get a new card as long as the best value of their hand is less
        than 17. If they go over 21, they bust.

        This function does not return anything. Instead, it:
            - Adds a new card to self.dealer each time the dealer hits.
            - Raises Busted exception (imported from ps4_classes.py) if the
              best value of the dealer's hand is greater than 21.
        """
        
        while self.best_value(self.get_dealer_cards()) < 17: #only hit when value is under 17
            self.dealer.append(self.deck.deal_card())
        
            if self.best_value(self.get_dealer_cards()) > 21: #make sure next card doesn't make them bust
                raise Busted
                
                
                
               
        
    def __str__(self):
        """
        Returns:
        str, representation of the player and dealer and dealer hands.

        Useful for debugging. DO NOT MODIFY. 
        """
        result = 'Player: '
        for c in self.player:
            result += str(c) + ','
        result = result[:-1] + '    '
        result += '\n   Dealer '
        for c in self.dealer:
            result += str(c) + ','
        return result[:-1]

#############
# PROBLEM 2 #
#############


def play_hand(deck, strategy, init_bet=1.0):
    """
    Plays a hand of Blackjack and determines the amount of money the player
    gets back based on the bet/wager of the hand.

    The player will get:

        - 2.5 times the bet of the hand if the player's first two cards equal 21,
          and the dealer's first two cards do not equal 21.

        - 2 times the bet of the hand if the player wins by having a higher best value than 
          the dealer after the dealer's turn concludes

        - 2 times the bet of the hand if the dealer busts

        - the exact bet amount of the hand if the game ends in a tie. 
          If the player and dealer both get blackjack from their first two cards, 
          this is also a tie.

        - 0 if the dealer wins with a higher best value, or the player busts.

        Remember, the double-stand strategy doubles the current bet under certain conditions.
        You do not have to worry about doubling the bet here for any double-stand if
        your double-stand strategy properly signals to alter the bet of the hand during the
        player's turn.

        Reminder of how the game flow works:

        1. Deal cards to player, then dealer, then player, then dealer.

        2. Check for initial blackjacks from either player. If at least one person has 
           blackjack, the game is over. Calculate how much the player receives.

        3. If no one has blackjack, then deal the player until they stand or bust 
           (use your play_player_turn function).

           If you catch a Busted exception from the player playing their turn,
           the player busted, and the game is over. Calculate how much the player receives.

        4. If the player has not bust, then deal the dealer until they stand or bust.
           (use your play_dealer_turn function).
           If the dealer busts, the game is over. Calculate how much the player receives.

        5. If no one has bust, determine the outcome of the game based on the
            best value of the player's cards and the dealer's cards.

    Parameters:
        deck - an instance of CardDeck
        strategy - function, one of the the four playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.copy_dealer_strategy)
        init_bet - float, the amount that the player initially bets (default=1.0)

    Returns:
        tuple (float, float): (amount_wagered, amount_won)
               amount_wagered, the current bet of the hand. Should use hand.get_bet().
               amount_won, the amount of money the player gets back. Should be 0 if they busted and lost.
    """
    game = BlackJackHand(deck, init_bet)
      
    #after intial cards are dealt 
    #if both blackjack after intitial deal, gain the bet back
    if game.best_value(game.get_player_cards()) == 21 and game.best_value(game.get_dealer_cards()) == 21:
        return (game.get_bet(), game.get_bet())
    
    #if player has blackjack but not dealer, win 2.5 times the bet
    if game.best_value(game.get_player_cards()) == 21 and game.best_value(game.get_dealer_cards()) != 21:
        return (game.get_bet(), 2.5*game.get_bet())
    
    #if dealer gets blackjack but not player, don't gain money
    if game.best_value(game.get_player_cards()) != 21 and game.best_value(game.get_dealer_cards()) == 21:
        return (game.get_bet(), 0)
    
    
    #if no winner after initial deal
    #play the player
    try:
        game.play_player_turn(strategy)   
    except Busted:
        return(game.get_bet(), 0)
    
    #play dealer
    try:
        game.play_dealer_turn()  
    except Busted:
        return (game.get_bet(), 2*game.get_bet())
    
    
    #determine result of game
    #get bet back if there is a tie
    if game.best_value(game.get_player_cards()) == game.best_value(game.get_dealer_cards()):
        return (game.get_bet(), game.get_bet())
    
    #get 2 times the bet back if have a higher value than the dealer
    if game.best_value(game.get_player_cards()) > game.best_value(game.get_dealer_cards()):
        return (game.get_bet(), 2*game.get_bet())
    
    #don't get any money if dealer has a higher value than the player
    if game.best_value(game.get_player_cards()) < game.best_value(game.get_dealer_cards()):
        return (game.get_bet(), 0)
    
    
 
    
#############
# PROBLEM 3 #
#############


def run_simulation(strategy, init_bet=2.0, num_decks=8, num_hands=20, num_trials=100, show_plot=False):
    """
    Runs a simulation and generates a normal distribution reflecting 
    the distribution of player's rates of return across all trials.

    The normal distribution is based on the mean and standard deviation of 
    the player's rates of return across all trials. 
    You should also plot the histogram of player's rates of return that 
    underlies the normal distribution. 
    For hints on how to do this, consider looking at 
        matplotlib.pyplot
        scipy.stats.norm.pdf

    For each trial:

        - instantiate a new CardDeck with the num_decks and type BlackJackCard
        - for each hand in the trial, call play_hand and keep track of how
          much money the player receives across all the hands in the trial
        - calculate the player's rate of return, which is
            100*(total money received-total money bet)/(total money bet)

    Parameters:

        strategy - function, one of the the four playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.copy_dealer_strategy)
        init_bet - float, the amount that the player initially bets each hand. (default=2)
        num_decks - int, the number of standard card decks in the CardDeck. (default=8)
        num_hands - int, the number of hands the player plays in each trial. (default=20)
        num_trials - int, the total number of trials in the simulation. (default=100)
        show_plot - bool, True if the plot should be displayed, False otherwise. (default=False)

    Returns:

        tuple, containing the following 3 elements:
            - list of the player's rate of return for each trial
            - float, the average rate of return across all the trials
            - float, the standard deviation of rates of return across all trials


    MORE PLOTTING HINTS:

    y_values = stats.norm.pdf(x_values, avg, std), This function returns the y-values of the normal distribution
    make sure x_values passed in are sorted. avg and std can be calculated using some numpy functions. 


    """
    return_rates = []
    
    #run trials
    for trial in range(num_trials):
        money_returned = 0
        total_bet = 0
        deck = CardDecks(num_decks, BlackJackCard) #new deck each trial
        for hand in range(num_hands): #play game for all hands
            result = play_hand(deck, strategy, init_bet)
            money_returned += result[1]
            total_bet += result[0]
        return_rates.append(100*(money_returned - total_bet)/(total_bet)) #add return rate of each trial to a list
    
    #calculate mean and standard deviation
    mean = np.mean(return_rates)
    std = np.std(return_rates) 
    
    
    #plot histogram and normal curve
    if show_plot == True:    
        
        x_vals = np.sort(return_rates) #sort the return rates on the axis
        y_vals = stats.norm.pdf(x_vals, mean, std)
        
        plt.hist(x_vals, bins = 10, density = True)
        plt.plot(x_vals, y_vals)
        plt.xlabel("% Return")
        plt.title("Player ROI on Playing "+ str(num_hands) + " Hands (" + str(strategy.__name__) + ") \n (Mean = " + str(mean) + "%, SD = " + str(std) + "%)")
        plt.show()
        
    return(return_rates, mean, std)
    


def run_all_simulations(strategies):
    """
    Runs a simulation for each strategy in strategies and generates a single graph with normal 
    distribution plot for each strategy. No need to graph the underlying histogram. Each guassian 
    (another name for normal) distribution should reflect the distribution of rates of return 
    for each strategy.

    You might find scipy.stats (imported as stats) helpful.

    You might find matplotlib.pyplot (imported as plt) helpful.

    Make sure to label each plot with the name of the strategy and the x axis label.

    Parameters:

        strategies - list of strategies to simulate
    """
    for strategy in strategies: #run simulation for each strategy and generate normal curves
        simulation = run_simulation(strategy)
        x_vals = np.sort(simulation[0])
        y_vals = stats.norm.pdf(x_vals, simulation[1], simulation[2])
        plt.plot(x_vals, y_vals, label = str(strategy.__name__))
    
    #add labels, title, and legend
    plt.xlabel("% Return")
    plt.title("Player ROI for Different Strategies")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    #
    # You can uncomment pieces of the following to test each strategy separately.
    #
    # Default plots:
    #
    run_simulation(BlackJackHand.copy_dealer_strategy, show_plot=True)
    run_simulation(BlackJackHand.cheating_strategy, show_plot=True)
    run_simulation(BlackJackHand.basic_strategy, show_plot=True)
    run_simulation(BlackJackHand.double_stand_strategy, show_plot=True)

    # # Uncomment to run all simulations:

    run_all_simulations([BlackJackHand.copy_dealer_strategy,
                        BlackJackHand.cheating_strategy,
                        BlackJackHand.basic_strategy,
                        BlackJackHand.double_stand_strategy])
# #
    pass
    