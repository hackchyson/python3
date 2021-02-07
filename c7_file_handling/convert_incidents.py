#!/usr/bin/env python3
# Copyright (c) @ 2021-02

import datetime
import gzip
import optparse
import os
import pickle
import re
# This module performs conversions between Python values and C structs represented as Python bytes objects.
import struct
import sys
import textwrap
import xml.dom.minidom
import xml.etree.ElementTree
import xml.parsers.expat
import xml.sax
import xml.sax.saxutils

USE_RESTRICTIVE_P_FORMAT = False
USE_LONG_WINDED_IMPORT_FUNCTION = False

# Any file that is compressed using gzip compression begins with a particular magic number.
# A magic number is a sequence of one or more bytes at the beginning of a file that is used to indicate the file’s type.
GZIP_MAGIC = b'\x1f\x8B'

# Manually binary
FORMAT_VERSION = b'\x00\x01'
MAGIC = b'AIB\x00'
# little endian; unsigned int; double; int; _Bool
NumbersStruct = struct.Struct('<Idi?')

NARRATIVE_END = '.NARRATIVE_END.'
NARRATIVE_START = '.NARRATIVE_START.'


class IncidentError(Exception):
    pass


class Incident:

    def __init__(self, report_id, date, airport, aircraft_id,
                 aircraft_type, pilot_percent_hours_on_type,
                 pilot_total_hours, midair, narrative=""):
        """
        >>> kwargs = dict(report_id="2007061289X")
        >>> kwargs["date"] = datetime.date(2007, 6, 12)
        >>> kwargs["airport"] = "Los Angeles"
        >>> kwargs["aircraft_id"] = "8184XK"
        >>> kwargs["aircraft_type"] = "CVS91"
        >>> kwargs["pilot_percent_hours_on_type"] = 17.5
        >>> kwargs["pilot_total_hours"] = 1258
        >>> kwargs["midair"] = False
        >>> incident = Incident(**kwargs)
        >>> incident.report_id, incident.date, incident.airport
        ('2007061289X', datetime.date(2007, 6, 12), 'Los Angeles')
        >>> incident.aircraft_id, incident.aircraft_type, incident.midair
        ('8184XK', 'CVS91', False)
        >>> incident.pilot_percent_hours_on_type, incident.pilot_total_hours
        (17.5, 1258)
        >>> incident.approximate_hours_on_type
        220
        >>> incident.narrative = "Two different\\nlines of text"
        >>> str(incident)
        "Incident('2007061289X', datetime.date(2007, 6, 12), 'Los Angeles', '8184XK', 'CVS91', 17.5, 1258, False, '''Two different\\nlines of text''')"
        >>> kwargs["report_id"] = "fail"
        >>> incident = Incident(**kwargs)
        Traceback (most recent call last):
        ...
        AssertionError: invalid report ID
        """
        assert len(report_id) >= 8 and len(report_id.split()) == 1, \
            "invalid report ID"
        self.__report_id = report_id  # read only
        self.date = date
        self.airport = airport
        self.aircraft_id = aircraft_id
        self.aircraft_type = aircraft_type
        self.pilot_percent_hours_on_type = pilot_percent_hours_on_type
        self.pilot_total_hours = pilot_total_hours
        self.midair = midair
        self.narrative = narrative

    @property
    def report_id(self):
        return self.__report_id

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        assert isinstance(date, datetime.date), 'invalid date'
        self.__date = date

    @property
    def pilot_percent_hours_on_type(self):
        return self.__pilot_percent_hours_on_type

    @pilot_percent_hours_on_type.setter
    def pilot_percent_hours_on_type(self, percent):
        assert 0.0 <= percent <= 100.0, 'out of range percentage'
        self.__pilot_percent_hours_on_type = percent

    @property
    def pilot_total_hours(self):
        "The total hours this pilot has flown"
        return self.__pilot_total_hours

    @pilot_total_hours.setter
    def pilot_total_hours(self, hours):
        assert hours > 0, "invalid number of hours"
        self.__pilot_total_hours = hours

    @property
    def approximate_hours_on_type(self):
        return int(self.__pilot_total_hours *
                   (self.__pilot_percent_hours_on_type / 100))

    @property
    def midair(self):
        "Whether the incident involved another aircraft"
        return self.__midair

    @midair.setter
    def midair(self, value):
        assert isinstance(value, bool), "invalid midair value"
        self.__midair = value

    @property
    def airport(self):
        "The incident's airport"
        return self.__airport

    @airport.setter
    def airport(self, airport):
        assert airport and "\n" not in airport, "invalid airport"
        self.__airport = airport

    @property
    def aircraft_id(self):
        "The aircraft ID"
        return self.__aircraft_id

    @aircraft_id.setter
    def aircraft_id(self, aircraft_id):
        assert aircraft_id and "\n" not in aircraft_id, \
            "invalid aircraft ID"
        self.__aircraft_id = aircraft_id

    @property
    def aircraft_type(self):
        "The aircraft type"
        return self.__aircraft_type

    @aircraft_type.setter
    def aircraft_type(self, aircraft_type):
        assert aircraft_type and "\n" not in aircraft_type, \
            "invalid aircraft type"
        self.__aircraft_type = aircraft_type

    @property
    def narrative(self):
        "The incident's narrative"
        return self.__narrative

    @narrative.setter
    def narrative(self, narrative):
        self.__narrative = narrative

    def __repr(self):
        return ("Incident({0.report_id!r}, {0.date!r}, "
                "{0.airport!r}, {0.aircraft_id!r}, "
                "{0.aircraft_type!r}, "
                "{0.pilot_percent_hours_on_type!r}, "
                "{0.pilot_total_hours!r}, {0.midair!r}, "
                "'''{0.narrative}''')".format(self))

    def __str__(self):
        return ("Incident({0.report_id}, {0.date}, "
                "{0.airport}, {0.aircraft_id}, "
                "{0.aircraft_type}, "
                "{0.pilot_percent_hours_on_type}, "
                "{0.pilot_total_hours}, {0.midair}, "
                "'''{0.narrative}''')".format(self))


