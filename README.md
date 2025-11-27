# Net Ctrl PC
Remote control of computers via MQTT
Client + Server | Python 3 | Systemd | i18n

---

## Description

Net Ctrl PC is a system for centralized management of computers in a local network using an MQTT broker.

The system consists of two components:

- **Server** — receives commands from the administrator, sends them to clients, and waits for confirmations.
- **Client** — runs on workstations, accepts commands, and performs corresponding actions (poweroff, reboot, custom scripts, etc.).

Full localization support is implemented using gettext.

---

## Features

### Server
- Sends commands to clients
- Receives status updates (received, executing, done, error)
- Logging with rotation
- Runs as a systemd service

### Client
- Connects to MQTT broker
- Listens to its command topic
- Executes actions based on configuration:
  - poweroff
  - reboot
  - running bash scripts
  - custom commands
- Sends status back to the server
- Fully localized (uk/en)

---

## Installation

1. Clone the repository

```bash
    git clone https://github.com/yourname/net-ctrl-pc.git
    cd net-ctrl-pc
```

2. Install the Python package

```bash
    sudo python3 setup.py install
```

3. Create configuration directory and copy config files

```bash
    sudo mkdir -p /etc/net-ctrl-pc  
    sudo cp configs/*.yaml /etc/net-ctrl-pc/
```

4. Install systemd service files and reload daemon

```bash
    sudo cp systemd/*.service /usr/lib/systemd/system/
    sudo systemctl daemon-reload
```

---

## Configuration

### Server configuration (/etc/net-ctrl-pc/server.yaml)

```yaml
mqtt:
  host: "mqtt.local"
  port: 1883
  username: "server"
  password: "1234"
  base_topic: "net-ctrl-pc"

logging:
  file: "/var/log/net-ctrl-pc-server.log"
  level: "INFO"

### Client configuration (/etc/net-ctrl-pc/client.yaml)

mqtt:
  host: "mqtt.local"
  port: 1883
  username: "client"
  password: "clientpass"
  base_topic: "net-ctrl-pc"

client:
  id: "pc001"
  exec_timeout: 1

### Commands configuration (/etc/net-ctrl-pc/commands.yaml)

commands:
  poweroff:
    action: "shell"
    cmd: "systemctl poweroff"

  reboot:
    action: "shell"
    cmd: "systemctl reboot"

  custom_script:
    action: "shell"
    cmd: "/usr/local/bin/test.sh"
```
---

## Localization

To create or update translation templates (.pot) and translation files (.po):

Generate .pot file:

    xgettext --language=Python --keyword=_ --package-name=net-ctrl-pc --output=locale/net-ctrl-pc.pot $(find . -name "*.py")

Update .po files:

    msgmerge -U locale/uk/LC_MESSAGES/net-ctrl-pc-client.po locale/net-ctrl-pc-client.pot
    msgmerge -U locale/uk/LC_MESSAGES/net-ctrl-pc-server.po locale/net-ctrl-pc-server.pot

Compile .mo files:

    ./scripts/update-mo.sh

---

## Running

### Server

Run manually:

    python3 -m net_ctrl_pc.server

Or enable and start via systemd:

    sudo systemctl enable --now net-ctrl-pc-server

### Client

Run manually:

    python3 -m net_ctrl_pc.client

Or enable and start via systemd:

    sudo systemctl enable --now net-ctrl-pc-client

---

## MQTT Command Testing

Send a command:

    mosquitto_pub -t "net-ctrl-pc/pc001/commands" -m '{"cmd": "poweroff"}'

Expected responses:

- received
- executing
- done

---

## License

MIT License
