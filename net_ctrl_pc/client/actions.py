import subprocess
from .i18n import _

def execute_system_command(command):
    try:
        print(_("Executing system command: {cmd}").format(cmd=command))
        subprocess.Popen(command, shell=True)
    except Exception as e:
        print(_("Failed to execute system command '{cmd}': {error}").format(cmd=command, error=e))

def handle_command(cmd, actions, exec_timeout, client, ack_topic):
    if cmd not in actions:
        print(_("Unknown command '{cmd}' received, ignoring").format(cmd=cmd))
        return

    print(_("Received command '{cmd}'").format(cmd=cmd))

    # ACK received
    client.publish(ack_topic, '{"cmd": "%s", "status": "received"}' % cmd)
    print(_("Sent status 'received'"))

    # Runtime simulation
    import time
    time.sleep(exec_timeout)

    # ACK executing
    client.publish(ack_topic, '{"cmd": "%s", "status": "executing"}' % cmd)
    print(_("Sent status 'executing'"))

    system_cmd = actions[cmd].get("system_cmd")
    if system_cmd:
        execute_system_command(system_cmd)
    else:
        print(_("No system command configured for '{cmd}'").format(cmd=cmd))
