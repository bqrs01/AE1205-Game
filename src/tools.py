"""
 File: tools.py
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
"""

import sys
import os
import io
import pygame as pg
import math
import random
import threading
import json

song_names = [
    "Zane Alexander - D a y",
    "Emil Rottmayer - Evade",
    "Unfound - Dawn",
    "FRACTAL MAN - Glimpses of Starlight",
    "A.L.I.S.O.N - Golden Dust",
    "Stratford Ct. - HOME - Still Life",
    "Unfound - Intercept",
    # ｌｏｏｓｅｇｏｏｓｅ - ＳＰＲＩＮＧＦＩＥＬＤ ＇９６",
    "l o o s e g o o s e - S P R I N G F I E L D ' 9 6",
    "Color Index - Intervals (Open Spectrum)",
    "Nowtro - Still Human (Teaser)",
    "Syntax - Syntax - Stratus (f. HOME)",
    "oDDling - Ascend"
]


class SoundManager:
    def __init__(self, filename):
        pg.mixer.init()
        self.sounds = []
        self.filenames = [filename]
        self.setup_data()
        self.volume = self.get_volume()

    def get_volume(self):
        data = self.get_data(self.filenames[0])
        if not "sfx_volume" in data:
            data['sfx_volume'] = 0.5
            self.set_data('prefs.json', data)
        return (data['sfx_volume'])

    def setup_data(self, force=False):
        basedir = os.path.dirname(os.path.join(os.getcwd(), f"src/data/"))
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        for filename in self.filenames:
            path = os.path.join(os.getcwd(), f"src/data/{filename}")
            exists = os.path.exists(path)
            if not exists or force:
                f = open(path, 'a')
                f.write('{}')
                f.close()

    def get_data(self, filename):
        try:
            with open(os.path.join(os.getcwd(), f"src/data/{filename}"), "r") as dataFile:
                return json.load(dataFile)
        except (TypeError, json.JSONDecodeError):
            self.setup_data(force=True)
            return self.get_data(filename)

    def set_data(self, filename, object):
        try:
            with open(os.path.join(os.getcwd(), f"src/data/{filename}"), "w") as dataFile:
                json.dump(object, dataFile)
        except (TypeError, json.JSONDecodeError):
            self.setup_data(force=True)
            return self.set_data(filename, object)

    def playSound(self, filename, duration):
        # print(pg.mixer.get_init())
        # soundfile = io.BufferedReader(open(os.path.join(
        #     os.getcwd(), f"src/soundeffects/{filename}"), "rb", buffering=0))
        sound = pg.mixer.Sound(file=(os.path.join(
            os.getcwd(), f"src/soundeffects/{filename}")))
        sound.set_volume(self.volume)
        sound.play(maxtime=duration)
        self.sounds.append({"name": filename, "sound": sound})

    def stopSound(self, filename):
        for soundData in self.sounds:
            if soundData.name == filename:
                soundData["sound"].stop()
                self.sounds.remove(soundData)


