import sys, os , time , re
import logging
import pytest
import globals as gbl

#--------------------------------------------------------------------
# Build logging

#logging.basicConfig(level=logging.INFO)
o_dir = os.path.join(os.path.dirname(__file__),"log")
print("\no_dir =",o_dir)
if not os.path.exists(o_dir):
    os.makedirs(o_dir)
o_log_name = __name__ + "-" + time.strftime("%Y%m%d-%H%M%S") + ".log"
print("o_log_name =",o_log_name)
o_log_name = "ICOS.log"
o_file = os.path.join(os.path.abspath(o_dir), o_log_name)
print("Log file name : ",o_file)
#'''
logging.basicConfig(filename=o_file, filemode="w", level=logging.INFO)
logg = logging.getLogger(__name__)
logg.info("Log file name : " + o_file)

def log(msg):
    logg.info(msg)
    print(msg)

@pytest.mark.usefixtures("common_setup")        
class Test_ICOS(object):
           
    def setup(self):
        log("\n*** Test_ICOS : setup section ***")    
#        testbed = TestbedLoader()
#        testbed = testbed.load("./config/sample.yaml")
#        print("\n--------------------------------------------------------------------")
#        print("\nAll value testbed = \n", testbed.__dict__)
#        print("\n--------------------------------------------------------------------")
#        print("testbed.devices = ",testbed , "\ndir = ", dir(testbed) )
#        assert testbed is not None, "Testbed object returned from TestbedLoader is none"
#            
#        print("\ncls = ",dir(cls),"\ndict = ",cls.__dict__)
#        for d in testbed.devices:
#            print("\n\nConnect Device : ", d , "\n" , dir(d))

    def test_1(self):
        ''' Check Mac address '''
        for rtr in gbl.testbed.devices :
            mgr = gbl.testbed.devices[rtr].connection_mgr
            log("\nICOS_Test::test1")
            output = mgr.execute("show version")
            print("\n output = \n",output.data)
            # Seacrch mac address 00:A0:C9:XX:XX:XX
            ret = re.search(r'(00[:-]A0[:-]C9)', output.data, re.I)
            assert ret == None, "MAC address is not configured"

    def test_2(self):
        assert 1 # for demo purposes

    def teardown(self):
        log("\n*** Test_ICOS : teardown section ***")
        for rtr in gbl.testbed.devices :
            mgr = gbl.testbed.devices[rtr].connection_mgr

