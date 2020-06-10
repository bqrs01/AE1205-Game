"""
 File: main.py
 Authors: Mario Padrón Tardáguila & Bryan Quadras
 
 Copyright (c) 2020 Mario Padrón Tardáguila & Bryan Quadras
 
 The MIT License
 
 Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
 and associated documentation files (the "Software"), to deal in the Software without restriction,
 including without limitation the rights to use, copy, modify, merge, publish, distribute, 
 sublicense, and/or sell copies of the Software, and to permit persons to whom the Software 
 is furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all copies 
 or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
 PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
 FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


>>> The main function is laid out here. It creates an instance of tools.Game,
    which handles the game states in its state_machine dictionary.
"""

from . import prepare, tools
from .states import splash, gameplay, gameover
from .states.menu import main_screen, settings, controls_screen


def main():
    # Initialise game screen
    screen = prepare.get_screen()
    caption = prepare.ORIGINAL_CAPTION
    states = {
        "SPLASH": splash.SplashScreen(),
        "GAMEPLAY": gameplay.GamePlay(),
        "GAMEOVER": gameover.GameOver(),
        "MAINSCREEN": main_screen.MainScreen(),
        "CONTROLS": controls_screen.ControlsScreen(),
        "SETTINGS": settings.SettingsScreen()}

    game = tools.Game(screen, caption, states, "SPLASH")
    game.run()
