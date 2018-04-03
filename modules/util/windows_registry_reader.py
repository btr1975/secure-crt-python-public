# $language = "python"
# $interface = "1.0"
import logging
import _winreg
__status__ = 'dev'
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


def get_win_registry_key(hkey_current_user_location, registry_key):
    """
    Function to retrieve a registry key value from hkey_current_user_location
    :param hkey_current_user_location: path to the key
    :param registry_key: The key you want
    :return:
    """
    LOGGER.debug('Starting get_win_registry_key')
    registry_obj = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)

    key = _winreg.OpenKey(registry_obj, hkey_current_user_location)
    for i in range(1024):
        try:
            key_name, key_value, t = _winreg.EnumValue(key, i)
            if key_name == registry_key:
                return key_value
        except EnvironmentError:
            break
        _winreg.CloseKey(key)
