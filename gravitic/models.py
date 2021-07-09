"""
Gravitic blocks for models.
"""
try:
    from heron.models.gw import HofTSurrogate, BBHNonSpinSurrogate
    from heron.models.torchbased import HeronCUDA
    import heron.models.georgebased
    import george
    import heron
    import torch
    import gpytorch
    from gpytorch.kernels import RBFKernel
    from gpytorch.constraints import GreaterThan, LessThan
    from heron.models.torchbased import train, HeronCUDAMix
except:
    pass

import numpy as np

try:
    from elk.waveform import Timeseries
except:
    pass

from gravitic.block import Block, blockmap

class HeronTrainingBlock(Block):
    """
    The training block for heron models.
    """
    def __init__(self, specification, pipeline=None):
        super().__init__(specification, pipeline=pipeline)
        self.ready = False

        self.inputs = 1
        self.outputs = 1

        self.output_files = {"weights":  f"{specification['name']}.pth"}

        if self.status == "finished":
            self.build()
        else:
            self.model = None
            #self.run()
            
        self.pipeline = pipeline

    def build(self):
        self.model = HeronCUDAMix(specification=self.specification, **self.input_data)
        self.ready = True
        
    def output(self):
        if self.ready:
            out = self.output_files
            out['specification'] = self.specification
            return out
        return None

    def run(self, **kwargs):
        if not self.ready:
            self.build()
        # Models need to be trained before the mean can be returned
        train(self.model, iterations=self.specification['iterations'])
        self.status = "finished"
        self.ready = True

blockmap.register_block("data.waveform.heron", HeronTrainingBlock)
