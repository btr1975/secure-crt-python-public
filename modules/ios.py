# $language = "python"
# $interface = "1.0"
import logging
import re
import os
from common import CommonMethods
from .util.windows_registry_reader import get_win_registry_key
from .util.pdt import list_to_file, remove_symbol_add_symbol
__status__ = 'dev'
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class Ios(CommonMethods):
    """
    Class for a Cisco IOS based system
    """
    def __init__(self, crt=None, ticket=None):
        LOGGER.debug('Init {}'.format(type(self)))
        CommonMethods.__init__(self, crt=crt)
        self.ticket = ticket
        self.model_number = None
        self.image_version = None
        self.pre_post = None
        if self.ticket:
            self.log_path = os.path.join(get_win_registry_key('Software\VanDyke\SecureCRT', 'Config Path'), 'Logs',
                                         self.date_log_directory, self.user_id, self.ticket)
        else:
            self.log_path = os.path.join(get_win_registry_key('Software\VanDyke\SecureCRT', 'Config Path'), 'Logs',
                                         self.date_log_directory, self.user_id)
        self.config_register = None
        self.general_pre_commands = [
            'show ip cef',
            'show ip route',
        ]
        self.bgp = None
        self.bgp_commands = [
            'show ip bgp summary',
            'show ip bgp',
        ]
        self.eigrp = None
        self.eigrp_commands = [
            'show ip eigrp neighbors',
            'show ip eigrp topology',
        ]
        self.ospf = None
        self.ospf_commands = [
            'show ip ospf neighbor',
            'show ip ospf database',
        ]
        self.pim = None
        self.pim_commands = [
            'show ip pim neighbor',
            'show ip mroute',
            'show ip pim rp mapping',
        ]
        self.health_commands = [
            'show interface',
            'show logging'
        ]
        self.hostname_regex = re.compile(r'^.*#|>')
        self.image_version_regex = re.compile(r'\d+\.\d+\(\d+\)([A-Z0-9]+)', re.IGNORECASE)
        self.config_register_regex = re.compile(r'\d+X\d+', re.IGNORECASE)
        self.bgp_regex = re.compile(r'router bgp')
        self.eigrp_regex = re.compile(r'router eigrp')
        self.ospf_regex = re.compile(r'router ospf')
        self.pim_regex = re.compile(r'ip multicast-routing')
        self.start_method = self.set_pre_settings
        self.pre_method = self.get_initial_configuration
        self.post_method = self.get_post_configuration
        self.diff_html_method = self.get_diff_html
        self.diff_xls_method = self.get_diff_xls
        self.health_method = self.check_health_data
        self._watcher()

    def __str__(self):
        return '<Class: Ios>'

    def set_pre_settings(self):
        """
        Method to get the hostname and set the terminal length to the current screen sizse
        :return:
            None

        """
        LOGGER.debug('Starting set_pre_settings {}'.format(type(self)))
        self.current_tab.Screen.Send('\r\n')
        self.set_hostname()
        log_file = '{}-{}.txt'.format(os.path.join(self.log_path, self.log_name), self.log_file_time)
        self._change_log_file(log_file)
        self.current_tab.Screen.Send('terminal length {}\r\n'.format(self.current_tab.Screen.Rows - 5))
        self.create_file_names()

    def get_initial_configuration(self):
        """
        Method to pull initial config, and output to a file
        :return:
            None

        """
        LOGGER.debug('Starting get_initial_configuration {}'.format(type(self)))
        self.pre_post = 'pre'
        self.current_tab.Screen.Send('terminal length 0\r\n')
        if self._check_if_file_created(self.file_names_created.get('init'), self.log_path):
            data_list = self._get_blob_data('show running-config\r\n', '{hostname}#'.format(hostname=self.hostname))
            list_to_file(data_list, self.file_names_created.get('init'), self.log_path)
        self.get_image_version()
        self.get_general_data()
        self.get_system_info()
        self.current_tab.Screen.Send('terminal length {}\r\n'.format(self.current_tab.Screen.Rows - 5))

    def get_post_configuration(self):
        """
        Method to pull post config, and output to a file
        :return:
            None

        """
        LOGGER.debug('Starting get_post_configuration {}'.format(type(self)))
        self.pre_post = 'post'
        self.current_tab.Screen.Send('terminal length 0\r\n')
        if self._check_if_file_created(self.file_names_created.get('end'), self.log_path):
            data_list = self._get_blob_data('show running-config\r\n', '{hostname}#'.format(hostname=self.hostname))
            list_to_file(data_list, self.file_names_created.get('end'), self.log_path)
        self.get_image_version()
        self.get_general_data()
        self.get_system_info()
        self.current_tab.Screen.Send('terminal length {}\r\n'.format(self.current_tab.Screen.Rows - 5))

    def set_hostname(self):
        """
        Method to set the hostname variable and correct for certain chars
        :return:
            None

        """
        LOGGER.debug('Starting set_hostname {}'.format(type(self)))
        screen_row = self.current_tab.Screen.CurrentRow + 0
        read_line = self.current_tab.Screen.Get(screen_row, 1, screen_row, 120)
        try:
            temp_hostname = re.search(self.hostname_regex, read_line).group(0).split('#')
            self.hostname = temp_hostname[0]

        except AttributeError:
            self.hostname = 'UNKNOWN'

        self.current_tab.Caption = self.hostname
        self.log_name = self.hostname
        self.log_name = remove_symbol_add_symbol(self.log_name, '/', '-')
        self.log_name = remove_symbol_add_symbol(self.log_name, ':', '-')

    def get_hostname(self):
        pass

    def get_model_number(self):
        pass

    def get_system_info(self):
        """
        Method to check the running config and decide what commands to run
        :return:
            None

        """
        LOGGER.debug('Starting get_system_info {}'.format(type(self)))
        found_data = self._get_regex_data_from_pull('show running-config\r\n',
                                                    '{hostname}#'.format(hostname=self.hostname),
                                                    self.bgp_regex,
                                                    self.eigrp_regex,
                                                    self.ospf_regex,
                                                    self.pim_regex)

        if len(found_data) >= 1:

            if found_data[0]:
                self.bgp = True
                self.get_bgp_data()

            if found_data[1]:
                self.eigrp = True
                self.get_eigrp_data()

            if found_data[2]:
                self.ospf = True
                self.get_ospf_data()

            if found_data[3]:
                self.pim = True
                self.get_pim_data()

    def get_image_version(self):
        """
        Method to check show version for specific items
        :return:
            None

        """
        LOGGER.debug('Starting get_image_version {}'.format(type(self)))
        found_data = self._get_regex_data_from_pull('show version\r\n', '{hostname}#'.format(hostname=self.hostname),
                                                    self.image_version_regex,
                                                    self.config_register_regex)

        if len(found_data) >= 1:

            if found_data[0]:
                self.image_version = found_data[0]
                LOGGER.debug('Found image_version {} get_image_version {}'.format(self.image_version, type(self)))

            else:
                self.image_version = 'UNKNOWN'

            if found_data[1]:
                self.config_register = found_data[1]
                LOGGER.debug('Found config_register {} get_image_version {}'.format(self.config_register, type(self)))

            else:
                self.config_register = 'UNKNOWN'

    def get_eigrp_data(self):
        """
        Method to retrieve EIGRP data and save it to a file
        :return:
            None

        """
        LOGGER.debug('Starting get_eigrp_data {}'.format(type(self)))
        if self._check_if_file_created(self.file_names_created.get('eigrp-{}'.format(self.pre_post)), self.log_path):
            data_list = list()
            self.commands_used += self.eigrp_commands
            for command in self.eigrp_commands:
                data_list.append('{hostname}#{command}'.format(hostname=self.hostname, command=command))
                data_list += self._get_blob_data('{}\r\n'.format(command), '{hostname}#'.format(hostname=self.hostname))

            list_to_file(data_list, self.file_names_created.get('eigrp-{}'.format(self.pre_post)), self.log_path)

    def get_pim_data(self):
        """
        Method to retrieve PIM data and save it to a file
        :return:
            None

        """
        LOGGER.debug('Starting get_pim_data {}'.format(type(self)))
        if self._check_if_file_created(self.file_names_created.get('pim-{}'.format(self.pre_post)), self.log_path):
            data_list = list()
            self.commands_used += self.pim_commands
            for command in self.pim_commands:
                data_list.append('{hostname}#{command}'.format(hostname=self.hostname, command=command))
                data_list += self._get_blob_data('{}\r\n'.format(command), '{hostname}#'.format(hostname=self.hostname))

            list_to_file(data_list, self.file_names_created.get('pim-{}'.format(self.pre_post)), self.log_path)

    def get_bgp_data(self):
        """
        Method to retrieve BGP data and save it to a file
        :return:
            None

        """
        LOGGER.debug('Starting get_bgp_data {}'.format(type(self)))
        if self._check_if_file_created(self.file_names_created.get('bgp-{}'.format(self.pre_post)),  self.log_path):
            data_list = list()
            self.commands_used += self.bgp_commands
            for command in self.bgp_commands:
                data_list.append('{hostname}#{command}'.format(hostname=self.hostname, command=command))
                data_list += self._get_blob_data('{}\r\n'.format(command), '{hostname}#'.format(hostname=self.hostname))

            list_to_file(data_list, self.file_names_created.get('bgp-{}'.format(self.pre_post)), self.log_path)

    def get_ospf_data(self):
        """
        Method to retrieve OSPF data and save it to a file
        :return:
            None

        """
        LOGGER.debug('Starting get_ospf_data {}'.format(type(self)))
        if self._check_if_file_created(self.file_names_created.get('ospf-{}'.format(self.pre_post)), self.log_path):
            data_list = list()
            self.commands_used += self.ospf_commands
            for command in self.ospf_commands:
                data_list.append('{hostname}#{command}'.format(hostname=self.hostname, command=command))
                data_list += self._get_blob_data('{}\r\n'.format(command), '{hostname}#'.format(hostname=self.hostname))

            list_to_file(data_list, self.file_names_created.get('ospf-{}'.format(self.pre_post)), self.log_path)

    def get_general_data(self):
        """
        Method to retrieve general data and save it to a file
        :return:
            None

        """
        LOGGER.debug('Starting get_general_data {}'.format(type(self)))
        if self._check_if_file_created(self.file_names_created.get('general-{}'.format(self.pre_post)), self.log_path):
            data_list = list()
            self.commands_used += self.general_pre_commands
            for command in self.general_pre_commands:
                data_list.append('{hostname}#{command}'.format(hostname=self.hostname, command=command))
                data_list += self._get_blob_data('{}\r\n'.format(command), '{hostname}#'.format(hostname=self.hostname))

            list_to_file(data_list, self.file_names_created.get('general-{}'.format(self.pre_post)), self.log_path)

    def check_health_data(self):
        LOGGER.debug('Starting check_health_data {}'.format(type(self)))
        self.current_tab.Screen.Send('terminal length 0\r\n')
        data_list = list()
        for command in self.health_commands:
            data_list += self._get_blob_data('{}\r\n'.format(command), '{hostname}#'.format(hostname=self.hostname))

        ethernet_regex = re.compile(r'Ethernet', re.IGNORECASE)
        input_error_regex = re.compile(r'[1-9]\d* input errors', re.IGNORECASE)
        output_errors_regex = re.compile(r'[1-9]\d* output errors', re.IGNORECASE)
        crc_errors_regex = re.compile(r'[1-9]\d* CRC', re.IGNORECASE)
        output_drops_regex = re.compile(r'Total output drops: [1-9]\d*', re.IGNORECASE)
        input_drops_regex = re.compile(r'Input queue: \d+/\d+/[1-9]\d*/\d+', re.IGNORECASE)
        temp_list = list()
        for line in data_list:
            if re.search(ethernet_regex, line):
                temp_list.append(line)

            elif re.search(input_drops_regex, line):
                temp_list.append(line)

            elif re.search(output_drops_regex, line):
                temp_list.append(line)

            elif re.search(input_error_regex, line):
                temp_list.append(line)

            elif re.search(output_errors_regex, line):
                temp_list.append(line)

            elif re.search(crc_errors_regex, line):
                temp_list.append(line)

        list_to_file(temp_list, 'test.txt', self.log_path)

        self.current_tab.Screen.Send('terminal length {}\r\n'.format(self.current_tab.Screen.Rows - 5))
