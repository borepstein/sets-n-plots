'''
Hash-based (dict based) generic classes.
'''

# begin class HashBased()
class HashBased():
    def __init__(self, **kwargs):
        self.setHash( **kwargs )

    def setHash(self, **kwargs):
        self.__hash = kwargs
        try:
            self.__recalc_func = kwargs['recalculate_func']
        except:
            self.__recalc_func = self.recalculateFunc
        self.recalculate()

    def getHash(self): return self.__hash

    def recalculate(self):
        return( self.__recalc_func( **self.__hash ) )

    def recalculateFunc(self, **kwargs):
        pass

    def setRecalculateFunc(self, f):
        self.__recalc_func = f
#end class HashBased()
