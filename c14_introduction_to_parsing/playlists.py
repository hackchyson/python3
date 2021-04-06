import re

import ReadKeyValue
import ReadM3U


def songs_from_dictionary(dictionary):
    NAME_NUMBER_RE = re.compile(r"^(?P<name>\D+)(?P<number>\d+)$")
    songs = []
    for file in (name for name in sorted(dictionary.keys()) if name.startswith("file")):
        name_number = NAME_NUMBER_RE.match(file)
        if name_number:
            name = name_number.group('name')
            number = name_number.group('number')
            filename = dictionary[file]
            title = dictionary.get(f'title{number}', filename)
            seconds = dictionary.get(f'length{number}', -1)
            songs.append(ReadM3U.Song(title, seconds, filename))
    return songs
