import arcade.gui
import gui.view_manager
from gui.screen_configuration import ScreenConfiguration


class RulesButton(arcade.gui.UIFlatButton):
    def __init__(self, config: ScreenConfiguration):
        super(RulesButton, self).__init__(text="Rules", width=200)
        self.config = config

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        view_manager = gui.view_manager.ViewManager()
        view_manager.show_rules_view()
