import os
import yaml
from .i18n import _

try:
    import importlib.resources as importlib_resources
except ImportError:
    import importlib_resources 

CONFIG_DIR = "/etc/net-ctrl-pc"
CONFIG_PATH = os.path.join(CONFIG_DIR, "server.yaml")

def load_yaml_config(path):
    if not os.path.isdir(CONFIG_DIR):
        raise FileNotFoundError(
            _("Config directory '{dir}' does not exist. Please create it and place server.yaml inside.").format(
                dir=CONFIG_DIR
            )
        )
    if not os.path.isfile(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(
            _("Failed to read configuration file '{file}': {error}").format(
                file=path, error=str(e)
            )
        )
    if not config:
        raise RuntimeError(
            _("Configuration file '{file}' is empty or invalid YAML.").format(
                file=path
            )
        )
    return config

def load_yaml_from_package(filename):
    try:
        package = __package__
        with importlib_resources.open_text(package, filename, encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(
            _("Failed to load packaged config '{file}': {error}").format(
                file=filename, error=str(e)
            )
        )
    if not config:
        raise RuntimeError(
            _("Packaged config file '{file}' is empty or invalid YAML.").format(
                file=filename
            )
        )
    return config

def load_config(path=None):
    cfg = load_yaml_config(CONFIG_PATH)
    if cfg is not None:
        return cfg
    return load_yaml_from_package("server.yaml")
