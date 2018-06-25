"""
Class collection for data set (incoming and outgoing)
"""

from hash_based import *
from table import *

# begin class DataSet
class DataSet(HashBased):
    '''
    Minimal structure:
    dataset = <dataset dict/hash/array>
    dataset_type = <dataset type>
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dataset = None
        self.__dataset_type = None
        
        if kwargs is None: return

        try:
            self.setDataSet( kwargs["dataset"] )
        except: pass

        try:
            self.setDataSetType( kwargs["dataset_type"] )
        except: pass
        
    def setDataSet(self, ds):
        self.__dataset = ds

    def setDataSetType(self, dst):
        self.__dataset_type = dst
        
    def getDataSet(self): return self.__dataset

    def getDataSetType(self): return self.__dataset_type
# end class DataSet

# begin class IncomingDataSet
class IncomingDataSet(DataSet):
    '''
    Minimal structure:
    dataset = <dataset>
    dataset_type = <dataset_type>
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
# end class IncomingDataSet

# begin class OutgoingDataSet
class OutgoingDataSet(DataSet):
    '''
    Minimal structure:
    dataset=<dataset>
    dataset_type=<dataset_type>
    status_rec=<status_rec>
    '''
    
    def __init__(self, **kwargs):
        self.__dataset_type = None
        self.__status_rec = None
        super().__init__(**kwargs)

        if kwargs is None: return

        try:
            self.__status_rec = kwargs["status_rec"]
        except: pass
                
    def getStatusRec( self ): return self.__status_rec
    
# end class OutgoingDataSet

# begin class BaseTableInDataSet(IncomingDataSet)
class BaseTableInDataSet(IncomingDataSet):
    '''
    Minimal configuration:
    dataset={
    fields:[<field1>, <field2>, <field3>,...]
    data:[<v1>, <v2>, <v3>, ...]
    }
    dataset_type=<dataset_type>
    '''
    def __init__(self, **kwargs):
        self.__table = None
        super().__init__(**kwargs)
        if kwargs is None: return

        try:
            self.__table = Table(
                    fields = kwargs["dataset"]["fields"],
                    data = kwargs["dataset"]["data"]
                )
        except:
            self.__table = None

    def getDataTable(self): return self.__table
# end class BaseTableInDataSet(IncomingDataSet)

# begin class BaseTableOutDataSet
class BaseTableOutDataSet(OutgoingDataSet):
    '''
    Minimal structure:
    dataset={table: <table>}
    '''
    
    def __init__(self, **kwargs):
        self.__output_table = None
        super().__init__(**kwargs)
        if kwargs is None: return

        try:
            self.__output_table = self.getHash()["table"]
        except:
            self.setOutputTable( None )
        
        
    def setOutputTable(self, t):
        self.__output_table = t
        gen_hash = self.getHash()
        gen_hash["table"] = t
        self.setHash( **gen_hash )
        
    def getOutputTable(self): return self.__output_table
# end class BaseTableOutDataSet
