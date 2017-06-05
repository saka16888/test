class AttrDict(dict):
    '''
    Attribute Dictionary class

    The goal of the AttrDict class is to provide a Python dict() build-in var
    type but with the additional capability of being able to access its content
    as object attributes in addition to the standard manner.

    Example:
    --------

        >>> actor = {'first': 'Arnold', 'last': 'Schwarzenegger'}
        >>> actor['first']
        'Arnold'

        >>> import AttrDict
        >>> actor = AttrDict(actor)
        >>> actor.first
        'Arnold'
        >>> actor['first']
        'Arnold'

    Known Limitations:
    ------------------
      Attributes follow the python def/variable rule, and thus dictionary keys
    with the special characters cannot be accessed via attribute (.) manner,
    such as: dot(.) comma(,) brackets() dash/hyphen(-) quotes(''/"") slashes(\/)
    etc.
    '''

    def __init__(self, *args, **kwargs):
        '''
        AttrDict object init

        How this works:
          - All python objects internally store their attributes in a dictionary
            that is named __dict__.
          - There is no requirement that the internal dictionary __dict__ would
            need to be "just a plain dict", so we can assign any subclass of
            dict() to the internal dictionary.
          - In our case we simply assign the AttrDict() instance we are
            instantiating (as we are in __init__).
          - By calling super()'s __init__() method we made sure that it
            (already)  behaves exactly like a dictionary, since that function
             calls all the dictionary instantiation code.

        Special Note:
          - Known to cause memory leak in Python < 2.7.3 and Python3 < 3.2.3
        '''
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           super(AttrDict, self).__repr__())
