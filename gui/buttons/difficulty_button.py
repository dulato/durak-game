import arcade.gui
import gui.view_manager
from gui.screen_configuration import ScreenConfiguration


class DifficultyButton(arcade.gui.UIFlatButton):

    def __init__(self, button_text, manager, mode, screen_config: ScreenConfiguration):
        super().__init__(
            text=button_text,
            center_x=0,
            center_y=0,
            width=200,
            height=50,
        )
        self.config = screen_config
        self.manager = manager
        self.mode = mode

    def on_click(self, event):
        view_manager = gui.view_manager.ViewManager()
        view_manager.show_game_view(self.config,self.mode)
        self.manager.disable()
