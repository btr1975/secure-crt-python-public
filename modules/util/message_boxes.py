# $language = "python"
# $interface = "1.0"
import logging
__status__ = 'dev'
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class CustomMessageBox(object):
    """
    Class for a Message Box
    """
    icon_dict = {
        16: 'Display the Error/Stop incon',
        32: 'Display the ? icon',
        48: 'Display the ! icon',
        64: 'Display the info icon',
    }
    button_dict = {
        0: 'OK button only',
        1: 'OK and Cancel buttons',
        2: 'Abort, Retry, and Ignore buttons',
        3: 'Yes, No, and Cancel buttons',
        4: 'Yes and No buttons',
        5: 'Retry and Cancel buttons',
    }
    button_response_dict = {
        1: 'OK button clicked',
        2: 'Cancel button clicked',
        3: 'Abort button clicked',
        4: 'Retry button clicked',
        5: 'Ignore button clicked',
        6: 'Yes button clicked',
        7: 'No button clicked',
    }

    def __init__(self, message, title='Title for Message Box', buttons=0, icon=64, crt=None):
        LOGGER.debug('Init {}'.format(type(self)))
        self.crt = crt
        self.message = message
        self.title = title
        self.buttons = buttons
        self.icon = icon

    def get_message_box(self):
        LOGGER.debug('Starting get_message_box {}'.format(type(self)))
        response = self.crt.Dialog.MessageBox(self.message, self.title, self.icon | self.buttons)
        LOGGER.debug('Found response {} get_message_box {}'.format(response, type(self)))
        return response


class CustomPromptBox(object):
    """
    Class for a Prompt Box
    """
    def __init__(self, message, title='Check Me', default=None, is_password=False, crt=None):
        LOGGER.debug('Init {}'.format(type(self)))
        self.crt = crt
        self.message = message
        self.title = title
        self.default = default
        self.is_password = is_password

    def get_message_box(self):
        LOGGER.debug('Starting get_message_box {}'.format(type(self)))
        response = self.crt.Dialog.Prompt(str(self.message), self.title)
        LOGGER.debug('Found response {} get_message_box {}'.format(response, type(self)))
        return response
