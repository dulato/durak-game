from game_logic.strategies.computer_strategy import Strategy


class SimpleStrategy(Strategy):
    def compute_best_attack_move(self):
        """
        This method will compute a move for the computer player by trying to play a card with a lower value.
        :return: The card to play
        """
        card_to_play = None
        if len(self.playground.get_mats()) == 1:
            #print("First move")
            available_cards = self.computer_area.get_cards()
            # Remove the cards that are the same suit as the trump card
            available_cards = {card for card in available_cards if card.suit != self.not_active_cards.trump_card.suit}
            if len(available_cards) == 0:
                card_to_play = None
            elif available_cards is not None:
                card_to_play = min(available_cards, key=lambda card: card.value)
            if card_to_play is None:
                card_to_play = min(self.computer_area.get_cards(), key=lambda card: card.value)
        else:
            # Get all the unused_cards from the main area
            cards = self.playground.get_all_cards()
            # empty set of playable unused_cards
            playable_cards = set()
            # Get the unused_cards with the same value
            for card in cards:
                playable_cards.update(self.computer_area.get_cards_with_same_value_as_card(card))
                # Filter out the unused_cards with the same suit as the trump card
                playable_cards = {card for card in playable_cards if card.suit != self.not_active_cards.trump_card.suit}
                # Get the card with the lowest value
                card_to_play = min(playable_cards, key=lambda card: card.value, default=None)

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
        # Get the card with the lowest value that is higher than the bottom card from cards_with_same_suit
        # Filter out the cards that have a value lower than the bottom card
        cards_with_same_suit = {card for card in cards_with_same_suit if card.value > bottom_card.value}
        # Get the card with the lowest value
        card_to_play = min(cards_with_same_suit, key=lambda card: card.value, default=None)

        if card_to_play is None and bottom_card.suit != self.not_active_cards.trump_card.suit:
            trump_cards = self.computer_area.get_cards_with_same_suit_as_card(self.not_active_cards.trump_card)
            if len(trump_cards) > 0:
                card_to_play = min(trump_cards, key=lambda card: card.value)

        return card_to_play
