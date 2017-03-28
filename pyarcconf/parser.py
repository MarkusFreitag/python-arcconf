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
