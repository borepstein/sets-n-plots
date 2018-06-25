'''
Graphical utilities and tools.
'''

from hash_based import *

# begin class Graphics(HashBased)
class Graphics(HashBased):
    '''
    Generic graphics data representation.
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        hash = self.getHash()

        try:
            temp = hash["in_data"]
        except:
            hash["in_data"] = None

        try:
            temp = hash["out_data"]
        except:
            hash["out_data"] = None

        try:
            temp = hash["graph_spec"]
        except:
            hash["graph_spec"] = None

        self.setHash( hash )

    def process(self): pass
        
# end class Graphics(HashBased)
