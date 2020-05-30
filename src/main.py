"""
The main function is laid out here. It creates an instance of tools.Game,
which handles the game states in its state_machine dictionary.
"""

from . import prepare, tools
from .states import splash, gameplay


def main():
    screen = prepare.get_screen()
    states = {
        "SPLASH": splash.SplashScreen(),
        "GAMEPLAY": gameplay.GamePlay()
    }

    game = tools.Game(screen, states, "SPLASH")
    game.run()
