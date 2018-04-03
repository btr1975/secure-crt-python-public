from .message_boxes import CustomMessageBox, CustomPromptBox
from .pdt import *
from .windows_registry_reader import get_win_registry_key
from .name_helpers import get_log_dir_name, get_log_file_name
from .global_data_class import GlobalData
from .diff_match_patch import diff_match_patch, patch_obj
from .xlsxwriter.workbook import Workbook
from .web_connections import FindDataInHTML, diff_prettyHtmlTable
