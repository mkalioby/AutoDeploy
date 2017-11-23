#! /usr/bin/env python

import ConfigParser
import os


mainPath=os.path.dirname(os.path.abspath( __file__ ))

config = ConfigParser.RawConfigParser()
config.read(os.path.join(mainPath , 'Config.cfg'))

publicKey=config.get('Server', 'publicKey')
port=config.get('Server', 'port')
try:
    log_limit=config.get('MISC', 'log_limit')
except:
    log_limit=100
