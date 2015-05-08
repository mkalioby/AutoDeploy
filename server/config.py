#! /usr/bin/env python

import ConfigParser
import os


mainPath=os.path.dirname(os.path.abspath( __file__ ))

config = ConfigParser.RawConfigParser()
config.read(os.path.join(mainPath , 'Config.cfg'))

publicKey=config.get('Server', 'publicKey')
port=config.get('Server', 'port')
