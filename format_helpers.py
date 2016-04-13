class FormatIterator(object):
    """
    A simple class to return an iterator for the `__format__`
    magic function.
    """
    def __init__(self, list):
        self.iteration = self.iterator(list)

    def iterator(self, array):
        for i in array:
            yield i

    def __format__(self, format):
        return self.iteration.next()


class FormatMultiplier(object):
    """
    A simple class to return multiple indecies for the `__format__`
    magic function.
    """
    def __init__(self, item):
        self.item = item

    def __format__(self, num):
        if num == '':
            return self.item
        return self.item * int(num)
