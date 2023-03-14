from abc import ABC, abstractmethod

from gui.card import Card
from play_areas.playground import Playground
from play_areas.not_active_cards import NotActiveCards
from play_areas.player_area import PlayerArea


class Strategy(ABC):

    def __init__(self, computer_area: PlayerArea, playground: Playground,
                 not_active_cards: NotActiveCards, player_area: PlayerArea):
        super().__init__()
        self.computer_area = computer_area
        self.playground = playground
        self.not_active_cards = not_active_cards

    @abstractmethod
    def compute_best_attack_move(self):
        pass

    @abstractmethod
    def compute_best_defense_move(self):
        pass

    def validate_defence_move(self, bottom_card, top_card):
        if bottom_card.suit == top_card.suit:
            if top_card.value > bottom_card.value:
                return True
        elif top_card.suit == self.not_active_cards.trump_card.suit and bottom_card.suit != self.not_active_cards.trump_card.suit:
            return True
        return False

    def validate_attack_move(self, top_card):
        if len(self.playground.cards[0]) == 0 and isinstance(top_card, Card):
            return True
        else:
            # Get all the unused_cards from the main area
            cards = self.playground.get_all_cards()
            # create a set with all the values from the unused_cards
            values = {card.value for card in cards}
            if top_card.value in values:
                return True
        return False

