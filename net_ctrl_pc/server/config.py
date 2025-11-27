
import os
import yaml
from .i18n import _

CONFIG_DIR = "/etc/net-ctrl-pc"
CONFIG_PATH = f"{CONFIG_DIR}/server.yaml"

def load_config(path=None):

    config_file = CONFIG_PATH

    # Перевірка на існування директорії
    if not os.path.isdir(CONFIG_DIR):
        raise FileNotFoundError(
            _("Config directory '{dir}' does not exist. Please create it and place server.yaml inside.").format(
                dir=CONFIG_DIR
            )
        )

    # Перевірка файлу
    if not os.path.isfile(config_file):
        raise FileNotFoundError(
            _("Configuration file not found: {file}. Please create it based on the template.").format(
                file=config_file
            )
        )

    # Читання YAML
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(
            _("Failed to read configuration file '{file}': {error}").format(
                file=config_file, error=str(e)
            )
        )

    # Перевірка на порожній YAML
    if not config:
        raise RuntimeError(
            _("Configuration file '{file}' is empty or invalid YAML.").format(
                file=config_file
            )
        )

    return config