class IncidentCollection(dict):
    def values(self):
        for report_id in self.keys():
            yield self[report_id]

    def items(self):
        for report_id in self.keys():
            yield report_id, self[report_id]

    def __iter__(self):
        for report_id in sorted(super().keys()):
            yield report_id

    keys = __iter__

    def __reversed__(self):
        for report_id in sorted(super().keys(), reverse=True):
            yield report_id

    def export(self, filename, writer=None, compress=False):
        extension = os.path.splitext(filename)[1].lower()
        if extension == '.aix':  # airport incident xml
            if writer == 'dom':
                return self.export_xml_dom(filename)
            elif writer == 'etree':
                return self.export_xml_etree(filename)
            elif writer == 'manual':
                return self.export_xml_manual(filename)
        elif extension == '.ait':
            return self.export_text(filename)
        elif extension == '.aib':
            return self.export_binary(filename, compress)
        elif extension == '.aip':
            return self.export_pickle(filename, compress)
        elif extension in ('.htm', '.html'):
            return self.export_html(filename)

    def import_(self, filename, reader=None):
        extension = os.path.splitext(filename)[1].lower()
        call = {
            ('.aix', 'dom'): self.import_xml_dom,
            ('.aix', 'etree'): self.import_xml_etree,
            ('.aix', 'sax'): self.import_xml_sax,
            ('.ait', 'manual'): self.import_text_manual,
            ('ait', 'regex'): self.import_text_regex,
            ('.aib', None): self.import_binary,
            ('.aip', None): self.import_pickle
        }
        result = call[extension, reader](filename)
        if not result:
            self.clear()
        return result

    if USE_LONG_WINDED_IMPORT_FUNCTION:
        def import_(self, filename, reader=None):
            pass

    def export_xml_dom(self, filename):
        pass

    def export_xml_etree(self, filename):
        """
        Export incident collection into xml format with Etree.

        Here is an example:
        -----------------------------------------------------------------
        <?xml version="1.0" encoding="UTF-8"?>
        <incidents>
            <incident report_id="20070222008099G" date="2007-02-22"
                aircraft_id="80342" aircraft_type="CE-172-M"
                pilot_percent_hours_on_type="9.09090909091"
                pilot_total_hours="440" midair="0">
                <airport>BOWERMAN</airport>
                <narrative>
                ON A GO-AROUND FROM A NIGHT CROSSWIND LANDING ATTEMPT THE AIRCRAFT HIT
                A RUNWAY EDGE LIGHT DAMAGING ONE PROPELLER.
                </narrative>
            </incident>
            <incident>
            ...
            </incident>
             :
        </incidents>
        -----------------------------------------------------------------
        :param filename:
        :return:
        """
        root = xml.etree.ElementTree.Element('incidents')
        for incident in self.values():
            element = xml.etree.ElementTree.Element(
                'incident',
                report_id=incident.report_id,
                date=incident.date.isoformat(),
                aircraft_id=incident.aircraft_id,
                aircraft_type=incident.aircraft_type,
                # all the attributes must be text
                pilot_percent_hours_on_type=str(incident.pilot_percent_hours_on_type),
                pilot_total_hours=str(incident.pilot_total_hours),
                midair=str(int(incident.midair))
            )
            airport = xml.etree.ElementTree.SubElement(element, 'airport')
            airport.text = incident.airport.strip()
            narrative = xml.etree.ElementTree.SubElement(element, 'narrative')
            narrative.text = incident.narrative.strip()
            root.append(element)
        tree = xml.etree.ElementTree.ElementTree(root)
        try:
            # The encoding name can be only one of the official names
            tree.write(filename, 'UTF-8')
        except EnvironmentError as err:
            print(f'{os.path.basename(sys.argv[0])}: export error: {err}')
            return False
        return True

    def import_xml_etree(self, filename):
        try:
            tree = xml.etree.ElementTree.parse(filename)
        except (EnvironmentError, xml.parsers.expat.ExpatError) as err:
            print(f'{os.path.basename(sys.argv[0])}: import error: {err}')
            return False

        self.clear()
        for element in tree.findall('incident'):
            try:
                data = {}
                for attribute in ('report_id',
                                  'date',
                                  'aircraft_id',
                                  'aircraft_type',
                                  'pilot_percent_hours_on_type',
                                  'pilot_total_hours', 'midair'):
                    data[attribute] = element.get(attribute)
                data['date'] = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
                data['pilot_percent_hours_on_type'] = float(data['pilot_percent_hours_on_type'])
                data['pilot_total_hours'] = int(data['pilot_total_hours'])
                data['midair'] = bool(int(data['midair']))

                data['airport'] = element.find('airport').text.strip()
                narrative = element.find('narrative').text
                data['narrative'] = narrative.strip() if narrative is not None else ''
                incident = Incident(**data)
                self[incident.report_id] = incident
            except (ValueError, LookupError, IncidentError) as err:
                print(f'{os.path.basename(sys.argv[0])}: import error: {err}')
                return False
        return True

    def export_xml_manual(self, filename):
        pass

    def export_text(self, filename):
        wrapper = textwrap.TextWrapper(initial_indent='    ', subsequent_indent='    ')
        fh = None
        try:
            fh = open(filename, 'w', encoding='utf8')
            for incident in self.values():
                narrative = '\n'.join(wrapper.wrap(incident.narrative.strip()))
                fh.write('[{0.report_id}]\n'
                         'date={0.date!s}\n'
                         "aircraft_id={0.aircraft_id}\n"
                         "aircraft_type={0.aircraft_type}\n"
                         "airport={airport}\n"
                         "pilot_percent_hours_on_type="
                         "{0.pilot_percent_hours_on_type}\n"
                         "pilot_total_hours={0.pilot_total_hours}\n"
                         "midair={0.midair}\n"
                         ".NARRATIVE_START.\n{narrative}\n"
                         ".NARRATIVE_END.\n\n"
                         .format(incident,
                                 airport=incident.airport.strip(),
                                 narrative=narrative)
                         )
            return True
        except EnvironmentError as err:
            print(f'{os.path.basename(sys.argv[0])}: export error: {err}')
            return False
        finally:
            if fh is not None:
                fh.close()

    def import_text_manual(self, filename):
        fh = None
        try:
            fh = open(filename, 'r', encoding='utf8')
            self.clear()
            data = {}
            # 1. As a state
            # 2. As a accumulator
            narrative = None
            for lino, line in enumerate(fh, start=1):
                line = line.strip()
                if not line and narrative is None:  # blank line
                    continue
                if narrative is not None:  # narrative
                    if line == NARRATIVE_END:
                        data['narrative'] = textwrap.dedent(narrative).strip()
                        if len(data) != 9:
                            raise IncidentError(f'missing data on line {lino}')
                        incident = Incident(**data)
                        self[incident.report_id] = incident
                        data = {}
                        narrative = None
                    else:
                        narrative += line + '\n'
                elif not data and line[0] == '[' and line[-1] == ']':  # report id
                    data['report_id'] = line[1:-1]
                elif '=' in line:
                    key, value = line.split('=', 1)  # only split once and into two part
                    if key == 'date':
                        data[key] = datetime.datetime.strptime(value, '%Y-%m-%d').date()
                    elif key == 'pilot_percent_hours_on_type':
                        data[key] = float(value)
                    elif key == 'pilot_total_hours':
                        data[key] = int(value)
                    elif key == 'midair':
                        data[key] = bool(int(value))
                    else:
                        data[key] = value
                elif line == NARRATIVE_START:
                    narrative = ''
                else:
                    raise KeyError(f'passing error in line {lino}')
            return True
        except (EnvironmentError, ValueError, KeyError, IncidentError) as err:
            pass
        finally:
            if fh is not None:
                fh.close()

    def export_binary(self, filename, compress=None):
        def pack_string(string):
            data = string.encode('utf8')
            # < little-endian
            # H unsigned short
            # s char[]
            format = f'<H{len(data)}s'
            return struct.pack(format, len(data), data)

        if USE_RESTRICTIVE_P_FORMAT:
            def pack_string(string):
                data = string.encode('utf8')
                format = f'<{len(data)}p'
                return struct.pack(format, data)

        fh = None
        try:
            if compress:
                fh = gzip.open(filename, 'wb')
            else:
                fh = open(filename, 'wb')
            fh.write(MAGIC)
            fh.write(FORMAT_VERSION)

            for incident in self.values():
                data = bytearray()
                data.extend(pack_string(incident.report_id))
                data.extend(pack_string(incident.airport))
                data.extend(pack_string(incident.aircraft_id))
                data.extend(pack_string(incident.aircraft_type))
                data.extend(pack_string(incident.narrative.strip()))
                data.extend(NumbersStruct.pack(
                    # data.toordinal convert data into a integer
                    incident.date.toordinal(),
                    incident.pilot_percent_hours_on_type,
                    incident.pilot_total_hours,
                    incident.midair
                ))
                fh.write(data)
            return True
        except EnvironmentError as err:
            print(f'{os.path.basename(sys.argv[0])}: export error: {err}')
            return False
        finally:
            if fh is not None:
                fh.close()

    def import_binary(self, filename):
        def unpack_string(fh, eof_is_error=True):
            uint16 = struct.Struct('<H')
            length_data = fh.read(uint16.size)
            if not length_data:
                if eof_is_error:
                    raise ValueError('missing or corrupt string size')
                return None
            length = uint16.unpack(length_data)[0]
            if length == 0:
                return ''
            data = fh.read(length)
            if not data or len(data) != length:
                raise ValueError('missing or corrupt string')
            format = f'<{length}s'
            return struct.unpack(format, data)[0].decode('utf8')

        if USE_RESTRICTIVE_P_FORMAT:
            def unpack_string(fh, eof_is_error=True):
                length_data = fh.read(1)
                if not length_data:
                    if eof_is_error:
                        raise ValueError('missing or corrupt string size')
                length = int(struct.unpack('<B', length_data)[0])
                if length == 0:
                    return ''
                data = fh.read(length)
                if not data or len(data) != length:
                    raise ValueError('missing or corrupt string')
                format = f'<{length}p'
                return struct.unpack(format, data)[0].decode('utf8')

        fh = None
        try:
            fh = open(filename, 'rb')
            magic = fh.read(len(GZIP_MAGIC))
            if magic == GZIP_MAGIC:
                fh.close()
                fh = gzip.open(filename, 'rb')
            else:
                fh.seek(0)

            magic = fh.read(len(MAGIC))
            if magic != MAGIC:
                raise ValueError('invalid .aib file format')

            version = fh.read(len(FORMAT_VERSION))
            if version > FORMAT_VERSION:
                raise ValueError('unrecognized .aib file version')
            self.clear()

            while True:
                report_id = unpack_string(fh, False)
                if report_id is None:
                    break
                data = {}
                data['report_id'] = report_id
                for name in ('airport', 'aircraft_id', 'aircraft_type', 'narrative'):
                    data[name] = unpack_string(fh)
                other_data = fh.read(NumbersStruct.size)
                numbers = NumbersStruct.unpack(other_data)
                data['date'] = datetime.date.fromordinal(numbers[0])
                data['pilot_percent_hours_on_type'] = numbers[1]
                data['pilot_total_hours'] = numbers[2]
                data['midair'] = numbers[3]
                incident = Incident(**data)
                self[incident.report_id] = incident
            return True
        except (EnvironmentError, ValueError, IndexError) as err:
            print(f'{os.path.basename(sys.argv[0])}: import error: {err}')
            return False
        finally:
            if fh is not None:
                fh.close()

    def export_pickle(self, filename, compress=None):
        fh = None
        try:
            if compress:
                fh = gzip.open(filename, 'wb')
            else:
                fh = open(filename, 'wb')
            pickle.dump(self, fh, pickle.HIGHEST_PROTOCOL)
            return True
        except (EnvironmentError, pickle.PicklingError) as err:
            print(f'{os.path.basename(sys.argv[0])}: export error: {err}')
            return False
        finally:
            if fh is not None:
                fh.close()

    def import_pickle(self, filename):
        fh = None
        try:
            # Note this trick
            fh = open(filename, 'rb')
            magic = fh.read(len(GZIP_MAGIC))
            if magic == GZIP_MAGIC:
                fh.close()
                fh = gzip.open(filename, 'rb')
            else:
                fh.seek(0)
            self.clear()
            self.update(pickle.load(fh))
            return True
        except (EnvironmentError, pickle.UnpicklingError) as err:
            print(f'{os.path.basename(sys.argv[0])}: import error: {err}')
            return False
        finally:
            if fh is not None:
                fh.close()

    def export_html(self, filename):
        pass


