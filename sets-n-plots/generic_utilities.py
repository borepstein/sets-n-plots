'''
Generic utility routines.
Functions such as utilities, set calculations, etc.
'''

import math
import numpy as np
import scipy.stats as sc_stats
from hash_based import *
from exceptions import *

# begin Set(HashBased)
'''
Minimal configuration:
Set(content=[<elem1>, <elem2>, <elem3>, ...])
'''
class Set(HashBased):
    def __init__(self, **kwargs):
        self.__hash = kwargs
        self.__content = {}
        self.__belongs_to_func = self.belongsToFunc
        self.__is_subset_func = self.isSubsetFunc

        try: self.__content = kwargs['content']
        except: pass

        self.__hash['content'] = self.__content

        try: self.__belongs_to_func = kwargs['belongs_to_func']
        except: pass

        self.__hash['belongs_to_func'] = self.__belongs_to_func

        try: self.__is_subset_func = kwargs['is_subset_func']
        except: pass

        self.__hash['is_subset_func'] = self.__is_subset_func

        HashBased.__init__(self, **self.__hash)
        
    def getContent(self):
        cont = {}

        try:
            cont = self.getHash()["content"]
        except: pass

        return cont

    def belongsTo(self, elem, **kwargs):
        return self.__belongs_to_func(elem, **kwargs)

    '''
    Implement in subclass or pass via 'belongs_to_func'.
    '''
    def belongsToFunc(self, elem, **kwargs):
        pass
    
    def isSubset(self, set, **kwargs):
        return self.__is_subset_func(set, **kwargs)

    '''
    Implement in subclass or pass via 'is_subset_func'.
    '''
    def isSubsetFunc(self, set, **kwargs):
        pass
    
# end Set(HashBased)

# begin FiniteSet(Set):
'''
Minimal configuration:
Set(content=[<elem1>, <elem2>, <elem3>, ...])
'''
class FiniteSet(Set):
    def __init__(self, **kwargs):
        cont = []
        
        try: cont = kwargs['content']
        except: pass

        if len( cont ) != len( set(cont) ):
            raise FiniteSetDuplicateValueException(message=\
                                                   "FiniteSet: " + self.__str__() + \
                                                   " : non-unique elements.")
        
        self.__hash = kwargs
        self.__hash['content'] = cont
        self.__hash['belongs_to_func'] = self.belongsToFunc
        self.__hash['is_subset_func'] = self.isSubsetFunc
        Set.__init__(self, **self.__hash)
        
    def belongsToFunc(self, elem, **kwargs):
        try:
            self.getContent().index(elem)
            return True
        except:
            return False

    def isSubsetFunc(self, set, **kwargs):
        try:
            for elem in set.getContent():
                if not self.belongsTo(elem): return False
            return True
        except:
            return False    
# end  FiniteSet(Set):

# begin NumericalSet(Set)
'''
Minimal configuration:
NumericalSet(content={lower_limit:value, include_lower_limit:Boolean, 
upper_limit:value, include_upper_limit:Boolean})

Example: Set(content={lower_limit:12, incude_lower_limit:True, 
upper_limit:25, include_upper_limit:False})
'''
class NumericalSet(Set):
    def __init__(self, **kwargs):
        self.__hash = kwargs
        self.__belongs_to_func = self.belongsToFunc
        self.__hash['belongs_to_func'] = self.__belongs_to_func
        self.__is_subset_func = self.isSubsetFunc
        self.__hash['is_subset_func'] = self.__is_subset_func
        Set.__init__(self, **self.__hash)
        
    def belongsToFunc(self, elem, **kwargs):
        try:
            cont = self.getContent()
            
            if elem < cont["lower_limit"]: return False

            if elem == cont["lower_limit"] and \
               not cont["include_lower_limit"]: return False

            if elem > cont["upper_limit"]: return False
            
            if elem == cont["upper_limit"] and \
               not cont["include_upper_limit"]: return False
            
            return True
        except: return False

    def isSubsetFunc(self, set, **kwargs):
        try:
            cont1 = self.getContent()
            cont2 = set.getContent()

            if cont2["lower_limit"] < cont1["lower_limit"]: return False

            if cont2["lower_limit"] == cont1["lower_limit"] and \
               not cont1["include_lower_limit"] and \
               cont2["include_lower_limit"] : return False

            if cont2["upper_limit"] > cont1["upper_limit"]: return False

            if cont2["upper_limit"] == cont1["upper_limit"] and \
               not cont1["include_upper_limit"] and \
               cont2["include_upper_limit"] : return False
               
            return True
        except: return False
# begin NumericalSet(Set)

# begin NumericalFiniteMultiSet(Set)
'''
Minimal structure: NumericalFiniteMultiSet(content=[<n1>, <n2>, <n3>, ...])
'''
class NumericalFiniteMultiSet(Set):
    def __init__(self, **kwargs):
        self.__hash = kwargs
        self.__hash['belongs_to_func'] = self.belongsToFunc
        self.__hash['is_subset_func'] = self.isSubsetFunc
        Set.__init__(self, **self.__hash)

    def belongsToFunc(self, elem, **kwargs):
        for e in self.getContent():
            if e == elem: return True
        return False

    def isSubsetFunc(self, a_set, **kwargs):
        for e in set( a_set.getContent() ):
            if not self.belongsTo( e ): return False
        return True
    
# end NumericalFiniteMultiSet(Set)

'''
Stand-alone functions.
'''

# begin integral
'''
Integral over a segment for a function f(x)
'''
def integral(**kwargs):
    segment = kwargs['segment']
    function = kwargs['function']
    num_parts = kwargs['num_parts']

    llimit = segment.getContent()['lower_limit']
    ulimit = segment.getContent()['upper_limit']
    step = (ulimit - llimit) / num_parts

    int_sum = 0

    for i in range(0, num_parts):
        int_sum += step * ((function(llimit + i * step) + \
                            function(limit + (i+1) * step)) / 2)

    return int_sum
# end integral

# begin normalPDF(**kwargs)
def normalPDF(**kwargs):
    mean = kwargs['mean']
    stdev = kwargs['stdev']
    x = kwargs['x']

    return (1/math.sqrt(2 * math.pi * (stdev ** 2))) * \
        (math.e ** -((x - mean) ** 2)/(2 * (stdev ** 2)))
# end normalPDF(**kwargs)






