import arcade.gui
import gui.view_manager
from gui.screen_configuration import ScreenConfiguration


class ToMenuButton(arcade.gui.UIFlatButton):
    def __init__(self, config: ScreenConfiguration, manager):
        super(ToMenuButton, self).__init__(text="Back to Menu", width=200)
        self.config = config
        self.manager = manager

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        view_manager = gui.view_manager.ViewManager()
        view_manager.show_menu_view()
        self.manager.disable()
