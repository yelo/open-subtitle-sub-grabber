# utils.py
# Simple utility class
# -*- coding: utf-8 -*-

import mimetypes
import os


def is_allowed_file_type(path):
    """
    :param path: The file path.
    :return: True if file is allowed, else False.
    """
    mimetype = str(mimetypes.guess_type(path)[0])
    return mimetype.split('/')[0] == 'video'


def download_subtitle(file_info, data):
    """
    :param file_info:  The file information object.
    :param data: The subtitle data.
    """
    target_file = '.'.join(file_info.name.split('.')[:-1]) + '.srt'
    target_directory = file_info.parent_directory
    with open(os.path.join(target_directory, target_file), 'wb') as subtitle:
        subtitle.write(data)
