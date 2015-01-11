# open_subtitles_parser.py
# -*- coding: utf-8 -*-
import urllib2

from . import utils
import settings


class OpenSubtitlesParser(object):
    """ This class will read and parse the data given by the
    OpenSubtitles ISDB API. This API is used by MPC to search and grab subtitles
    and it does not require any kind of authentication. It should be safe to use
    this, because if it's changed it will break compatibility with MPC.
    """
    def __init__(self, file_info):
        self.file_info = file_info
        self.formatted_url = settings.BASE_URL.format(file_info.size, file_info.hash)
        self.subtitle_list = urllib2.urlopen(self.formatted_url).read()
        self.ticket = str()
        self.parsed_data = {}

    def parse_data(self):
        """ This method will parse the returned ISDB data and create
        a structured and usable dictionary to be used to download a subtitle.
        """
        lines = self.subtitle_list.split('\n')
        self.ticket = lines[0].split('=')[1]

        start = 2
        stop = 9
        sub_list = []

        for pos in range(len(lines)):
            sub = lines[start:stop]
            if len(sub) > 1:
                sub_list.append(sub)
            start += 12
            stop += 12
            if pos > stop:
                break

        for pos in range(len(sub_list)):
            self.parsed_data[pos] = {}
            for sub in sub_list[pos]:
                self.parsed_data[pos][sub.split('=')[0]] = sub.split('=')[1]

    def grab_subtitle(self, language=settings.ISO639):
        """ This method will download the first found subtitle matching the value
        of settings.ISO639, default is 'en'.
        """
        self.parse_data()
        for nr in range(len(self.parsed_data)):
            if self.parsed_data[nr]['iso639_2'] == language:
                sub = urllib2.urlopen((settings.DL_URL.format(
                    self.parsed_data[nr]['subtitle'], self.ticket)))
                utils.download_subtitle(self.file_info, sub.read())
                return True
        return False

    def __str__(self):
        return "OpenSubtitlesParser -> formatted_url: {0}" \
            .format(self.formatted_url)
