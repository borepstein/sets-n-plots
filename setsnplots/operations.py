'''
Operations-related classes.
'''

import copy
import numpy as np
from .hash_based import *
from .generic_utilities import *
from .table import *
from .dataset import *
from .graphical_utils import *
from .exceptions import *

# begin class Operation()
'''
Minimal parameters:
op_desc : Operation description
structure describing operation requested.

in_dataset : incoming dataset

out_dataset : outgoing (resultant) dataset
'''
class Operation(HashBased):    
    def __init__(self, **kwargs):
        hash = kwargs
        self.__process_func = self.processFunc
        self.__op_desc = None
        self.__in_dataset = None
        self.__out_dataset = None

        try:
            self.__op_desc = kwargs["op_desc"]
        except:
            raise InputDataFormatException(message ="Operation: Parameter \'op_desc\' is required.")

        try:
            self.__in_dataset = kwargs["in_dataset"]
        except:
            raise InputDataFormatException(message ="Operation: Parameter \'in_dataset\' is required.")

        try:
            self.__out_dataset = kwargs["out_dataset"]
        except:
            raise InputDataFormatException(message ="Operation: Parameter \'out_dataset\' is required.")
        
        try:
            self.__process_func = hash['process_func']
        except:
            hash['process_func'] = self.processFunc
        
        super().__init__(**hash)

    def process(self, **kwargs):
        return self.getHash()['process_func'](**kwargs)

    """
    Override with the actual processing logic.
    """
    def processFunc(self, **kwargs):
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
'''
Format:
op_desc : op_type = "single_column_summary"
op_desc : field = <field name>
in_dataset : incoming dataset
out_dataset : outgoing dataset
'''
class BaseSingleColumnSummaryAnalysis(Operation):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
           if type( kwargs['in_dataset'] ) is not BaseTableInDataSet:
               raise InputDataFormatException(message="BaseSincleColumnSummaryAnalysis: \'in_dataset\' must be of type BaseTableInDataSet")

           if type( kwargs['out_dataset'] ) is not BaseTableOutDataSet:
               raise InputDataFormatException(message="BaseSincleColumnSummaryAnalysis: \'out_dataset\' must be of type BaseTableOutDataSet")
        except:
            raise InputDataFormatException(message="BaseSincleColumnSummaryAnalysis: format error.")
        
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
class DiscreteDistroBaseProc(Operation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if type( kwargs['in_dataset'] ) is not DiscreteDistroInDataSet:
            raise InputDataFormatExceptio(message="DiscreteDistroBaseProc: \'in_dataset\' must be of type \'DiscreteDistroInDataSet\'")

        if type( kwargs['out_dataset'] ) is not DiscreteDistroInDataSet:
            raise InputDataFormatExceptio(message="DiscreteDistroBaseProc: \'out_dataset\' must be of type \'DiscreteDistroOutDataSet\'")

        try:
            if kwargs['op_desc']['op_type'] != \
               "disc_distro_base_analysis" or \
               not kwargs['op_desc']['output_type'] or \
               not kwargs['op_desc']['output_directory'] or \
               not kwargs['op_desc']['hist_file']:
                raise InputDataFormatExceptio(message="DiscreteDistroBaseProc: input parameter error.")
        except:
            raise InputDataFormatExceptio(message="DiscreteDistroBaseProc: input parameter error.")
        
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
        data_set = self.getInDataSet().getDataTable()
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

# begin GroupTableByCriteria(Operation)
'''
Format:
op_desc : op_type = "group_by_criteria"
selection_criteria=[<field1>, <field2>, ...]
in_dataset : incoming dataset
out_dataset : outgoing dataset
'''
class GroupTableByCriteria(Operation):
    def __init__(self, **kwargs):
        hash = kwargs
        Operation.__init__(self, **hash)
        hash['process_func'] = self.processFunc
        hash['selection_fields_tag']='selection_fields'
        
        if type( hash['in_dataset'] ) is not BaseTableInDataSet:
            raise InputDataFormatException(message="GroupTableByCriteria: \'in_dataset\' must be of type \'BaseTableInDataSet\'")

        if type( hash['out_dataset'] ) is not BaseTableOutDataSet:
            raise InputDataFormatException(message="GroupTableByCriteria: \'out_dataset\' must be of type \'BaseTableOutDataSet\'")        
                 
        HashBased.setHash(self, **hash)

    def processFunc(self, **kwargs):
        def getOutTableFields(table, sel_fields):         
            return [{self.getHash()['selection_fields_tag'] : set(sel_fields)}] + \
                [{f:None} for f in table.getFieldNames() if f not in sel_fields]
            
        def fillOutTable(in_t, out_t, sel_fields):
            sel_field_value = None
            exclusion_index = []
            row_index = []
            query = {}
            
            for i in range(0, in_t.getRowCount()):
                if i in exclusion_index: continue
                sel_fields_value = [{f:in_t.getDataCell(f, i)} for f in sel_fields]

                query = {}
                for elem in sel_fields_value:
                    query[list(elem.keys())[0]] = elem[list(elem.keys())[0]]
                    
                row_index = in_t.getRowIndexANDSelection(query)
                exclusion_index += row_index
                out_t.addRow([sel_fields_value] +\
                             [in_t.getColumn(f, row_index) for f in in_t.getFieldNames() \
                              if f not in sel_fields])
            
        in_t = ExtendedTable( fields = \
                              self.getInDataSet().getDataTable().getFieldNames(),
                              data = \
                              self.getInDataSet().getDataTable().getData() )

        out_t = ExtendedTable(fields=\
                              getOutTableFields(in_t, \
                                                self.getHash()['selection_criteria']), \
                              data=[])
        fillOutTable(in_t, out_t, self.getHash()['selection_criteria'])
            
        self.getOutDataSet().setOutputTable(out_t)
        
# begin GroupTableByCriteria(Operation)

# begin FullGroupAnalysis(Operation)
class FullGroupAnalysis(Operation):
    def __init__(self, **kwargs):
        self.__cat_label = "Category_"
        Operation.__init__(self, **kwargs)

        if type( kwargs['in_dataset'] ) is not DiscreteDistroInDataSet:
            raise InputDataFormatException(message = "FullGroupAnalysis: \'in_dataset\' must be of type \'DiscreteDistroInDataSet\'")

        if type( kwargs['out_dataset'] ) is not DiscreteDistroOutDataSet:
            raise InputDataFormatException(message = "FullGroupAnalysis: \'out_dataset\' must be of type \'DiscreteDistroOutDataSet\'")

    def processFunc(self, **kwargs):
        try:
            labels = self.getInDataSet().getHash()['dataset']['labels']

            if len(labels) != len( self.getInDataSet().getData() ):
               raise InputDataFormatException(
                   message = \
                   "FullGroupAnalysis: processFunc: \'dataset->data\' and \'dataset->labels\' must have the same number of members.")
           
        except:
            hash = self.getInDataSet().getHash()
            labels = []
            i = 0
            for elem in self.getInDataSet().getData():
                i += 1
                labels.append(self.__cat_label + i.__str__())
            hash['dataset']['labels'] = labels
            self.getInDataSet().setHash(**hash)
            
        
        val_sum = 0

        output_table = Table(fields = ["Label", "Value", "Percentage"], data=[] )
        
        for x in self.getInDataSet().getData():
            val_sum += x

        perc_flag = False
        if val_sum != 0:
            perc_flag = True

        i = 0
        new_row = []
        for l in labels:
            new_row = [l, self.getInDataSet().getData()[i], None]
            if perc_flag: new_row[2] = \
               ( self.getInDataSet().getData()[i] / val_sum ) * 100
            output_table.addRow( new_row )
            i += 1

        output_data = {}
        output_data['table'] = output_table
        self.getOutDataSet().setDataSet( output_data )
# end FullGroupAnalysis(Operation)
