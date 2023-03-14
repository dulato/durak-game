from game_logic.strategies.computer_strategy import Strategy
from play_areas.playground import Playground
from play_areas.not_active_cards import NotActiveCards
from play_areas.player_area import PlayerArea


class DifficultStrategy(Strategy):
    def __init__(self, computer_area: PlayerArea, playground: Playground,
                 not_active_cards: NotActiveCards, player_area: PlayerArea):
        super().__init__(computer_area, playground, not_active_cards, player_area)
        self.not_played_cards = {"Clubs": [range(6, 15)], "Diamonds": [range(6, 15)], "Hearts": [range(6, 15)], "Spades": [range(6, 15)]}
        self.player = player_area

    def remove_played_cards(self):
        """
        Remove the played cards from the not_played_cards dict
        """
        for card in self.not_active_cards.played_cards:
            if card in self.not_played_cards[card.suit]:
                self.not_played_cards[card.suit].remove(card.value)

    def calc_bot_hand(self):
        """
        Calculates the available cards in the bot hand
        :return: the available cards in the bot hand
        """
        # get the available card suits
        available_cards = {}
        for card in self.computer_area.cards:
            if card.suit != self.not_active_cards.trump_card.suit:
                if card.suit not in available_cards:
                    available_cards[card.suit] = []
                available_cards[card.suit].append(card.value)

        return available_cards

    def lenght_of_suit_not_played(self):
        """
        Calculates how many cards are not played in each suit and sorts them by value
        :return: A dict with the suits and the number of cards that are not played
        """
        # Get the lenght of each suit
        lenght_of_suit = {}
        for suit in self.not_played_cards:
            lenght_of_suit[suit] = len(self.not_played_cards[suit])

        # sort the dict by value
        lenght_of_suit = {k: v for k, v in sorted(lenght_of_suit.items(), key=lambda item: item[1])}

        return lenght_of_suit

    def find_card(self, suit, value):
        """
        Finds the card in the computer_area by finding the intersection of the suit and value
        :param suit: The suit of the card
        :param value: The value of the card
        :return: The card
        """
        suit_lst = self.computer_area.get_cards_with_same_suit_str(suit)
        value_lst = self.computer_area.get_cards_with_same_value_int(value)
        return suit_lst.intersection(value_lst)

    def validate_bot_hand(self, bot_hand):
        """
        Validates the bot hand by removing the cards that are not playable
        :param bot_hand: The bot hand
        :return: The validated bot hand with only playable cards
        """
        # Create a set with all the values that are in the main area
        values = set()
        for card in self.playground.get_all_cards():
            values.add(card.value)

        valid_bot_hand = {}

        # Remove the values that are not in the main area
        for suit in bot_hand:
            for value in bot_hand[suit]:
                if value in values:
                    if suit not in valid_bot_hand:
                        valid_bot_hand[suit] = []
                    valid_bot_hand[suit].append(value)

        return valid_bot_hand

    def compute_best_attack_move(self):
        """
        Computes the best attack move for the bot by checking the available cards in the bot hand and the cards that
        are not played yet. The bot will try to play the card with the lowest value in the suit that has the least cards
        left to play.
        :return: The card that the bot should play
        """
        card_to_play = None
        lenght_of_suit_not_played = self.lenght_of_suit_not_played()
        if len(self.playground.mat_list) == 1:
            bot_hand = self.calc_bot_hand()
            bot_hand_trump = None
            if self.not_active_cards.trump_card.suit in bot_hand:
                # Remove trump suit from the bot hand in extra dict
                bot_hand_trump = bot_hand[self.not_active_cards.trump_card.suit]
                # Remove trump suit from the bot hand
                bot_hand.pop(self.not_active_cards.trump_card.suit)

            # The lenghth_of_suit_not_played dict is sorted by value, so the first key is the suit with the lowest value
            for suit in lenght_of_suit_not_played:
                if suit in bot_hand:
                    card_to_play = min(bot_hand[suit])
                    # find the instance of the card
                    card_to_play = self.find_card(suit, card_to_play)
                    # Get the card out of the set
                    card_to_play = card_to_play
                    break

            if card_to_play is None and bot_hand_trump is not None:
                # Get the minimum value of bot_hand_trump
                card_to_play = min(bot_hand_trump)
                card_to_play = self.find_card(self.not_active_cards.trump_card.suit, card_to_play)

            # If the card_to_play is still None, then the bot should play the lowest card
            elif card_to_play is None:
                card_to_play = min(self.computer_area.cards, key=lambda card: card.value)

        else:
            hand = self.calc_bot_hand()
            valid_bot_hand = self.validate_bot_hand(hand)
            #lenght_of_suit_bot = self.lenght_of_suit_bot(valid_bot_hand)

            if self.not_active_cards.trump_card.suit in valid_bot_hand:
                # Remove trump suit from the bot hand
                valid_bot_hand.pop(self.not_active_cards.trump_card.suit)
            for suit in lenght_of_suit_not_played:
                if suit in valid_bot_hand:
                    card_to_play = min(valid_bot_hand[suit], default=None)
                    card_to_play = self.find_card(suit, card_to_play)
                    break

        if card_to_play is None:
            return None
        # Check if card_to_play is a set
        elif isinstance(card_to_play, set):
            if len(card_to_play) == 0:
                return None
            else:
                return card_to_play.pop()
        else:
            return card_to_play

    def compute_best_defense_move(self):
        """
        Computes the best defense move for the bot by trying to play the card with the lowest value possible
        :return: The card that the bot should play
        """
        # Filter out the unused_cards that are not playable
        bottom_card = self.playground.get_bottom_card()
        # Filter the computer_area cards with the same suit as the bottom card
        cards_with_same_suit = self.computer_area.get_cards_with_same_suit_as_card(bottom_card)
        # Filter out the cards that have a value lower than the bottom card
        cards_with_same_suit = {card for card in cards_with_same_suit if card.value > bottom_card.value}
        # Get the card with the lowest value
        card_to_play = min(cards_with_same_suit, key=lambda card: card.value, default=None)

        if card_to_play is None and bottom_card.suit != self.not_active_cards.trump_card.suit and len(self.not_active_cards.unused_cards) < 20:
            trump_cards = self.computer_area.get_cards_with_same_suit_as_card(self.not_active_cards.trump_card)
            if len(trump_cards) > 0:
                card_to_play = min(trump_cards, key=lambda card: card.value)

        return card_to_play
