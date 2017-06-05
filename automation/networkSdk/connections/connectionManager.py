import weakref
import importlib
import os

from networkSdk.datastructure.attrdict import AttrDict
from networkSdk.connectors import *

class ConnectionManager(object):
    '''Connection Manager class

    This class is used to contain all connection_manager to a particular device. It is
    to be used as part of any device class's connection_manager attribute.

    '''

    @property
    def device(self):
        return self.__device__()

    @device.setter
    def device(self, obj):
        self.__device__ = weakref.ref(obj)

    def __init__(self,device):
        self.device = device
        self.default_alias = device.alias
        self.connections = AttrDict()
        
        print("\n ConnectionManager self = ",self.__dict__)
        try:
            self.connect()
        except Exception as e:
            print (type(e))
            raise ConnectionManagerEstablishConnectionException(e)

    def __getattr__(self, attr):
        if attr in self.connections:
            return self.connections[attr]
        elif self.default_alias in self.connections and \
             hasattr(self.connections[self.default_alias], attr):
            return getattr(self.connections[self.default_alias], attr)
        else:
            raise AttributeError("'ConnectionManager' object has no attribute "
                                 "'%s'" % attr)

    def __dir__(self):
        '''built-in __dir__

        API to overload default dir() behavior on this api, and enable chaining
        to self.connection_manager so that all connection_manager in this manager is also
        seen as an attribute to this object.

        Used in conjunction with __getattr__.

        Arguments
        ---------
            None

        Returns
        -------
            List of attributes for this connectionmgr and its connection_manager.
        '''

        # base items = this object's stuff
        #items = super(ConnectionManager, self).__dir__()

        # include it's connection_manager if any
        items = []
        #items.extend(dir(ConnectionManager))
        items.extend(self.connections.keys())

        # include default connection if it's created
        if self.default_alias in self.connections:
            items.extend(dir(self.connections[self.default_alias]))

        return items

    def connect(self,
                cls = None,
                alias = None,
                via = None,
                *args,
                **kwargs):

        # use default alias
        if not alias:
            alias = self.default_alias
        # check if there is an existing connection object
        # if there is, just call connect()
        if alias in self.connections:
            return self.connections[alias].connect()
        # create the connection
        platform_type = self.device.deviceType

        print("\nConnectionManager Connect self = ",self.__dict__)
        self.connections[alias] = AbstractConnector.factory(platform_type)(device = self.device)
        
        self.connections[alias].connect()
        if not self.connections[alias].connected:
            raise Exception('Could not connect to device')

    def disconnect(self, alias = None):
        '''Disconnects device connection

        This API disconnects the device connection and removes the connection
        object from the device instance.

        Argument:
            alias (str): connection alias to operate on.
                         Defaults: 'default'

        Examples:
            >>> device.disconnect()
        '''

        # use default alias
        if not alias:
            alias = self.default_alias

        if alias in self.connections:
            # call disconnect
            self.connections[alias].disconnect()

    def is_connected(self, alias = None):
        '''Checks for connection to device

        This is an API that returns whether there is an active connection to
        the given device.

        Argument:
            alias (str): connection alias to operate on.
                         Defaults: 'default'

        Examples:
            >>> device.is_connected()
        '''

        # use default alias
        if not alias:
            alias = self.default_alias

        if alias in self.connections:
            return self.connections[alias].connected
        else:
            return False

    def destroy_connection(self, alias = None):
        '''Destroy a connection to device

        This is the API to destroy a connection object to the target device.
        It will first disconnect the connection, the remove it from the
        device connection manager.

        Arguments:
            alias (str): connection alias to operate on.
                         Defaults: 'default'

        Examples:
            >>> device.destroy_connection(alias = 'vty1')

        '''
        # use default alias
        if not alias:
            alias = self.default_alias

        if alias in self.connections:
            self.connections[alias].disconnect()
            del self.connections[alias]

    def disconnect_all(self):
        '''Disconnects all connection_manager

        This API disconnects all live connection_manager managed by this connection
        manager. Note that when a connection is disconnected, it is only a
        state change: the object persists and is not deleted

        Arguments:
            None

        Returns:
            None
        '''
        for connection in self.connections.values():
            connection.disconnect()

    def destroy_all(self):
        '''Destroys all connection_manager

        This API attempts to disconnect a live connection and unset it from
        the connection manager (attempt to delete the object)

        Arguments:
            None

        Returns:
            None
        '''

        while self.connections:
            alias, connection = self.connections.popitem()
            connection.disconnect()

class ConnectionManagerEstablishConnectionException(Exception):
    pass
