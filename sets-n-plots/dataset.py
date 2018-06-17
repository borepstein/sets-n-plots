"""
Class collection for data set (incoming and outgoing)
"""

import table

# begin class DataSet
class DataSet():

    def __init__(self, **kwargs):
        self.__dataset = None

        if kwargs is None: return

        for key in kwargs.keys():
            if key == "dataset":
                self.setDataSet( kwargs[key] )
                continue

    def getDataSet(self): return(self.__dataset)

# end class DataSet

# begin class IncomingDataSet
class IncomingDataSet(DataSet):

    def __init__(self, **kwargs):
        self.__ops_req = None
        super().__init__(**kwargs)

        if kwargs is None: return

        for key in kwargs.keys():
            if key == "ops_req":
                self.setOpsReq( kwargs[key] )

    def getOpsReq( self ): return self.__ops_req
    
# end class IncomingDataSet

# begin class OutgoingDataSet
class OutgoingDataSet(DataSet):

    def __init__(self, **kwargs):
        self.__status_rec = None
        super().__init__(**kwargs)

        if kwargs is None: return

        for key in kwargs.keys():
            if key == "status_rec":
                self.setStatusRec( kwargs[key] )

    def setStatusRec( self, status_rec ):
        self.__status_rec = status_rec

    def getStatusRec( self ): return self.__status_rec
    
# end class OutgoingDataSet

# begin class BaseTableInDataSet(IncomingDataSet)
class BaseTableInDataSet(IncomingDataSet):
    def __init__(self, **kwargs):
        self.__table = None
        super().__init__(**kwargs)
        if kwargs is None: return

        try:
            self.__table = Table(
                "table_content" = {
                    "fields" : kwargs["dataset"]["fields"},
                    "data" : kwargs["dataset"]["data"]
                    }
                )
        except:
            self.__table = None

    def getDataTable(self): return self.__table
# end class BaseTableInDataSet(IncomingDataSet)

# begin class BaseTableOutClass
class BaseTableOutClass(OutgoingDataSet):
    def __init__(self, **kwargs):
        self.__output_table = None
        super().__init__(**kwargs)
        if kwargs is None: return

        try:
            self.__output_table = Table(
                "table_content" = {
                    "fields" = kwargs["dataset"]["fields"],
                    "data" = kwargs["dataset"]["data"]
                }
            )
        except: pass
        
    
    def getOutputTable(self): return self.__output_table
# end class BaseTableOutClass
