import os
import yaml
from .i18n import _

try:
    import importlib.resources as importlib_resources
except ImportError:
    import importlib_resources

CONFIG_DIR = "/etc/net-ctrl-pc"
CLIENT_CONFIG_FILE = os.path.join(CONFIG_DIR, "client.yaml")
ACTIONS_CONFIG_FILE = os.path.join(CONFIG_DIR, "actions.yaml")

def load_yaml_config(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        raise RuntimeError(_("Error loading config {path}: {error}").format(path=path, error=e))

def load_yaml_from_package(filename):
    try:
        package = __package__
        with importlib_resources.open_text(package, filename, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(_("Error loading packaged config {filename}: {error}").format(filename=filename, error=e))

def load_client_config():
    cfg = load_yaml_config(CLIENT_CONFIG_FILE)
    if cfg is not None:
        return cfg
    return load_yaml_from_package("client.yaml")

def load_actions_config():
    cfg = load_yaml_config(ACTIONS_CONFIG_FILE)
    if cfg is not None:
        return cfg
    return load_yaml_from_package("actions.yaml")
