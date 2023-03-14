import arcade
import arcade.gui


class QuitButton(arcade.gui.UIFlatButton):
    def __init__(self):
        super(QuitButton, self).__init__(text="Quit Game", width=200)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()
