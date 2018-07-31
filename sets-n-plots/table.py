"""
Variable length table handling logic.
"""

from hash_based import *
from generic_utilities import *

# begin Table
'''
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
'''
class Table(HashBased):
    
    def __init__(self, **kwargs):
        hash = kwargs 

        try: hash['fields']
        except: hash['fields'] = []

        try: hash['data']
        except: hash['data'] = []

        HashBased.__init__(self, **hash)

    def getData(self): return self.getHash()['data']

    def getFieldNames(self): return self.getHash()['fields']

    def getColNumByFieldName(self, field):
        col = None

        try:
            col = self.getFieldNames().index( field )
        except:
            pass

        return( col )

    def getRow(self, row_num):
        row = []
        num_fields = len(self.getHash()['fields'])

        try: row = self.getHash()['data'][ num_fields * row_num : \
                                           num_fields*(row_num + 1) ]
        except: pass
        
        return row

    def getRowCount(self):
        cnt = 0

        try: cnt = int( len(self.getHash()['data'])/\
                        len(self.getHash()['fields']) )
        except: pass

        return cnt

    def getColumn(self, field_name):
        col = []

        try:
            pos = self.getColNumByFieldName( field_name )
            if pos is None: return col
            num_fields = len( self.getHash()['fields'] )
        except:
            return col

        while pos <= len( self.getHash()['data'] ):            
            col.append( self.getHash()['data'][pos] )
            pos += num_fields

        return col
        
    def getDataCell(self, field_name, row):
        cell = None

        try:
            pos = self.getColNumByFieldName( field_name )
            num_fields = len( self.getHash()['fields'] )
            cell = self.getHash()['data'][row * num_fields + pos]
        except:
            pass
        
        return cell
    
# end Table

# begin ExtendedTable(Table)
'''
Table with extended field definitions [{<field_name>:{<attr1>,<attr2>,...},...]

Table data format:
{"fields": [{field1:attr1}, {field2:attr2}, {ield3:attr3},...],
"data" : [v11, v12, v13,
v21, v22, v23]
}

Example:
{"fields" : [{"first_name":"Person's first name"}, {"last_name":"Person's last name"}, {"DOB":"Date of birth"}],
"data": ["Bob", "Jones", "1950/01/05",
"Jane", "Smith", "1990/10/09"
]
}
'''
class ExtendedTable(Table):
    def getFieldNames(self):
        return [list(m.keys())[0] for m in Table.getFieldNames(self)]

    def getFieldAttributeTable(self):
        return Table.getFieldNames(self)
# end ExtendedTable(Table)
