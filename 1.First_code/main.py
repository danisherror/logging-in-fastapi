import logging
import logging.config
from fastapi import FastAPI
from typing import Union
import uvicorn
from uvicorn.config import LOGGING_CONFIG

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def set_logging(log_file):
    # Formatter commun
    file_format = "%(asctime)s %(levelname)-8s : %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(file_format, datefmt=date_format)

    # Setup File Handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Setup Console Handler (affiche dans la console)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Configure logging pour Uvicorn
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = file_format
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = file_format
    LOGGING_CONFIG["formatters"]["default"]["datefmt"] = date_format
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = date_format

    # Définition des handlers pour les logs dans Uvicorn
    LOGGING_CONFIG["handlers"]["default"] = {
        "class": "logging.FileHandler",
        "formatter": "default",
        "level": "INFO",
        "filename": log_file
    }

    LOGGING_CONFIG["handlers"]["access"] = {
        "class": "logging.FileHandler",
        "formatter": "access",
        "level": "INFO",
        "filename": log_file
    }

    # Ajouter le console handler à la configuration par défaut
    LOGGING_CONFIG["handlers"]["console"] = {
        "class": "logging.StreamHandler",
        "formatter": "default",
        "level": "INFO"
    }

    LOGGING_CONFIG["loggers"]["uvicorn"]["handlers"] = ["default", "console"]
    LOGGING_CONFIG["loggers"]["uvicorn.access"]["handlers"] = ["access", "console"]

    # Appliquer la configuration de logging
    logging.config.dictConfig(LOGGING_CONFIG)

def main():
    log_file = "app.log"
    set_logging(log_file)

    uvicorn.run("main:app", host="0.0.0.0",
                port=8000,
                log_level="info",
                proxy_headers=True,
                root_path="",
                use_colors=False)
if __name__ == "__main__":
    main()
