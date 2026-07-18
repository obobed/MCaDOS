import logging, os, datetime, sys

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

def setup_logging():
    os.makedirs(LOG_PATH, exist_ok=True)

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_filename = f"{current_date}.log"
    full_log_path = os.path.join(LOG_PATH, log_filename)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(full_log_path)
        ]
    )

    logger = logging.getLogger(__name__)

    def log_exceptions(type, value, traceback): # this looks complex lol but its just boilerplate from the docs
        if issubclass(type, KeyboardInterrupt): # let ctrl cs work
            sys.__excepthook__(type, value, traceback)
            return
        logger.critical("Uncaught exception", exc_info=(type, value, traceback))

    sys.excepthook = log_exceptions