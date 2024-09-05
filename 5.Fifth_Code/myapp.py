import os
import logging
import logging.config
from typing import Union
from fastapi import FastAPI, Request
from starlette.responses import Response
from uvicorn.config import LOGGING_CONFIG

class MyApp:
    def __init__(self):
        self.app = FastAPI()
        self.setup_logging()
        self.setup_routes()
        self.app.middleware("http")(self.log_requests)

    def setup_logging(self):
        log_file = "app.log"

        # Create a file handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_format = "%(asctime)s %(levelname)-8s : %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(file_format, datefmt=date_format)
        file_handler.setFormatter(formatter)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Configure the logger
        logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

        # Configure Uvicorn's logging with your format
        LOGGING_CONFIG["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)-8s : %(message)s"
        LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelname)-8s : %(message)s"
        LOGGING_CONFIG["formatters"]["default"]["datefmt"] = date_format
        LOGGING_CONFIG["formatters"]["access"]["datefmt"] = date_format

        logging.config.dictConfig(LOGGING_CONFIG)
        self.log = logging.getLogger("uvicorn")

    def setup_routes(self):
        @self.app.get('/')
        def read_root():
            return {'message': 'Hello, World!'}

        @self.app.get('/items/{item_id}')
        def read_item(item_id: int, q: Union[str, None] = None):
            return {'item_id': item_id, 'q': q}

    async def log_requests(self, request: Request, call_next):
        response: Response = await call_next(request)
        try:
            status_code = str(response.status_code)
            message = f"Request {request.method} {request.url} called with {response.status_code} status"
            if status_code[0] == "2":
                self.log.info(message)
            elif status_code[0] == "3":
                self.log.warning(message)
            elif status_code[0] == "4":
                self.log.error(message)
            elif status_code[0] == "5":
                self.log.critical(message)
            else:
                self.log.debug(message)
        except Exception as e:
            self.log.error(f"Error while logging request: {str(e)}")
        return response

app_inst = MyApp()
app = app_inst.app
