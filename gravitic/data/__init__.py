""" 
Definitions of data blocks
"""

from ..block import Block, blockmap
from . import waveform
import os

class Training(Block):
    inputs = 0 
    outputs = 1
    
    def __init__(self, specification, pipeline=None):
        super().__init__(specification, pipeline)
        self.ready = False
        self.pipeline = pipeline
        self.data_generator = None
        self.output_files = {"training_data": os.path.join(self.pipeline.locations['data'], f"{self.name}.dat")}
        
    def run(self):
        self.data_generator = waveform.MultiWaveformTraining(specification = self.specification)
        self.data_generator.build()
        self.ready = True
        self.status = "finished"
        
    def report(self):
        return self.data_generator._report()
        
    def outputs(self):
        if not self.ready:
            self.run()
        return [self.data_generator.payload]

    def package(self):
        
        self.data_generator.package(self.output_files["training_data"])

blockmap.register_block("data.waveform.training", Training)
