# coding=utf-8

import os


class Application:

    def __init__(self):
        pass

    def make_config(self):
        pass

    def logger(self):
        pass

    def _get_debug(self):
        return self.config['DEBUG']

    def _set_debug(self, value):
        self.config['DEBUG'] = value

    def log_exception(self, exc_info):
        pass

    def name(self):
        """The name of the application.  This is usually the import name
        with the difference that it's guessed from the run file if the
        import name is main.  This name is used as a display name when
        Flask needs the name of the application.  It can be set and overridden
        to change the value.
        .. versionadded:: 0.8
        """
        if self.import_name == '__main__':
            fn = getattr(sys.modules['__main__'], '__file__', None)
            if fn is None:
                return '__main__'
            return os.path.splitext(os.path.basename(fn))[0]
        return self.import_name

    def __repr__(self):
        return '<%s %r>'.format() % (
            self.__class__.__name__,
            self.name,
        )
