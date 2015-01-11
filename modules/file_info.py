# file_info.py
# -*- coding: utf-8 -*-

import os
import struct


class FileInfo(object):
    """ Simple class which holds file information.
    """
    def __init__(self, path):
        self.path = path
        self.parent_directory = os.path.dirname(os.path.abspath(path))
        self.name = path.split("/")[-1]
        self.size = hex(os.path.getsize(path))
        self.hash = self._os_hash_file()

    def _os_hash_file(self):
        """ Code taken (and pythonified) from
        http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
        """
        try:
            longlongformat = "q"  # long long
            bytesize = struct.calcsize(longlongformat)

            f = open(self.path, "rb")

            file_size = os.path.getsize(self.path)
            file_hash = file_size

            if file_size < 65536 * 2:
                return "SizeError"

            for x in range(65536 / bytesize):
                buffered = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffered)
                file_hash += l_value
                file_hash &= 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

            f.seek(max(0, file_size - 65536), 0)
            for x in range(65536 / bytesize):
                buffered = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffered)
                file_hash += l_value
                file_hash &= 0xFFFFFFFFFFFFFFFF

            f.close()
            returned_hash = "%016x" % file_hash
            return returned_hash

        except IOError:
            return "IOError"

    def __str__(self):
        return "FileInfo -> path: {0} | size: {1} | hash: {2} "\
            .format(self.path, self.size, self.hash)
