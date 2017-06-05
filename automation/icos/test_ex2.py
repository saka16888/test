import sys, os , time

import pytest

#from testbed.testbed_loader import TestbedLoader
#import testbed

#--------------------------------------------------------------------
# Build logging
#import logging
from common import logger
class logg(object):

    def __init__(self):
        self.log = logger.log

    def log(self,msg):
        print(msg)
        
logg.info("Posting a static policy to the controller.")
