import os
import sys
from gin.common.logging import Logging as GinLogging
import logging

ASG_TOOL_LOGGER = "asg_tool"
logger = logging.getLogger(ASG_TOOL_LOGGER)

gin_loggers = ["base", "llm", "agentic_workflow", "tool_calling", "mapping_service"]

noisy_lib_loggers = [
    "httpx",
    "openai",
    "_config",
    "_base_client",
    "_trace",
    "_client",
]


def setup_logging():
    # first, set up my logging, just to enable logging GIN_DEBUG
    _setup_logging()
    gin_log_level = "DEBUG" if os.getenv("GIN_DEBUG") else "INFO"
    logger.debug(f"gin_log_level={gin_log_level}")
    logger.debug(f"gin_loggers={gin_loggers}")
    logger.debug(f"noisy_lib_loggers={noisy_lib_loggers}")

    # now, let GIN do its thing (this disables my settings)
    GinLogging(log_level=gin_log_level)

    # now, take back the control
    _setup_logging()

    # if GIN_DEBUG not set, silence its loggers
    if not os.getenv("GIN_DEBUG"):
        for name in gin_loggers:
            _silence_logger(name, logging.WARNING)

    # silence other unwanted loggers
    for name in noisy_lib_loggers:
        _silence_logger(name, logging.WARNING)


def _silence_logger(noisy_logger_name: str, level):
    noisy_logger = logging.getLogger(noisy_logger_name)
    noisy_logger.setLevel(level)  # cap them unless GIN_DEBUG is set
    noisy_logger.propagate = True  # let it bubble to your root handlers


def _setup_logging():
    format = (
        "%(asctime)s [%(levelname)s] %(module)s.%(funcName)s.%(lineno)d: %(message)s"
    )
    formatter = Formatter(format, datefmt="%H:%M")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logging.basicConfig(
        handlers=[handler],
        level=logging.WARNING,
        force=True,  # override previous handlers
    )
    logging.getLogger(ASG_TOOL_LOGGER).setLevel(
        logging.DEBUG if os.getenv("DEBUG") else logging.INFO
    )


COLORS = {
    logging.DEBUG: "\033[34m",  # blue
    logging.INFO: "\033[32m",  # green
    logging.WARNING: "\033[33m",  # yellow
    logging.ERROR: "\033[31m",  # red
    logging.CRITICAL: "\033[41m\033[30m",  # red bg, black text
}


class Formatter(logging.Formatter):
    def __init__(self, fmt: str, datefmt: str, use_color: bool = True):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.fmt = fmt
        self.datefmt = datefmt
        self.use_color = use_color

    def format(self, record):
        fmt = self.fmt
        if self.use_color and record.levelno in COLORS:
            fmt = COLORS[record.levelno] + self.fmt + "\033[0m"
        formatter = logging.Formatter(fmt, self.datefmt)
        return formatter.format(record)


# %(pathname)s → full file system path (too long, usually not useful in logs)
# %(filename)s → just the file name (e.g. my_module.py)
# %(module)s → file name without extension (e.g. my_module)
# %(name)s → logger name (usually the dotted module path if you did logging.getLogger(__name__))
# %(funcName)s → the function/method name
