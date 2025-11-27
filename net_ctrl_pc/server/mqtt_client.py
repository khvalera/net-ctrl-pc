
from .i18n import _  # Імпорт функції перекладу

import paho.mqtt.client as mqtt
import threading
import json

class MQTTClient:
    def __init__(self, config, logger, on_trigger_callback, on_ack_callback):
        self.config = config
        self.logger = logger
        self.on_trigger_callback = on_trigger_callback
        self.on_ack_callback = on_ack_callback

        self.client = mqtt.Client("net_ctrl_server")
        self.client.username_pw_set(config["mqtt"]["username"], config["mqtt"]["password"])
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.trigger_topics = set()

    def connect(self):
        self.client.connect(self.config["mqtt"]["host"], self.config["mqtt"]["port"], 60)
        self.client.loop_start()
        self.logger.info(_("MQTT loop started in background thread"))

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info(_("Connected to MQTT broker"))

            for rule in self.config.get("auto_rules", []):
                if rule.get("enabled", False):
                    topic = rule["trigger"]["topic"]
                    if topic not in self.trigger_topics:
                        self.trigger_topics.add(topic)
                        client.subscribe(topic)
                        self.logger.info(_("Subscribed to trigger topic: {topic}").format(topic=topic))
            base_topic = self.config["mqtt"]["base_topic"]
            for cl in self.config.get("clients", []):
                ack_topic = f"{base_topic}/{cl['id']}/ack"
                client.subscribe(ack_topic)
                self.logger.info(_("Subscribed to ack topic: {ack_topic}").format(ack_topic=ack_topic))
        else:
            self.logger.error(_("Failed to connect to MQTT broker, rc={rc}").format(rc=rc))

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        self.logger.info(_("Message received on topic {topic}: {payload}").format(topic=topic, payload=payload))

        if topic in self.trigger_topics:
            self.on_trigger_callback(topic, payload)
        elif topic.endswith("/ack"):
            self.on_ack_callback(topic, payload)

    def publish(self, topic, payload, qos=1):
        return self.client.publish(topic, payload, qos=qos)
