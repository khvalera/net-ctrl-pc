import paho.mqtt.client as mqtt
import json
import time
from .config import load_config, load_actions_config
from .actions import execute_system_command
from .i18n import _
import logging

class NetCtrlPCClient:
    def __init__(self):
        self.config = load_client_config()
        self.actions_cfg = load_actions_config()
        self.logger = logging.getLogger("net_ctrl_pc.client")

        mqtt_cfg = self.config["mqtt"]
        client_cfg = self.config["client"]

        self.base_topic = mqtt_cfg.get("base_topic", "net-ctrl-pc")
        self.client_id = client_cfg["id"]
        self.exec_timeout = client_cfg.get("exec_timeout", 1)

        self.actions = {a["cmd"]: a for a in self.actions_cfg.get("actions", {}).values()}

        self.client = mqtt.Client(self.client_id)
        self.client.username_pw_set(mqtt_cfg.get("username"), mqtt_cfg.get("password"))
        self.client.user_data_set(self)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info(_("Connected to MQTT broker"))
            topic = f"{self.base_topic}/{self.client_id}/commands"
            client.subscribe(topic)
            self.logger.info(_("Subscribed to topic {topic}").format(topic=topic))
        else:
            self.logger.error(_("Failed to connect to MQTT broker, rc={rc}").format(rc=rc))

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            cmd = payload.get("cmd")

            if not cmd:
                self.logger.warning(_("Received message without 'cmd' field"))
                return

            if cmd not in self.actions:
                self.logger.warning(_("Unknown command '{cmd}' received, ignoring").format(cmd=cmd))
                return

            self.logger.info(_("Received command '{cmd}'").format(cmd=cmd))

            ack_topic = f"{self.base_topic}/{self.client_id}/ack"

            # Send ACK of receipt
            client.publish(ack_topic, json.dumps({"cmd": cmd, "status": "received"}))
            self.logger.info(_("Sent status 'received'"))

            # Simulate execution time
            time.sleep(self.exec_timeout)

            # Send ACK of the start of execution
            client.publish(ack_topic, json.dumps({"cmd": cmd, "status": "executing"}))
            self.logger.info(_("Sent status 'executing'"))

            # Execute the system command
            system_cmd = self.actions[cmd].get("system_cmd")
            if system_cmd:
                execute_system_command(system_cmd, self.logger)
            else:
                self.logger.warning(_("No system command configured for '{cmd}'").format(cmd=cmd))

        except Exception as e:
            self.logger.error(_("Error processing message: {error}").format(error=e))

    def run(self):
        mqtt_cfg = self.config["mqtt"]
        self.client.connect(mqtt_cfg["host"], mqtt_cfg["port"], 60)
        self.client.loop_forever()
