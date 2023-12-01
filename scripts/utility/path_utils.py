import os

from config import ROOT_DIR


def get_path_from_root(*subdirs):
    """
    Construct a path based on the root directory.

    :param subdirs: LIst of subdirectories or files; in order
    :return: full path from the root directory
    """
    return os.path.join(ROOT_DIR, *subdirs)


def get_raw_data_path(filename):
    """
    Get the full path to the raw data files.

    :param filename: Name of the data file
    :return: path to the data file based on input
    """

    return get_path_from_root("data", "raw", filename)
