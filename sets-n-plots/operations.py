'''
Operations-related classes.
'''

from hash_based import *
from table import *
from dataset import *
import numpy as np

# begin class Operation()
class Operation(HashBased):
    '''
    Minimal parameters:
    op_desc : Operation description
    structure describing operation requested.

    in_dataset : incoming dataset

    out_dataset : outgoing (resultant) dataset
    '''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__op_desc = None
        self.__in_dataset = None
        self.__out_dataset = None

        try:
            self.__op_desc = kwargs["op_desc"]
        except: pass

        try:
            self.__in_dataset = kwargs["in_dataset"]
        except: pass

        try:
            self.__out_dataset = kwargs["out_dataset"]
        except: pass

    def process(self):
        """
        Override with the actual processing logic.
        """
        pass

    def getInDataSet(self): return self.__in_dataset

    def getOutDataSet(self): return self.__out_dataset

    def getOpDesc(self): return self.__op_desc
# end class Operation()

# begin class BaseSingleColumnSummaryAnalysis(Operation)
class BaseSingleColumnSummaryAnalysis(Operation):
    '''
    Format:
    op_desc : op_type = "single_column_summary"
    op_desc : field = <field name>
    in_dataset : incoming dataset
    out_dataset : outgoing dataset
    '''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def process(self):
        if self.getOpDesc()["op_type"] != "single_column_summary": return

        try:
            in_t = self.getInDataSet().getDataTable()
            col = in_t.getColumn(self.getOpDesc()["op_desc"]["field"])
            out_t = Table(fields = ["min", "5th perc", "median",
                                    "95th perc", "max"],
                          data = [np.min(col), np.percentile(col, 5),
                                  np.percentile(col, 50),
                                  np.percentile(col, 95),
                                  np.max(col) ] )

            if self.getOutDataSet() is None:
                self.setOutDataSet(
                    BaseTableOutDataSet(status_rec =
                                        "column processed")
                )

            self.getOutDataSet().setOutputTable( out_t )
        except:
            self.getOutDataSet().setOutputTable(None)
        
# end class BaseSingleColumnSummaryAnalysis(Operation)
