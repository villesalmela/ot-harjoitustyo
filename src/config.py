import os
import sys
import logging

from dotenv import load_dotenv


class StreamToLogger:
    """
    Fake file-like stream object that redirects writes to a logger instance.

    Generated with ChatGPT.
    """

    def __init__(self, logger_name, log_level):
        self.logger = logging.getLogger(logger_name)
        self.log_level = log_level

    def write(self, buffer):
        for line in buffer.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


def configure_logging() -> None:
    """
    Redirects logs to a file.

    stdout, stderr and all logs from the logging framework are redirected to a file.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
        filename="logs/app.log",
        filemode="w"
    )

    sys.stdout = StreamToLogger("STDOUT", logging.INFO)
    sys.stderr = StreamToLogger("STDERR", logging.ERROR)


configure_logging()

load_dotenv()  # handles searching for .env file and gracefully handles if it doesn't exist
DB_PATH = os.getenv("DB_PATH", "database.db")
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "30"))
FILESIZE_LIMIT_BYTES = int(os.getenv("FILESIZE_LIMIT_BYTES", "100000000"))  # 100 MB
