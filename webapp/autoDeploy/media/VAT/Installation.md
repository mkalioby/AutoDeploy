# Introduction

This document shows how to install autoDeploy on Ubuntu System

# Install Server

* Create an autodeploy user
```sh
# adduser --system --home /opt/autodeploy/home --shell /bin/bash autodeploy
```
* Add autodeploy to sudoers.
```sh
# adduser autodeploy sudo
```
* Download The latest release from [github](https://github.com/mkalioby/AutoDeploy/releases)
* Expand the downloaded archive to '/opt/autodeploy/home'
* Copy the file in UnixConfig to /etc/sudoers.d/

* Install the Client Library
```sh
# cd client; python setup.py install
```

* Edit Server init script so that it points to installation directory

* Copy server init script to /etc/init.d
* Add the init script to the start defaults
```sh
# update-rc.d autodeploy-server start
```

# Install Web Application

* Install required Packages
```sh
# pip install django==1.8 django-tables2==1.0.4 django-tables2-reports
```

* Configure your database
* Create empty database in your DBMS.  
* Edit Settings file in `webapp/autoDeploy/settings.py`.

* Create Database by 
```sh
$ python manage.py migrate
```
1. Start Django Sever
```sh
python manage.py runserver IP:PORT
```

TBD: A Guide to show how to configure autodeploy Django webapp with Apache should be done.

 



