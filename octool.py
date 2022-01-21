#!/usr/bin/python
import os
import subprocess
import sys

import click
import yaml
from click import style
from columnar import columnar

oc_login_dir = os.getenv("HOME") + "/.oc-tool"
oc_login_config_file = oc_login_dir + "/config.yml"
servers = []


@click.group(name="OC Tool")
@click.version_option(version='0.1.2')
def commands():
    pass


@commands.command(name="list")
def list_servers():
    """List servers"""
    headers = ('SERVER', 'DESCRIPTION', 'API URL', 'CONSOLE OPENSHIFT URL')
    patterns = [
        ('dev.+', lambda text: style(text, fg='white')),
        ('pre.+', lambda text: style(text, fg='yellow')),
        ('pro.+', lambda text: style(text, fg='red')),
    ]
    if len(servers) > 0:
        print(columnar(servers, headers, no_borders=True, patterns=patterns))
    else:
        print("Ops! No servers found. Check your configuration file: {}".format(oc_login_config_file))


@commands.command(name="login")
@click.argument("server")  # add the name argument
@click.option('--username', '-u', envvar='OC_LOGIN_USER', prompt="Username",
              help='The username for server. Default value is taken from OC_LOGIN_USER env var.')
@click.password_option('--password', '-p', envvar='OC_LOGIN_PASSWORD', confirmation_prompt=False,
                       help='The password for server. Default value is taken from OC_LOGIN_PASSWORD env var.')
def login_server(server, username, password):
    """Login against server by using the username"""

    if not username:
        print("Username is mandatory.")
        exit(1)

    if not password:
        print("password is mandatory.")
        exit(1)

    url = list(filter(lambda s: s[0] == server, servers))
    if len(url) == 0:
        print("Server '{0}' not found".format(server))
        exit(1)

    print("Trying to connect against: {0}".format(url[0][2]))
    command = "oc login " + url[0][
        2] + " --username=" + username + " --password=" + password + " --insecure-skip-tls-verify=true"
    do_command(command)


def do_command(command):
    sub_process = subprocess.Popen(command.split(), universal_newlines=True, stdout=subprocess.PIPE)
    while True:
        output = sub_process.stdout.readline()
        if output:
            print(output.strip())
        elif sub_process.poll() is not None:
            break


def read_config_file():
    if not os.path.exists(oc_login_config_file):
        os.makedirs(oc_login_dir, exist_ok=True)
        with open(oc_login_config_file, 'w'):
            pass

    global servers
    with open(oc_login_config_file, 'r') as config_file:
        config = yaml.full_load(config_file)

    if config:
        for server in config["servers"]:
            servers.append([server["server"], server["description"], server["api-url"], server["console-url"]])


if __name__ == "__main__":
    read_config_file()
    commands()

    sys.exit(0)
