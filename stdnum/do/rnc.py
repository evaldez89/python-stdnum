# rnc.py - functions for handling Dominican Republic tax registration
#
# Copyright (C) 2015-2017 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""RNC (Registro Nacional del Contribuyente, Dominican Republic tax number).

The RNC is the Dominican Republic taxpayer registration number for
institutions. The number consists of 9 digits.

>>> validate('1-01-85004-3')
'101850043'
>>> validate('1018A0043')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('101850042')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('131246796')
'1-31-24679-6'
"""

from stdnum.exceptions import *
from stdnum.util import clean


# list of RNCs that do not match the checksum but are nonetheless valid
whitelist = set('''
101581601 101582245 101595422 101595785 10233317 131188691 401007374
501341601 501378067 501620371 501651319 501651823 501651845 501651926
501656006 501658167 501670785 501676936 501680158 504654542 504680029
504681442 505038691
'''.split())


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def calc_check_digit(number):
    """Calculate the check digit."""
    weights = (7, 9, 8, 6, 5, 4, 3, 2)
    check = sum(w * int(n) for w, n in zip(weights, number)) % 11
    return str((10 - check) % 9 + 1)


def validate(number):
    """Check if the number provided is a valid RNC."""
    number = compact(number)
    if not number.isdigit():
        raise InvalidFormat()
    if number in whitelist:
        return number
    if len(number) != 9:
        raise InvalidLength()
    if calc_check_digit(number[:-1]) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number provided is a valid RNC."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return '-'.join((number[:1], number[1:3], number[3:-1], number[-1]))
