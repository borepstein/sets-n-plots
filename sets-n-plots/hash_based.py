'''
Hash-based (dict based) generic classes.
'''

# begin class HashBased()
class HashBased():
    def __init__(self, **kwargs):
        self.__hash = kwargs

    def setHash(self, **kwargs):
        self.__hash = kwargs
        self.recalculate()

    def getHash(self): return self.__hash

    '''
    Implement in subclasses to recalculate parameters dependent
    upon the hash.
    '''
    def recalculate(self):
        pass
#end class HashBased()
