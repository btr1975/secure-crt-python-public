# $language = "python"
# $interface = "1.0"
import logging
import shelve as __shelve
import csv as __csv
import os as __os
import sys as __sys
import re as __re
import random as __random
import string as __string
__status__ = 'prod'
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


def verify_file_exists(file_name, file_location):
    """
    Function to verify if a file exists
    Args:
        file_name: The name of file to check
        file_location: The location of the file, derive from the os module

    Returns: returns boolean True or False

    """
    return __os.path.isfile(__os.path.join(file_location, file_name))


def file_name_increase(file_name, file_location):
    """
    Function to increase a filename by a number 1
    Args:
        file_name: The name of file to check
        file_location: The location of the file, derive from the os module

    Returns: returns a good filename.

    """
    add_one = 1
    file_name_temp = file_name
    while verify_file_exists(file_name_temp, file_location):
        try:
            name, file_extension = file_name.split('.')
            file_name_temp = '%s-%i.%s' % (name, add_one, file_extension)
        except Exception as e:
            LOGGER.critical('Function file_name_increase Error {error} ignoring any errors'.format(error=e))
            name = file_name
            file_name_temp = '%s-%i' % (name, add_one)
        add_one += 1
    file_name = file_name_temp
    return file_name


def verify_directory(directory_name, directory_location, directory_create=False):
    """
    Function to verify if a directory exists
    Args:
        directory_name: The name of directory to check
        directory_location: The location of the directory, derive from the os module
        directory_create: If you want to create the directory

    Returns: returns boolean True or False, but if you set directory_create to True it will create the directory

    """
    if not directory_create:
        return __os.path.exists(__os.path.join(directory_location, directory_name))
    elif directory_create:
        good = __os.path.exists(__os.path.join(directory_location, directory_name))
        if not good:
            __os.mkdir(__os.path.join(directory_location, directory_name))


def create_nested_directories(start_known_path, *args):
    """
    Function to create nested directories
    :param start_known_path: A known starting path that exists
    :param args: Strings, directory names in a row
    :return:
        None

    """
    current_folders = list()
    current_path_check = start_known_path

    if not __os.path.isdir(__os.path.join(start_known_path, '\\'.join(args))):
        for nested_path in args:
            if not __os.path.isdir(__os.path.join(current_path_check, '\\'.join(current_folders), nested_path)):
                verify_directory(nested_path, __os.path.join(current_path_check, '\\'.join(current_folders)),
                                     directory_create=True)
                current_folders.append(nested_path)


def list_to_file(orig_list, file_name, file_location):
    """
    Function to export a list to a text file
    Args:
        orig_list: The list you want exported
        file_name: The name of the exported file
        file_location: The location of the file, derive from the os module

    Returns: returns the filename info

    """
    file = __os.path.join(file_location, file_name)

    def add_line_break(list_line):
        """
        Create a line break at the end of a string
        Args:
            list_line: string

        Returns: A string with a line break

        """
        list_line = ('%s\n' % (list_line,))
        return list_line
    write_file = open(file, "a")
    for orig_list_line in orig_list:
        write_file.write(add_line_break(str(orig_list_line)))
    write_file.close()
    return file_name


def file_to_list(file_name, file_location):
    """
    Function to import a text file to a list
    Args:
        file_name: The name of file to be import
        file_location: The location of the file, derive from the os module

    Returns: returns a list

    """
    file = __os.path.join(file_location, file_name)
    read_file = open(file, "r")
    temp_list = read_file.read().splitlines()
    read_file.close()
    return temp_list


def csv_to_dict(file_name, file_location):
    """
    Function to import a csv as a dictionary
    Args:
        file_name: The name of the csv file
        file_location: The location of the file, derive from the os module

    Returns: returns a dictionary

    """
    file = __os.path.join(file_location, file_name)
    try:
        csv_read = open(file, "r")
    except Exception as e:
        LOGGER.critical('Function csv_to_dict Error {error} ignoring any errors'.format(error=e))
        print('Error {error} ignoring any errors'.format(error=e))
        csv_read = open(file, "r", errors='ignore')
    data_row = __csv.DictReader(csv_read, dialect="excel")
    dict_key = 1
    temp_dict = dict()
    for row in data_row:
        temp_dict[dict_key] = row
        dict_key += 1
    csv_read.close()
    return temp_dict


def dict_to_csv(orig_dict, file_name, field_names_tuple, file_location):
    """
    Function to export a dictionary to a csv file
    Args:
        orig_dict: The dictionary you want exported
        file_name: The name of the exported file
        field_names_tuple: The fieldnames in a tuple
        file_location: The location of the file, derive from the os module

    Returns: returns the filename info

    """
    file = __os.path.join(file_location, file_name)
    csv_write = open(file, 'a')
    writer = __csv.DictWriter(csv_write, fieldnames=field_names_tuple, lineterminator='\n')
    headers = dict((n, n) for n in field_names_tuple)
    writer.writerow(headers)
    for dict_key, a in list(orig_dict.items()):
        writer.writerow(orig_dict[dict_key])
    csv_write.close()
    return file_name


def store_object(file_name, save_key, file_location, object_to_store=None):
    """
    Function to store objects in a shelve
    Args:
        file_name: Shelve storage file name
        save_key: The name of the key to store the item to
        file_location: The location of the file, derive from the os module
        object_to_store: The object you want to store

    Returns:

    """
    file = __os.path.join(file_location, file_name)
    try:
        shelve_store = __shelve.open(file)
    except Exception as e:
        LOGGER.critical('Function store_object Error {error} ignoring any errors'.format(error=e))
        print('Bad storage dB, rebuilding!!')
        __os.remove(file)
        shelve_store = __shelve.open(file)
    shelve_store[save_key] = object_to_store
    shelve_store.close()


