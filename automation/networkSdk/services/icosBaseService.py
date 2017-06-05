from .abstractService import AbstractService
from networkSdk.datastructure import AttrDict
import re
from .exceptions import *

class ICOSBaseService(AbstractService):

    PRIVILEGED_EXEC_MODE_PROMPT = '[^>#\n]+#'
    
    def __init__(self, connection, **kwargs):
        self.connection = connection
        self.error_patterns = ['Invalid input detected']
        # add the keyword arguments to the object
        self.__dict__.update(kwargs)

    def pre_service(self, *args, **kwargs):
        # IF connection is not yet established create a Connection
#        print('\npre_service')
        if self.connection.connected:
            return
        else:
            self.connection.connect()

    def post_service(self, *args, **kwargs):
#        print('\npost_service')
        return

    def get_service_result(self):
#        print('\nget_service_result')
        service_result = AttrDict()
        if isinstance(self.result, str):
            self.__check_for_error()
            service_result['success'] = not self.error
            service_result['data'] = self.result
            return service_result
        elif isinstance(self.result, AttrDict):
            return self.result
        else:
            raise InvalidServiceResult("Service Result not understood or unsupported")

    def __check_for_error(self):
#        print('\n__check_for_error')
        self.error = False
        for error_pattern in self.error_patterns:
            if re.search(error_pattern, self.result):
                self.error = True
        return

    def add_error_patterns(self, error_patterns):
        print(add_error_patterns)
        self.error_patterns.extend(error_patterns)

    def __call__(self, *args, **kwargs):
        try:
            return super(ICOSBaseService, self).__call__(*args, **kwargs)
        except Exception as e:
            print(e)
            #self.connection.log(e)
            raise
