# open-subtitles-sub-grabber

## Info
I made this because I didn't find any convenient way to
download subtitles in OS X. Supposedly there's a plugin
for VLC which should download subtitles, but I never got
it to work. So I created this.

### Tested on
* OS X Yosemite
* Windows 8.1

I guess it should work on various linux and bsd flavours too.

## How to use it
```
usage: letsgrabasubtitle.py [-h] [-d] [-r] path

Let's grab a subtitle -- an easy to use command line subtitle downloader

positional arguments:
  path                  file or path to look up

optional arguments:
  -h, --help            show this help message and exit
  -d, --directory-scan  Scan and download subtitles for a given directory
  -r, --recursive       Recursive directory scan
```