if __name__ == '__main__':
    incident_collections = IncidentCollection()
    incident_collections_back = IncidentCollection()

    kwargs = dict(report_id="2007061289X")
    kwargs["date"] = datetime.date(2007, 6, 12)
    kwargs["airport"] = "Los Angeles"
    kwargs["aircraft_id"] = "8184XK"
    kwargs["aircraft_type"] = "CVS91"
    kwargs["pilot_percent_hours_on_type"] = 17.5
    kwargs["pilot_total_hours"] = 1258
    kwargs["midair"] = False
    incident = Incident(**kwargs)
    incident.narrative = "Two different\\nlines of text"

    incident_collections[incident.report_id] = incident

    EXPORT = False
    if EXPORT:
        incident_collections.export_pickle('ai.aip')  # pickle
        incident_collections.export_binary('ai.aib')  # binary
        incident_collections.export_text('ai.ait')  # text
        incident_collections.export_xml_etree('ai.aix')  # xml
    else:
        # incident_collections_back.import_pickle('ai.aip') # pickle
        # incident_collections_back.import_binary('ai.aib')  # binary
        # incident_collections_back.import_text_manual('ai.ait') # text
        incident_collections_back.import_xml_etree('ai.aix')  # xml
    for i, j in zip(incident_collections_back.values(), incident_collections.values()):
        print(i, j, str(i) == str(j), sep='\n')
