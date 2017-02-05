#!/usr/bin/env python

import signal
import logging
import logging.handlers
import ConfigParser

import os
import psutil 
import time 
import datetime
import sys 
from ISStreamer.Streamer import Streamer

# -- Get configuration information
dname = os.path.dirname(os.path.abspath(__file__))

# read values from the config file
config = ConfigParser.ConfigParser()
config.read(dname + "/config.txt")

# -- Setup Logging
logLevelConfig = config.get('logging', 'loglevel')
if logLevelConfig == 'info':
    LOG_LOGLEVEL = logging.INFO
elif logLevelConfig == 'warn':
    LOG_LOGLEVEL = logging.WARNING
elif logLevelConfig ==  'debug':
    LOG_LOGLEVEL = logging.DEBUG

frequency = int(config.get('main', 'checkfrequency'))
failcount = int(config.get('main', 'failcount'))

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LOGLEVEL)
handler = logging.handlers.TimedRotatingFileHandler(config.get('logging','logfile'), 
                                                    when=config.get('logging','logrotation'), 
                                                    backupCount=int(config.get('logging','logcount')))
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MyLogger(object):
        def __init__(self, logger, level):
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

sys.stdout = MyLogger(logger, logging.INFO)
sys.stderr = MyLogger(logger, logging.ERROR)


def main(argv):
	count = 0
	while True:
		try:
			f = open("/sys/class/net/wlan0/operstate","r")
			state = f.read()
			f.close()
			if state.startswith("up"):
				count = 0
				logger.debug("Network Up")
			else :
				logger.info("Network Down")
				count = count + 1
				if (count >= failcount):
					logger.info("Shutting down")
					os.system("shutdown -r now")
					time.sleep(30)
				else :	
					logger.info("Restarting interface")
					os.system("ifdown --force wlan0")
					time.sleep(10)
					os.system("ifup wlan")
		except:
			pass
		
		time.sleep(frequency)
	
if __name__ == "__main__":
	main(sys.argv)	
