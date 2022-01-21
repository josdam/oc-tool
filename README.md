# OC Tools

OpenShit Client Tools

## OC Login

A simple wrapper over `oc login` command.

### Options

- List servers
- Login against server

## Examples Usage

### List servers

```
oclogin.py list
```

Show the list of servers defined in `$HOME/.oc-tools/oc-login/config.yml`

### Login against server

```
oclogin.py login [server] --username=foo --password=bar
```

the [server] option has to be filled with some value listed by the to list servers option. If username and/or password
are not given, default values are taken from OC_LOGIN_USER and OC_LOGIN_PASSWORD environment variables.

