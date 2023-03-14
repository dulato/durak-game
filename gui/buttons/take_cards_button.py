import arcade.gui
from gui.screen_configuration import ScreenConfiguration


class TakeCardsButton(arcade.gui.UIFlatButton):

    def __init__(self, playground, game_logic, human):
        super(TakeCardsButton, self).__init__(text="Take Cards", width=200)
        self.playground = playground
        self.game_logic = game_logic
        self.human = human

    def on_click(self, event):
        if self.human.is_turn and len(self.playground.get_cards()[-1]) == 1:
            self.human.is_turn = False
            self.human.is_taking = True
            self.game_logic.take_all_cards_human()
