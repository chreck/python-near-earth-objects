"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
import datetime


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation: str = info["pdes"]
        self.name: str = None
        if info["name"]:
            self.name: str = info["name"]
        self.diameter = float("nan")
        if info["diameter"]:
            self.diameter = float(info["diameter"])
        if info["pha"] == "Y":
            self.hazardous = True
        elif info["pha"] == "N":
            self.hazardous = False
        else:
            self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches: list[CloseApproach] = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if not self.designation and not self.name:
            return f"(Unknown)"
        if self.designation and not self.name:
            return f"{self.designation}"
        if not self.designation and self.name:
            return f"({self.name})"
        if self.designation and self.name:
            return f"{self.designation} ({self.name})"

    def __str__(self):
        """Return `str(self)`."""
        hazardous: str = "is not"
        if self.hazardous:
            hazardous: str = "is"
        return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and {hazardous} potenzially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
            f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
        )

    def serialize(self):
        """Serialize the NearEarthObject object for writing

        Returns:
            dict: The dictionary for serialization
        """
        return {
            "designation": self.designation,
            "name": self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = str(info["des"])
        self.time: datetime.datetime = cd_to_datetime(info["cd"])
        self.distance = float("nan")
        if info["dist"]:
            self.distance = float(info["dist"])
        self.velocity = float("nan")
        if info["v_rel"]:
            self.velocity = float(info["v_rel"])

        self.neo: NearEarthObject = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        name = self._designation
        if self.neo:
            name = self.neo.fullname
        return f"At {self.time_str}, '{name}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (
            f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
        )

    def serialize(self):
        """Serialize the CloseApproach object for writing

        Returns:
            dict: The dictionary for serialization
        """
        return {
            "datetime_utc": self.time_str,
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }
