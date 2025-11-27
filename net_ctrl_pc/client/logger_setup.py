import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "/var/log/net-ctrl-pc"
LOG_FILE = os.path.join(LOG_DIR, "client.log")

def setup_logger():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger("net_ctrl_pc.client")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