class Vector:
    def __init__(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction

    def updateVector(self, magnitude, direction):
        self.magnitude = magnitude
        self.direction = direction

    @staticmethod
    def getQuadrant(direction):
        pi = math.pi
        boundaries = [-pi, -pi/2, 0, pi/2, pi]
        quadrants = [3, 4, 1, 2]

        for i in range(len(boundaries)):
            if direction == boundaries[i]:
                return quadrants[i]
            elif direction == boundaries[i+1]:
                return quadrants[i]
            elif direction > boundaries[i] and direction < boundaries[i+1]:
                return quadrants[i]

        return None

    def getTrigRatios(self):
        direction = self.getDirection()
        quadrant = self.getQuadrant(direction)

        if quadrant == 1:
            xfactor = math.cos(direction)
            yfactor = math.sin(direction)
        elif quadrant == 2:
            direction -= math.pi/2
            xfactor = -math.sin(direction)
            yfactor = math.cos(direction)
        elif quadrant == 3:
            direction = abs(direction)
            direction -= math.pi/2
            xfactor = -math.sin(direction)
            yfactor = -math.cos(direction)
        else:
            direction = abs(direction)
            xfactor = math.cos(direction)
            yfactor = -math.sin(direction)

        return (xfactor, yfactor)

    def getMagnitude(self):
        return self.magnitude

    def getDirection(self):
        return self.direction

    def getXComponent(self):
        return self.getTrigRatios()[0] * self.getMagnitude()

    def getYComponent(self):
        return self.getTrigRatios()[1] * self.getMagnitude()

    def getComponents(self):
        return (self.getXComponent(), self.getYComponent())

    @staticmethod
    def getReverseDirection(direction):
        quadrant = Vector.getQuadrant(direction)
        if quadrant == 1 or quadrant == 2:
            return -math.pi + direction
        else:
            return math.pi + direction


class Game(object):
    def __init__(self, screen, caption, states, start_state):
        """
        Initialise the Game object, and save some important variables.
        """
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.fps_visible = False
        self.caption = caption
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

        self.filenames = ['prefs.json']
        self.setup_data()

        self.music_vol = self.get_music_volume()
        self.sfx_vol = self.get_sfx_volume()

        self.music_pos = [0, 149, 358, 610, 928,
                          1197, 1389, 1606, 1775, 1900, 2277, 2488, 2670]
        self.music_index = random.randint(0, 11)
        self.music_start = self.music_pos[self.music_index]
        self.music_end = self.music_pos[self.music_index + 1]
        self.music_current_seek = self.music_start
        self.game_music("music.ogg")
        # Get it from file..

    def setup_data(self, force=False):
        basedir = os.path.dirname(os.path.join(os.getcwd(), f"src/data/"))
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        for filename in self.filenames:
            path = os.path.join(os.getcwd(), f"src/data/{filename}")
            exists = os.path.exists(path)
            if not exists or force:
                f = open(path, 'a')
                f.write('{}')
                f.close()

    def get_data(self, filename):
        try:
            with open(os.path.join(os.getcwd(), f"src/data/{filename}"), "r") as dataFile:
                return json.load(dataFile)
        except (TypeError, json.JSONDecodeError):
            self.setup_data(force=True)
            return self.get_data(filename)

    def set_data(self, filename, objectVar):
        try:
            with open(os.path.join(os.getcwd(), f"src/data/{filename}"), "w") as dataFile:
                json.dump(objectVar, dataFile)
        except (TypeError, json.JSONDecodeError):
            self.setup_data(force=True)
            return self.set_data(filename, objectVar)

    def game_music(self, filename):
        # Game music
        pg.mixer.music.load(os.path.join(
            os.getcwd(), f"src/soundeffects/{filename}"))
        pg.mixer.music.set_volume(self.music_vol)
        pg.mixer.music.play(start=self.music_start)
        self.set_bgmusic()

    def pause_music(self, duration):
        pg.mixer.music.pause()
        threading.Timer(duration, pg.mixer.music.unpause).start()

    def get_music_volume(self):
        data = self.get_data('prefs.json')
        try:
            if not "music_volume" in data:
                data['music_volume'] = 0.08
                self.set_data('prefs.json', data)
            return (data['music_volume'])
        except TypeError:
            self.setup_data(force=True)

    def set_music_volume(self, newVolume):
        self.music_vol = newVolume
        pg.mixer.music.set_volume(self.music_vol)

    def get_sfx_volume(self):
        data = self.get_data('prefs.json')
        try:
            if not "sfx_volume" in data:
                data['sfx_volume'] = 0.2
                self.set_data('prefs.json', data)
            return (data['sfx_volume'])
        except TypeError:
            self.setup_data(force=True)

    def set_sfx_volume(self, newVolume):
        self.sfx_vol = newVolume

    def get_min_and_secs(self, time_s):
        mins = time_s // 60
        secs = time_s % 60
        return (mins, secs)

    def save_music_volume(self):
        data = self.get_data('prefs.json')
        data['music_volume'] = self.music_vol
        data['sfx_volume'] = self.sfx_vol
        self.set_data('prefs.json', data)

    def event_loop(self):
        """Events are passed to current state"""
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_F5:
                self.toggle_show_fps(event.key)
            self.state.handle_event(event)

    def switch_state(self):
        """Switch to the next state."""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        game_data = self.state.game_data  # Persistent data
        self.state = self.states[self.state_name]
        self.set_bgmusic()
        self.state.startup(game_data)

    def set_bgmusic(self):
        self.state.bgmusic = {
            "song_name": song_names[self.music_index], "pause_music": self.pause_music,
            "get_volume": self.get_music_volume, "set_volume": self.set_music_volume,
            "save_volume": self.save_music_volume, "get_sfx_volume": self.get_sfx_volume,
            "set_sfx_volume": self.set_sfx_volume, "current_position": self.get_min_and_secs(self.music_current_seek),
            "song_length": self.get_min_and_secs(self.music_end-self.music_start)}

    def toggle_show_fps(self, key):
        """Press f5 to turn on/off displaying the framerate in the caption."""
        if key == pg.K_F5:
            self.fps_visible = not self.fps_visible
            if not self.fps_visible:
                pg.display.set_caption(self.caption)

    def update(self, dt):
        """Check for state switch and update state if needed"""
        self.music_current_seek = pg.mixer.music.get_pos()//1000
        self.state.bgmusic["current_position"] = self.get_min_and_secs(
            self.music_current_seek)
        if self.music_current_seek >= (self.music_end - self.music_start):
            self.music_index = random.randint(0, 11)
            self.music_start = self.music_pos[self.music_index]
            self.music_end = self.music_pos[self.music_index + 1]
            self.state.bgmusic["song_name"] = song_names[self.music_index]
            self.state.bgmusic["current_position"] = (0, 0)
            self.state.bgmusic["song_length"] = self.get_min_and_secs(
                self.music_end-self.music_start)
            # print(song_names[self.music_index])
            pg.mixer.music.play(start=self.music_start)
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.switch_state()
        self.state.update(dt)

    def draw(self):
        """Pass surface to state for drawing"""
        self.state.draw(self.screen)
        self.show_fps()

    def show_fps(self):
        """
        Display the current FPS in the window handle if fps_visible is True.
        """
        if self.fps_visible:
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pg.display.set_caption(with_fps)

    def run(self):
        """Game loop will run in the while loop here"""
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


class State(object):
    """Base class for game states"""

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.game_data = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, game_data):
        """Called when state is about to become active or resumes being active."""
        self.game_data = game_data

    def handle_event(self, event):
        """Handle events passed by Game"""
        pass

    def update(self, dt):
        """Update the state."""
        pass

    def draw(self, surface):
        """Draw scene to screen"""
        pass


