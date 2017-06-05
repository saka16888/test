import weakref
class Weakreflist(list):

    def __init__(self, items=()):
        super(Weakreflist, self).__init__([weakref.ref(i) for i in items])

    def __contains__(self, item):
        return super(Weakreflist, self).__contains__(weakref.ref(item))

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [i() for i in super(Weakreflist,self).__getitem(index)]
        else:
            return super(Weakreflist, self).__getitem__(index)()

    def __setitem__(self, index, item):
        if isinstance(index, slice):
            return super(Weakreflist, self).__setitem__(index, [weakref.ref(i) for i in item])
        else:
            return super(Weakreflist, self).__setitem(index, weakref(item))

    def __iter__(self):
        for i in super(Weakreflist,self).__iter__():
            yield i()

    def __eq__(self, other):
        return self[:] == other

    def __reversed__(self):
        return self[::-1]

    def __iadd__(self, item):
        return super(Weakreflist, self).__iadd__([weakref.ref(i) for i in item])

    def append(self, item):
        return super(Weakreflist, self).append(weakref.ref(item))

    def extend(self, items):
        return super(Weakreflist, self).extend([weakref.ref(i) for i in items])
