from .. import config_parser as parser
from .. import logger_settings
from helpers.Error import ExceptionType
from helpers.Error import UATError

import paramiko
import base64
import sys
sys.path.append("..")


def nodeipexecute(hostname, command, custom_user=None, custom_password=None, custom_port=None):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if custom_port is not None:
            port = int(custom_port)
        else:
            port = int(parser.config_params('sshserver')['port'])
        if custom_user is not None:
            username = custom_user
            password = custom_password
        else:
            username = parser.config_params('sshserver')['user']
            password = base64.b64decode(parser.config_params('sshserver')['password'])
        ssh.connect(hostname,
                    port=port,
                    username=username,
                    password=password)

        # Executing command in the host 
        my_node_exec = 'Command to be executed {0} on server {1}'.format(command, hostname)
        logger_settings.logger.debug(my_node_exec)
        stdin, stdout, stderr = ssh.exec_command(command)
        stderr_print = stderr.read().rstrip()
        stdout_print = stdout.read().rstrip()
        ret = {'stderr': stderr_print, 'stdout': stdout_print}

        # Examining return value from previous execution and raise an exception if neccesary
        msg = "[ " + command + " ]" + " -> Successful"
        if len(stderr_print) == 0 and len(stdout_print) == 0:
            logger_settings.logger.info(msg)
            return ''
        elif len(stderr_print) == 0 and len(stdout_print) != 0:
            logger_settings.logger.info(msg)
            msg2 = "stdout = " + stdout_print
            logger_settings.logger.info(msg2)
            return stdout_print
        else:
            logger_settings.logger.info('stderr= {0} '.format(ret.get('stderr')))
            logger_settings.logger.info('stdout= {0} '.format(ret.get('stdout')))
            msg = str(ret.get('stderr')) + " at function nodeipexecute"
            raise (UATError(ExceptionType.IO_SSH, msg))

    except paramiko.AgentKey as e:
        raise (UATError(ExceptionType.IO_SSH, ' at nodeipexecute ssh agent key [ {0} ]'.format(e)))
    except paramiko.AuthenticationException as e:
        raise (UATError(ExceptionType.IO_SSH, ' at nodeipexecute ssh authentication failed because some reason [ {0} ]'.format(e)))
    except paramiko.BadHostKeyException as e:
        raise (UATError(ExceptionType.IO_SSH, ' at nodeipexecute ssh server\'s host could not be verified [ {0} ]'.format(e)))
    except paramiko.SSHException as e:
        raise (UATError(ExceptionType.IO_SSH, ' at nodeipexecute ssh password is invalid [ {0} ]'.format(e)))
    except:
        raise (UATError(ExceptionType.IO_SSH, "Can\'t connect/authenticate to the host"))
    finally:
        # Close this SSHClient and its underlying Transport.
        ssh.close()

