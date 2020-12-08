""" 
Definitions of data blocks
"""

from ..block import Block, blockmap
from . import waveform

class Training(Block):
    inputs = 0 
    outputs = 1
    
    def __init__(self, specification, pipeline=None):
        super().__init__(specification)
        self.ready = False
        self.data_generator = None
        
    def run(self):
        self.data_generator = waveform.MultiWaveformTraining(specification = self.specification)
        self.data_generator.build()
        self.ready = True
        
    def report(self):
        return self.data_generator._report()
        
    def outputs(self):
        if not self.ready:
            self.run()
        return [self.data_generator.payload]

    def package(self):
        self.data_generator.package(f"{self.name}.dat")

blockmap.register_block("data.waveform.training", Training)
