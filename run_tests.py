import time
import helpers.config_parser as parser
from helpers import logger_settings
from helpers.file_utils import delete_files_from_folder

from tests.AUTHENTICATION.login_test import LoginTest
from tests.AUTHENTICATION.logout_test import LogoutTest
from tests.FILE.create_dir import FileCreateTest
from tests.FILE.upload import FileUploadTest
from tests.FILE.share import FileShareTest
from tests.FILE.unshare import FileUnshareTest
from tests.FILE.sha import FileShaTest
from tests.FILE.delete import FileDeleteTest
from tests.FILE.put import FilePutTest
from tests.VERSION.version import GetVersionTest
from tests.STATUS.status import GetStatusTest
from tests.JOB.job_submit import CommandJobTest
from tests.FILE.custom_ssh_get_file import CustomGetSshFIle

from helpers.Error import UATError
from helpers.colors import bcolors

import inspect

if __name__ == '__main__':
    start_time = time.time()
    logger_settings.logger.info('Starting HPC-API suite')

    if parser.config_params('clean')['docleanlogs'] in 'True':
        logger_settings.logger.info(bcolors.WARNING + 'Deleting the logs and html artifacts' + bcolors.ENDC)
        delete_files_from_folder('html')
        delete_files_from_folder('logs')
    else:
        pass

    try:

        # ADMIN --------------------------------------------------------------------
        POST_login = LoginTest(parser)
        POST_logout = LogoutTest(parser, POST_login.getTicket())

        # FILE ---------------------------------------------------------------------
        POST_sha = FileShaTest(parser)
        POST_file_create = FileCreateTest(parser)
        GET_file = FileUploadTest(parser)
        GET_share = FileShareTest(parser)
        GET_unshare = FileUnshareTest(parser)
        GET_delete = FileDeleteTest(parser)
        PUT_file = FilePutTest(parser)
        GET_version = GetVersionTest(parser)
        GET_status = GetStatusTest(parser)

        # JOB ARRAY SUBMIMISSION -----------------------------------------------
        POST_job_R = CommandJobTest(parser, 'array')
        # JOB SUBMIMISSION workflows via command plugins -----------------------
        POST_job_R = CommandJobTest(parser, 'R')
        POST_job_nonmem = CommandJobTest(parser, 'nonmem')
        # CUSTOM MKDIR TEST
        GET_ssh_file = CustomGetSshFIle(parser)

    except UATError as e:
        logger_settings.logger.info('This error should not be catch here: {0}'.format(e.emsg()))
    except Exception as e:
        logger_settings.logger.info(
            'Problems with HPC-API suite .............................{0}'.format(inspect.trace()))

    logger_settings.logger.debug('It took {0} seconds to execute the suite'.format(round(time.time() - start_time)))
