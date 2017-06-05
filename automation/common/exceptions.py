from common import logger


class UniqException(Exception):
    """ Base exception class in uniq takes an error message to get initialized

    It makes a log entry of level exception using the error message used while calling
    UniqException. The log entry has a tag of [UniqException], for the purpose of
    easy filtering.

    UniqException can be directly raised as an exception as well.

    Usage:
        raise UniqException("error_message")
    """

    # Class variable to keep count of the number of times the UniqException is raised in
    # the life of a test case.
    __counter = 0

    __extra_action = None

    def __init__(self, error_message):
        """ Initializes the test exception instance. """

        super(UniqException, self).__init__()
        self.__class__.__counter += 1
        logger.log.exception("[{0}] {1}".format(self.__class__.__name__, error_message))
        self.error_message = error_message
        if self.__class__.__extra_action:
            self.__class__.__extra_action()

    def __str__(self):
        return self.error_message

    @classmethod
    def set_extra_action(cls, method):
        """ Set what actions to take when UniqException object being created.

        Args:
            method (function): method to call when object init.
        """

        cls.__extra_action = method


class TimeoutException(UniqException):
    """ Exception for Timeout"""

    pass


class PlatformException(UniqException):
    """ Platform exception class takes an error message to get initialized

    It makes a log entry of level exception using the error message used while calling
    PlatformException. The log entry has a tag of [PlatformException], for the purpose of
    easy filtering.

    PlatformException can be directly raised as an exception as well.

    Usage:
        raise PlatformException("error_message")
    """

    pass


class ToolsException(UniqException):
    """ Tools exception class takes an error message to get initialized

    It makes a log entry of level exception using the error message used while calling
    ToolsException. The log entry has a tag of [ToolsException], for the purpose of
    easy filtering.

    ToolsException can be directly raised as an exception as well.

    Usage:
        raise ToolsException("error_message")
    """

    pass


class WtfException(UniqException):
    """ Wtf exception class takes an error message to get initialized

    It makes a log entry of level exception using the error message used while calling
    WtfException. The log entry has a tag of [WtfException], for the purpose of
    easy filtering.

    Wtfexception can be directly raised as an exception as well.

    Usage:
        raise WtfException("Element is not displayed in DOM")
    """

    pass
