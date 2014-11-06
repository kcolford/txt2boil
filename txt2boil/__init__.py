# Copyright (C) 2014 Kieran Colford
#
# This file is part of txt2boil.
#
# txt2boil is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# txt2boil is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with txt2boil.  If not, see <http://www.gnu.org/licenses/>.

"""Transform comments into boilerplate.

This package processes contains all the interfaces for generating
boilerplate for a specific language.  Each language is implemented in
the langs module and is exposed via the toplevel function defined here
called ``language``.

Currently only the following are explicitly supported but the
framework allows for more languages to be added easily.

Supported Languages:
- C
- C++
- Java
- Python
- Racket

Further support can be added be simply adding classes to the langs
module.

"""

import os
import collections


def language(fname, is_forced=False):
    """Return the language class that fname is suited for.

    Searches through the module langs for the class that matches up
    with fname.  If is_forced is True then fname will be taken to be
    the extension for a language.

    """

    from . import langs
    for nm in langs.__all__:
        assert hasattr(langs, nm)
        cls = getattr(langs, nm)
        assert hasattr(cls, 'ext')

        for e in cls.ext:
            if is_forced:
                if fname.startswith('.'):
                    fname = fname.strip('.')
                if '.' + fname == e:
                    return cls
            else:
                if fname.endswith(e):
                    return cls
    return langs.Unknown
