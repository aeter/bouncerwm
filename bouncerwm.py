#!/usr/bin/python3

from random import randint
from time import sleep
from Xlib import display, X


class Bouncerwm:
    def __init__(self):
        self.display = display.Display()
        self.root_window = self.display.screen().root
        self.moving_windows = set()

    def current_active_window(self):
        window_id = self.root_window.get_full_property(
            self.display.intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType).value[0]
        return self.display.create_resource_object('window', window_id)

    def move_window(self, window):
        screen_height = self.display.screen().height_in_pixels
        screen_width = self.display.screen().width_in_pixels
        w = window.query_tree().parent.get_geometry()

        # check bounds
        out_of_screen_right = w.x + w.width > screen_width
        out_of_screen_bottom = w.y + w.height > screen_height
        out_of_screen_left = w.x < 0
        out_of_screen_top = w.y < 0

        # check obstacles (maybe a top/bottom panel prevent window
        # to reach end of screen)
        obstacle_left_or_right = window.last_x == w.x
        obstacle_top_or_bottom = window.last_y == w.y

        if out_of_screen_right or out_of_screen_left or obstacle_left_or_right:
            window.dx = -1 * window.dx
        if out_of_screen_top or out_of_screen_bottom or obstacle_top_or_bottom:
            window.dy = -1 * window.dy

        window.configure(x=w.x + window.dx, y=w.y + window.dy)

        window.last_x = w.x
        window.last_y = w.y

    def run(self):
        while True:
            window = self.current_active_window()
            if not window in self.moving_windows:
                window.dx = randint(1, 10)
                window.dy = randint(1, 10)
                window.last_x = window.query_tree().parent.get_geometry().x
                window.last_y = window.query_tree().parent.get_geometry().y
                self.moving_windows.add(window)
            for window in self.moving_windows:
                self.move_window(window)
                self.display.sync()
            sleep(0.03)


if __name__ == '__main__':
    Bouncerwm().run()
