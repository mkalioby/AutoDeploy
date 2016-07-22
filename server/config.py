#! /usr/bin/env python

import ConfigParser
import os


mainPath=os.path.dirname(os.path.abspath( __file__ ))

config = ConfigParser.RawConfigParser()
config.read(os.path.join(mainPath , 'Config.cfg'))

publicKey=config.get('Server', 'publicKey')
port=config.get('Server', 'port')

main_url=config.get('mainserver',"url")
main_token=config.get('mainserver',"token")
main_interval=int(config.get('mainserver',"interval"))