from networkSdk.TopologyObject import TopologyObject

from ipaddress import IPv4Interface, IPv6Interface
import weakref

class Interface(TopologyObject):

    # defaults
    __device__ = None
    __link__ = None

    def __init__(self,
                 name,
                 alias = None,
                 link = None,
                 device = None,
                 ipv4 = None,
                 ipv6 = None,
                 type = None,
                 **kwargs):
        super(Interface, self).__init__(name, alias)

        # initialize self
        self.type = type

        if link:
            link.connect_interface(self)

        if device:
            device.add_interface(self)

        if ipv4:
            self.ipv4 = IPv4Interface(ipv4)
        else:
            self.ipv4 = None

        if ipv6:
            self.ipv6 = IPv6Interface(ipv6)
        else:
            self.ipv6 = None

        # add other Key value pair
        for name, value in kwargs:
            setattr(self, name, value)

    def __repr__(self):
        return ('%r(name=%r, alias=%r, type=%r,\
        ipv4=%r, ipv6= %r' % (self.__class__,
                              self.name,
                              self.alias,
                              self.type,
                              self.ipv4,
                              self.ipv6))
    @property
    def link(self):
        return self.__link__

    @link.setter
    def link(self,link):
        self.__link__ = link
        if self not in link:
            link.connect_interface(self)

    @property
    def remote_interfaces(self):
        if not self.link:
            return set()
#         if self not in self.link.interfaces:
#             raise Exception e
        return set([i for i in self.link.interfaces if self != i])

    @property
    def remote_devices(self):
        return set([intf.device for intf in self.remote_interfaces])

    @property
    def device(self):
        '''
            Returns the actual device object and we just store the weak ref here
        '''
        if self.__device__:
            return self.__device__()

    @device.setter
    def device(self,device):
        if device is None:
            # untagg interface from device
            if self.__device__ and self in self.__device__():
                self.__device__().remove_interface(self)
            self.__device__ = None
        else:
            # Storing only the weak reference
            self.__device__ = weakref.ref(device)



