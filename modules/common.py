# $language = "python"
# $interface = "1.0"
import logging
import os
import re
import itertools
from .util.diff_match_patch import diff_match_patch
from .util.xlsxwriter import Workbook
from .util.name_helpers import get_log_file_name, get_log_dir_name
from .util.web_connections import diff_prettyHtmlTable
from .util.pdt import list_to_file, verify_file_exists, file_to_list
from .util.message_boxes import CustomMessageBox
__status__ = 'dev'
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class CommonRunner(object):
    """
    Class for a common runner
    """
    def __init__(self, crt=None):
        LOGGER.debug('Init {}'.format(type(self)))
        self.crt = crt
        self.crt.Synchronous = True
        self.current_tab = crt.GetScriptTab()
        self.user_id = os.environ.get('USERNAME')
        self.date_log_directory = get_log_dir_name()
        self.log_file_time = get_log_file_name()
        self.main_wait_strings = [
            '#START\r',
            '#START\r'.lower(),
            '#PRE\r',
            '#PRE\r'.lower(),
            '#POST\r',
            '#POST\r'.lower(),
            '#DIFFHTML\r',
            '#DIFFHTML\r'.lower(),
            '#DIFFXLS\r',
            '#DIFFXLS\r'.lower(),
            'sername:',
            'ogin:',
            '#HEALTH\r',
            '#HEALTH\r'.lower(),
        ]
        self.username_found = False
        path, garbage = os.path.split(self.crt.Session.LogFileName)
        self.pre_log_file = os.path.join(path, 'temp.txt')
        self._change_log_file(self.pre_log_file)
        self.file_names_created = dict()
        self.start_method = None
        self.pre_method = None
        self.post_method = None
        self.diff_html_method = None
        self.diff_xls_method = None
        self.health_method = None

    def __str__(self):
        return '<Class: CommonRunner>'

    def _watcher(self):
        """
        Method to start a command watcher to run other methods
        :return:
            None

        """
        LOGGER.debug('Starting _watcher {}'.format(type(self)))
        while True:
            if not self.current_tab.Session.Connected:
                break

            result = self.current_tab.Screen.WaitForStrings(self.main_wait_strings)

            if result in (1, 2):
                if self.start_method:
                    self.start_method()

            elif result in (3, 4):
                if self.pre_method:
                    self.pre_method()

            elif result in (5, 6):
                if self.post_method:
                    self.post_method()

            elif result in (7, 8):
                if self.diff_html_method:
                    self.diff_html_method()

            elif result in (9, 10):
                if self.diff_xls_method:
                    self.diff_xls_method()

            elif result in (11, 12):
                if not self.username_found:
                    self.current_tab.Screen.Send('{username}\n'.format(username=self.user_id))
                    self.username_found = True

            elif result in (13, 14):
                if self.health_method:
                    self.health_method()

            elif self.current_tab.Session.Connected in (False, 0):
                break

            LOGGER.debug('Result _watcher {} {}'.format(result, type(self)))

    def _get_regex_data_from_pull(self, command, prompt_ending, *args, **kwargs):
        """
        Method to grab random data from the screen with a regex
        :param command: The command you want to run on the device you must include \r\n
        :param prompt_ending: The prompt ending you want to wait for such as # or >
        :param args: The regular expressions to match
        :param kwargs: Available keywords are wait_time
        :return:
            A String, or None

        """
        LOGGER.debug('Starting _get_regex_data_from_pull {}'.format(type(self)))
        if kwargs.get('wait_time'):
            wait_time = kwargs.get('wait_time')

        else:
            wait_time = 0

        found_data = list()
        self.current_tab.Screen.IgnoreEscape = True

        self.current_tab.Screen.Send(command)

        self.current_tab.Screen.WaitForString(command, wait_time)

        screen_data = self.current_tab.Screen.ReadString(prompt_ending)

        for find in args:

            try:
                found_data.append(re.search(find, screen_data).group(0))

            except AttributeError:
                found_data.append(None)

        return found_data

    def _change_log_file(self, log_file):
        """
        Method to change where logs are output to
        :param log_file: Full path to the log file
        :return:
            None

        """
        LOGGER.debug('Starting _change_log_file {}'.format(type(self)))
        if self.current_tab.Session.Logging == 1:
            self.current_tab.Session.Log(False)
            self.current_tab.Session.LogFileName = '{}'.format(log_file)
            self.current_tab.Session.Log(True)

    def _get_blob_data(self, command, prompt_ending, **kwargs):
        """
        Method to retrieve a blob of data from a command
        :param command: The command you want to run on the device you must include \r\n
        :param prompt_ending: What the prompt should be to end
        :param kwargs: Available keywords are wait_time
        :return:
            A list of data

        """
        LOGGER.debug('Starting _get_blob_data {}'.format(type(self)))
        if kwargs.get('wait_time'):
            wait_time = kwargs.get('wait_time')

        else:
            wait_time = 0

        self.current_tab.Screen.IgnoreEscape = True

        self.current_tab.Screen.Send(command)

        self.current_tab.Screen.WaitForString(command, wait_time)

        screen_data = self.current_tab.Screen.ReadString(prompt_ending)

        return screen_data.splitlines()

    def _diff_init_and_post_files(self, init_file, post_file, diff_file, log_path):
        """
        Method to create a html diff table
        :param init_file: A list of the file
        :param post_file: A list of the file
        :param diff_file: The name of the output file
        :param log_path: The full path to store the file in
        :return:
            None

        """
        LOGGER.debug('Starting _diff_init_and_post_files {}'.format(type(self)))
        diff_object = diff_match_patch()

        temp_html = list()
        temp_html.append(diff_prettyHtmlTable(diff_object.diff_lineMode(init_file, post_file, deadline=20)))

        list_to_file(temp_html, diff_file, log_path)

    def _check_if_file_created(self, file_name, log_path):
        """
        Method to check if the file exists, if so ask if you want to delete it
        :param file_name: The file name
        :param log_path: The path to the file
        :return:
            Boolean True if ok to proceed, False if it is not ok to proceed

        """
        if verify_file_exists(file_name, log_path):
            msg_box = CustomMessageBox('The file named {} already exists do you want to delete it? '
                                       'You will not be asked are you sure.'.format(file_name),
                                       title='File Name Exists', buttons=4, icon=48, crt=self.crt)
            response = msg_box.get_message_box()
            if response == 6:
                os.remove(os.path.join(log_path, file_name))
                return True

            else:
                return False

        else:
            return True


