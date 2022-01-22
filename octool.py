#!/usr/bin/python

"""OC Tool: OpenShit Client Tool"""
import os
import subprocess
import sys

import click
import yaml
from click import style
from columnar import columnar

OC_LOGIN_DIR = os.getenv("HOME") + "/.oc-tool"
OC_LOGIN_CONFIG_FILE = OC_LOGIN_DIR + "/config.yml"
SERVERS = []


@click.group(name="OC Tool")
@click.version_option(version='0.1.5')
def commands():
    """Commands group"""


@commands.command(name="list")
def list_servers():
    """List servers"""
    headers = ('SERVER', 'DESCRIPTION', 'API URL', 'CONSOLE OPENSHIFT URL')
    patterns = [
        ('dev.+', lambda text: style(text, fg='white')),
        ('pre.+', lambda text: style(text, fg='yellow')),
        ('pro.+', lambda text: style(text, fg='red')),
    ]
    if len(SERVERS) > 0:
        print(columnar(SERVERS, headers, no_borders=True, patterns=patterns))
    else:
        print(f"Ops! No servers found. Check your configuration file: {OC_LOGIN_CONFIG_FILE}.")


@commands.command(name="login")
@click.argument("server")  # add the name argument
@click.option('--username', '-u', envvar='OC_LOGIN_USER', prompt="Username",
              help='The username for server. Default value is taken from OC_LOGIN_USER env var.')
@click.password_option('--password', '-p', envvar='OC_LOGIN_PASSWORD', confirmation_prompt=False,
                       help='The password for server. Default value is taken '
                            'from OC_LOGIN_PASSWORD env var.')
def login_server(server, username, password):
    """Login against server"""

    if not username:
        print("Username is mandatory.")
        sys.exit(1)

    if not password:
        print("Password is mandatory.")
        sys.exit(1)

    url = list(filter(lambda s: s[0] == server, SERVERS))
    if len(url) == 0:
        print(f"Server '{server}' not found.")
        sys.exit(1)

    print(f"Trying to connect against: {url[0][2]}")
    command = "oc login " \
              + url[0][2] \
              + " --username=" + username + " --password=" + password \
              + " --insecure-skip-tls-verify=true"
    do_command(command)


def do_command(command):
    """Execute the given command"""

    with subprocess.Popen(command.split(), universal_newlines=True,
                          stdout=subprocess.PIPE) as sub_process:
        while True:
            output = sub_process.stdout.readline()
            if output:
                print(output.strip())
            elif sub_process.poll() is not None:
                break


def read_config_file():
    """Read and load config file"""

    if not os.path.exists(OC_LOGIN_CONFIG_FILE):
        os.makedirs(OC_LOGIN_DIR, exist_ok=True)
        with open(OC_LOGIN_CONFIG_FILE, 'w', encoding='UTF-8'):
            pass

    with open(OC_LOGIN_CONFIG_FILE, 'r', encoding='UTF-8') as config_file:
        config = yaml.full_load(config_file)

    if config:
        for server in config["servers"]:
            SERVERS.append(
                [server["server"],
                 server["description"],
                 server["api-url"],
                 server["console-url"]])


if __name__ == "__main__":
    read_config_file()
    commands()

    sys.exit(0)
