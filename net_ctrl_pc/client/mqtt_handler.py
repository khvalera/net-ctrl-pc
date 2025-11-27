import paho.mqtt.client as mqtt
import json
from .i18n import _

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(_("Client connected to broker"))
        base_topic = userdata['base_topic']
        client_id = userdata['client_id']
        client.subscribe(f"{base_topic}/{client_id}/commands")
    else:
        print(_("Failed to connect, rc={rc}").format(rc=rc))

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        cmd = payload.get("cmd")
        if cmd is None:
            print(_("No 'cmd' in payload"))
            return
        ack_topic = f"{userdata['base_topic']}/{userdata['client_id']}/ack"
        from .actions import handle_command
        handle_command(cmd, userdata["actions"], userdata['exec_timeout'], client, ack_topic)
    except Exception as e:
        print(_("Error in on_message: {error}").format(error=e))

def create_mqtt_client(userdata):
    client = mqtt.Client(userdata["client_id"])
    mqtt_cfg = userdata["mqtt_cfg"]
    client.username_pw_set(mqtt_cfg.get("username"), mqtt_cfg.get("password"))
    client.user_data_set(userdata)
    client.on_connect = on_connect
    client.on_message = on_message
    return client
