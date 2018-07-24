'''
Generic utility routines.
Functions such as utilities, set calculations, etc.
'''

import numpy as np
from hash_based import *

# begin Set(HashBased)
'''
Minimal configuration:
Set(content=[<elem1>, <elem2>, <elem3>, ...])
'''
class Set(HashBased):
    def getContent(self):
        cont = {}

        try:
            cont = self.getHash()["content"]
        except: pass

        return cont

    '''
    Implement in subclass
    '''
    def belongsTo(self, elem):
        return True

    '''
    Implement in subclass.
    '''
    def isSubset(self, set):
        return True
# end Set(HashBased)

# begin FiniteSet(Set):
'''
Minimal configuration:
Set(content=[<elem1>, <elem2>, <elem3>, ...])
'''
class FiniteSet(Set):
    def belongsTo(self, elem):
        try:
            self.getContent().index(elem)
            return True
        except:
            return False

    def isSubset(self, set):
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
Set(content={lower_limit:value, include_lower_limit:Boolean, 
upper_limit:value, include_upper_limit:Boolean})

Example: Set(content={lower_limit:12, incude_lower_limit:True, 
upper_limit:25, include_upper_limit:False})
'''
class NumericalSet(Set):
    def belongsTo(self, elem):
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

    def isSubset(self, set):
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



