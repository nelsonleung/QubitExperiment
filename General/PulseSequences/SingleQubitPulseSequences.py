__author__ = 'Nelson'

from slab.instruments.awg.PulseSequence import *
from numpy import arange, linspace
from slab.experiments.ExpLib.PulseSequenceBuilder import *
from slab.experiments.ExpLib.QubitPulseSequence import *

from liveplot import LivePlotClient


class RabiSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','general', self.pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.expt_cfg['iq_freq'])


class T1Sequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.idle(pt)


class RamseySequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','half_pi', self.pulse_type)
        self.psb.idle(pt)
        self.psb.append('q','half_pi', self.pulse_type)


class SpinEchoSequence(QubitPulseSequence):
    def __init__(self,name,cfg, expt_cfg):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','half_pi', self.pulse_type)
        self.psb.idle(pt/2.0)
        self.psb.append('q','pi', self.pulse_type)
        self.psb.idle(pt/2.0)
        self.psb.append('q','half_pi', self.pulse_type)


class EFRabiSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq)

    def define_pulses(self,pt):
        if self.expt_cfg['ge_pi']:
            self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q','general', 'square', amp=self.expt_cfg['a'], length=pt,freq=self.ef_sideband_freq)
        #self.psb.append('q','general', self.pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.ef_sideband_freq)
        self.psb.append('q','pi', self.pulse_type)


class EFRamseySequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq + self.expt_cfg['ramsey_freq'])

    def define_pulses(self,pt):
        if self.expt_cfg['ge_pi']:
            self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q','general', self.pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.ef_sideband_freq)
        self.psb.append('q','general', 'square',amp=self.expt_cfg['a'],length = self.expt_cfg['half_pi_eg'], freq=self.ef_sideband_freq )
        self.psb.idle(pt)
        self.psb.append('q','general', 'square',amp=self.expt_cfg['a'],length = self.expt_cfg['half_pi_eg'],freq=self.ef_sideband_freq )
        self.psb.append('q','pi', self.pulse_type)