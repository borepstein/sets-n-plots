'''
Operations-related classes.
'''

import table
import dataset
import numpy as np

# begin class Operation()
class Operation():
    def __init__(self, **kwargs):
        self.__op_desc = None
        self.__in_dataset = None
        self.__out_dataset = None

        try:
            self.__op_desc = kwargs["op_desc"]
        except: pass

        try:
            self.__in_dataset = kwargs["in_dataset"]
        except: pass

    def process(self):
        """
        Override with the actual processing logic.
        """
        pass

    def getInDataset(self): return self.__in_dataset

    def getOutDataset(self): return self.__out_dataset

    def getOpDess(self): return self.__op_desc
# end class Operation()

# begin class BaseSingleColumnSummaryAnalysis(Operation)
class BaseSingleColumnSummaryAnalysis(Operation):
    def __init__(self, **kwargs):
        super.__init__(**kwargs)
        self.__op_desc = super().getOpDesc()
        self.__in_data = super().getInDataset()
        self.__out_data = super().getOutDataset()
        
    def process(self):
        if self.__op_desc["op_type"] != "single_column_summary": return
        in_t = self._in_data.getDataTable()
        col = in_t.getColumn()
        out_t = Table({"fields" : ["min", "5th perc", "median",
                                   "95th perc", "max"],
                       "data" : [np.min(col), np.percentile(col, 5),
                                 np.percentile(col, 50), np.percentile(col, 95),
                                 np.max(col) ] })
        
        self.__out_data.setOutputData(out_t)

    def getOutDataset(self): return self.__out_data
        
# end class BaseSingleColumnSummaryAnalysis(Operation)