class CommonMethods(CommonRunner):
    """
    Class of common methods
    """
    def __init__(self, crt=None):
        CommonRunner.__init__(self, crt=crt)
        self.log_path = None
        self.log_name = None
        self.commands_used = list()
        self.hostname = None

    def __str__(self):
        return '<Class: CommonMethods>'

    def collect_diff_data(self, *args):
        """
        Method to return the data from the files
        :param args: A list of what pairs you want, options are eigrp, bgp, pim, ospf, general, config
        :return:
            2 Lists

        """
        LOGGER.debug('Starting collect_diff_data {}'.format(type(self)))
        pre_list = list()
        post_list = list()

        dict_of_file_names = self.get_available_paired_files(*args)

        for key in dict_of_file_names:
            pre_list += file_to_list(dict_of_file_names[key].get('pre'), self.log_path)
            post_list += file_to_list(dict_of_file_names[key].get('post'), self.log_path)
            pre_list.append('')
            post_list.append('')

        return pre_list, post_list

    def get_available_paired_files(self, *args):
        """
        Method to check for files before doing a diff
        :param args: A list of what pairs you want, options are eigrp, bgp, pim, ospf, general, config
        :return:
            A Dictionary

        """
        LOGGER.debug('Starting get_available_paired_files {}'.format(type(self)))
        dict_of_file_names = {
            'eigrp': {},
            'bgp': {},
            'pim': {},
            'ospf': {},
            'general': {},
            'config': {},
        }

        for key in self.file_names_created.keys():
            if 'eigrp' in key and 'pre' in key:
                dict_of_file_names['eigrp'].update({'pre': self.file_names_created.get(key)})

            elif 'eigrp' in key and 'post' in key:
                dict_of_file_names['eigrp'].update({'post': self.file_names_created.get(key)})

            elif 'bgp' in key and 'pre' in key:
                dict_of_file_names['bgp'].update({'pre': self.file_names_created.get(key)})

            elif 'bgp' in key and 'post' in key:
                dict_of_file_names['bgp'].update({'post': self.file_names_created.get(key)})

            elif 'pim' in key and 'pre' in key:
                dict_of_file_names['pim'].update({'pre': self.file_names_created.get(key)})

            elif 'pim' in key and 'post' in key:
                dict_of_file_names['pim'].update({'post': self.file_names_created.get(key)})

            elif 'ospf' in key and 'pre' in key:
                dict_of_file_names['ospf'].update({'pre': self.file_names_created.get(key)})

            elif 'ospf' in key and 'post' in key:
                dict_of_file_names['ospf'].update({'post': self.file_names_created.get(key)})

            elif 'general' in key and 'pre' in key:
                dict_of_file_names['general'].update({'pre': self.file_names_created.get(key)})

            elif 'general' in key and 'post' in key:
                dict_of_file_names['general'].update({'post': self.file_names_created.get(key)})

            elif 'init' in key:
                dict_of_file_names['config'].update({'pre': self.file_names_created.get(key)})

            elif 'end' in key:
                dict_of_file_names['config'].update({'post': self.file_names_created.get(key)})

        for pair in dict_of_file_names.keys():
            if pair in args:
                if not verify_file_exists(dict_of_file_names.get(pair).get('pre'), self.log_path) \
                        or not verify_file_exists(dict_of_file_names.get(pair).get('post'), self.log_path):
                    dict_of_file_names.pop(pair)

            else:
                dict_of_file_names.pop(pair)

        return dict_of_file_names

    def create_file_names(self):
        """
        Method to pre load what file names could be created
        :return:
            None

        """
        LOGGER.debug('Starting create_file_names {}'.format(type(self)))
        self.file_names_created['init'] = '{}-init.txt'.format(self.log_name)
        self.file_names_created['end'] = '{}-end.txt'.format(self.log_name)
        self.file_names_created['eigrp-pre'] = '{}-eigrp-pre.txt'.format(self.log_name)
        self.file_names_created['eigrp-post'] = '{}-eigrp-post.txt'.format(self.log_name)
        self.file_names_created['bgp-pre'] = '{}-bgp-pre.txt'.format(self.log_name)
        self.file_names_created['bgp-post'] = '{}-bgp-post.txt'.format(self.log_name)
        self.file_names_created['ospf-pre'] = '{}-ospf-pre.txt'.format(self.log_name)
        self.file_names_created['ospf-post'] = '{}-ospf-post.txt'.format(self.log_name)
        self.file_names_created['pim-pre'] = '{}-pim-pre.txt'.format(self.log_name)
        self.file_names_created['pim-post'] = '{}-pim-post.txt'.format(self.log_name)
        self.file_names_created['general-pre'] = '{}-general-pre.txt'.format(self.log_name)
        self.file_names_created['general-post'] = '{}-general-post.txt'.format(self.log_name)
        self.file_names_created['html'] = '{}-diff.html'.format(self.log_name)
        self.file_names_created['xls'] = '{}.xlsx'.format(self.log_name)

    def get_diff_html(self):
        """
        Method to create a html diff report
        :return:
            None

        """
        LOGGER.debug('Starting get_diff_html {}'.format(type(self)))
        if self._check_if_file_created(self.file_names_created.get('html'), self.log_path):
            if verify_file_exists(self.file_names_created.get('init'), self.log_path) and \
                    verify_file_exists(self.file_names_created.get('end'), self.log_path):
                pre, post = self.collect_diff_data('config')
                self._diff_init_and_post_files('\n'.join(pre), '\n'.join(post), self.file_names_created.get('html'),
                                               self.log_path)

            else:
                msg_box = CustomMessageBox('Either {} or {} does not exists to diff '
                                           'against!'.format(self.file_names_created.get('init'),
                                                             self.file_names_created.get('end')),
                                           title='File Missing Cannot Complete #diffhtml!', buttons=0, icon=48,
                                           crt=self.crt)
                msg_box.get_message_box()

    def get_diff_xls(self):
        """
        Method to create a 'Mike Paulson' spreadsheet
        :return:
            None

        """
        LOGGER.debug('Starting get_diff_xls {}'.format(type(self)))
        if self._check_if_file_created(self.file_names_created.get('xls'), self.log_path):
            if verify_file_exists(self.file_names_created.get('init'), self.log_path) and \
                    verify_file_exists(self.file_names_created.get('end'), self.log_path):
                pre, post = self.collect_diff_data('eigrp', 'bgp', 'pim', 'ospf', 'general')
                workbook = WriteXlsx(pre, post, self.file_names_created.get('xls'), self.log_path, self.commands_used,
                                     self.hostname)
                workbook.close()

            else:
                msg_box = CustomMessageBox('Either {} or {} does not exists to diff '
                                           'against!'.format(self.file_names_created.get('init'),
                                                             self.file_names_created.get('end')),
                                           title='File Missing Cannot Complete #diffxls!', buttons=0, icon=48,
                                           crt=self.crt)
                msg_box.get_message_box()


class WriteXlsx(Workbook):
    """
    Class to Write the Spreadsheet in the 'Mike Paulson' way
    """
    def __init__(self, pre, post, file_name, file_path, commands_used, hostname):
        Workbook.__init__(self, filename=os.path.join(file_path, file_name))
        self.file_name = file_name
        self.file_path = file_path
        self.commands_used = commands_used
        self.hostname = hostname
        self.pre_cleaned = pre
        self.post_cleaned = post
        self.__write_diff_data()

    def __str__(self):
        return '<Class: WriteXlsx>'

    def __pre_cell_format(self):
        """
        Method to change the format of a changed cell to light green
        :return:
            The cell format

        """
        cellformat = self.add_format({
            'border': 1,
            'fg_color': '#ccffcc'})
        return cellformat

    def __post_cell_format(self):
        """
        Method to change the format of a changed cell to light blue
        :return:
            The cell format

        """
        cellformat = self.add_format({
            'border': 1,
            'fg_color': '#99ccff'})
        return cellformat

    def __yellow_cell_format(self):
        """
        Method to change the format of a changed cell to light blue
        :return:
            The cell format

        """
        cellformat = self.add_format({
            'border': 1,
            'fg_color': '#ffff99'})
        return cellformat

    def __black_cell_format(self):
        """
        Method to change the format of a changed cell to light blue
        :return:
            The cell format

        """
        cellformat = self.add_format({
            'border': 1,
            'fg_color': '#000000'})
        return cellformat

    def __regular_cell_format(self):
        """
        Method to change the format of a normal cell
        :return:
            The cell format

        """
        cellformat = self.add_format({
            'border': 1})
        return cellformat

    def __sheet_create(self, sheet_name):
        """
        Method to create a sheet
        :param sheet_name: The name of the sheet
        :return:
            A sheet object

        """
        sheet_obj = self.add_worksheet(sheet_name)
        sheet_obj.hide_gridlines(2)
        return sheet_obj

    def __write_diff_data(self):
        """
        Method to write the diff sheet
        :return:
            None

        """
        sheet_obj = self.__sheet_create('DIFF')
        sheet_obj.set_column(0, 30, 80.00)
        row = 0

        sheet_obj.write(row, 0, 'Before', self.__pre_cell_format())
        sheet_obj.write(row, 1, 'After', self.__post_cell_format())
        row += 1

        sheet_obj.write(row, 0, self.hostname, self.__yellow_cell_format())
        sheet_obj.write(row, 1, self.hostname, self.__yellow_cell_format())
        row += 1

        for command in self.commands_used:
            sheet_obj.write(row, 0, command, self.__pre_cell_format())
            sheet_obj.write(row, 1, command, self.__post_cell_format())

            row += 1

        sheet_obj.write_blank(row, 0, None, self.__pre_cell_format())
        sheet_obj.write_blank(row, 1, None, self.__post_cell_format())
        row += 1

        sheet_obj.write_blank(row, 0, None, self.__black_cell_format())
        sheet_obj.write_blank(row, 1, None, self.__black_cell_format())
        row += 1

        for pre, post in itertools.izip_longest(self.pre_cleaned, self.post_cleaned):
            sheet_obj.write(row, 0, pre, self.__pre_cell_format())
            sheet_obj.write(row, 1, post, self.__post_cell_format())

            row += 1
