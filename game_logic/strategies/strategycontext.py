from game_logic.strategies.computer_strategy import Strategy


class StrategyContext:
    def __init__(self, strategy: Strategy, playground, computer_area) -> None:
        self.playground = playground
        self.computer_area = computer_area
        self.__strategy = strategy
        self.is_turn = False
        self.is_attack = False

    @property
    def strategy(self) -> Strategy:
        return self.__strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self.__strategy = strategy

    def make_computer_move(self, is_attack):
        card_to_play = self.pick_card(is_attack)
        if card_to_play is not None:
            card_to_play.face_up()
            # Add the card and mat to the main area
            self.playground.add_new_card(card_to_play)
            # Remove the card and mat from the computer_area area
            self.computer_area.remove_card(card_to_play)
            return True
        elif card_to_play is None:
            return False

    def pick_card(self, is_attack):
        if is_attack:
            return self.strategy.compute_best_attack_move()
        else:
            return self.strategy.compute_best_defense_move()

    def validate_defence_move(self, bottom_card, top_card):
        return self.strategy.validate_defence_move(bottom_card, top_card)

    def validate_attack_move(self, card):
        return self.strategy.validate_attack_move(card)

    def take_cards_from_main_area(self):
        return self.playground.get_and_remove_all_cards()
