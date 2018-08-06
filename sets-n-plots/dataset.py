"""
Class collection for data set (incoming and outgoing)
"""

from hash_based import *
from table import *
from exceptions import *

# begin class DataSet
'''
Minimal structure:
dataset = <dataset dict/hash/array>
dataset_type = <dataset type>
'''
class DataSet(HashBased):
    def __init__(self, **kwargs):
        hash = kwargs
        super().__init__(**hash)
        
        try:
            kwargs["dataset"]
        except:
            raise InputDataFormatException(\
                                           message = \
                                           "Format error: DataSet: \'dataset\' parameter not specified")

        self.setDataSet( kwargs["dataset"] )
        
        try:
            self.setDataSetType( kwargs["dataset_type"] )
        except: raise InputDataFormatException(message = "Format error: DataSet: \'dataset_type\' parameter not specified")
        
    def setDataSet(self, ds):
        self.__dataset = ds

    def setDataSetType(self, dst):
        self.__dataset_type = dst
        
    def getDataSet(self): return self.__dataset

    def getDataSetType(self): return self.__dataset_type
# end class DataSet

# begin class IncomingDataSet
'''
Minimal structure:
dataset = <dataset>
dataset_type = <dataset_type>
'''
class IncomingDataSet(DataSet):
    def __init__(self, **kwargs):
        hash = kwargs

        try:
            if hash['dataset'] is None:
                raise InputDataFormatException("Format error: IncomingDataSet: \'dataset\' parameter can not be \'None\'.")
        except:
            raise InputDataFormatException("Format error: IncomingDataSet: \'dataset\' parameter required.")
        
        super().__init__(**hash)
# end class IncomingDataSet

# begin class OutgoingDataSet
'''
Minimal structure:
dataset=<dataset>
dataset_type=<dataset_type>
status_rec=<status_rec>
'''
class OutgoingDataSet(DataSet):
    
    def __init__(self, **kwargs):
        hash = kwargs

        try: hash['dataset']
        except: hash['dataset'] = None

        try: hash['status_rec']
        except: hash['status_rec'] = None
        
        try: hash['dataset_type']
        except:
            raise InputDataFormatException("Format error: OutgoingDataSet: \"dataset_ype\" parameter required.")
            
        super().__init__(**hash)
                
    def getStatusRec( self ): return self.getHash()['status_rec']
    
# end class OutgoingDataSet

# begin class BaseTableInDataSet(IncomingDataSet)
'''
Minimal configuration:
dataset={
table: <table>
}
dataset_type=<dataset_type>
'''
class BaseTableInDataSet(IncomingDataSet):    
    def getDataTable(self): return self.getHash()['dataset']['table']
# end class BaseTableInDataSet(IncomingDataSet)

# begin class BaseTableOutDataSet
'''
Minimal structure:
<optional> dataset={table: <table>}
'''
class BaseTableOutDataSet(OutgoingDataSet):

    def __init__(self, **kwargs):
        hash = kwargs

        try: hash['dataset']['table']
        except: hash['dataset'] = {'table':None}
        HashBased.__init__(self, **hash)
        
    def setOutputTable(self, t):
        gen_hash = self.getHash()
        gen_hash['dataset']['table'] = t
        self.setHash( **gen_hash )
        
    def getOutputTable(self): return self.getHash()['dataset']['table']
# end class BaseTableOutDataSet

# begin class DiscreteDistroInDataSet(IncomingDataSet)
'''
Minimal structure:
dataset = { 'data':[ val1, val2. val3, ...], }
dataset_type = <dataset_type> }
'''
class DiscreteDistroInDataSet(IncomingDataSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getData(self): return self.getHash()["dataset"]["data"]
    
# begin class DiscreteDistroInDataSet(IncomingDataSet)

# begin class DiscreteDistroOutDataSet(OutgoingDataSet)
class DiscreteDistroOutDataSet(OutgoingDataSet):
    '''
    Minimal structure:
    dataset=<dataset>
    dataset_type=<dataset_type>
    status_rec=<status_rec>
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setDataSet(self, ds):
        hash = self.getHash()
        hash["dataset"] = ds
        self.setHash( **hash )

    def getDataSet(self): return self.getHash()["dataset"]
    
# begin class DiscreteDistroOutDataSet(OutgoingDataSet)
