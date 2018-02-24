#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import logging
import time
from gbcore.sqlalchemy import SQLAlchemy


class Application(object):
    """
    Application class for all global config
    """

    def __init__(self, config_path):
        self.name = 'python_messenger'
        self.default_config = {
            "ENV": None,
            "DEBUG": None,
            "DEBUG_LEVEL": "DEBUG",
            "SECRET_KEY": None,
            "SERVER_NAME": None,
            "APPLICATION_ROOT": os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
        }
        self.config = self.make_config()

        logger = Logger.inst(self.config)
        self.logger = logger.logger
        self.config.from_json("config/env.json")

        sql_path = os.path.join(self.config["APPLICATION_ROOT"], "sql", self.config["SQLALCHEMY"]["DB"])
        sql_uri = "sqlite:///{}".format(sql_path)
        self.logger.info(sql_uri)
        self.db = SQLAlchemy(self, sql_uri)

    def make_config(self):
        """
        Создание словаря с глобальными настройками проекта
        :return:
        """
        defaults = dict(self.default_config)
        root_path = defaults["APPLICATION_ROOT"]
        config = Config(root_path, defaults)
        return config


class Logger(object):
    __instance = None

    @staticmethod
    def inst(config):
        if Logger.__instance is None:
            Logger.__instance = Logger(config)
        return Logger.__instance

    def __init__(self, config):
        logger = logging.getLogger(__class__.__name__)
        if config["DEBUG_LEVEL"]:
            debug_level = config["DEBUG_LEVEL"]
        else:
            debug_level = logging.ERROR
        logger.setLevel(debug_level)
        # create file handler which logs even debug messages
        log_path = os.path.join(config["APPLICATION_ROOT"],
                                "logs",
                                str(time.strftime("%d_%m_%Y")) + '.log')
        fh = logging.FileHandler(log_path)
        fh.setLevel(debug_level)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(debug_level)
        # create formatter and add it to the handlers
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        self.logger = logger


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