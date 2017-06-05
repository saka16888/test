import sys, os , time
import pytest
from networkSdk import TestbedLoader
import globals as gbl

print("ICOS path added :",os.path.dirname(__file__))
print("This is conftest.py")

#--------------------------------------------------------------------

def pytest_report_header(config):
    return "ICOS Sanity"

def pytest_addoption(parser):
    parser.addoption("--config", action="store", help="Full path to custom configuration yaml file.")

@pytest.fixture
def cmdopt(request):
    print("-- config = ",request.config.getoption("--config"))
    return request.config.getoption("--config")


#testbed = TestbedLoader()
#testbed = testbed.load("./config/sample.yaml")
#print("\n--------------------------------------------------------------------")
#print("\nAll value testbed = \n", testbed.__dict__)
#print("--------------------------------------------------------------------")
#print("testbed.devices = ",testbed, "\ndir = ", dir(testbed) )
    
#@pytest.fixture(autouse=True)

@pytest.fixture(scope="session")
def common_setup(request):
    
    print("\n---------------------------------------------------------")
    print("\n------             common_setup section            ------")
    print("\n---------------------------------------------------------")
    testbed = TestbedLoader()
    testbed = testbed.load("./config/sample.yaml")
#    testbed = testbed.load("/home/mihung/pytest/delta/icos/config/sample.yaml")
    
    print("\nAll value testbed = \n", testbed.__dict__)
    print("--------------------------------------------------------------------")
    print("testbed.devices = ",testbed, "\ndir = ", dir(testbed) )
    assert testbed is not None, "Testbed object returned from TestbedLoader is none"

#    r1=testbed.devices["rtr1"].connection_mgr
#    ret = r1.execute("show run")
#    print("\nret = \n",ret.data)
#    cmd=["int 0/1" , "shutdown", "ip address 1.1.1.1 255.255.255.0","no shutdown"]
#    r1.config(cmd)
#    
#    r2=testbed.devices["rtr2"].connection_mgr
#    ret = r2.execute("show run")
#    print("\nret = \n",ret.data)
#    cmd=["int 0/5" , "shutdown", "ip address 1.1.1.2 255.255.255.0","no shutdown"]
#    r2.config(cmd)
#    ret = r2.execute("ping 1.1.1.1")
#    print(ret)
#    print("\nret = \n",ret.data)                 
#        print("\n\nConnect Device : ", dir(testbed.devices["rtr2"].connection_mgr))
#        print(testbed.devices[d].connection_mgr.execute("show run"))
        #mgr= d.connection_mgr
        #d.execute()
        #d.execute("show clock")

    def common_teardown():
        print ("\n--- common_teardown ---")
        for d in testbed.devices:
            print("Closing connection for device : ",d)
#            print(testbed.devices[d].connection_mgr.destroy_all())
    request.addfinalizer(common_teardown)
    gbl.testbed = testbed
    #return None

    