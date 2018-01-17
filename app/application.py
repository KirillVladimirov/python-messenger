# coding=utf-8

import os
import json
import logging
import time


class Application(object):

    def __init__(self):
        self.name = 'python_messenger'
        self.default_config = {
            'ENV': None,
            'DEBUG': None,
            'SECRET_KEY': None,
            'SERVER_NAME': None,
            'APPLICATION_ROOT': os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
        }
        self.config = self.make_config()

    def make_config(self):
        defaults = dict(self.default_config)
        root_path = defaults['APPLICATION_ROOT']
        config = Config(root_path, defaults)
        config.from_json('config/env.json')
        return config

    @property
    def logger(self):
        logger = logging.getLogger(__class__.__name__)
        if self.config["DEBUG"]:
            debug_level = logging.DEBUG
        else:
            debug_level = logging.ERROR
        logger.setLevel(debug_level)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(self.config["APPLICATION_ROOT"] + "/logs/" + str(time.strftime("%d_%m_%Y")) + '.log')
        fh.setLevel(debug_level)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(debug_level)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

    # def name(self):
    #     """The name of the application.  This is usually the import name
    #     with the difference that it's guessed from the run file if the
    #     import name is main.  This name is used as a display name when
    #     Flask needs the name of the application.  It can be set and overridden
    #     to change the value.
    #     .. versionadded:: 0.8
    #     """
    #     if self.import_name == '__main__':
    #         fn = getattr(sys.modules['__main__'], '__file__', None)
    #         if fn is None:
    #             return '__main__'
    #         return os.path.splitext(os.path.basename(fn))[0]
    #     return self.import_name
    #
    # def __repr__(self):
    #     return '<%s %r>'.format() % (
    #         self.__class__.__name__,
    #         self.name,
    #     )


class Config(dict):

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


if __name__ == "__main__":
    app = Application()
