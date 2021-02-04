"""
Gravitic blocks for models.
"""

from heron.models.gw import HofTSurrogate, BBHNonSpinSurrogate
from heron.models.torchbased import HeronCUDA
import heron.models.georgebased
import george
import numpy as np

import heron
import torch
import gpytorch
from gpytorch.kernels import RBFKernel
from gpytorch.constraints import GreaterThan, LessThan

from elk.waveform import Timeseries

from heron.models.torchbased import train, HeronCUDAMix
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

        self.model = None
        self.pipeline = pipeline

        self.output_files = {"training_data": self.input_data['training_data'],
                             "weights":  f"{specification['name']}.pth"}

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
        if self.status_flag == "ready":
            # Models need to be trained before the mean can be returned
            train(self.model, iterations=self.specification['iterations'])
            # TODO update the specification
            # self.specification

        return self.model.mean(times=kwargs['times'],
                               p=kwargs['p'])

blockmap.register_block("data.waveform.heron", HeronTrainingBlock)
