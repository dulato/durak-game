import arcade

from gui.screen_configuration import ScreenConfiguration
from gui.view_manager import ViewManager

if __name__ == '__main__':
    config = ScreenConfiguration()
    window = arcade.Window(config.width, config.height, config.screen_title, fullscreen=True)
    view_manager = ViewManager()
    view_manager.show_menu_view()
    arcade.run()
