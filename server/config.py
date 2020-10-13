#! /usr/bin/env python3.7

import configparser
import os


mainPath=os.path.dirname(os.path.abspath( __file__ ))

config = configparser.RawConfigParser()
config.read(os.path.join(mainPath , 'Config.cfg'))

publicKey=config.get('Server', 'publicKey')
port=config.get('Server', 'port')
client_url = config.get('Client', 'url')
try:
    log_limit=config.get('MISC', 'log_limit')
except:
    log_limit=100
