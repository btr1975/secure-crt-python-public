# $language = "python"
# $interface = "1.0"
import logging
import sys
import os
from shutil import copy2
this_script_path = os.path.abspath(os.path.dirname(__file__))
if not this_script_path in sys.path:
    sys.path.insert(0, this_script_path)
import modules as mod


__status__ = 'dev'
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


def main():
    """
    Main Function
    :return:
        None

    """
    make_logger()
    start_control()


def start_control():
    LOGGER.debug('Starting start_control()')
    ticket_number = None
    global_data_obj = mod.GlobalData()
    message_box = mod.CustomMessageBox('Is this for a ticket?', title='Ticket', buttons=4, crt=crt)
    button_click = message_box.get_message_box()
    if button_click == 6:
        prompt = mod.CustomPromptBox('What is the ticket number, or folder you want to save data to?',
                                     title='Ticket Number' ,crt=crt)
        ticket_number = prompt.get_message_box().upper()

    try:
        prompt = mod.CustomPromptBox('What is the OS of the device?  Example: ios, nxos, or exit',
                                     title='OS Type Entry', crt=crt)
        os_type = None
        while os_type not in ('IOS',):
            os_type = prompt.get_message_box().upper()
            LOGGER.debug('Found OS type {}'.format(os_type))
            if os_type in ('IOS',):
                mod.Ios(crt=crt, ticket=ticket_number)

            elif os_type in ('NXOS', 'NX-OS', 'NEXUS'):
                mod.Nexus(crt=crt, ticket=ticket_number)

            elif os_type in ('XR', 'IOS-XR', 'IOSXR'):
                mod.IosXr(crt=crt, ticket=ticket_number)

            elif os_type == 'EXIT':
                message_box = mod.CustomMessageBox('Do yu want to stop running the script?', title='Exit Script',
                                                   buttons=4, crt=crt)
                button_click = message_box.get_message_box()
                if button_click == 6:
                    break

    except Exception as e:
        LOGGER.critical(e)


def make_logger():
    logging.basicConfig(format='%(asctime)s: %(name)s - %(levelname)s - %(message)s',
                        filename=os.path.join(os.path.join(mod.get_win_registry_key('Software\VanDyke\SecureCRT',
                                                                                    'Config Path'),
                                                           'Logs', 'securecrt-script-logs.txt')))
    logging.getLogger().setLevel(logging.DEBUG)
    LOGGER.warning('Logging Started!!')


main()
