# New : Python 2to3
from six import add_metaclass
from abc import abstractmethod, abstractproperty
from networkSdk.datastructure import AttrDict
from networkSdk.datastructure  import DeviceDict

class TopologyObject(object):
    '''TopologyObject Base class

    '''
    def __init__(self, name, alias = None):
        '''built in class __init__

        Instanciates the base topology object.

        Arguments
        ---------
            name (str): name of the topology object
            alias (str): alias of the topology object, default to name

        Example
        -------
            >>> object1 = TopologyObject(name = 'object1')
            >>> object2 = TopologyObject(name = 'object2', alias = 'alias_object2')

        '''
        print("\n\nTopologyObject ","name = ", name ,"alias = ", alias,"\n dir(self) = ",dir(self))
        self.name = name
        self.alias = alias or name
        
        

class TestbedClassFactory(type):
    def __call__(self, *args, **kwargs):
        print("TestbedClassFactory args = ",args,"kwargs = ", kwargs)
        return super(TestbedClassFactory, PhysicalTestbed).__call__(*args, **kwargs)
#        if 'virl_host' in kwargs:
#            #print (issubclass(VirtualTestbed, type))
#            return super(TestbedClassFactory, VirtualTestbed).__call__(*args, **kwargs)
#        else:
#            return super(TestbedClassFactory, PhysicalTestbed).__call__(*args, **kwargs)

@add_metaclass(TestbedClassFactory)
class Testbed(TopologyObject):

    #__metaclass__ = TestbedClassFactory

    @abstractmethod
    def add_device(self, device):
            raise NotImplementedError

    @abstractproperty
    def links(self):
        raise NotImplementedError


class VirtualTestbed(Testbed):

    def __init__(self, name, alias = None, credentials = None, **kwargs):
        pass

    def __contains__(self, device):
        pass

    def __iter__(self):
        pass

    def __getitem__(self, attr):
        pass


    def add_device(self, device):
        pass

    @property
    def links(self):
        pass


class PhysicalTestbed(Testbed):

    def __init__(self, name, alias = None, **kwargs):
        print ("\n\nPhysicalTestbed Type of Testbed : PHYSICAL")
        super(PhysicalTestbed, self).__init__(name,alias)
        print ("name = ",name,
               "\nalias = ",alias,
               "\nkwargs = ",kwargs)
                 
        self.devices= DeviceDict()
        print("self.devices = ", self.devices)
        
        #add kwargs to self
        for name,value in kwargs.items():
            print("name = ",name, "value = ",value)
            setattr(self, name, value)

    def __contains__(self, device):
        # Could be device object itself
        if isinstance(device, device):
            return device in self.devices.values()
        # Could be device name or alias
        if isinstance(device, str):
            return device in self.devices or device in [self.devices[key].alias for key in self.devices]
        return None

    def __iter__(self):
        print("\n\n self.devices = ", self.devices.__dict__)
        return self.devices.itervalues()

    def __getitem__(self, attr):
        if attr in self.devices:
            return self.devices[attr]
        else:
            return next((device for device in self if device.alias == attr), None)
        # TDOD Return an exception
        print ("Not able to get device")
        return None

    def add_device(self, device):
        print("\n\nPhysicalTestbed add_device = ", device)
        device.testbed = self
#        device.connections.ip = self.virl_host
#        device.connections.port = self.physical_ports[device.name]      
        self.devices[device.name] = device

    @property
    def links(self):
        links = []
        for device in self.devices.values():
            links.extend(device.links)
        return links
