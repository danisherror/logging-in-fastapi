import logging
import os
import time
from typing import Union


class PefixLogger(logging.LoggerAdapter):
    """custom logger to add a prefix"""

    def process(self, message, kwargs):
        return f"[{self.extra}] {message}", kwargs


class HtmlFileHandler(logging.FileHandler):
    """Html file handler - to be implemented"""


class Logger:
    """Wrapper for root logger"""

    def __init__(
        self,
        name: str = "",
        level: str = "DEBUG",
        console: bool = True,
        file: bool = True,
        log_format: str = "",
        file_path: str = ".",
        file_name: Union[str, None] = None,
        html_file: Union[str, None] = None,
    ):
        if name:
            self.name = name
            self.logger = logging.getLogger(self.name)
        else:
            self.name = ""
            self.logger = logging.getLogger()  # root logger
        self.remove_existing_handlers()
        self.add_logger_level(level)

        if console:
            self.add_stream_handler(level, log_format)
        if file:
            self.add_file_handler(level, log_format, file_path, file_name=file_name)
        if html_file:
            self.add_html_handler(level, log_format, html_file)

    def add_logger_level(self, level: str) -> None:
        self.logger.setLevel(logging.getLevelName(level))

    def get_stream_handler(self):
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                return handler
        return None

    def add_stream_handler(self, level: str, log_format: str) -> None:
        stream_handler = self.get_stream_handler()
        if not stream_handler:
            stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.getLevelName(level))
        stream_handler.setFormatter(logging.Formatter(log_format))
        self.logger.addHandler(stream_handler)

    def add_file_handler(
        self,
        level: str,
        log_format: str,
        file_path: str,
        file_name: Union[str, None] = None,
    ) -> None:
        if not file_name:
            file_name = f"{self.name}_{time.strftime('%Y_%m_%d_%H_%M_%S')}.log"
        else:
            file_name = f"{self.name}_{time.strftime('%Y_%m_%d_%H_%M_%S')}.log"
        file_handler = logging.FileHandler(
            os.path.join(file_path, file_name), encoding="utf-8"
        )
        file_handler.setLevel(logging.getLevelName(level))
        file_handler.setFormatter(self.set_format(log_format))
        self.logger.addHandler(file_handler)

    def add_html_handler(
        self,
        level: str,
        log_format: str,
        file_path: str,
    ) -> None:
        file_handler = HtmlFileHandler(filename=file_path)
        file_handler.setLevel(logging.getLevelName(level))
        file_handler.setFormatter(self.set_format(log_format))
        self.logger.addHandler(file_handler)

    def set_format(self, log_format=None) -> logging.Formatter:
        if log_format:
            return logging.Formatter(log_format)
        return logging.Formatter(
            "%(asctime)s %(levelname)-8s : %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

    def remove_existing_handlers(self) -> None:
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)

    def get_logger(self):
        return self.logger


def get_logger(
    name: Union[str, logging.Logger, None, logging.LoggerAdapter] = "",
    *args,
    **kwargs,
):
    if isinstance(name, logging.Logger):
        return name
    if isinstance(name, logging.LoggerAdapter):
        return name
    if not name:
        name = "log"
    if name in logging.Logger.manager.loggerDict.keys():
        return logging.getLogger(name)
    return Logger(name, *args, **kwargs).get_logger()


class InitializeLogger:
    def __init__(self):
        self.log = get_logger(
            name="",
            level="DEBUG",
            console=True,
            file=True,
            log_format="%(asctime)s %(levelname)-8s : %(message)s",
            file_path=os.path.join(os.getcwd()),
        )

    def hi(self):
        self.log.info("aas")
        self.log.debug("hi")
        self.log.warning("aas")
        self.log.error("aas")
        self.log.critical("aas")


inst = InitializeLogger()

inst.hi()
