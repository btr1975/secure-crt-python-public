# $language = "python"
# $interface = "1.0"
import logging
import os
from ConfigParser import ConfigParser
__status__ = 'dev'
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class GlobalData(object):
    """
    Class to hold global required data
    """
    def __init__(self):
        LOGGER.debug('Init {}'.format(type(self)))
        self.id = os.environ.get('USERNAME')
        self.user_id = os.environ.get('USERNAME')
        self.primary_qip = "nusswdc-qes02"
        self.uat_qip = "nusmwdc-qes01-new"
        self.local_script_directory = None
        self.remote_script_directory = None

    def set_local_script_directory(self, local_script_directory):
        self.local_script_directory = local_script_directory

    def get_local_script_directory(self):
        return self.local_script_directory

    def set_remote_script_directory(self, remote_script_directory):
        self.remote_script_directory = remote_script_directory

    def get_remote_script_directory(self):
        return self.remote_script_directory

    def get_script_directory(self):
        if self.local_script_directory:
            return self.local_script_directory

        elif self.remote_script_directory:
            return self.remote_script_directory

        else:
            pass

    @staticmethod
    def get_config_ini(ini_file, section, option):
        temp_dict = dict()
        config = ConfigParser()
        config.read(ini_file)
        config.sections()

        for opt in config.options(section):
            try:
                temp_dict[opt] = config.get(section, opt)

            except Exception as e:
                print(e)
                temp_dict[opt] = None

        return temp_dict.get(option.lower())
