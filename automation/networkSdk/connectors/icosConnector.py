
#import device.Device
import pexpect
import inspect
import pytest
import sys
import time
from .abstractConnector import AbstractConnector
from networkSdk.services import ICOSBaseService
from networkSdk.datastructure import AttrDict
from inspect import isclass
from .exceptions import  *

@AbstractConnector.register('ICOS')
class ICOSConnector(AbstractConnector):

    TERM_LENGTH_CMD = 'terminal length 0'
    SHOW_VERSION = 'show version'
    USER_NAME_PROMPT = 'Username:'
    LOGIN_PROMPT = 'login:'
    USER_PROMPT = 'user:'
    PASSWORD_PROMPT = 'Password:'
    NEW_LINE_CHARACTER = '\r\n'
    SHOW_RUN_CMD = 'show run'
    CLI_ERROR_MESSAGES = 'incorrect password attempts'
    ICOS_LOGIN = 'sudo icos-cli'
    TIMEOUT=10
        
    def __init__(self, device):
        self.__name = device.name
        if not self.__is_valid_device(device):
            # TODO return an exception here
            print ("Not a valid or supported device object")

        print("\n ICOSConnector __init__",device.__dict__)
        self._credentials = device.credentials
        self._username = self._credentials["username"]
        self._password = self._credentials["password"]
        self._enable_password = self._credentials["enable_password"]
        self._termserver_ip = device.connections.ip
        self._termserver_port = device.connections.port
        self.__is_connected = None
        self.USER_EXEC_MODE_PROMPT = self.__name+':~'
        self.ICOS_PASSWORD_PROMPT = 'password *'
        self.ICOS_EXEC_MODE_PROMPT = '\(' + self.__name + '\)' + ' #'
        self.ICOS_CONFIG_MODE_PROMPT = r'\([^()]*\)'
        self.ICOS_INIT_CONSOLE_PROMPT = 'Initializing console session'
        self.ICOS_EXIT_PROMPT = r'(' + self.__name + r') ' + '>'

        # Should be declared true when all the services are inited
        self.__service_init  = False
        self.__handle = None
        self.base_service = ICOSBaseService        

        print("\nICOSConnector __init__",self.__dict__)
        print("\nUSER_EXEC_MODE_PROMPT = ",self.USER_EXEC_MODE_PROMPT)
        print("PASSWORD_PROMPT = ",self.PASSWORD_PROMPT)
        print("ICOS_EXEC_MODE_PROMPT = ",self.ICOS_EXEC_MODE_PROMPT)
        print("ICOS_CONFIG_MODE_PROMPT = ",self.ICOS_CONFIG_MODE_PROMPT)
        print("ICOS_PASSWORD_PROMPT = ",self.ICOS_PASSWORD_PROMPT)
        print("ICOS_INIT_CONSOLE_PROMPT = ",self.ICOS_INIT_CONSOLE_PROMPT)
        print("ICOS_EXIT_PROMPT = ",self.ICOS_EXIT_PROMPT)

    def __dir__(self):
        return self.__dict__.keys()

    def __is_valid_device(self, device):
        #return isinstance(device, device)
        return True

    @property
    def connected(self):
        return self.__is_connected

    def connect(self):

        print("\n ICOSConnector connect",self.__dict__)
        child = pexpect.spawn('telnet %s %s' % (self._termserver_ip, self._termserver_port), 
                                encoding='utf8',
                                timeout = self.TIMEOUT)
        child.logfile_read = sys.stdout
        child.logfile_send = sys.stdout

        # To pass over the banner that comes before login prompt
        child.send(self.NEW_LINE_CHARACTER)
        child.send(self.NEW_LINE_CHARACTER)

        for j in range(20):
            i = child.expect([self.LOGIN_PROMPT,
                              self.PASSWORD_PROMPT,
                              self.USER_EXEC_MODE_PROMPT,
                              self.ICOS_PASSWORD_PROMPT,
                              self.ICOS_EXEC_MODE_PROMPT,
                              self.ICOS_INIT_CONSOLE_PROMPT,
                              self.ICOS_CONFIG_MODE_PROMPT,
                              self.ICOS_EXIT_PROMPT,
                              self.CLI_ERROR_MESSAGES])
#            print("i =",i)
            if i in [0]: 
                child.sendline(self._username)
            elif i in [1]:
                child.sendline(self._password)
                #child.send(self.NEW_LINE_CHARACTER)
            elif i in [2]:
                child.sendline(self.ICOS_LOGIN)
                #time.sleep(1)
            elif i in [3]:
                child.sendline(self._enable_password)
                #time.sleep(1)
            elif i in [4]:
                child.send(self.NEW_LINE_CHARACTER)
                break
            elif i in [5]:
                child.send(self.NEW_LINE_CHARACTER)
                child.send(self.NEW_LINE_CHARACTER)
                child.send(self.NEW_LINE_CHARACTER)
                break
            elif i in [6]:           
                child.sendline("end")
                child.send(self.NEW_LINE_CHARACTER)
                break
            elif i in [7]:           
                child.sendline("quit")
                child.sendline(self.ICOS_LOGIN)
                #break            
            else:
                print("\nNo matching")
                break

        self._prompt = self.ICOS_EXEC_MODE_PROMPT

        # Now we are in ICOS prompt       
        child.sendline(self.TERM_LENGTH_CMD)
        child.expect(self.TERM_LENGTH_CMD)
#        child.send(self.NEW_LINE_CHARACTER)
        child.expect(self._prompt)

        # Now we are in enabled prompt
        child.sendline(self.SHOW_VERSION)
#        child.send(self.NEW_LINE_CHARACTER)
        child.expect(self.SHOW_VERSION)
        child.expect(self._prompt)

        child.send(self.NEW_LINE_CHARACTER)
        child.expect(self._prompt)
        self.__is_connected = True
        self.handle = child
        self.__init_services()

    def __init_services(self):
        # Discover all services
        for cls in self.__find_services():
            # Instantiate them
            try:
                obj = cls(connection = self)
            except Exception as e:
                raise ServiceCreationFailed(e)
            self.add_services(obj)

    def __find_services(self):
        all_services = []
        import networkSdk.ICOS_Service as ICOS_Service
        for name, cls in inspect.getmembers(ICOS_Service):
            if isclass(cls) \
               and issubclass(cls, self.base_service) \
               and cls.__name__ is not 'ICOSBaseService':
               print("\n__find_services : ",name,cls)
               all_services.append(cls)
        return all_services

    def add_services(self, obj):        
        if hasattr(self, obj.__SERVICE_NAME__):
            raise ServiceInstallationFailed("Duplicate Service " + obj.__SERVICE_NAME__+ ", Installation Failed ")
        self.__dict__[str(obj.__SERVICE_NAME__)] = obj

    def get_services(self):
        service_list = []
        for item in self.__dict__.items():
            if isinstance(item, ICOSBaseService):
                service_list.append([item, item.__class__.__name__])
        print("service_list = ",service_list)
        return service_list

    def disconnect(self):
        if self.__is_connected:
            self.__is_connected = False
            print("disconnect !!!")
            self.handel.sendline('exit')
            self.handle.close()
        else:
            print ("Connection already closed")
