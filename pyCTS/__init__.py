#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Matteo Romanello, matteo.romanello@gmail.com

from __future__ import print_function


class BadCtsUrnSyntax(Exception):
    """Exception raised when attempting to create a URN with invalid syntax."""
    pass


class InvalidDepthLevel(Exception):
    """
    >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173")
    >>> urn.get_passage(3)
    Traceback (most recent call last):
     ...
    pyCTS.InvalidDepthLevel: Max depth: 2; limit = 3
    """
    pass


class CTS_URN(object):
    """
    Object representing a CTS URN as defined in the CTS protocol.

    Examples:

    # create a work-level URN
    >>> urn_string = "urn:cts:greekLit:tlg0003.tlg001"
    >>> urn = CTS_URN(urn_string)

    >>> urn_string = u"urn:cts:greekLit:tlg0008.tlg001:173f#δημήτριος"
    >>> print(CTS_URN(urn_string))
    urn:cts:greekLit:tlg0008.tlg001:173f#δημήτριος

    # attempt to create an invalid URN
    >>> bogus_string = "abc:def"
    >>> bogus_urn = CTS_URN(bogus_string)
    Traceback (most recent call last):
     ...
    pyCTS.BadCtsUrnSyntax: Bad syntax for pseudo-URN: abc:def
    """
    def __init__(self, inp_string):
        self._as_string = inp_string
        self._cts_namespace = None
        self._passage_component = None
        self._work_component = None
        self._version = None
        self._work = None
        self._textgroup = None
        self._passage_node = None
        self._range_begin = None
        self._range_end = None
        self._subref1 = None
        self._subref_idx1 = None
        self._subref2 = None
        self._subref_idx2 = None

        try:
            self._initialize_URN(inp_string)
        except Exception as e:
            raise e

    @property
    def passage_component(self):
        """Returns the passage component of a CTS URN.

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173")
        >>> urn.passage_component
        '1.173'

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001")
        >>> assert urn.passage_component is None
        """
        return self._passage_component

    @property
    def work_component(self):
        """Returns the entire work component.

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001.perseus-grc1")
        >>> urn.work_component
        'tlg0003.tlg001.perseus-grc1'
        """
        return self._work_component

    @property
    def cts_namespace(self):
        """Returns the namespace component of a CTS URN.

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173")
        >>> urn.cts_namespace
        'greekLit'
        """
        return self._cts_namespace

    @property
    def version(self):
        """Returns the version part of a CTS URN.

        # URN without version component
        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001")
        >>> assert urn.version is None

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001.perseus-grc1")
        >>> urn.version
        'perseus-grc1'
        """
        return self._version

    @property
    def work(self):
        """Returns only the work identifier (not the work component!).

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173")
        >>> urn.work
        'tlg001'
        """
        return self._work

    @property
    def textgroup(self):
        """
        Returns the textgroup (roughly 'author') component of a CTS URN.

        :return: the textgroup component of the URN
        :rtype: str

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173")
        >>> urn.textgroup
        'tlg0003'
        """
        return self._textgroup

    def is_range(self):
        """Checks whether the URN's passage is a range (e.g. "1-10").

        :rtype: boolean

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173-1.180")
        >>> urn.is_range()
        True
        """
        return self._range_begin is not None

    def _initialize_URN(self, urn_string):
        """Private method for initializing a URN."""
        components = urn_string.split(":")
        try:
            assert components[0] == "urn" and components[1] == "cts"
        except AssertionError:
            raise BadCtsUrnSyntax(
                "Bad syntax for pseudo-URN: {}".format(urn_string)
            )

        size = len(components)

        # split the URN into its main components
        if(size == 5):
            self._passage_component = components[4]
            if(components[3]):
                self._work_component = components[3]
                self._cts_namespace = components[2]
            else:
                raise BadCtsUrnSyntax(
                    "Bad URN syntax: no textgroup in {}".format(urn_string)
                )
        elif(size == 4):
            if(components[3]):
                self._work_component = components[3]
                self._cts_namespace = components[2]
            else:
                raise BadCtsUrnSyntax(
                    "Bad URN syntax: no textgroup in {}".format(urn_string)
                )
        else:
            raise BadCtsUrnSyntax(
                "Method initializeURN: bad syntax: in {}".format(urn_string)
            )

        # split the work_component into its sub-parts
        work_components = self.work_component.split('.')
        size = len(work_components)
        if(size == 3):
            self._version = work_components[2]
            self._work = work_components[1]
            self._textgroup = work_components[0]
        elif(size == 2):
            self._work = work_components[1]
            self._textgroup = work_components[0]
        else:
            self._textgroup = work_components[0]
        #
        if(self.passage_component):
            range_components = self.passage_component.split('-')
            size = len(range_components)
            if(size == 2):
                self._initialize_range(
                    range_components[0],
                    range_components[1]
                )
            elif(size == 1):
                self._initialize_point(range_components[0])
        return

    def _index_subref(self, istring):
        """docstring for _index_subref"""
        import re
        regexp = re.compile(r'(.*)\[(.+)\]')
        match = regexp.match(istring)
        if(match is not None):
            return match.groups()
        else:
            return (istring,)

    def _parse_scope(self, istring):
        """docstring for _parse_scope"""
        result = None
        split_sub = istring.split('#')
        size = len(split_sub)
        if(size == 1):
            return (split_sub[0],)
        elif(size == 2):
            return (split_sub[0],) + self._index_subref(split_sub[1])
        return result

    def _initialize_range(self, str1, str2):
        """docstring for initialize_range"""
        temp = self._parse_scope(str1)
        if(len(temp) == 1):
            self._range_begin = temp[0]
        elif(len(temp) == 2):
            self._range_begin = temp[0]
            self._subref1 = temp[1]
        elif(len(temp) == 3):
            self._range_begin = temp[0]
            self._subref1 = temp[1]
            self._subref_idx1 = int(temp[2])
        else:
            raise BadCtsUrnSyntax("Bad URN syntax in ".format(temp))

        temp = self._parse_scope(str2)
        if(len(temp) == 1):
            self._range_end = temp[0]
        elif(len(temp) == 2):
            self._range_end = temp[0]
            self._subref2 = temp[1]
        elif(len(temp) == 3):
            self._range_end = temp[0]
            self._subref2 = temp[1]
            self._subref_idx2 = int(temp[2])
        else:
            raise BadCtsUrnSyntax("Bad URN syntax in ".format(temp))

    def _initialize_point(self, point):
        """
        docstring for initialize_range
        """
        temp = self._parse_scope(point)
        if(len(temp) == 1):
            self._passage_node = temp[0]
        elif(len(temp) == 2):
            self._passage_node = temp[0]
            self._subref1 = temp[1]
        elif(len(temp) == 3):
            self._passage_node = temp[0]
            self._subref1 = temp[1]
            self._subref_idx1 = int(temp[2])
        else:
            raise BadCtsUrnSyntax("Bad URN syntax in {}".format(temp))

    def get_urn_without_passage(self):
        """Returns the URN without its passage component.

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173")
        >>> urn.get_urn_without_passage()
        'urn:cts:greekLit:tlg0003.tlg001'
        """
        return u"urn:cts:{}:{}".format(
            self._cts_namespace,
            self._work_component
        )

    def get_passage(self, limit):
        """Returns the passage component up to a certain depth level.

        :param limit: the depth level to stop at
        :type limit: int

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173")
        >>> urn.get_passage(1)
        '1'
        >>> urn.get_passage(2)
        '1.173'
        >>> urn.get_passage(3)
        Traceback (most recent call last):
         ...
        pyCTS.InvalidDepthLevel: Max depth: 2; limit = 3
        """
        if self.is_range():
            psg_vals = self._range_begin.split('.')
        else:
            psg_vals = self._passage_component.split('.')

        passage = [psg_vals[0]]
        count = 1
        if(limit > len(psg_vals)):
            raise InvalidDepthLevel(
                'Max depth: {}; limit = {}'.format(len(psg_vals), limit)
            )
        else:
            while(count < limit and count <= self.get_citation_depth()):
                passage.append(psg_vals[count])
                count += 1
            return ".".join(passage)

    def get_citation_depth(self):
        """
        Returns the max depth level of the URN.

        This method is often used in conjunction with `trim_passage` or
        `get_passage`.

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173")
        >>> urn.get_citation_depth()
        2
        """
        if(self.is_range()):
            return len(self._range_begin.split('.'))
        else:
            return len(self._passage_component.split('.'))

    def trim_passage(self, limit):
        """Returns the URN's up to a certain depth level.

        >>> urn = CTS_URN("urn:cts:greekLit:tlg0003.tlg001:1.173")
        >>> urn.trim_passage(1)
        'urn:cts:greekLit:tlg0003.tlg001:1'

        >>> urn.trim_passage(2)
        'urn:cts:greekLit:tlg0003.tlg001:1.173'

        >>> urn.trim_passage(3)
        Traceback (most recent call last):
         ...
        pyCTS.InvalidDepthLevel
        """
        if limit > self.get_citation_depth():
            raise InvalidDepthLevel
        else:
            return "{}:{}".format(
                self.get_urn_without_passage(),
                self.get_passage(limit)
            )

    def __unicode__(self):
        return self._as_string

    def __str__(self):
        return self._as_string

    def __repr__(self):
        return self._as_string


if __name__ == "__main__":
    import doctest
    doctest.testmod()
