'''
Graphical utilities and tools.
'''

import os
import matplotlib.pyplot as plt
from hash_based import *

# begin class Graphics(HashBased)
class Graphics(HashBased):
    '''
    Generic graphics data representation.

    Minimal structure:
    in_data=<incoming data>
    out_data=<outgoing data>
    graph_spec=<specification for graphics>
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

        self.setHash( **hash )

    '''
    Generating graphics.
    Implement in subclasses.
    '''
    def process(self): pass
        
# end class Graphics(HashBased)

# begin class DiscreteSetBaseGraph(Graphics)
class DiscreteSetBaseGraph(Graphics):
    '''
    Minimal structure:
    in_data : data_set : <[num1, num2, num3, ...]>
    in_data : hist_file_dir : <output  directory>
    in_data : hist_file_name : <histogram file name>
    (optional) in_data : num_bins : <number of histogram bins>
    '''

    def __init__(self, **kwargs):
        self.__num_bins = 100
        super().__init__(**kwargs)

        try:
            self.__num_bins = self.gethash()["in_data"]["num_bins"]
        except: pass
    
    def process(self):
        fig, ax = plt.subplots()
        ax.hist( self.getHash()["in_data"]["data_set"],
                 self.__num_bins)
        fig.savefig( self.getFullHistFilePath() )
        
        
    def getFullHistFilePath(self):
        return os.path.join(
            self.getHash()["in_data"]["hist_file_dir"],
            self.getHash()["in_data"]["hist_file_name"] )
    
# end class DiscreteSetBaseGraph(Graphics)
