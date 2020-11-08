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
failure_try = config.get('Client','failure_try')
sleep_time = config.get('Client','sleep_time')
Owner='autodeploy'