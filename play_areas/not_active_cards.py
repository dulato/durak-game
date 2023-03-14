import random

import arcade

from gui.screen_configuration import ScreenConfiguration


class NotActiveCards:
    def __init__(self, config: ScreenConfiguration):
        self.unused_cards = arcade.SpriteList()
        self.played_cards = arcade.SpriteList()
        self.config = config
        self.trump_card = None

    def get_played_cards(self):
        return self.played_cards

    def get_unused_cards(self):
        return self.unused_cards

    def add_new_card(self, card):
        self.unused_cards.append(card)

    # remove and return card from the list at index
    def remove_card(self, index):
        return self.unused_cards.pop(index)

    # remove and return last card from the list
    def remove_last_card(self):
        if len(self.unused_cards) > 1:
            return self.unused_cards.pop()
        elif len(self.unused_cards) == 1:
            card = self.unused_cards.pop()
            card.angle = 0
            return card

    def set_trump_card(self, card):
        self.trump_card = card

    def add_played_card(self, card):
        # Check if the angle is 0, if not, set it to a random angle
        angle = random.randint(0, 3)
        random_offset = random.randint(0, 5)
        center_y = self.config.current_y / 2 + random_offset
        center_x = self.config.start_x + self.config.x_spacing * 2 + random_offset
        card.change_angle = angle
        card.destination_point = center_x, center_y

        card.face_down()
        self.played_cards.append(card)
