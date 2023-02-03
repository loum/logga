# Logga

`logga` wraps the standard [Python logging](https://docs.python.org/3/library/logging.html) module and
abstracts some of the messy parts. `logging` itself is similar to (possibly even motivated by) the
[log4j](https://logging.apache.org/log4j/2.x/) project. Most importantly, `logging` guarantees a singleton object
that can be used throughout your project.

Other useful links:

- [logging.config — Logging configuration](https://docs.python.org/3/library/logging.config.html#module-logging.config)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

## Simplest Usage (Console)

!!! note
    Behind the scenes, the `logga` log handler object is instantiated through the module-level
    function `logging.getLogger(name)`. Multiple calls to `getLogger()` with the same name will always
    return a reference to the same logger object.

    `name` is defined as the highest level Python calling module. For example, in the
    [Module usage](#module-usage) sample below,
    `name` will be `you_beaut.py`. For normal console-based output, name would be `<stdin>`.

The following example demonstrates console-based usage that writes to `STDOUT` from within the Python interpreter:

``` sh title="Logga from the Python interpreter"
>>> from logga import log, set_log_level
>>> log.info("This is an INFO level log")
2023-01-08 22:56:56 logga [INFO]: This is an INFO level log
```

`logga` provides a default logger for you. This defaults to the log level `INFO`. You can set the
log level with the `set_log_level` function:

``` sh title="Change log level to WARNING. DEBUG is suppressed."
>>> set_log_level("WARNING")
>>> log.debug("This is a DEBUG level log")
>>>
```

``` sh title="Change log level to DEBUG. DEBUG is displayed."
>>> set_log_level("DEBUG")
>>> log.debug("This is a DEBUG level log")
>>> 2023-01-08 23:03:13 logga [DEBUG]: This is a DEBUG level log
```

## Module usage
Logging from your `*.py` is probably a more useful proposition. To demonstrate, add the
following code into a file called `you_beaut.py`:

``` sh title="you_beaut.py"
from logga import log

log.info("Log from inside my Python module")
```

To execute:

``` sh
python you_beaut.py
```

``` sh title="you_beaut.py logs"
2023-01-08 23:20:14 logga [INFO]: Log from inside my Python module
```

But what if you want to log to a file? In this case you will have to provide configuration. The structure
of the config is standard `logging`. For example, place the following configuration into a file called `log.conf`
in the same directory as `you_beaut.py`:

``` sh title="Sample log.conf"
[loggers]
keys=root,you_beaut.py,console

[handlers]
keys=youBeautFileHandler,consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_console]
level=DEBUG
handlers=consoleHandler
qualname=console
propagate=0

[logger_you_beaut.py]
level=DEBUG
qualname=you_beaut.py
handlers=youBeautFileHandler

[handler_youBeautFileHandler]
class=handlers.TimedRotatingFileHandler
level=DEBUG
formatter=simpleFormatter
args=(os.path.join(os.sep, "var", "tmp", "you_beaut.log"), "midnight")

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout, )

[formatter_simpleFormatter]
format=%(asctime)s (%(levelname)s): %(message)s
datefmt=
```

Now, when you `python you_beaut.py` you will notice that output to the console is suppressed.
Instead, the output is directed to a file stream defined by the `handler_youBeautFileHandler` section from
the `log.conf` file. To verify:

``` sh
cat /var/tmp/you_beaut.log
```

``` sh title="File-based logging output"
2023-01-08 23:23:57,361 (INFO): Log from inside my Python module
```
