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

"""A generator class that will identify command comments.

It then parses them, and adds their content to the code.

"""

from .extractor import Extractor
import re


class _Gen(Extractor):

    def collectTriggers(self, rgx, code):
        """Return a dictionary of triggers and their corresponding matches
        from the code.

        """

        return {m.group(0): m for m in re.finditer(rgx, code)}

    def genOutputs(self, code, match):
        """Return a list out template outputs based on the triggers found in
        the code and the template they create.

        """

        out = sorted((k, match.output(m)) for (k, m) in
                     self.collectTriggers(match.match, code).items())
        out = list(map(lambda a: a[1], out))
        return out

    def gen(self, text, start=0):
        """Return the source code in text, filled with autogenerated code
        starting at start.

        """

        for cc in self.chunkComment(text, start):
            c = self.extractChunkContent(cc)
            cc = ''.join(cc)
            m = self.matchComment(c)
            idx = text.index(cc, start)
            e = idx + len(cc)
            if m:
                assert text[idx:e] == cc

                try:
                    end = text.index('\n\n', e - 1) + 1
                except ValueError:
                    end = len(text)
                text = text[:e] + text[end:]
                new = self.genOutputs(self.code(text), m)
                new = ''.join(new)
                text = text[:e] + new + text[e:]

                return self.gen(text, e + len(new))
        return text


class Gen(_Gen):

    """The generator class for boilerplate code.

    """

    def matchComment(self, comm):
        """Return a HookedRegex according to what comments this generator
        looks at.

        Overload this method to match different comments.  A standard
        overload should make use of the coop.nonNoneCMI function
        decorator so that multiple different comments can be processes
        with one class.

        For example, if one were to write a Foo generator then it
        would look something like this:

        from txt2boil.core import *
        import txt2boil.cmi

        class Foo(Gen):

            @cmi.nonNoneCMI(lambda: Foo)
            def matchComment(self, comm):
                return HookedRegex(...)

        Note the way that Foo was wrapped in a lambda before being
        passed to the cmi decorator.  If this was not done then it
        would cause a syntax error because Foo is not defined at this
        point.

        """

        pass


__all__ = ['Gen']
