"""
Waveform training data generation 
"""

import pycbc.waveform
import numpy as np
from pycbc.waveform import get_td_waveform
import yaml
import otter.bootstrap as bt
import matplotlib.pyplot as plt
from gravitic.block import Block

class MultiWaveformTraining:
    """
    Waveform-based training data sets using multiple waveform families.
    """
    def __init__(self, specification):
        """
        Set-up the training set from a specification dictionary.
        """
        self.specification = specification
        self.payload = None

    def coalign(self, location):

        M = location['total mass']
        if "m1" in location:
            m1 = location['m1']
            m2 = location['m2']
        elif "mass ratio" in location:
            m1 = M / (1+location['mass ratio'])
            m2 = M / (1+1/location['mass ratio'])

        unaligned = {}
        for apx in self.specification['families']:
            # Generate the waveforms from the models
            unaligned[apx] = {}
            unaligned[apx]['hp'], unaligned[apx]['hc'] = get_td_waveform(approximant=apx,
                                                                         mass1=m1,
                                                                         mass2=m2,
                                                                         delta_t=1.0/self.specification['sample rate'],
                                                                         f_lower=self.specification['lower frequency'])
        hp = {apx: waveform['hp'] for apx, waveform in unaligned.items()}
        hc = {apx: waveform['hc'] for apx, waveform in unaligned.items()}

        aligned = {"hp": {apx: waveform for apx, waveform in zip(hp.keys(), pycbc.waveform.coalign_waveforms(*hp.values()))},
                   "hc": {apx: waveform for apx, waveform in zip(hc.keys(), pycbc.waveform.coalign_waveforms(*hc.values()))}}

        return aligned

    def _report(self):
        """
        Build a report containing the generated waveforms.
        """
        # report = otter.Otter(
        #     os.path.join(config.get("project", "webroot"),
        cards = bt.Container()
        for waveform in self.payload:
            f, ax = plt.subplots(1,1)
            ax.plot(waveform[2, :], waveform[4, :])
            card = bt.Card(title=f"p={waveform[1, 0]} q={waveform[3, 0]}")
            card + f
            cards + card
        return cards

    def build(self):
        # Columns:
        # Approximant | Polarisation | Time | Mass ratio
        data_all = []
        qs = np.linspace(self.specification['q']['min'],
                         self.specification['q']['max'],
                         self.specification['q']['number'])

        apx_idx = {family: i
                   for i, family in enumerate(self.specification['families'])}

        pol_idx = {"hp": 0, "hc": 1}

        for q in qs:
            waveform = self.coalign(location={"mass ratio": q, "total mass": self.specification['total mass']})
            idx = (list(waveform['hp'].values())[0].sample_times > self.specification['time']['min']) & (list(waveform['hp'].values())[0].sample_times < self.specification['time']['max'])
            data = np.ones((sum(idx), 5))
            for tag, polarisation in waveform.items():
                for approximant_tag, approximant in polarisation.items():
                    data = np.ones((sum(idx), 5))
                    data[:, 0] *= apx_idx[approximant_tag]
                    data[:, 1] = data[:, 1] * pol_idx[tag]
                    data[:, 2]  = approximant.sample_times[idx]
                    data[:, 3] *= q
                    data[:, 4]  = approximant.data[idx]
                    data_all.append(data.T)
        self.payload = data_all

    def package(self, outfile):
        print(outfile)
        if not isinstance(self.payload, type(None)):
            np.savetxt(outfile, np.hstack(self.payload).T)
