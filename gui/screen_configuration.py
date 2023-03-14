import math

import arcade


class ScreenConfiguration:
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.screen_title = "Durak"
        self.__standard_screen_diagonal = math.sqrt(1920**2 + 1080**2)

    def init_current_screen(self):
        self.current_x, self.current_y = arcade.get_window().get_size()
        self.current_diagonal = math.sqrt(self.current_x ** 2 + self.current_y ** 2)
        self.screen_ratio = self.current_diagonal / self.__standard_screen_diagonal
        self.__init_card_sizes()

    def __init_card_sizes(self):
        self.card_scale = 0.25 * self.screen_ratio
        self.card_width = 500 * self.card_scale
        self.card_height = 726 * self.card_scale
        self.__init_mat_sizes()

    def __init_mat_sizes(self):
        self.mat_px_oversize = 10 * self.screen_ratio
        self.mat_height = int(self.card_height + self.mat_px_oversize)
        self.mat_width = int(self.card_width + self.mat_px_oversize)
        self.__init_spacing()

    def __init_spacing(self):
        self.vertical_margin_percent = 0.10
        self.horizontal_margin_percent = 0.10

        self.bottom_y = self.mat_height / 2 + self.mat_height * self.vertical_margin_percent
        # The X of where to start putting things on the left side
        self.start_x = self.mat_width / 2 + self.mat_width * self.horizontal_margin_percent
        self.start_x_bottom = self.start_x
        #The X for the bots cards
        self.start_x_top = self.current_x - self.start_x_bottom
        # The Y of the top row
        self.top_y = self.current_y - self.mat_height / 2 - self.mat_height * self.vertical_margin_percent
        # The Y of the middle row
        self.middle_y = self.current_y / 2
        # How far apart each pile goes
        self.x_spacing = self.mat_width + self.mat_width * self.horizontal_margin_percent
        self.__init_values()

    def __init_values(self):
        self.sprite_color = arcade.csscolor.GOLD
        self.card_values = ["6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.card_suites = ["Clubs", "Hearts", "Spades", "Diamonds"]
