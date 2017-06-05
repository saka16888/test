
from networkSdk.services import ICOSBaseService
import re

class WarmUpService(ICOSBaseService):

    __SERVICE_NAME__ = 'get_os_type'

    def call_service(self, *args, **kwargs):
        send_command = "show version"
        print("======================================================")
        print ("|    Executing command show version to get ICOS OS Type    |")
        print("======================================================")
        self.result = self.connection.execute(send_command)
        if self.result.success:
            raw_data = self.result.data
            for location, os_type in re.findall(r"System image file is (.*):(.*)", raw_data):
                self.result = os_type
