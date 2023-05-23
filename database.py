"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""

from datetime import datetime
from filters import AttributeFilter
from models import NearEarthObject, CloseApproach


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos: list[NearEarthObject], approaches: list[CloseApproach]):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos: list[NearEarthObject] = neos
        self._approaches: list[CloseApproach] = approaches

        # extra auxiliary attributes for faster search
        self._neos_by_name = {}
        self._neos_by_designation = {}

        # iterate through all neos
        for neo in self._neos:
            # setup the faster lookup dictionaries
            if neo.name:
                self._neos_by_name[neo.name] = neo
            if neo.designation:
                self._neos_by_designation[neo.designation] = neo

        # iterate through all approaches
        for approach in self._approaches:
            designation = approach._designation
            neo = self.get_neo_by_designation(designation)
            if neo:
                # link approache to neo and neo to approaches
                neo.approaches.append(approach)
                approach.neo = neo

        # needs isinstance test because `test_write` loads the files as tuple, see tests/test_write.py:40
        if isinstance(self._approaches, list):
            # sort all approaches by filter order for faster query
            self._approaches.sort(
                key=lambda a: a.time_str
                + str(a.distance)
                + str(a.velocity)
                + str(a.neo.diameter)
                + str(a.neo.hazardous)
            )

    def get_neo_by_designation(self, designation) -> NearEarthObject:
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        if designation in self._neos_by_designation:
            return self._neos_by_designation[designation]
        return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        if name in self._neos_by_name:
            return self._neos_by_name[name]
        return None

    def query(self, filters: tuple[AttributeFilter] = ()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:
            if all(f(approach) for f in filters if f.value != None):
                yield approach
