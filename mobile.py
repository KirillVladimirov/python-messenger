#!/usr/bin/python3
# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.uix.label import Label


class AppKivy(App):

    def build(self):
        return Label(text='Здравствуй Мир')


if __name__ == '__main__':
    AppKivy().run()
