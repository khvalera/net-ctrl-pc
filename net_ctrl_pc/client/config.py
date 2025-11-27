import os
import yaml
from .i18n import _

CONFIG_DIR = "/etc/net-ctrl-pc"
CLIENT_CONFIG_FILE = os.path.join(CONFIG_DIR, "client.yaml")
ACTIONS_CONFIG_FILE = os.path.join(CONFIG_DIR, "actions.yaml")

def load_yaml_config(path):
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(_("Config file not found: {path}").format(path=path))
    except Exception as e:
        raise RuntimeError(_("Error loading config {path}: {error}").format(path=path, error=e))

def load_client_config():
    return load_yaml_config(CLIENT_CONFIG_FILE)

def load_actions_config():
    return load_yaml_config(ACTIONS_CONFIG_FILE)
