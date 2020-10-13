#! /usr/bin/env python3.7

import configparser
import os


mainPath=os.path.dirname(os.path.abspath( __file__ ))

config = configparser.RawConfigParser()
config.read(os.path.join(mainPath , 'Config.cfg'))

#ServerHost=config.get('Server', 'ServerHost')
#ServerPort=int(config.get('Server','ServerPort'))
#Owner=config.get('Client','ID')
privateKey = config.get('Client','privateKey')

Owner='autodeploy'