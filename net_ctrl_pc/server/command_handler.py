import threading
import json
import time
from .i18n import _

class CommandHandler:
    def __init__(self, config, mqtt_client, logger):
        self.config = config
        self.mqtt_client = mqtt_client
        self.logger = logger
        self.lock = threading.Lock()
        self.pending_commands = {}

    def run_auto_rule(self, name, command, retries, clients):
        self.logger.info(_("Running auto_rule '{name}' with command '{command}' on clients: {clients}").format(
            name=name, command=command, clients=clients))

        sub_clients = []
        main_clients = set()

        # We divide customers into sub and main ones
        for client_id in clients:
            conf = self.get_client_config(client_id)
            if not conf:
                self.logger.warning(_("Client config for '{client_id}' not found, skipping").format(client_id=client_id))
                continue
            if "main" in conf:
                sub_clients.append(client_id)
                main_clients.add(conf["main"])
            else:
                main_clients.add(client_id)

        main_clients = list(main_clients)

        # Process subclients — do not interrupt the loop on error
        for client_id in sub_clients:
            conf = self.get_client_config(client_id)
            retries_client = conf.get("retries", retries)
            exec_timeout = conf.get("exec_timeout", 5)
            success = self.send_command_with_retries(client_id, command, retries_client, exec_timeout)
            if not success:
                self.logger.warning(_("Command '{command}' failed on sub-client '{client_id}'. Continuing with main clients.").format(
                    command=command, client_id=client_id))
                # We don't interrupt - we continue

        delay = self.config.get("main_command_delay", 0)
        if delay > 0:
            self.logger.info(_("Waiting {delay} seconds before sending commands to main clients...").format(delay=delay))
            time.sleep(delay)

        # We process major clients
        for main_client_id in main_clients:
            conf = self.get_client_config(main_client_id)
            if not conf:
                self.logger.warning(_("Main client config '{main_client_id}' not found, skipping").format(main_client_id=main_client_id))
                continue
            retries_client = conf.get("retries", retries)
            exec_timeout = conf.get("exec_timeout", 5)
            success = self.send_command_with_retries(main_client_id, command, retries_client, exec_timeout)
            if not success:
                self.logger.warning(_("Command '{command}' failed on main client '{client_id}'. Continuing with next clients.").format(
                    command=command, client_id=main_client_id))
                # Continue to the next

    def get_client_config(self, client_id):
        for c in self.config.get("clients", []):
            if c["id"] == client_id:
                return c
        return None

    def send_command_with_retries(self, client_id, command, retries, exec_timeout):
        base_topic = self.config["mqtt"]["base_topic"]
        cmd_topic = f"{base_topic}/{client_id}/commands"

        ack_received = threading.Event()
        exec_started = threading.Event()
        with self.lock:
            self.pending_commands[client_id] = {'ack_received': ack_received, 'exec_started': exec_started}

        for attempt in range(1, retries + 1):
            self.logger.info(_("Sending command '{command}' to {client_id}, attempt {attempt}/{retries}").format(
                command=command, client_id=client_id, attempt=attempt, retries=retries))
            payload = json.dumps({"cmd": command})
            result = self.mqtt_client.publish(cmd_topic, payload, qos=1)
            if result.rc != 0:
                self.logger.warning(_("Failed to publish command to {cmd_topic}, rc={rc}").format(
                    cmd_topic=cmd_topic, rc=result.rc))
                continue
            else:
                self.logger.info(_("Published command to {cmd_topic}").format(cmd_topic=cmd_topic))

            if not ack_received.wait(timeout=exec_timeout):
                self.logger.warning(_("[{client_id}] No ACK received, retrying...").format(client_id=client_id))
                continue

            if not exec_started.wait(timeout=exec_timeout):
                self.logger.warning(_("[{client_id}] No execution start ACK received, retrying...").format(client_id=client_id))
                continue

            self.logger.info(_("[{client_id}] Command '{command}' executed successfully").format(client_id=client_id, command=command))
            with self.lock:
                self.pending_commands.pop(client_id, None)
            return True

        else:
            self.logger.error(_("[{client_id}] Failed to execute command '{command}' after {retries} retries").format(
                client_id=client_id, command=command, retries=retries))

        with self.lock:
            self.pending_commands.pop(client_id, None)
        return False

    def handle_ack(self, topic, payload):
        base_topic = self.config["mqtt"]["base_topic"]
        parts = topic.split('/')
        if len(parts) == 3:
            client_id = parts[1]
            try:
                data = json.loads(payload)
            except Exception as e:
                self.logger.warning(_("Error parsing ACK message JSON: {error}").format(error=e))
                return

            cmd = data.get("cmd")
            status = data.get("status")
            if client_id in self.pending_commands:
                events = self.pending_commands[client_id]
                if status == "received":
                    events['ack_received'].set()
                    self.logger.info(_("[{client_id}] ACK received for command '{cmd}'").format(client_id=client_id, cmd=cmd))
                elif status == "executing":
                    events['exec_started'].set()
                    self.logger.info(_("[{client_id}] Command '{cmd}' execution started").format(client_id=client_id, cmd=cmd))

    def handle_trigger(self, topic, payload):
        try:
            val = float(payload)
        except ValueError:
            self.logger.warning(_("Cannot convert payload '{payload}' to float").format(payload=payload))
            return

        for rule in self.config.get("auto_rules", []):
            if not rule.get("enabled", False):
                continue
            trigger = rule["trigger"]
            if trigger["topic"] != topic:
                continue

            cond = trigger["condition"]
            val_min = cond["value"] - cond.get("range", 0)
            val_max = cond["value"]
            val_type = cond["type"]

            self.logger.debug(_("Checking condition: val={val}, type={val_type}, value={value}, range={range_val}").format(
                val=val, val_type=val_type, value=cond["value"], range_val=cond.get("range",0)))
            cond_result = False
            if val_type == "numeric_less_equal":
                cond_result = (val_min <= val <= val_max)
            else:
                self.logger.warning(_("Unsupported condition type: {val_type}").format(val_type=val_type))

            self.logger.debug(_("Condition range: {val_min} <= {val} <= {val_max}").format(val_min=val_min, val=val, val_max=val_max))
            self.logger.debug(_("Condition result: {cond_result}").format(cond_result=cond_result))

            if cond_result:
                self.logger.info(_("Condition matched! Running auto_rule '{rule_name}'").format(rule_name=rule['name']))
                action = rule["action"]
                cmd = action["command"]
                retries = action.get("retries", 3)
                clients = action.get("clients", [])
                threading.Thread(target=self.run_auto_rule, args=(rule['name'], cmd, retries, clients), daemon=True).start()
                # After running the rule, complete the verification cycle
                break
