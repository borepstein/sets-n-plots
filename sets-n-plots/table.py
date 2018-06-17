"""
Variable length table handling logic.
"""

# begin Table
class Table():
    ###
    Table data format:
    {"fields": [field1, field2, field3],
     "data" : [v11, v12, v13,
               v21, v22, v23]
    }

    Example:
    {"fields" : ["first_name", "last_name", "DOB"],
     "data": ["Bob", "Jones", "1950/01/05",
              "Jane", "Smith", "1990/10/09"
     ]
    }
    ###
    
    def __init__(self, **kwargs):
        self.__table_content = None
        
        if kwargs is None: return

        for key in kwargs.keys():
            if key == "table_content":
                self.__table_content = kwargs[key]
                continue
            if key == "fields":
                self.__fields = kwargs[key]
                continue
            

    def getTableContent(self): return self.__table_content

    def getFieldNames(self): return self.__table_content["fields"]

    def getColNumByFieldName(self, field):
        col = None

        try:
            col = self.__table_content["fields"].index( field )
        except:
            pass

        return( col )

    def getRow(self, row_num):
        row = []
        num_fields = len(self.__table_content["fields"])

        try:
            for i in range(row_num * num_fields,
                           row_num * (num_fields + 1) -1 ):
                row.append( self.__table_content["data"][i]  )
        except:
            return []
        
        return row

    def getColumn(self, field_name):
        col = []

        try:
            pos = self.getColNumByFieldName( field_name )
            num_fields = len( self.__table_content["fields"] )
        except:
            return col
        
        while pos <= len( self.__table_content["data"] ):            
            col.append( self.__table_content["data"][pos] )
            pos += num_fields

        return col
        
    def getDataCell(self, field_name, row):
        cell = None

        try:
            pos = self.getColNumByFieldName( field_name )
            num_fields = len( self.__table_content["fields"] )
            cell = self.__table_content["data"].[row * num_fields + pos]
        except:
            pass
        
        return cell
    
# end Table

