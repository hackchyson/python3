#!/usr/bin/env python3
"""
@project: python3
@file: dvds_sql
@author: mike
@time: 2021/2/25
 
@function:
"""
import os
import sqlite3
import Util
import sys
import Console
import datetime
import xml
import xml.sax.saxutils
import xml.etree.ElementTree
import xml.parsers.expat

DISPLAY_LIMIT = 3


def connect(filename):
    create = not os.path.exists(filename)
    db = sqlite3.connect(filename)
    if create:
        cursor = db.cursor()
        cursor.execute(
            'CREATE TABLE directors ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, '
            'name TEXT UNIQUE NOT NULL)'
        )
        cursor.execute(
            'CREATE TABLE dvds ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, '
            'title TEXT NOT NULL, '
            'year INTEGER NOT NULL, '
            'duration INTEGER NOT NULL, '
            'director_id INTEGER NOT NULL, '
            'FOREIGN KEY (director_id) REFERENCES directors)'
        )
        db.commit()
    return db


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
    filename = os.path.join(os.path.dirname(__file__), 'dvds.sdb')
    db = None
    try:
        db = connect(filename)
        action = ''
        while True:
            count = dvd_count(db)
            print(f'\nDVDs ({os.path.basename(filename)})')
            if action != 'l' and 1 <= count < DISPLAY_LIMIT:
                list_dvds(db)
            else:
                print(f'{count} dvd{Util.s(count)}')
            print()
            menu = ('(A)dd (E)dit (L)ist (R)emove (I)mport e(X)port (Q)uit'
                    if count else '(A)dd (I)mport (Q)uit')
            valid = frozenset('aelrixq' if count else 'aiq')
            action = Console.get_menu_choice(menu, valid, 'l' if count else 'a', True)
            functions[action](db)
    finally:
        if db is not None:
            db.close()


def add_dvd(db):
    # Prepare data
    title = Console.get_string('Title', 'title')
    if not title:
        return
    director = Console.get_string('Director', 'director')
    if not director:
        return
    year = Console.get_integer('Year', 'year', minimum=1896, maximum=datetime.date.today().year)
    duration = Console.get_integer('Duration (minutes)', 'minutes', minimum=0, maximum=60 * 48)
    director_id = get_and_set_director(db, director)

    # Add data into database
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO dvds '
        '(title,year,duration,director_id) '
        'VALUES (?, ?, ?, ?)',
        (title, year, duration, director_id)
    )
    db.commit()


def get_and_set_director(db, director):
    # Query
    director_id = get_director_id(db, director)
    if director_id is not None:
        return director_id

    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO directors (name) VALUES (?)',
        (director,)
    )
    db.commit()
    return get_director_id(db, director)


def get_director_id(db, director):
    cursor = db.cursor()
    cursor.execute(
        'SELECT id FROM directors WHERE name=?',
        (director,)
    )
    fields = cursor.fetchone()
    return fields[0] if fields is not None else None


def edit_dvd(db):
    title, identity = find_dvd(db, "edit")
    if title is None:
        return
    title = Console.get_string("Title", "title", title)
    if not title:
        return

    # Get the old data
    cursor = db.cursor()
    cursor.execute("SELECT dvds.year, dvds.duration, directors.name "
                   "FROM dvds, directors "
                   "WHERE dvds.director_id = directors.id AND "
                   "dvds.id=:id", dict(id=identity))
    year, duration, director = cursor.fetchone()

    # Get the new data
    director = Console.get_string("Director", "director", director)
    if not director:
        return
    year = Console.get_integer("Year", "year", year, 1896,
                               datetime.date.today().year)
    duration = Console.get_integer("Duration (minutes)", "minutes",
                                   duration, minimum=0, maximum=60 * 48)

    # Edit
    director_id = get_and_set_director(db, director)
    cursor.execute("UPDATE dvds SET title=:title, year=:year, "
                   "duration=:duration, director_id=:director_id "
                   "WHERE id=:identity", locals())
    db.commit()


def list_dvds(db):
    cursor = db.cursor()
    sql = ("SELECT dvds.title, dvds.year, dvds.duration, "
           "directors.name FROM dvds, directors "
           "WHERE dvds.director_id = directors.id")
    start = None
    if dvd_count(db) > DISPLAY_LIMIT:
        start = Console.get_string("List those starting with "
                                   "[Enter=all]", "start")
        sql += " AND dvds.title LIKE ?"
    sql += " ORDER BY dvds.title"
    print()
    if start is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, (start + "%",))
    for record in cursor:
        print("{0[0]} ({0[1]}) {0[2]} minutes, by {0[3]}".format(
            record))


