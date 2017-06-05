import sys, os

sys.path.insert(0, os.path.dirname(__file__))
print("path added :",os.path.dirname(__file__))

import pytest
import requests
import json
from common.logger import Logger

Logger.setup(sys.path,"output.log",INFO)

class ICOS_TEST:

    def __init__(self):
        self.log = Logger.log
        self.output_file_name = time.strftime("%Y%m%d-%H%M%S") + ".log"
        self.__test_case_o_file = os.path.join(self.test_case_o_dir, output_file_name)
        self.__create_dir(self.test_case_o_dir)
        
    @pytest.fixture(autouse=True)
    def icos_t1(self):
        """ ICOS test 1  """
        self.log("ICOS test 1")
        print("ICOS test 1")
        pass

    def icos_t2(self):
       """ ICOS test 2  """
       #self.log("ICOS test 2")
       print("ICOS test 2")
       pass

print("file = ",__name__)
if __name__ == 'icos':
    a1=ICOS_TEST()
    a1.icos_t1()
    a1.icos_t2()
    
    