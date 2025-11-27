import logging
import sys
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from .i18n import _

def setup_logger(config):
    log_cfg = config.get("logging", {})
    log_file = log_cfg.get("file", "/var/log/net-ctrl-pc/server.log")
    log_level_str = log_cfg.get("level", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    log_rotation = log_cfg.get("rotation", "size")
    log_max_bytes = log_cfg.get("max_bytes", 10*1024*1024)
    log_backup_count = log_cfg.get("backup_count", 5)
    log_when = log_cfg.get("when", "midnight")
    log_interval = log_cfg.get("interval", 1)

    logger = logging.getLogger("NetCtrlServer")
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    except Exception as e:
        print(_("Failed to create log directory: {error}").format(error=e))

    if log_rotation == "size":
        file_handler = RotatingFileHandler(log_file, maxBytes=log_max_bytes, backupCount=log_backup_count)
        logger.info(_("Logging with size-based rotation: maxBytes={max_bytes}, backup count={backup_count}").format(
            max_bytes=log_max_bytes, backup_count=log_backup_count))
    else:
        file_handler = TimedRotatingFileHandler(log_file, when=log_when, interval=log_interval, backupCount=log_backup_count)
        logger.info(_("Logging with time-based rotation: when={when}, interval={interval}, backup count={backup_count}").format(
            when=log_when, interval=log_interval, backup_count=log_backup_count))

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info(_("Logger initialized. Log file: {log_file}, Level: {level}").format(log_file=log_file, level=log_level_str))

    return logger
