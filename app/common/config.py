import json
import sys
import getopt


def get_json_options(file):
    """
    Get program options from json file
    :param file: File name
    :return: Dict with setup options
    """
    try:
        with open(file, "r") as f:
            config = json.load(f)
    except ValueError as err:
        print("Can`t read config file: {}, with error: {}".format(file, err))
        sys.exit(2)
    return config


def get_command_options(args, short_opts):
    """
    Get options from command line args
    :param args:
    :param short_opts:
    :return:
    """
    try:
        opts, _ = getopt.getopt(args[1:], short_opts)
    except getopt.GetoptError as err:
        print("Invalid argument value with error: {}".format(err))
        sys.exit(2)
    return opts