def list_directors(db):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM directors")
    count = cursor.fetchone()[0]
    sql = "SELECT name FROM directors"
    start = None
    if count > DISPLAY_LIMIT:
        start = Console.get_string("List those starting with "
                                   "[Enter=all]", "start")
        sql += " WHERE name LIKE ?"
    sql += " ORDER BY name"
    print()
    if start is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, (start + "%",))
    for fields in cursor:
        print(fields[0])


def remove_dvd(db):
    title, identity = find_dvd(db, "remove")
    if title is None:
        return
    ans = Console.get_bool("Remove {0}?".format(title), "no")
    if ans:
        cursor = db.cursor()
        cursor.execute("DELETE FROM dvds WHERE id=?", (identity,))
        db.commit()


def import_(db):
    filename = Console.get_string("Import from", "filename")
    if not filename:
        return
    try:
        tree = xml.etree.ElementTree.parse(filename)
    except (EnvironmentError,
            xml.parsers.expat.ExpatError) as err:
        print("ERROR:", err)
        return

    cursor = db.cursor()
    cursor.execute("DELETE FROM directors")
    cursor.execute("DELETE FROM dvds")

    for element in tree.findall("dvd"):
        get_and_set_director(db, element.get("director"))
    for element in tree.findall("dvd"):
        try:
            year = int(element.get("year"))
            duration = int(element.get("duration"))
            title = element.text.strip()
            director_id = get_director_id(db, element.get("director"))
            cursor.execute("INSERT INTO dvds "
                           "(title, year, duration, director_id) "
                           "VALUES (?, ?, ?, ?)",
                           (title, year, duration, director_id))
        except ValueError as err:
            db.rollback()
            print("ERROR:", err)
            break
    else:
        db.commit()
    count = dvd_count(db)
    print("Imported {0} dvd{1}".format(count, Util.s(count)))


def dvd_count(db):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM dvds")
    return cursor.fetchone()[0]


def export(db):
    TITLE, YEAR, DURATION, DIRECTOR = range(4)
    filename = os.path.join(tempfile.gettempdir(), "dvds.xml")
    cursor = db.cursor()
    cursor.execute("SELECT dvds.title, dvds.year, dvds.duration, "
                   "directors.name FROM dvds, directors "
                   "WHERE dvds.director_id = directors.id "
                   "ORDER BY dvds.title ")
    try:
        with open(filename, "w", encoding="utf8") as fh:
            fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            fh.write("<dvds>\n")
            for record in cursor:
                fh.write('<dvd year="{0}" duration="{1}" '
                         'director={2}>'.format(
                    record[YEAR], record[DURATION],
                    xml.sax.saxutils.quoteattr(record[DIRECTOR])))
                fh.write(xml.sax.saxutils.escape(record[TITLE]))
                fh.write("</dvd>\n")
            fh.write("</dvds>\n")
    except EnvironmentError as err:
        print(err)
    count = dvd_count(db)
    print("exported {0} dvd{1} to {2}".format(
        count, Util.s(count), filename))


def quit_(db):
    if db is not None:
        count = dvd_count(db)
        db.commit()
        db.close()
        print("Saved {0} dvd{1}".format(count, Util.s(count)))
    sys.exit()


def find_dvd(db, message):
    message = "(Start of) title to " + message
    cursor = db.cursor()
    while True:
        start = Console.get_string(message, "title")
        if not start:
            return (None, None)
        cursor.execute("SELECT title, id FROM dvds "
                       "WHERE title LIKE ? ORDER BY title",
                       (start + "%",))
        records = cursor.fetchall()
        if len(records) == 0:
            print("There are no dvds starting with", start)
            continue
        elif len(records) == 1:
            return records[0]
        elif len(records) > DISPLAY_LIMIT:
            print("Too many dvds ({0}) start with {1}; try entering "
                  "more of the title".format(len(records), start))
            continue
        else:
            for i, record in enumerate(records):
                print("{0}: {1}".format(i + 1, record[0]))
            which = Console.get_integer("Number (or 0 to cancel)",
                                        "number", minimum=1, maximum=len(records))
            return records[which - 1] if which != 0 else (None, None)


if __name__ == '__main__':
    main()