class _BaseSprite(pg.sprite.Sprite):
    """The base class for all types of sprites"""

    def __init__(self, pos, size, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.rect = pg.Rect(pos, size)
        self.exact_pos = list(self.rect.topleft)
        self.old_pos = self.exact_pos[:]

    def reset_position(self, value):
        """
        Set sprite location to new point. By default `value`
        specifies a position in the topleft corner.
        """
        setattr(self.rect, "topleft", value)
        self.exact_pos = list(self.rect.topleft)
        self.old_pos = self.exact_pos[:]

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def rotateImage(surf, image, pos, originPos, angle):
    """Method that rotates objects (sprites) by center by an angle."""
    # calcaulate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pg.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]

    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[
        0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[
        0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pg.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0],
              pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pg.transform.rotate(image, angle)

    return rotated_image, origin


class Slider(_BaseSprite):
    def __init__(self, starting_value, position, when_update):
        super().__init__(position, (300, 50))
        self.value = starting_value
        self.position = position
        self.when_update = when_update

        self.max = 200

        self.setup()

    def setup(self):
        self.image = pg.Surface((204, 20), pg.SRCALPHA).convert_alpha()
        # self.image.fill((255, 255, 0))
        # self.image.set_colorkey((255, 255, 0))

        # Outer rect
        pg.draw.rect(self.image, pg.color.Color(
            'yellow'), (0, 0, 204, 20), True)

        # Inner rect
        val = 200 * self.value
        pg.draw.rect(self.image, pg.color.Color('red'), (2, 2, val, 16))

    def draw(self, surface):
        self.setup()
        surface.blit(self.image, self.rect)

    def set_value(self, posx):
        posx = min(posx, self.max)
        posx = max(posx, 0)

        self.value = (posx/self.max)

        self.when_update(self.value)

    def handle_mouse(self, pos):
        self.set_value(pos[0] - self.rect.x)
