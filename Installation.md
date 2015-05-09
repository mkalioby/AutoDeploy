# Introduction

This document shows how to install autoDeploy on Ubuntu System

1. Create an autodeploy user
```sh
# adduser --system --home /opt/autodeploy/home --shell /bin/bash autodeploy
```
2. Add autodeploy to sudoers.
```sh
# adduser autodeploy sudo
```
3. Copy the file in UnixConfig to /etc/sudoers.d/

