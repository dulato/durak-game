import os
import arcade
import arcade.gui
import gui.view_manager
from gui.text_fields.rules import Rules
from gui.screen_configuration import ScreenConfiguration


class RulesView(arcade.View):
    def __init__(self, config: ScreenConfiguration):
        super().__init__()
        self.config = config

        # get current working directory
        cwd = os.getcwd()

        # create a path to the file
        path = os.path.join(cwd, "resources")

        # open File and read Rules
        with open(f'{path}/Rules.txt', 'r', encoding='UTF-8') as f:
            self.__rules = f.read()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create Vertical Box to place the items in
        self.v_box = arcade.gui.UIBoxLayout()

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

        # Text Field to be put in V_Box
        rules = Rules(self.config.width / 2, self.config.height / 2,
                      self.config.width * 0.7, self.config.height * 0.7, self.__rules, 'arial', 25,
                      arcade.color.BLACK, True, 5.5)

        self.v_box.add(rules)

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
            view_manager = gui.view_manager.ViewManager()
            view_manager.show_menu_view()