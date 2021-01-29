# coding=utf8
"""
@project: python3
@file: generate_usernames
@author: mike
@time: 2021/1/29
 
@function:
"""
import collections
import sys

# constant name is more easy to understand by numbers
ID, FORENAME, MIDDLENAME, SURNAME, DAPARTMENT = range(5)  # unpacking

User = collections.namedtuple('User', 'username forename middlename surname id')


def main():
    if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
        print('usage: {} file1 [file2 [... fileN]]'.format(sys.argv[0]))
        sys.exit()

    usernames = set()  # avoid duplication
    users = {}
    for filename in sys.argv[1:]:
        for line in open(filename):
            line = line.rstrip()
            if line:  # nonempty line
                user = process_line(line, usernames)
                users[(user.surname.lower(), user.forename.lower(), user.id)] = user
    print_users(users)


def process_line(line, usernames):
    fields = line.split(':')
    username = generate_username(fields, usernames)
    user = User(username, fields[FORENAME], fields[MIDDLENAME], fields[SURNAME], fields[ID])
    return user


def generate_username(fields, usernames):
    # by using a slice we get the first letter if there is one, or an empty string otherwise
    # avoiding IndexError if the middle name is empty
    username = (fields[FORENAME][0] + fields[MIDDLENAME][:1] + fields[SURNAME]).replace('-', '').replace("'", '')
    username = original_name = username[:8].lower()
    count = 1
    while username in usernames:
        username = '{}{}'.format(original_name, count)
        count += 1
    usernames.add(username)
    return username


def print_users(users):
    namewidth = 32
    usernamewith = 9

    print('{:<{nw}} {:^6} {:{uw}}'.format('Surname, forename, middlename', 'ID', 'Username', nw=namewidth, uw=usernamewith))
    print('{0:-<{nw}} {0:-<6} {0:-<{uw}}'.format('', nw=namewidth, uw=usernamewith))

    for key in sorted(users):
        user = users[key]
        initial = ''
        if user.middlename:
            initial = ' ' + user.middlename[0]
        name = '{0.surname}, {0.forename}{1}'.format(user, initial)
        print('{0:.<{nw}} ({1.id:4}) {1.username:{uw}}'.format(name, user, nw=namewidth, uw=usernamewith))


if __name__ == '__main__':
    main()
