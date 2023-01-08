"""Custom logger based on content from https://docs.python.org/3/howto/logging-cookbook.html

Configuration file for the logging module can be provided in the following locations:
- A place named by the environment variable `LOGGA_CONF`
- Current directory - `./log.conf`
- User's home directory - `~$USER/log.conf`

If not found, fallback is Logga's own configuration.

This arrangement is analogous to "rc" files. for example, "bashrc", "vimrc", etc.

"""
from typing import List, Optional, Text
import datetime
import inspect
import logging
import logging.config
import os
import pathlib


def locations() -> List[Text]:
    """Provide logging configuration directory locations in order of precedence.

    Returns a list of locations as a set of strings that represent the directory location of the
    log.conf file.

    """
    def items():
        return (os.environ.get('LOGGA_CONF'),
                os.getcwd(),
                pathlib.Path.home())

    return items()


def get_logger_name() -> Optional[Text]:
    """Identify logger name to target handlers.

    The calling script will be the outermost call in the stack. Parse the
    resulting frame to get the name of the script.

    `<stdin>` is a special case that will explicitly return `None`

    Returns the logger name as a string, or None.

    """
    _name = os.path.basename(inspect.stack()[-1][1])
    if _name == '<stdin>':
        _name = None

    return _name


def source_logger_config():
    """Source logger config.

    """
    config_found = False
    for loc in locations():
        if loc is None:
            continue

        try:
            with open(os.path.join(loc, 'log.conf'), encoding='utf-8') as _fh:
                logging.config.fileConfig(_fh)
                config_found = True
                break
        except IOError:
            # Not a bad thing if the open failed. Just means that the log
            # source does not exist.
            continue

    logger_name: Optional[Text] = get_logger_name()

    if not config_found:
        logger_name = 'logga'

        # If we've fallen through to here, then use Logga's own config.
        config_path = os.path.join(pathlib.Path(__file__).resolve().parents[0],
                                   'config',
                                  'log.conf')
        with open(config_path, encoding='utf-8') as _fh:
            logging.config.fileConfig(_fh)

    return logger_name


def logger_name() -> Optional[Text]:
    """
    """
    def source():
        return source_logger_config()

    return source()

log = logging.getLogger(source_logger_config())

if log.name is not None:
    # Contain logging to the configured handler only (not console).
    log.propagate = False


def set_console():
    """Drop back to the root logger handler. This is typically the console.

    This can be used to override the logging file output stream and send
    log messages to the console. For example, consider the following
    code that has a ``log.conf`` that writes to the log file ``my.log``::

        from logga import log, set_console
        set_console()
        log.debug('Log from inside my Python module')

    The ``set_console()`` call will force the log message to write
    ``Log from inside my Python module`` to the console.

    """
    def default_console_config() -> logging.StreamHandler:
        """Default console config that can be used as a fallback.

        Returns a logging.StreamHandler configured with a simple format.

        """
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(asctime)s [%(levelname)s]:: %(message)s")
        console_handler.setFormatter(console_formatter)

        return console_handler

    for hdlr in log.handlers:
        log.removeHandler(hdlr)

    log.propagate = False

    log.addHandler(default_console_config())
    log.level = logging.NOTSET


def set_log_level(level='INFO'):
    """Set the lower threshold of logged message level. Level
    defaults to ``INFO``. All default log levels are supported
    ``NOTSET``, ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR`` and
    ``CRITICAL`` in order of severity.

    For example::

        >>> from logga import log, set_log_level
        >>> log.debug('This DEBUG message should display')
        2014-06-30 12:50:48,407 DEBUG:: This DEBUG message should display
        >>> set_log_level(level='INFO')
        >>> log.debug('This DEBUG message should now not display')
        >>> log.debug('This DEBUG message should now not display')
        >>> log.info('This INFO message should display')
        2014-06-30 12:51:44,782 INFO:: This INFO message should display

    **Kwargs:**
        *level*: the lower log level threshold. All log levels including
        and above this level in serverity will be logged

    """
    level_map = {
        'CRITICAL': logging.INFO,
        'ERROR': logging.INFO,
        'WARNING': logging.INFO,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.DEBUG,
    }

    log.setLevel(level_map[level])


def suppress_logging():
    """Provides an overriding (to level ``CRITICAL``) suppression mechanism
    for all loggers which takes precedence over the logger`s own level.

    When the need arises to temporarily throttle logging output down
    across the whole application, this function can be useful.
    Its effect is to disable all logging calls below severity level
    ``CRITICAL``. For example::

        >>> from logga import log, suppress_logging
        >>> log.debug('This DEBUG message should display')
        2014-06-30 13:00:39,882 DEBUG:: This DEBUG message should display
        >>> suppress_logging()
        >>> log.debug('This DEBUG message should now not display')
        >>> log.critical('But CRITICAL messages will get through')
        2014-06-30 13:02:59,159 CRITICAL:: But CRITICAL messages will get through

    """
    logging.disable(logging.ERROR)


def enable_logging():
    """Opposite of the :func:`logga.suppress_logging` function.

    Re-enables logging to ``DEBUG`` level and above::

        >>> from logga import log, suppress_logging, enable_logging
        >>> suppress_logging()
        >>> log.debug('This DEBUG message should now not display')
        >>> enable_logging()
        >>> log.debug('This DEBUG message should now display')
        2014-06-30 13:08:22,173 DEBUG:: This DEBUG message should now display

    """
    logging.disable(logging.NOTSET)


def autolog(message):
    """Automatically log the current function details.

    Used interchangeably with the ``log`` handler object. Handy for
    for verbose messaging during development by adding more verbose detail
    to the logging message, such as the calling function/method name
    and line number that raised the log call::

        >>> from logga import autolog
        >>> autolog('Verbose')
        2014-06-30 13:13:08,063 DEBUG:: Verbose: <module> in <stdin>:1
        >>> log.debug('DEBUG message')
        2014-06-30 13:15:35,319 DEBUG:: DEBUG message
        >>> autolog('DEBUG message')
        2014-06-30 13:15:41,760 DEBUG:: DEBUG message: <module> in <stdin>:1

    **Args:**
        *message*: the log message to display

    """
    if log.isEnabledFor(logging.DEBUG):
        # Get the previous frame in the stack.
        # Otherwise it would be this function!!!
        frame = inspect.currentframe().f_back.f_code
        lineno = inspect.currentframe().f_back.f_lineno

        # Dump the message function details to the log.
        log.debug('%s: %s in %s:%i', message, frame.co_name, frame.co_filename, lineno)
