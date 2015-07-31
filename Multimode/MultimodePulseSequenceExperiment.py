__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.experiments.ExpLib.QubitPulseSequenceExperiment import *
from numpy import mean, arange


class MultimodeRabiExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Rabi', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeRabiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass
