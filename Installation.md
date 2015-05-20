# Introduction

This document shows how to install autoDeploy on Ubuntu System

*. Create an autodeploy user
```sh
# adduser --system --home /opt/autodeploy/home --shell /bin/bash autodeploy
```
*. Add autodeploy to sudoers.
```sh
# adduser autodeploy sudo
```
*. Copy the file in UnixConfig to /etc/sudoers.d/

* Install the Client Library
```sh
# python setup.py install
```

* Install pyCrypto
```sh
# pip install python-pycrypto
```

* Install yaml
```sh
# pip install pyyaml
```

* Edit Server init script so that it points to installation directory

* Copy server init script to /etc/init.d

* Configure your database
  *   Edit Settings file.
  *   Create empty database in your DBMS.
```sh
python manage.py migrate
```


 



