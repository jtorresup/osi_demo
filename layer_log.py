import sys


LOG_LAYER_PREFIX_FMT = "%s[%s::%s]\x1b[0m %s"
INFO_COLOR_FMT = "\x1b[32m%s\x1b[0m: %s"
WARN_COLOR_FMT = "\x1b[33m%s\x1b[0m: %s"
ERROR_COLOR_FMT = "\x1b[31m%s\x1b[0m: %s"


def info(layername: str, message: str, *args, **kwargs):
    print(
        LOG_LAYER_PREFIX_FMT % ("\x1b[32m", layername, "INFO", message),
        *args,
        **kwargs,
    )


def warn(layername: str, message: str, *args, **kwargs):
    print(
        LOG_LAYER_PREFIX_FMT % ("\x1b[33m", layername, "WARN", message),
        *args,
        **kwargs,
    )


def error(layername: str, message: str, *args, **kwargs):
    print(
        LOG_LAYER_PREFIX_FMT % ("\x1b[31m", layername, "ERROR", message),
        *args,
        **kwargs,
        file=sys.stderr,
    )
