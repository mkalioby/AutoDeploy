import ConfigParser
import os


mainPath=os.path.dirname(os.path.abspath( __file__ ))[:-6]+''

config = ConfigParser.RawConfigParser()
config.read(os.path.join(mainPath ,'config' ,'config.cfg'))

ServerHost=config.get('Server', 'ServerHost')
ServerPort=config.get('Server','ServerPort')
Owner=config.get('Client','ID')
