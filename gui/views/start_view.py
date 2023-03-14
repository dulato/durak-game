import arcade
import arcade.gui

from gui.buttons.quit_button import QuitButton
from gui.buttons.rules_button import RulesButton
from gui.buttons.start_button import StartButton
from gui.screen_configuration import ScreenConfiguration


class StartView(arcade.View):
    def __init__(self, screen_config: ScreenConfiguration):
        super().__init__()

        self.config = screen_config
        self.config.init_current_screen()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.rgb = [125, 1, 1]
        self.multiplier = 1

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = StartButton(self.config, self.manager)
        self.v_box.add(start_button.with_space_around(bottom=20))

        rules_button = RulesButton(self.config)
        self.v_box.add(rules_button.with_space_around(bottom=20))

        # Again, method 1. Use a child class to handle events.
        quit_button = QuitButton()
        self.v_box.add(quit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_update(self, delta_time: 0.25):
        self.rgb[1] += self.multiplier * 2
        self.rgb[2] += self.multiplier * 4
        for f in self.rgb[1:]:
            if f > 255:
                self.multiplier = -1
            elif f < 0:
                self.multiplier = 1

        arcade.set_background_color(self.rgb)

    def on_draw(self):
        self.clear()
        self.manager.draw()
