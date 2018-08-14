'''
Hash-based (dict based) generic classes.
'''

# begin class HashBased()
class HashBased():
    def __init__(self, **kwargs):
        self.setHash( **kwargs )

    def setHash(self, **kwargs):
        self.__hash = kwargs

    def getHash(self): return self.__hash
#end class HashBased()
