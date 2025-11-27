
import sys
import os
from .config import load_config
from .logger_setup import setup_logger
from .i18n import setup_i18n
from .mqtt_client import MQTTClient
from .command_handler import CommandHandler

def main():
    config_file = "server.yaml"
    config = load_config(config_file)
    logger = setup_logger(config)
    # i18n initialization, _ — translation function
    _ = setup_i18n()

    cmd_handler = CommandHandler(config, None, logger)

    def trigger_callback(topic, payload):
        cmd_handler.handle_trigger(topic, payload)

    def ack_callback(topic, payload):
        cmd_handler.handle_ack(topic, payload)

    mqtt_client = MQTTClient(config, logger, trigger_callback, ack_callback)
    cmd_handler.mqtt_client = mqtt_client

    mqtt_client.connect()

    try:
        while True:
            # main loop, everything is asynchronous in mqtt loop
            pass
    except KeyboardInterrupt:
        logger.info(_("Shutting down..."))

if __name__ == "__main__":
    main()
