# $language = "python"
# $interface = "1.0"
import logging
from datetime import datetime
__status__ = 'dev'
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


def get_log_file_name():
    """
    Function to get current date and time for log file naming
    :return:
        String of date and time

    """
    LOGGER.debug('Starting get_log_file_name')
    return '{date}_{hour}{min}{sec}'.format(date=datetime.now().date().strftime("%m-%d"),
                                            hour=datetime.now().time().hour, min=datetime.now().time().minute,
                                            sec=datetime.now().time().second)


def get_log_dir_name():
    """
    Function to get current date from log directory naming
    :return:
        String of date and time

    """
    LOGGER.debug('Starting get_log_dir_name')
    return '{date}'.format(date=datetime.now().date().strftime("%m_%Y"))
