import arcade
import arcade.gui

from gui.screen_configuration import ScreenConfiguration
import gui.view_manager


class WinLoseView(arcade.View):
    def __init__(self, config: ScreenConfiguration, win_lose_img):
        super().__init__()

        self.config = config
        self.view_manager = gui.view_manager.ViewManager()

        self.scaling_x = self.config.current_x / 9
        self.scaling_y = self.config.current_y / 15

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.lose_image = arcade.load_texture(win_lose_img)

        # Create Vertical Box to place the items in
        self.v_box = arcade.gui.UIBoxLayout()

        arcade.set_background_color(arcade.color.BLACK)

        self.back_to_menu_button = arcade.gui.UIFlatButton(text="Back to Menu", height=self.scaling_y,
                                                           width=self.scaling_x)

        self.v_box.add(self.back_to_menu_button)

        self.back_to_menu_button.on_click = self.back_to_menu_screen

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="bottom",
                child=self.v_box)
        )

    def back_to_menu_screen(self, event):
        self.view_manager.show_menu_view()
        self.manager.disable()

    def on_draw(self):
        # This command has to happen before we start drawing
        self.clear()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured((self.config.current_x / 2) - 585 * self.config.screen_ratio,
                                            (self.config.current_y / 2) - 85 * self.config.screen_ratio,
                                            1170 * self.config.screen_ratio, 170 * self.config.screen_ratio,
                                            self.lose_image)
        self.manager.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            from gui.views.start_view import MenuView
            arcade.get_window().show_view(MenuView(self.config))
