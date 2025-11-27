from .config import load_client_config, load_actions_config
from .mqtt_handler import create_mqtt_client
from .i18n import _

def main():
    try:
        client_cfg = load_client_config()
        actions_cfg = load_actions_config()
    except Exception as e:
        print(_("Failed to load config: {error}").format(error=e))
        return

    mqtt_cfg = client_cfg["mqtt"]
    client_info = client_cfg["client"]

    userdata = {
        "base_topic": mqtt_cfg.get("base_topic", "net-ctrl-pc"),
        "client_id": client_info["id"],
        "exec_timeout": client_info.get("exec_timeout", 1),
        "actions": {a["cmd"]: a for a in actions_cfg.get("actions", {}).values()},
        "mqtt_cfg": mqtt_cfg,
    }

    client = create_mqtt_client(userdata)

    try:
        client.connect(mqtt_cfg["host"], mqtt_cfg["port"], 60)
    except Exception as e:
        print(_("Failed to connect to MQTT broker: {error}").format(error=e))
        return

    client.loop_forever()

if __name__ == "__main__":
    main()
