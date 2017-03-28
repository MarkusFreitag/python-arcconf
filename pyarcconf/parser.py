"""Pyarcconf submodule, which provides methods for easier output parsing."""

def cut_lines(info_str, start, end):
    """Cut a number of lines from the start and the end.

    Args:
        info_str (str): command output from arcconf
        start (int): offset from start
        end (int): offset from end
    Returns:
        str: cutted info_str
    """
    return '\n'.join(info_str.split('\n')[start:end*-1])


def convert_attribute(key, value):
    """Convert an attribute into the most pratical datatype.
   
    If the value is 'enabled', 'yes', 'true', 'disabled', 'no' or 'false'
    it will be converted into boolean, otherwise it stays a string.
    Args:
        key (str): attribute key
        value (str): attribute value
    Returns:
        str, bool: key, value pair
        str, str: formated key, value pair
    """
    key = key.strip().lower()
    for char in [' ', '-', ',', '/']:
        key = key.replace(char, '_')
    for char in ['.']:
        key = key.replace(char, '')
    if '(' in key:
        key = key.split('(')[0]

    if len(value.split()) == 2:
        size, unit = value.split()
        if size.isdigit() and unit in ['B', 'KB', 'MB', 'GB']:
            return key, conv_bytes_up(size, unit)
    value = value.strip().lower()
    if value in ['enabled', 'yes', 'true']:
        return key, True
    elif value in ['disabled', 'no', 'false']:
        return key, False
    return key, value
