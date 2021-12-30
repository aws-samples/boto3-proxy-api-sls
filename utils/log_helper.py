"""
Log related utilities
"""
# pylint: disable=unused-argument, protected-access, arguments-differ,no-name-in-module,
# import-error,wrong-import-position

import logging
import uuid
import os


def get_context_id(logger):
    """
    Find if the logger is of type default or custom logger class and return context id
    Args:
        logger:

    Returns:

    """
    if type(logger) is Logger:
        return logger.get_uuid()
    else:
        return None


class Logger(object):
    """
    Class with custom log formatter to include request context id in log statements for tracking
    """
    def __init__(self):
        log = logging.getLogger()
        for h in log.handlers:
            h.setFormatter(logging.Formatter("[%(levelname)s]:%(message)s"))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get("LOG_LEVEL", logging.INFO))
        self.set_new_uuid()

    def set_new_uuid(self):
        """
        Generate context id
        Returns:

        """
        self._id = uuid.uuid4().hex

    def get_uuid(self):
        """
        Retrieve context id
        Returns:

        """
        return self._id

    def set_uuid(self, id):
        """
        Overwrite default context id
        Args:
            id:

        Returns:

        """
        self._id = id

    def format_msg(self, msg):
        return "{}: {}".format(self._id, msg)

    def error(self, msg, *args):
        self.logger.error(self.format_msg(msg), *args)

    def info(self, msg, *args):
        self.logger.info(self.format_msg(msg), *args)

    def warn(self, msg, *args):
        self.logger.warning(self.format_msg(msg), *args)

    def warning(self, msg, *args):
        self.logger.warning(self.format_msg(msg), *args)

    def debug(self, msg, *args):
        self.logger.debug(self.format_msg(msg), *args)