"""
Main module of Olympe's Medals Quest.
"""

###############
### Imports ###
###############

### Kivy imports ###

# Disable back arrow
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from kivy.uix.screenmanager import (
    ScreenManager,
    NoTransition,
    Screen
)
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock, mainthread

### Local imports ###

from tools.path import (
    PATH_IMAGES,
    ANDROID_MODE
)
from tools.constants import (
    FPS,
    MSAA_LEVEL,
    USER_DATA
)
import screens.opening
from lupa_libraries import (
    LoadingPopup
)

###############
### General ###
###############


class WindowManager(ScreenManager):
    """
    Screen manager, which allows the navigation between the different menus.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        self.list_previous_screens = []
        current_screen = Screen(name="temp")
        self.add_widget(current_screen)
        self.current = "temp"

        # Constant used for multiple games
        self.id_game = 1

    def go_to_previous_screen(self):
        if len(self.list_previous_screens) != 0:
            previous_screen = self.list_previous_screens.pop()
            screen_name = previous_screen[0]
            self.get_screen(screen_name).reload_kwargs(previous_screen[1])
            self.current = screen_name

    def go_to_next_screen(self, next_screen_name, current_dict_kwargs={}, next_dict_kwargs={}):
        current_screen_name = self.current
        self.list_previous_screens.append(
            (current_screen_name, current_dict_kwargs))
        self.get_screen(next_screen_name).reload_kwargs(next_dict_kwargs)
        self.current = next_screen_name


class MainApp(App, Widget):
    """
    Main class of the application.
    """

    def build_config(self, config):
        """
        Build the config file for the application.

        It sets the FPS number and the antialiasing level.
        """
        config.setdefaults('graphics', {
            'maxfps': str(FPS),
            'multisamples': str(MSAA_LEVEL)
        })

    def build(self):
        """
        Build the application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        Window.clearcolor = (1, 1, 1, 1)
        self.icon = PATH_IMAGES + "logo.png"

    @mainthread
    def on_resume(self):
        print("reloading")
        current_screen_name = self.root_window.children[0].current
        screen = self.root_window.children[0].get_screen(current_screen_name)
        loading_popup = LoadingPopup(
            font_ratio=screen.font_ratio,
            primary_color=screen.primary_color,
            secondary_color=screen.secondary_color,
        )
        loading_popup.open()
        Clock.schedule_once(loading_popup.dismiss, 2)
        return super().on_resume()

    def on_start(self):
        if ANDROID_MODE:
            Window.update_viewport()

        # Open the opening screen
        opening_screen = screens.opening.OpeningScreen(name="opening")
        self.root_window.children[0].add_widget(opening_screen)
        self.root_window.children[0].current = "opening"

        Clock.schedule_once(
            self.root_window.children[0].get_screen("opening").launch_thread)

        print("Main app started")

        return super().on_start()

    def on_stop(self):
        super().on_stop()
        USER_DATA.stop_game(id_game = self.root_window.children[0].id_game)
        USER_DATA.save_changes()

# Run the application
if __name__ == "__main__":
    if not ANDROID_MODE:
        Window.size = (405, 720)
        # Window.size = (720, 1080)
        # Window.size = (200, 400)
        # Window.size = (1080, 2340)
    MainApp().run()
