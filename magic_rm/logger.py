#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
#
# Author Georgy Schapchits <gogi.soft.gm@gmail.com>.
import logging

class Logger(object):

    JSON = "JSON"
    HUMAN = "HUMAN"

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    LEVELS = [DEBUG, INFO, WARNING, ERROR]
    FORMATS = [HUMAN, JSON]

    def __init__(self,
                 log_level=ERROR,
                 verbose_level=WARNING,
                 file_path=None,
                 mode=HUMAN):

        self.log_level = log_level
        self.verbose_level = verbose_level
        self.mode = mode
        self.file_path = file_path
        self.logger = self._create_logger()

    def alert(self, message, message_type=INFO):
        self.logger.log(self._get_level(message_type), message)

    def _create_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        if self.mode == Logger.JSON:
            template = '''{"time": "%(asctime)",
                        "type": "%(levelname)",
                        "message": "%(message)"}'''
            formatter = logging.Formatter(template)
        elif self.mode == Logger.HUMAN:
            template = '%(asctime)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(template)

        if self.file_path != None:
            file_handler = logging.FileHandler(self.file_path)
            file_handler.setLevel(self._get_level(self.log_level))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self._get_level(self.verbose_level))
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger

    def _get_level(self, level):
        if level == Logger.DEBUG:
            return logging.DEBUG
        elif level == Logger.WARNING:
            return logging.WARNING
        elif level == Logger.INFO:
            return logging.INFO
        elif level == Logger.ERROR:
            return logging.ERROR
