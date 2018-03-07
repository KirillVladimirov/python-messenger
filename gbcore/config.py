#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json


def make_config(config_path):
    """
    Создание словаря с глобальными настройками проекта
    :return:
    """
    default_config = {
        "ENV": None,
        "DEBUG": None,
        "DEBUG_LEVEL": "DEBUG",
        "SECRET_KEY": None,
        "SERVER_NAME": None,
        "APPLICATION_ROOT": os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
    }

    defaults = dict(default_config)
    root_path = defaults["APPLICATION_ROOT"]
    config = Config(root_path, defaults)
    config.from_json(config_path)
    return config


class Config(dict):
    """"
    Словарь, в котором хранятся настройки приложения
    """

    def __init__(self, root_path, defaults=None):
        dict.__init__(self, defaults or {})
        self.root_path = root_path

    def from_json(self, filename):
        filename = os.path.join(self.root_path, filename)

        try:
            with open(filename) as json_file:
                obj = json.loads(json_file.read())
        except IOError as e:
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        return self.from_mapping(obj)

    def from_mapping(self, *mapping, **kwargs):
        mappings = []
        if len(mapping) == 1:
            if hasattr(mapping[0], 'items'):
                mappings.append(mapping[0].items())
            else:
                mappings.append(mapping[0])
        elif len(mapping) > 1:
            raise TypeError(
                'expected at most 1 positional argument, got %d' % len(mapping)
            )
        mappings.append(kwargs.items())
        for mapping in mappings:
            for (key, value) in mapping:
                if key.isupper():
                    self[key] = value
        return True
