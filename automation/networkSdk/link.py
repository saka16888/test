from networkSdk.TopologyObject import TopologyObject
from networkSdk.datastructure import Weakreflist
class Link(TopologyObject):

    def __init__(self,
                 name,
                 alias = None,
                 interfaces = None,
                 **kwargs):
        super(Link, self).__init__(name,alias)
        self.name = name
        self.alias = alias or name
        self.interfaces = Weakreflist()
        if interfaces:
            for interface in interfaces:
                self.connect_interface(interface)

        # Other Key value pairs
        for key, value in kwargs:
            setattr(self, key, value)

    def __iter__(self):
        return iter(self.interfaces)

    def __repr__(self):
        return ('%r(name=%r, alias=%r)' % (self.__class__, self.name, self.alias))

    def __contains__(self, interface):
        return interface in self.interfaces

    def connect_interface(self, interface):
        if interface in self.interfaces:
            raise LinkErrorException("Interface already part of link : " + interface)
        self.interfaces.append(interface)
        interface.link = self

    @property
    def connected_device(self):
        return set([interface.device for interface in self])


class LinkErrorException(Exception):
    pass
