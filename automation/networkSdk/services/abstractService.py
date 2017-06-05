from abc import ABCMeta, abstractmethod, abstractproperty
from six import add_metaclass

@add_metaclass(ABCMeta)
class AbstractService(object):
    #__metaclass__ = ABCMeta
    
    """ Abstract base class for defining the basic
    interface for service class.
    """

    @abstractproperty
    def __SERVICE_NAME__(self):
        raise NotImplementedError

    @abstractmethod
    def pre_service(self, *args, **kwargs):
        """ execute things before main service """
        raise NotImplementedError

    @abstractmethod
    def call_service(self, *args, **kwargs):
        """ execute main logic of the service """
        raise NotImplementedError

    @abstractmethod
    def post_service(self, *args, **kwargs):
        """ execute post service """
        raise NotImplementedError

    @abstractmethod
    def get_service_result(self):
        """ returns the service result to caller """
        raise NotImplementedError

    @classmethod
    def platform_check(cls, *args, **kwargs):
        ''' logic to verify whether this service
        is applicable for the given platform.
        '''
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        """ calls all the methods of the service """

        self.pre_service(*args, **kwargs)

        self.call_service(*args, **kwargs)

        self.post_service(*args, **kwargs)

        return self.get_service_result()
