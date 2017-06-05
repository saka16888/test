class TopologyObject(object):
    '''TopologyObject Base class

    '''
    def __init__(self, name, alias = None):
        '''built in class __init__

        Instanciates the base topology object.

        Arguments
        ---------
            name (str): name of the topology object
            alias (str): alias of the topology object, default to name

        Example
        -------
            >>> obja = TopologyObject(name = 'obja')
            >>> objb = TopologyObject(name = 'objb', alias = 'alias_objb')

        '''
        self.name = name
        self.alias = alias or name
