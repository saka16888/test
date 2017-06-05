

class ServiceInstallationFailed(Exception):
    def __init__(self, message):
        super(ServiceInstallationFailed, self).__init__(message)

class ServiceCreationFailed(Exception):
    def __init__(self, message):
        super(ServiceCreationFailed, self).__init__(message)

class DeviceConnectionException(Exception):
    def __init__(self, message):
        super(DeviceConnectionException, self).__init__(message)

