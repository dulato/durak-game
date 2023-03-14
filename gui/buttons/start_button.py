import arcade.gui
import gui.view_manager
from gui.screen_configuration import ScreenConfiguration


class StartButton(arcade.gui.UIFlatButton):
    def __init__(self, screen_config: ScreenConfiguration, manager):
        super(StartButton, self).__init__(text="Start Game", width=200)
        self.manager = manager
        self.config = screen_config

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        view_manager = gui.view_manager.ViewManager()
        view_manager.show_difficulty_view(self.config)
        self.manager.disable()
