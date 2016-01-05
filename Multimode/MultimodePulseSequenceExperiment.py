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

class MultimodeEFRabiExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_EF_Rabi', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeEFRabiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass

class MultimodeRamseyExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Ramsey', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeRamseySequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing Ramsey Data"
        fitdata = fitdecaysin(expt_pts, expt_avg_data)

        self.offset_freq =self.cfg['multimode_ramsey']['ramsey_freq'] - fitdata[1] * 1e9

        suggested_offset_freq = self.cfg['multimodes'][int(self.cfg['multimode_ramsey']['id'])]['dc_offset_freq'] - (fitdata[1] * 1e9 - self.cfg['multimode_ramsey']['ramsey_freq'])
        print "Suggested offset frequency: " + str(suggested_offset_freq)
        print "Oscillation frequency: " + str(fitdata[1] * 1e3) + " MHz"
        print "T2*: " + str(fitdata[3]) + " ns"


class MultimodeEFRamseyExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_EF_Ramsey', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeEFRamseySequence, pre_run=self.pre_run,
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


class MultimodeEFRabiSweepExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_EF_Rabi_Sweep', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeEFRabiSweepSequence, pre_run=self.pre_run,
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


class MultimodeEntanglementExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Entanglement', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeEntanglementSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass


class MultimodeCPhaseTestsExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_CPhase_Experiment', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeCPhaseTestsSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass

class MultimodePi_PiExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Pi_Pi_Experiment', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodePi_PiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass