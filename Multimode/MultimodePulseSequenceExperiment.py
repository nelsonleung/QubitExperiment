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


class MultimodeRabiSweepExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Rabi_Sweep', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeRabiSweepSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)



    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        #print self.data_file
        slab_file = SlabFile(self.data_file)
        with slab_file as f:
            f.append_pt('flux_freq', self.flux_freq)
            f.append_line('sweep_expt_avg_data', expt_avg_data)
            f.append_line('sweep_expt_pts', expt_pts)

            f.close()


class MultimodeT1Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_T1', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeT1Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass