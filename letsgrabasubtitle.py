#!/usr/bin/env python
#
# Download subtitles from opensubtitles.org using the
# same API that media player classic does.
#
# -*- coding: utf-8 -*-

from __future__ import print_function
from modules import file_info, utils, osparser

import argparse
import os

arg_parser = argparse.ArgumentParser(description='Let\'s grab a subtitle -- an easy'
                                                 ' to use command line subtitle '
                                                 'downloader')
arg_parser.add_argument('path', help='file or path to look up')
arg_parser.add_argument('-d', '--directory-scan', action='store_true',
                        help='Scan and download subtitles for a given directory')
arg_parser.add_argument('-r', '--recursive', action='store_true',
                        help='Recursive directory scan')

args = arg_parser.parse_args()


def main():
    if args.directory_scan or args.recursive:
        if os.path.isdir(args.path):
            scan_directory(args.path, args.recursive)
        else:
            print(' - \'{0}\' is not a valid directory'.format(args.path))
    else:
        if utils.is_allowed_file_type(args.path):
            init_search_and_download(args.path)
        else:
            print(' - \'{0}\' is not a valid video file'.format(args.path))


def scan_directory(path, recursive=False):
    """
    :param path: Path to directory to scan.
    :param recursive: True if the scan should be recursive.
    """
    found_files = False
    if recursive:
        for root, sub_folders, files in os.walk(args.path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if utils.is_allowed_file_type(file_path):
                    found_files = True
                    init_search_and_download(file_path)
    else:
        for file_name in os.listdir(path):
            absolute_path = os.path.join(path, file_name)
            if utils.is_allowed_file_type(absolute_path):
                found_files = True
                init_search_and_download(absolute_path)
    if not found_files:
        print(' - No supported video files found in \'{0}\''.format(path))


def init_search_and_download(file_path):
    """
    :param file_path: The path to the file we want to download a subtitle for
    """
    fi = file_info.FileInfo(file_path)
    sub_parser = osparser.OpenSubtitlesParser(fi)

    if sub_parser.grab_subtitle():
        print(' + Subtitle successfully downloaded for \'{0}\''.format(fi.name))
    else:
        print(' - No subtitle found for \'{0}\''.format(fi.name))


if __name__ == '__main__':
    main()
