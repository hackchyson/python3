# coding=utf8
"""
@project: python3
@file: data_and_time
@author: mike
@time: 2021/2/4
 
@function:
"""
import calendar
import datetime
import time

# current seconds
current_second = time.time()

# current date and time
current_time = datetime.datetime.now()

# current struct time
current_struct_time = time.localtime()
current_struct_time = time.localtime(current_second)

# format from struct time
string_time = time.strftime('%Y-%m-%d %H:%M:%S', current_struct_time)

# struct time from string
struct_time = time.strptime('2021-02-04 11:07:09', '%Y-%m-%d %H:%M:%S')

# seconds from struct time
seconds = time.mktime(current_struct_time)

# moon_datetime_a = datetime.datetime(1969, 7, 20, 20, 17, 40)
# print(moon_datetime_a)
# moon_time = calendar.timegm(moon_datetime_a.utctimetuple())
# print(moon_time)
# moon_datetime_b = datetime.datetime.utcfromtimestamp(moon_time)
# print(moon_datetime_b)
# moon_datetime_a.isoformat()
# moon_datetime_b.isoformat()
# print(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(moon_time)))
#
# print(datetime.datetime.now())
# print(datetime.datetime.utcnow())
# print(time.mktime(time.localtime()))
# print(time.time())
