#!/usr/bin/env python3
"""
@project: python3
@file: dvds_dbm
@author: mike
@time: 2021/2/25
 
@function:
"""
import datetime
import os
import pickle
import shelve  # for DBM
import sys
import tempfile
import xml.etree.ElementTree
import xml.parsers.expat
import xml.sax.saxutils
import Console
import Util

DISPLAY_LIMIT = 3


def main():
    functions = dict(
        a=add_dvd,
        e=edit_dvd,
        l=list_dvds,
        r=remove_dvd,
        i=import_,
        x=export,
        q=quit_
    )
    filename = os.path.join(os.path.dirname(__file__), 'dvds.dbm')
    db = None
    try:
        db = shelve.open(filename, protocol=pickle.HIGHEST_PROTOCOL)
        action = ''
        while True:
            print(f'\nDVDs ({os.path.basename(filename)})')
            if action != 'l' and 1 <= len(db) < DISPLAY_LIMIT:
                list_dvds(db)
            else:
                print(f'{len(db)} dvd{Util.s(len(db))}')
            print()
            menu = ('(A)dd (E)dit (L)ist (R)emove (I)mport e(X)port (Q)uit'
                    if len(db) else '(A)dd (I)mport (Q)uit')
            valid = frozenset('aelrixq' if len(db) else 'aiq')
            action = Console.get_menu_choice(menu, valid, 'l' if len(db) else 'a', True)
            functions[action](db)
    finally:
        if db is not None:
            db.close()


def add_dvd(db):
    title = Console.get_string('Title', 'title')
    if not title:
        return
    director = Console.get_string('Director', 'director')
    if not director:
        return
    year = Console.get_integer('Year', 'year', minimum=1896, maximum=datetime.date.today().year)
    duration = Console.get_integer('Duration (minutes)', 'minutes', minimum=0, maximum=10 * 48)
    db[title] = (director, year, duration)
    db.sync()


def edit_dvd(db):
    old_title = find_dvd(db, 'edit')
    if old_title is None:
        return
    title = Console.get_string('Title', 'title', old_title)
    if not title:
        return
    director, year, duration = db[old_title]
    director = Console.get_string('Director', 'director', director)
    if not director:
        return
    year = Console.get_integer('Year', 'year', year, 1896, datetime.date.today().year)
    duration = Console.get_integer('Duration (minutes)', 'minutes', duration, minimum=0, maximum=60 * 48)
    db[title] = (director, year, duration)
    if title != old_title:
        del db[old_title]
    db.sync()


def find_dvd(db, message):
    message = '(Start of) title to ' + message
    while True:
        matches = []
        start = Console.get_string(message, 'title')
        if not start:
            return None
        for title in db:
            if title.lower().startswith(start.lower()):
                matches.append(title)
        if len(matches) == 0:
            print('There are no dvds starting with', start)
        elif len(matches) == 1:
            return matches[0]
        elif len(matches) > DISPLAY_LIMIT:
            print(f'Too many dvds start with {start};'
                  'try entering more of the title')
            continue
        else:
            matches = sorted(matches, key=str.lower)
            for i, match in enumerate(matches, start=1):
                print(f'{i}: {match}')
            which = Console.get_integer('Number (or 0 to cancel)', 'number', minimum=1, maximum=len(matches))
            return matches[which - 1] if which != 0 else None


def list_dvds(db):
    start = ''
    if len(db) > DISPLAY_LIMIT:
        start = Console.get_string('List those starting with [Enter=all]', 'start')
    print()
    for title in sorted(db, key=str.lower):
        if not start or title.lower().startswith(start.lower()):
            director, year, duration = db[title]
            print(f'{title} ({year}) {duration} minute{Util.s(duration)}, by {director}')


def remove_dvd(db):
    title = find_dvd(db, 'remove')
    if title is None:
        return
    ans = Console.get_bool(f'Remove {title}?', 'no')
    if ans:
        del db[title]
        db.sync()


def import_(db):
    filename = Console.get_string('Import from', 'filename')
    if not filename:
        return
    try:
        tree = xml.etree.ElementTree.parse(filename)
    except (EnvironmentError, xml.parsers.expat.ExpatError) as err:
        print('ERROR:', err)
        return

    db.clear()
    for element in tree.findall('dvd'):
        try:
            year = int(element.get('year'))
            duration = int(element.get('duration'))
            director = element.get('director')
            title = element.text.strip()
            db[title] = (director, year, duration)
        except ValueError as err:
            print('ERROR:', err)
            return
    print(f'Imported {len(db)} dvd{Util.s(len(db))}')
    db.sync()


def export(db):
    filename = os.path.join(os.path.dirname(__file__), 'dvds.xml')
    with open(filename, 'w', encoding='utf8') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write('<dvds>\n')
        for title in sorted(db, key=str.lower):
            director, year, duration = db[title]
            fh.write(f'<dvd year="{year}" duration="{duration}" director={xml.sax.saxutils.quoteattr(director)}>')
            fh.write(xml.sax.saxutils.escape(title))
            fh.write('</dvd>\n')
        fh.write('</dvds>\n')
        fh.close()
    print(f'exported {len(db)} dvd{Util.s(len(db))} to {filename}')


def quit_(db):
    print(f'Saved {len(db)} dvd{Util.s(len(db))}')
    db.close()
    sys.exit()


if __name__ == '__main__':
    main()
