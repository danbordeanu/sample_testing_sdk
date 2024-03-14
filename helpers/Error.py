from enum import Enum
import sys
import os


class ExceptionType(Enum):
    ARGUMENTS = 'arguments'
    CONNECTION = 'connection'
    IO_SSH = 'io operations over SSH'
    IO_LOCAL = 'io local operations'
    AUTHENTICATION = 'authentication'
    RETURN_VALUES = 'The returned value is wrong'
    HPCAPI = 'something was wrong, perhaps the provided args to the endpoint'
    HPCAPI_RET_FALSE = 'Json return value from hpcapi is = False'
    HPCAPI_FORDBIDDEN = 'User has no acces to resource'
    HPCAPI_TIMEOUT= 'http time out'
    HPCAPI_TOOMANYREDIRECTS= 'http Redirect problem'
    HPCAPI_OTHER= 'Request problem'


class Error(Exception):
    pass


class UATError(Error):
    def __init__(self, exceptionType, msg=None):
        self.exceptionType = exceptionType
        self.msg = msg
        self.sms = []

    def emsg(self, arg = None):
        if self.msg:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.sms.append(str(fname))
            self.sms.append(str(', '))
            self.sms.append(str(exc_tb.tb_lineno))
            ret = 'UAT ERROR: {0} > {1} > {2}'.format(self.exceptionType.value, self.msg, self.sms)
        else:
            ret = 'UAT ERROR: {0} >  {1}'.format(self.exceptionType.value, self.sms)

        if arg is 'asString':
            return ret
        else:
            print ret


