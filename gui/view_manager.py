import arcade

from gui.screen_configuration import ScreenConfiguration
from gui.views.difficulty_view import DifficultyView
from gui.views.rules_view import RulesView
from gui.views.start_view import StartView
from gui.views.game_views import GameView

from gui.views.win_lose_view import WinLoseView


class ViewManager(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(ViewManager, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.view = None
        self.config = ScreenConfiguration()
        self.__rules_view = RulesView(self.config)

    def show_game_view(self, config, difficulty):
        arcade.get_window().show_view(GameView(config, difficulty))

    def show_rules_view(self):
        arcade.get_window().show_view(self.__rules_view)

    def show_difficulty_view(self, config):
        arcade.get_window().show_view(DifficultyView(config))

    def show_menu_view(self):
        arcade.get_window().show_view(StartView(self.config))

    def show_win_lose_view(self, status, config):
        arcade.get_window().show_view(WinLoseView(config, status))


