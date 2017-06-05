from networkSdk.TopologyObject import TopologyObject
from networkSdk.interface import Interface
from networkSdk.datastructure.devicedict import DeviceDict
from networkSdk.datastructure.attrdict import AttrDict
from networkSdk.connections.connectionManager import ConnectionManager
class Device(TopologyObject):

    def __init__(self, name,
                 alias = None,
                 deviceType = None,
                 connections = None,
                 testbed = None,
                 interfaces = None,
                 **kwarg):
#        print("\n\nDevice : kwarg = ",kwarg)
        super(Device, self).__init__(name, alias)
        self.name = name
        self.alias = alias or name
        self.deviceType = deviceType
        self.connections = AttrDict()
        self.testbed = testbed
        self.interfaces = DeviceDict()
        self.credentials = AttrDict()
        
        if interfaces:
            for interface in interfaces:
                self.add_intf(interface)

        if connections:
            self.connections.update(connections)
        else:
            # Could be Virtual testbed which does not have static console ports
            self.connections = {}

        #add other key value to device
        for key,value in kwarg.items():
            print("Device : key = ",key,", value = ",value)
            setattr(self, key, value)

        #self.connection_mgr = ConnectionManager(device = self, credentials = self.credentials)
        self.connection_mgr = ConnectionManager(device = self)

        print("\n\nDevice all value :",self.connection_mgr.__dict__)
       

    def __iter__(self):
        return self.interfaces.itervalues()

    def __repr__(self, *args, **kwargs):
        return ('%r(name=%r, alias = %r, deviceType = %r)' % (self.__class__, self.name, self.alias, self.deviceType))

    def __contains__(self, interface):
        if isinstance(interface, Interface):
            # Interface Object is provided
            return interface in self.interfaces.values()
        elif isinstance(interface , str):
            # Interface name or alias name is provided
            return interface in self.interfaces or interface in [self.interfaces[key].alias for key in self.interfaces]
        else:
            return None

    def __getattr__(self, attr):
        if hasattr(self.connection_mgr, attr):
            return getattr(self.connection_mgr, attr)
        else:
            print("Attribute not present")

    def __dir__(self):
        return dir(Device) + dir(self.connection_mgr)

    @property
    def links(self):
        return [interface.link for interface in self]

    def add_intf(self, interface):
        self.interfaces[interface.name] = interface
        interface.device = self

