'''
Generic utility routines.
Functions such as utilities, set calculations, etc.
'''

import math
import numpy as np
import scipy.stats as sc_stats
from .hash_based import *
from .exceptions import *

# begin Set(HashBased)
'''
Minimal configuration:
Set(content=<content>)
'''
class Set(HashBased):
    def __init__(self, **kwargs):
        self.__hash = kwargs
        self.__content = {}
        self.__belongs_to_func = self.belongsToFunc
        self.__is_subset_func = self.isSubsetFunc

        try: self.__content = kwargs['content']
        except: raise InputDataFormatException(message='Set: __init__; \'content\' input missing.')

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
        Set.__init__(self, **kwargs)
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
        HashBased.setHash(self, **self.__hash)
        
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

Example: NumericalSet(content={lower_limit:12, incude_lower_limit:True, 
upper_limit:25, include_upper_limit:False})
'''
class NumericalSet(Set):
    def __init__(self, **kwargs):
        hash = kwargs
        Set.__init__(self, **hash)
        self.__belongs_to_func = self.belongsToFunc
        hash['belongs_to_func'] = self.__belongs_to_func
        self.__is_subset_func = self.isSubsetFunc
        hash['is_subset_func'] = self.__is_subset_func
        HashBased.setHash(self, **hash)
        
        
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
                            function(llimit + (i+1) * step)) / 2)

    return int_sum
# end integral

# begin normalPDF(**kwargs)
def normalPDF(**kwargs):
    mean = kwargs['mean']
    stdev = kwargs['stdev']
    x = kwargs['x']
    coeff = 1/math.sqrt(2 * math.pi * (stdev ** 2))
    exponent = -((x - mean) ** 2) / (2 * (stdev ** 2))
    return coeff * (math.e ** exponent)
# end normalPDF(**kwargs)

# begin listIncidence(**kwargs)
def listIncidence(**kwargs):
    l = [float(x) for x in kwargs['input_list']]
    sl = sorted(l)
    ul = sorted( list( set(sl) ) )
    l_pos = 0
    ret_list = []

    for elem in ul:
        inc = 0

        while l_pos < len(sl) and sl[l_pos] == elem:
            inc += 1
            l_pos += 1

        ret_list.append({elem:inc})

    return ret_list
# end  listIncidence(**kwargs)

# begin discreteStepPDF(**kwargs)
'''
discreteStepPDF(in_list = [el1, el2, el3, ...],
num_parts = <num_parts>,
clearance = <clearance>,
summary_probability = <value|0 <value <<1, x=<x value>)

'''
def discreteStepPDF(**kwargs):
    inc_l = listIncidence(input_list = kwargs['input_list'])
    d_list = kwargs['input_list']
    x = kwargs['x']
    summ_prob = kwargs['summary_probability']
    num_parts = kwargs['num_parts']
    clearance = kwargs['clearance']
    s_list = sorted( d_list )
    min_val = s_list[0]
    max_val = s_list[len(s_list) - 1]
    start_pt = min_val - clearance
    end_pt = max_val + clearance

    if x < start_pt or x > end_pt : return 0
    
    step = (end_pt - start_pt)/num_parts
    lower_limit = None
    upper_limit = None
    sl_index = 0
    rank_arr = [0 for i in range(0, num_parts)]
    curr_seg = None
    include_lower_limit = True
    include_upper_limit = False
    lower_limit = None
    upper_limit = None
    init_area = 0
    
    for i in range(0, num_parts):
        seg_rank = 0
        lower_limit = start_pt + step*i
        upper_limit = start_pt + step*(i+1)

        if sl_index == len(s_list): break
        
        if s_list[sl_index] >= upper_limit and \
           not (s_list[sl_index] == upper_limit and \
                (i == num_parts - 1)):
            continue
        
        while sl_index < len(s_list) and \
              s_list[sl_index] < lower_limit:
            sl_index += 1

        while sl_index < len(s_list) and \
              s_list[sl_index] >= lower_limit and \
              ( s_list[sl_index] < upper_limit or \
                (i == num_parts - 1 and
                 s_list[sl_index] == upper_limit) ):
            sl_index += 1
            seg_rank += 1
            init_area += step

        rank_arr[i] = seg_rank
        
    try:
        coeff = summ_prob/init_area
    except:
        return 0
        
    seg_index = int((x - start_pt) // step)
    return coeff * rank_arr[seg_index]
# end discreteStepPDF(**kwargs)

# begin linear(**kwargs)
'''
linear(point1 = [<x1>, <y1>], point2 = [<x2>, <y2>], x=<x>)
'''
def linear(**kwargs):
    x1 = kwargs['point1'][0]
    y1 = kwargs['point1'][1]
    x2 = kwargs['point2'][0]
    y2 = kwargs['point2'][1]
    x = kwargs['x']

    return y1 + ((x - x1)/(x2 - x1))*(y2-y1)
    
# end linear(**kwargs)



