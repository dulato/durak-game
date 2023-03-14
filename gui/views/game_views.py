import arcade
import arcade.gui
from arcade import SpriteList

from game_logic.game_logic import GameLogic
from gui.buttons.finish_move_buton import FinishMoveButton
from gui.buttons.take_cards_button import TakeCardsButton
from gui.card import Card

from play_areas.playground import Playground
from play_areas.not_active_cards import NotActiveCards
from play_areas.player_area import PlayerArea
from gui.screen_configuration import ScreenConfiguration
import gui.view_manager


class GameView(arcade.View):
    """ Main application class. """

    def __init__(self, screen_config: ScreenConfiguration, difficulty: int):
        self.config = screen_config
        super().__init__()

        self.view_manager = gui.view_manager.ViewManager()

        arcade.set_background_color(arcade.color.AMAZON)
        # Show buttons if needed
        self.show_btn = False

        # List of unused_cards we are dragging with the mouse
        self.held_card = None

        # Original location of unused_cards we are dragging with the mouse in case
        # they have to go back.
        self.held_card_original_position = None

        # Sprite list with all the mats that unused_cards lay on.
        self.mat_list: arcade.SpriteList = arcade.SpriteList()

        # Flag for checking if card was moved to new area
        self.card_moved = False

        # Initialize the sprite lists
        self.playground = Playground(self.config)
        self.human_player = PlayerArea(self.config.start_x_bottom, self.config.bottom_y,
                                       self.config.x_spacing, self.config.current_x)
        self.computer_player = PlayerArea(self.config.start_x_top, self.config.top_y,
                                          -self.config.x_spacing, self.config.current_x)
        self.not_active_cards = NotActiveCards(self.config)

        # Initialize the utils so we can use helper functions
        self.game_logic = GameLogic(self.human_player, self.computer_player, self.playground, self.not_active_cards,
                                    difficulty)
        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        self.finish_move_button = FinishMoveButton(self.playground, self.game_logic, self.human_player,
                                                   self.computer_player)
        self.v_box.add(self.finish_move_button.with_space_around(bottom=20))

        self.take_cards_button = TakeCardsButton(self.playground, self.game_logic, self.human_player)
        self.v_box.add(self.take_cards_button.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_y=self.config.bottom_y - self.config.card_height * 2,
                child=self.v_box)
        )
        self.hint_text = "Your turn!\nAttack!"
        self.computer_text = ""
        self.trump_card_text = ""

        self.setup()

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # List of unused_cards we are dragging with the mouse
        self.held_card = arcade.Sprite

        # Original location of unused_cards we are dragging with the mouse in case
        # they have to go back.
        self.held_card_original_position = ()

        # init main playing area with one sprite
        self.playground.add_new_sprite()

        # Create every card
        for card_suit in self.config.card_suites:
            for card_value in self.config.card_values:
                card = Card(card_suit, card_value, self.config.card_scale)
                card.position = self.config.start_x, self.config.middle_y
                self.not_active_cards.add_new_card(card)

        # Shuffle the unused_cards
        self.not_active_cards.get_unused_cards().shuffle()

        for index in range(0, 12):
            card = self.not_active_cards.remove_last_card()
            if index < 6:
                card.face_up()
                self.human_player.add_new_card(card)
            else:
                self.computer_player.add_new_card(card)

        # Pick the trump card
        trump_card: Card = self.not_active_cards.get_unused_cards()[0]
        self.not_active_cards.set_trump_card(trump_card)
        trump_card.face_up()
        trump_card.angle = 90
        trump_card.center_x = self.config.card_width * 1.2
        self.trump_card_text = "Trump:" + trump_card.suit

    def finish_turn(self):
        if self.computer_player.is_taking:
            self.game_logic.computer_take_cards()
            self.computer_player.is_taking = False
            self.human_player.is_turn = True

        elif self.human_player.is_turn:
            self.human_player.is_turn = False

            self.game_logic.finish_turn()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats for the main card area
        self.playground.get_mats().draw()

        # if any cards placed in the playground draw them
        self.playground.get_all_cards().draw()

        # draw not active cards
        self.not_active_cards.get_unused_cards().draw()

        # draw played cards
        self.not_active_cards.get_played_cards().draw()

        # draw computer_area cards
        self.computer_player.get_cards().draw()

        # draw the label
        arcade.draw_text(self.hint_text, self.config.start_x, self.config.bottom_y + self.config.card_height,
                         arcade.color.BLACK, 24)
        # draw the label
        arcade.draw_text(self.computer_text, self.config.start_x, self.config.top_y - (self.config.card_height * 1.5),
                         arcade.color.BLACK, 24)

        arcade.draw_text(self.trump_card_text, self.config.current_x - 2 * self.config.x_spacing,
                         self.config.bottom_y + self.config.card_height,
                         arcade.color.BLACK, 24)

        if self.show_btn:
            # Draw v_box with buttons
            self.manager.draw()

        # draw player_area cards
        self.human_player.get_cards().draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards: list[arcade.Sprite] = arcade.get_sprites_at_point((x, y), self.human_player.get_cards())

        # Have we clicked on a card?
        if len(cards) > 0:
            # Might be a stack of unused_cards, get the top one
            self.held_card = cards[-1]

            # Check if the card has a destination point, if so, we set the position to the destination
            if self.held_card.destination_point is not None:
                self.held_card.position = self.held_card.destination_point

            # Stop the animation
            self.held_card.destination_point = self.held_card.position

            # Get original position
            self.held_card_original_position = self.held_card.position

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any unused_cards, who cares
        if not isinstance(self.held_card, Card):
            return

        # Find the closest mat, in case we are in contact with more than one
        mat, distance = arcade.get_closest_sprite(self.held_card, self.playground.get_mats())
        reset_position = True

        # See if we are in contact with the closest mat
        if arcade.check_for_collision(self.held_card, mat):
            # Take index of the mat the player_area wants to put his card on
            mat_index = self.playground.get_mats().index(mat)

            # Check if the card can be placed on the mat
            reset_position = self.game_logic.player_move(mat_index, self.held_card)

        # Check if the card must be put back
        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the card's position
            # to its original spot.
            # self.held_card.position = self.held_card_original_position
            self.held_card.destination_point = self.held_card_original_position
        else:
            # Add the card and mat to the main unused_cards list
            self.playground.add_new_card(self.held_card)

            # remove card from human player_area
            self.human_player.remove_card(self.held_card)
            self.human_player.is_turn = False
            self.show_btn = True

        # We are no longer holding unused_cards
        self.held_card = None

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        # If we are holding a card , move them with the mouse
        if isinstance(self.held_card, Card):
            self.held_card.center_x += dx
            self.held_card.center_y += dy

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.view_manager.show_menu_view()

    def on_update(self, delta_time: 1 / 150):
        # Update the cards
        self.human_player.get_cards().on_update(delta_time)
        self.computer_player.get_cards().on_update(delta_time)
        self.playground.get_all_cards().on_update(delta_time)
        self.not_active_cards.get_played_cards().on_update(delta_time)

        # Check if game is over
        self.game_logic.game_over(self.view_manager, self.config)

        self.show_btn, self.hint_text, self.computer_text = self.game_logic.on_update_logic(self.show_btn,
                                                                                            self.hint_text,
                                                                                            self.computer_text)
