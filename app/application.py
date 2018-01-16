# coding=utf-8

import os
import sys


class Application(object):

    def __init__(self):
        self.name = 'python_messenger'
        #: Default configuration parameters.
        self.default_config = {
            'ENV': None,
            'DEBUG': None,
            'TESTING': False,
            'SECRET_KEY': None,
            'SERVER_NAME': None,
            'APPLICATION_ROOT': '/',
        }
        # self.config = self.make_config(instance_relative_config)
        pass

    # def make_config(self, instance_relative=False):
    #     """Used to create the config attribute by the Flask constructor.
    #     The `instance_relative` parameter is passed in from the constructor
    #     of Flask (there named `instance_relative_config`) and indicates if
    #     the config should be relative to the instance path or the root path
    #     of the application.
    #     .. versionadded:: 0.8
    #     """
    #     root_path = self.root_path
    #     if instance_relative:
    #         root_path = self.instance_path
    #     defaults = dict(self.default_config)
    #     defaults['ENV'] = get_env()
    #     defaults['DEBUG'] = get_debug_flag()
    #     return self.config_class(root_path, defaults)

    # def logger(self):
    #     return logger.create_logger(self)
    #
    # def _get_debug(self):
    #     return self.config['DEBUG']
    #
    # def _set_debug(self, value):
    #     self.config['DEBUG'] = value
    #
    # def log_exception(self, exc_info):
    #     pass
    #
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
    #
    # def get_env():
    #     """Get the environment the app is running in, indicated by the
    #     :envvar:`FLASK_ENV` environment variable. The default is
    #     ``'production'``.
    #     """
    #     return os.environ.get('FLASK_ENV') or 'production'



class Config(dict):

    def __init__(self, root_path, defaults=None):
        dict.__init__(self, defaults or {})
        self.root_path = root_path

#     def from_envvar(self, variable_name, silent=False):
#         rv = os.environ.get(variable_name)
#         if not rv:
#             if silent:
#                 return False
#             raise RuntimeError('The environment variable %r is not set '
#                                'and as such configuration could not be '
#                                'loaded.  Set this variable and make it '
#                                'point to a configuration file' %
#                                variable_name)
#         return self.from_pyfile(rv, silent=silent)
#
#     def from_pyfile(self, filename, silent=False):
#         filename = os.path.join(self.root_path, filename)
#         d = types.ModuleType('config')
#         d.__file__ = filename
#         try:
#             with open(filename, mode='rb') as config_file:
#                 exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
#         except IOError as e:
#             if silent and e.errno in (
#                 errno.ENOENT, errno.EISDIR, errno.ENOTDIR
#             ):
#                 return False
#             e.strerror = 'Unable to load configuration file (%s)' % e.strerror
#             raise
#         self.from_object(d)
#         return True
#
#     def from_object(self, obj):
#         if isinstance(obj, string_types):
#             obj = import_string(obj)
#         for key in dir(obj):
#             if key.isupper():
#                 self[key] = getattr(obj, key)
#
#     def from_json(self, filename, silent=False):
#         filename = os.path.join(self.root_path, filename)
#
#         try:
#             with open(filename) as json_file:
#                 obj = json.loads(json_file.read())
#         except IOError as e:
#             if silent and e.errno in (errno.ENOENT, errno.EISDIR):
#                 return False
#             e.strerror = 'Unable to load configuration file (%s)' % e.strerror
#             raise
#         return self.from_mapping(obj)
#
#     def from_mapping(self, *mapping, **kwargs):
#         """Updates the config like :meth:`update` ignoring items with non-upper
#         keys.
#         .. versionadded:: 0.11
#         """
#         mappings = []
#         if len(mapping) == 1:
#             if hasattr(mapping[0], 'items'):
#                 mappings.append(mapping[0].items())
#             else:
#                 mappings.append(mapping[0])
#         elif len(mapping) > 1:
#             raise TypeError(
#                 'expected at most 1 positional argument, got %d' % len(mapping)
#             )
#         mappings.append(kwargs.items())
#         for mapping in mappings:
#             for (key, value) in mapping:
#                 if key.isupper():
#                     self[key] = value
#         return True
#
#     def get_namespace(self, namespace, lowercase=True, trim_namespace=True):
#         rv = {}
#         for k, v in iteritems(self):
#             if not k.startswith(namespace):
#                 continue
#             if trim_namespace:
#                 key = k[len(namespace):]
#             else:
#                 key = k
#             if lowercase:
#                 key = key.lower()
#             rv[key] = v
#         return rv
#
#     def __repr__(self):
#         return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))
#
#
# class ConfigAttribute(object):
#     """Makes an attribute forward to the config"""
#
#     def __init__(self, name, get_converter=None):
#         self.__name__ = name
#         self.get_converter = get_converter
#
#     def __get__(self, obj, type=None):
#         if obj is None:
#             return self
#         rv = obj.config[self.__name__]
#         if self.get_converter is not None:
#             rv = self.get_converter(rv)
#         return rv
#
#     def __set__(self, obj, value):
#         obj.config[self.__name__] = value
