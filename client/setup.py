#!/usr/bin/env python3.7

from distutils.core import setup

setup(name='autodeploy_client',
      version='0.5',
      description='The Client for the autodeploy system',
      author='Mohamed El-Kalioby',
      author_email='mkalioby@mkalioby.com',
      url='https://github.com/mkalioby/autoDeploy',
      packages=['autodeploy_client'],
      package_data={"autodeploy_client":["my","Config.cfg"]}
     )