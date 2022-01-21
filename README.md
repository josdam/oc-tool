# OC Tool

OpenShit Client Tool

### Options

- List servers defined into `$HOME/.oc-tool/config.yml`.
- Login against server: A simple wrapper over `oc login` command.

## Examples Usage

### List servers

```
octool.py list
```

Show the list of servers defined in `$HOME/.oc-tool/config.yml`

#### Example: [config.yml](./config.yml)

### Login against server

```
octool.py login [server] --username=foo --password=bar
```

The _[server]_ option will take the value of the one from the listed in the SERVER column from `octool.py list`.

If _username_ and/or _password_ are not given, default values are taken from OC_LOGIN_USER and OC_LOGIN_PASSWORD
environment variables.

