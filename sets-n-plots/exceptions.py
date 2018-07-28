'''
Collection of Exception() subclasses for the use in sets-n-graphs
'''

import sys
from hash_based import *

# begin class SNPException(Exception)
'''
General exception class for SNP (Sets-N-Plots)
'''
class SNPException(Exception, HashBased):
    def __init__(self, **kwargs):
        self.__hash = kwargs

        try:
            msg = self.__hash['message']
        except:
            msg = ''
            self.__hash['message'] = msg
            
        Hash.__init__(self, **self.__hash)
        Exception.__init__(self, msg)

    def getMessage(self): return self.getHash()['message']
#end class SNPException(Exception)

#begin FiniteSetDuplicateValueException(SNPException)
class FiniteSetDuplicateValueException(SNPException):
    pass
#begin FiniteSetDuplicateValueException(SNPException)

# begin NumericalSetFormatException(SNPException)
class NumericalSetFormatException(SNPException):
    pass
# end NumericalSetFormatException(SNPException)