def retrieve_object_from_file(file_name, save_key, file_location):
    """
    Function to retrieve objects from a shelve
    Args:
        file_name: Shelve storage file name
        save_key: The name of the key the item is stored in
        file_location: The location of the file, derive from the os module

    Returns: Returns the stored object

    """
    shelve_store = None
    file = __os.path.join(file_location, file_name)
    try:
        shelve_store = __shelve.open(file)
    except Exception as e:
        LOGGER.critical('Function retrieve_object_from_file Error {error} ignoring any errors'.format(error=e))
        __sys.exit('Storage dB is not readable, closing App!!')
    stored_object = shelve_store.get(save_key)
    shelve_store.close()
    return stored_object


def delete_object_from_file(file_name, save_key, file_location):
    """
    Function to delete objects from a shelve
    Args:
        file_name: Shelve storage file name
        save_key: The name of the key the item is stored in
        file_location: The location of the file, derive from the os module

    Returns:

    """
    file = __os.path.join(file_location, file_name)
    shelve_store = __shelve.open(file)
    del shelve_store[save_key]
    shelve_store.close()


def verify_key_in_shelve(file_name, save_key, file_location):
    """
    Function to check for a key in a shelve
    Args:
        file_name: Shelve storage file name
        save_key: The name of the key the item is stored in
        file_location: The location of the file, derive from the os module

    Returns: returns true or false

    """
    file = __os.path.join(file_location, file_name)
    shelve_store = __shelve.open(file)
    exists = shelve_store.get(save_key)
    shelve_store.close()
    if exists:
        return True

    elif not exists:
        return False


def get_keys_from_shelve(file_name, file_location):
    """
    Function to retreive all keys in a shelve
    Args:
        file_name: Shelve storage file name
        file_location: The location of the file, derive from the os module

    Returns:
        a list of the keys

    """
    temp_list = list()
    file = __os.path.join(file_location, file_name)
    shelve_store = __shelve.open(file)
    for key in shelve_store:
        temp_list.append(key)
    shelve_store.close()
    return temp_list


def remove_spaces(string_item):
    """
    Remove all spaces from a string
    Args:
        string_item: String that you want to remove spaces from

    Returns: returns a string without any spaces

    """
    string_item = ''.join(string_item.split())
    return string_item


def remove_spaces_add_hyphen(string_item):
    """
    Remove all spaces from a string and replace them with a hyphen
    Args:
        string_item: String that you want to remove spaces from

    Returns: returns a string with spaces replaced with a hyphen

    """
    string_item = '-'.join(string_item.split())
    return string_item


def remove_extra_spaces(string_item):
    """
    Remove all extra spaces from a string leaving single spaces
    Args:
        string_item: String that you want to remove spaces from

    Returns: returns a string with single spacing

    """
    string_item = ' '.join(string_item.split())
    return string_item


def remove_symbol_add_symbol(string_item, remove_symbol, add_symbol):
    """
    Remove a symbol from a string, and replace it with a different one
    Args:
        string_item: String that you want to replace symbols in
        remove_symbol: Symbol to remove
        add_symbol: Symbol to add

    Returns: returns a string with symbols swapped

    """
    string_item = add_symbol.join(string_item.split(remove_symbol))
    return string_item


def list_files_in_directory(full_directory_path):
    """
    List the files in a specified directory
    Args:
        full_directory_path: The full directory path to check, derive from the os module

    Returns: returns a list of files

    """
    files = list()
    for file_name in __os.listdir(full_directory_path):
        if __os.path.isfile(__os.path.join(full_directory_path, file_name)):
            files.append(file_name)
    return files


def list_directories_in_directory(full_directory_path):
    """
    List the directories in a specified directory
    Args:
        full_directory_path: The full directory path to check, derive from the os module

    Returns: returns a list of directories

    """
    directories = list()
    for directory_name in __os.listdir(full_directory_path):
        if __os.path.isdir(__os.path.join(full_directory_path, directory_name)):
            directories.append(directory_name)
    return directories


def split_string_retain_spaces(string):
    """
    Function to split a string, and retain spaces to rejoin
    :param string: A String
    :return:
        A split sting

    """
    return __re.split(r'(\s+)', string)


def join_split_string(split_string):
    """
    Function to join a split string
    :param split_string: A Split String
    :return:
        A joined string

    """
    return ''.join(split_string)


def split_strings_in_list_retain_spaces(orig_list):
    """
    Function to split every line in a list, and retain spaces for a rejoin
    :param orig_list: Original list
    :return:
        A List with split lines

    """
    temp_list = list()
    for line in orig_list:
        line_split = __re.split(r'(\s+)', line)
        temp_list.append(line_split)

    return temp_list


def random_line_data(chars_per_line=80):
    """
    Function to create a line of a random string
    Args:
        chars_per_line: An integer that says how many characters to return

    Returns:
        A String

    """
    return ''.join(__random.choice(__string.ascii_letters) for x in range(chars_per_line))


def random_data(line_count=1, chars_per_line=80):
    """
    Function to creates lines of random string data
    Args:
        line_count: An integer that says how many lines to return
        chars_per_line: An integer that says how many characters per line to return

    Returns:
        A String

    """
    divide_lines = chars_per_line * line_count
    return '\n'.join(random_line_data(chars_per_line) for x in range(int(divide_lines / chars_per_line)))