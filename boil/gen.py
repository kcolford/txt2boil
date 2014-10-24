"""A generator class that will identify command comments.

It then parses them, and adds their content to the code.

"""

from extractor import Extractor
import re


class Gen(Extractor):
    """The generator class for boilerplate code.

    """

    def matchComment(self, comm):
        """Return a HookedRegex according to what comments this generator
        looks at.

        Overload this method to match different comments.

        """
        
        pass

    def collectTriggers(self, rgx, code):
        """Return a dictionary of triggers and their corresponding matches
        from the code.

        """

        return { m.group(0):m for m in re.finditer(rgx, code) }

    def genOutputs(self, code, match):
        """Return a list out template outputs based on the triggers found in
        the code and the template they create.

        """
        
        out = sorted((k, match.output(m)) for (k, m) in 
                     self.collectTriggers(match.group(1), code).items())
        out = list(map(lambda a: a[1], out))
        return out

    def gen(self, text, start=0):
        """Return the source code in text, filled with autogenerated code
        starting at start.

        """

        assert type(self) is not Gen
        # if type(self) is Gen:
        #     return text
        
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

