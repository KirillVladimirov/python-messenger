import logging
import time
import os


def make_logger(config_dict):
    logger = Logger.inst(config_dict)
    return logger.logger


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
