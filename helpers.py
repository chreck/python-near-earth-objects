"""Convert datetimes to and from strings.

NASA's dataset provides timestamps as naive datetimes (corresponding to UTC).

The `cd_to_datetime` function converts a string, formatted as the `cd` field of
NASA's close approach data, into a Python `datetime`

The `datetime_to_str` function converts a Python `datetime` into a string.
Although `datetime`s already have human-readable string representations, those
representations display seconds, but NASA's data (and our datetimes!) don't
provide that level of resolution, so the output format also will not.
"""
import datetime
from typing import Iterable


def cd_to_datetime(calendar_date):
    """Convert a NASA-formatted calendar date/time description into a datetime.

    NASA's format, at least in the `cd` field of close approach data, uses the
    English locale's month names. For example, December 31st, 2020 at noon is:

        2020-Dec-31 12:00

    This will become the Python object `datetime.datetime(2020, 12, 31, 12, 0)`.

    :param calendar_date: A calendar date in YYYY-bb-DD hh:mm format.
    :return: A naive `datetime` corresponding to the given calendar date and time.
    """
    return datetime.datetime.strptime(calendar_date, "%Y-%b-%d %H:%M")


def datetime_to_str(dt):
    """Convert a naive Python datetime into a human-readable string.

    The default string representation of a datetime includes seconds; however,
    our data isn't that precise, so this function only formats the year, month,
    date, hour, and minute values. Additionally, this function provides the date
    in the usual ISO 8601 YYYY-MM-DD format to avoid ambiguities with
    locale-specific month names.

    :param dt: A naive Python datetime.
    :return: That datetime, as a human-readable string without seconds.
    """
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M")


def progress(
    iter: Iterable,
    every=1000,
    fun=lambda e: e,
    start_text="Load",
    end_text="done.",
    suppress=True,
):
    """Generates a progress indicator and calls fun on every element

    Args:
        iter (_type_): Iterable to iterate through
        every (int, optional): Show progress indicator on that index step. Defaults to 1000.
        fun (lambda, optional): Function with entry parameter on every element. Defaults to lambda e:e.
        start_text (str, optional): The text which is printed on start of the progress. Default is "Load".
        end_text (str, optional): The text which is printed on the end of the iteration. Default is "done.".
        suppress (bool, optional): Dont show the indicator at all. Default is True.
    """
    for index, next in enumerate(iter):
        if index == 0 and not suppress:
            print(start_text, end="", flush=True)
        if index % every == 0 and not suppress:
            print(".", end="", flush=True)
        fun(next)
    if not suppress:
        print(end_text, flush=True)
