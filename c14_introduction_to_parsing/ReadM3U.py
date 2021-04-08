"""
Handcraft parsing M3U format.
"""
import re
import collections

"""
#EXTM3U
#EXTINF:230,Blondie - Atomic Blondie\Atomic\01-Atomic.ogg
...
#EXTINF:-1,Blondie - I'm Gonna Love You Too
Blondie\Atomic\18-I'm Gonna Love You Too.ogg
"""

"""
M3U      ::= '#EXTM3U\n' ENTRY+
ENTRY    ::= INFO '\n' FILENAME '\n'
INFO     ::= '#EXTINF:' SECONDS ',' TITLE
SECONDS  ::= '-'? \d+
TITLE    ::= [^\n]+
FILENAME ::= [^\n]+
"""

Song = collections.namedtuple('Song', 'title seconds filename')


def songs_regex(fh):
    if fh.readline() != '#EXTM3U\n':
        print('This is not a .m3u file')
        return []

    songs = []
    INFO_RE = re.compile(r"#EXTINF:(?P<seconds>-?\d+),(?P<title>.+)")
    title = seconds = None
    WANT_INFO, WANT_FILENAME = range(2)
    state = WANT_INFO
    for lino, line in enumerate(fh, start=2):
        line = line.strip()
        if not line:
            continue
        if state == WANT_INFO:
            info = INFO_RE.match(line)
            if info:
                title = info.group('title')
                seconds = info.group('seconds')
                state = WANT_FILENAME
            else:
                print(f'Failed to parse line {lino}: {line}')
        elif state == WANT_FILENAME:
            songs.append(Song(title, seconds, line))
            title = seconds = None
            state = WANT_INFO
    return songs
