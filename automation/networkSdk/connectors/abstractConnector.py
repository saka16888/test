from abc import ABCMeta, abstractmethod, abstractproperty
#from _pyio import __metaclass__
from six import add_metaclass

@add_metaclass(ABCMeta)
class AbstractConnector(object):
    
    #__metaclass__ = ABCMeta
    
    __entities__ = {}
    '''Abstract Connection class

    Abstract base class for all connection class/objects. This defines the bare
    minimum interface offered for any device connection, be it a router, switch,
    wireless lan controller , AP , traffic generator or server.

    All connection types/objects/classes under the infrastructure
    must be inherit this class.

    Standard Services:
        connect()
            connects to device

        disconnect()
            disconnects from device

        connected
            property, True/False for whether the device is connected

        execute()
            executes a command on the device through this connection

    Other Requirements:
        1. __init__ needs to at least device object as input

    '''
    @classmethod
    def factory(cls, entity):
        try:
            return cls.__entities__[entity]
        except KeyError as e:
            # TODO release a proper exception
            print (e)
            print ("Subclass not understood")

    @classmethod
    def register(cls, entity):
        def decorator(subclass):
            cls.__entities__[entity] = subclass
            subclass._entity_ = entity
            return subclass
        return decorator

    @abstractproperty
    def connected(self):
        '''abstract method returning True/False if connection is up'''
        raise NotImplementedError

    @abstractmethod
    def __dir__(self):
        '''abstract method for connecting to device'''
        raise NotImplementedError

    @abstractmethod
    def connect(self):
        '''abstract method for connecting to device'''
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        '''abstract method for disconnecting from to device'''
        raise NotImplementedError
