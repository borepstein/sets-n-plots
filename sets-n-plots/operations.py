'''
Operations-related classes.
'''

import numpy as np
from hash_based import *
from table import *
from dataset import *
from graphical_utils import *
from exceptions import *

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

    def report(self):
        '''
        Report on the operation status/completion status.
        Implement in subclasses.
        '''
        pass
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

# begin class DiscreteDistroBaseProc(Operation)
class DiscreteDistroBaseProc(Operation):
    '''
    Minimal structure:
    op_desc : Operation description
    op_desc : op_type : "disc_distro_base_analysis"
    op_desc : output_type : "file_system"
    op_desc : output_directory : <directory>
    op_desc : hist_file : <histogram file>
    in_dataset: <dataset>
    out_dataset: <dataset>
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getOutputDir(self): return self.getHash()["op_desc"]["output_directory"]

    def process(self):
        output_data = {}
        output_data["count"] = 0
        output_data["min"] = None
        output_data["max"] = None
        output_data["median"] = None
        output_data["stdev"] = None
        output_data["variance"] = None
        output_data["hist_file_dir"] = None
        data_set = self.getInDataSet().getData()
        output_data["ssize"] = len( data_set )

        # Submitting blank data in a dataset as it is empty.
        if output_data["ssize"] == 0:
            self.getOutDataSet().setDataSet(output_data)
            return

        # Filling in the data.
        output_data["min"] = np.min( data_set )
        output_data["max"] = np.max( data_set )
        output_data["median"] = np.median( data_set )
        output_data["stdev"] = np.std( data_set )
        output_data["variance"] = np.var( data_set )
        output_data["hist_file_dir"] = self.getOpDesc()["output_directory"]
        output_data["hist_file"] = self.getOpDesc()["hist_file"]

        gr = DiscreteSetBaseGraph(
            in_data = {"data_set" : data_set,
                       "hist_file_dir" : output_data["hist_file_dir"],
                        "hist_file_name" : output_data["hist_file"]})

        gr.process()
        
        self.getOutDataSet().setDataSet(output_data)
        

# end class DiscreteDistroBaseProc(Operation)
