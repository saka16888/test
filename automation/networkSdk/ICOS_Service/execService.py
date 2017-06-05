from networkSdk.services import ICOSBaseService
from networkSdk.services import InvalidExecuteCommand

class ExecService(ICOSBaseService):
    """
    Name : ICOSExecService()

    Description: This service shall allow user to executes exec_command on the
                 router current state (disable or enable) and returns the
                 router console output.

            Arguments: <Command to execute on device>
            Return Values:

    Examples/Usage:
            result = rtr1.execute("show clock")

    """
    __SERVICE_NAME__ = 'execute'
    
#    PRIVILEGED_EXEC_MODE_PROMPT = '[^>#\n]+#'

    def call_service(self, *args, **kwargs):
        if len(args) <= 0:
            raise InvalidExecuteCommand("Command to execute is null")
        command_to_send = args[0]
        #expect_regex_list = self.connection.PRIVILEGED_EXEC_MODE_PROMPT
        expect_regex_list = '[^>#\n]+#'
        self.connection.handle.sendline(command_to_send)
        self.connection.handle.expect(command_to_send)
        self.connection.handle.expect(expect_regex_list, timeout = 60)
        self.result = self.connection.handle.before

class ConfigService(ICOSBaseService):
    """
    Name : ICOSExecService()

    Description: This service shall allow user to executes exec_command on the
                 router current state (disable or enable) and returns the
                 router console output.

            Arguments: <Command to execute on device>
            Return Values:

    Examples/Usage:
            result = rtr1.config("int 0/3
                                  shutdown")

    """
    __SERVICE_NAME__ = 'config'
    
#    PRIVILEGED_EXEC_MODE_PROMPT = '[^>#\n]+#'

    def call_service(self, *args, **kwargs):
        if len(args) <= 0:
            raise InvalidExecuteCommand("Command to execute is null")
        command_to_send = args[0]
        #expect_regex_list = self.connection.PRIVILEGED_EXEC_MODE_PROMPT
        expect_regex_list = '[^>#\n]+#'
        self.connection.handle.sendline('config')
        self.connection.handle.sendline(command_to_send)
        self.connection.handle.expect(command_to_send)
        self.connection.handle.expect(expect_regex_list, timeout = 60)
        self.result = self.connection.handle.before