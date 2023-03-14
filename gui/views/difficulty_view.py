import arcade
import arcade.gui

from Constants import EASY, MEDIUM, HARD
from gui.buttons.difficulty_button import DifficultyButton
from gui.screen_configuration import ScreenConfiguration
import gui.view_manager


class DifficultyView(arcade.View):
    def __init__(self, screen_config: ScreenConfiguration):
        super().__init__()

        # This is the manager used to switch between views
        self.view_manager = gui.view_manager.ViewManager()

        self.config = screen_config

        # self.scaling_x = self.config.current_x / 9
        self.scaling_y = self.config.current_y / 15
        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Add the difficulty buttons
        self.easy_button = DifficultyButton(button_text="Easy", manager=self.manager, mode=EASY,
                                            screen_config=self.config)
        self.medium_button = DifficultyButton(button_text="Medium", manager=self.manager, mode=MEDIUM,
                                              screen_config=self.config)
        self.hard_button = DifficultyButton(button_text="Hard", manager=self.manager, mode=HARD,
                                            screen_config=self.config)

        # Add to V_Box with spacing
        self.v_box.add(self.easy_button.with_space_around(bottom=self.scaling_y / 3))
        self.v_box.add(self.medium_button.with_space_around(bottom=self.scaling_y / 3))
        self.v_box.add(self.hard_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.view_manager.show_menu_view()
            self.manager.disable()
