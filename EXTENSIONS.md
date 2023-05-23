# MyPy

In some parts of the code I used static typing instead of dynamic typing. I made
it backwards compatible so that it can be used with the python version 3.6 as well.

# Helpers

I created a definition `progress` in the `helpers.py` file which makes it possible to display the progress of larger Iterable. The `fun` argument is called on every next element in the Iterable. It displays a start and end text as also the progress indicator which is printed as a simple dot `.` . I implemented this functionality to give the user a hint that the loading of the big data files can take a while.
