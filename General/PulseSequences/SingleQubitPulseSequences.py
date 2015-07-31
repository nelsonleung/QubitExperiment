__author__ = 'Nelson'

from slab.instruments.awg.PulseSequence import *
from numpy import arange, linspace
from slab.experiments.ExpLib.PulseSequenceBuilder import *
from slab.experiments.ExpLib.QubitPulseSequence import *

from liveplot import LivePlotClient


class RabiSequence(QubitPulseSequence):
    def __init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg, qubit_cfg ,buffer_cfg):
        QubitPulseSequence.__init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg, buffer_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('general', self.pulse_type, amp=1, length=pt)


class T1Sequence(QubitPulseSequence):
    def __init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg, qubit_cfg ,buffer_cfg):
        QubitPulseSequence.__init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg, buffer_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('pi', self.pulse_type)
        self.psb.idle(pt)


class RamseySequence(QubitPulseSequence):
    def __init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg, qubit_cfg ,buffer_cfg):
        QubitPulseSequence.__init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg, buffer_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('half_pi', self.pulse_type)
        self.psb.idle(pt)
        self.psb.append('half_pi', self.pulse_type)


class SpinEchoSequence(QubitPulseSequence):
    def __init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg, qubit_cfg ,buffer_cfg):
        QubitPulseSequence.__init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg,buffer_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('half_pi', self.pulse_type)
        self.psb.idle(pt/2.0)
        self.psb.append('pi', self.pulse_type)
        self.psb.idle(pt/2.0)
        self.psb.append('half_pi', self.pulse_type)


class EFRabiSequence(QubitPulseSequence):
    def __init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg, qubit_cfg ,buffer_cfg):
        self.qubit_cfg = qubit_cfg
        self.pulse_cfg = pulse_cfg
        QubitPulseSequence.__init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg,buffer_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq)

    def define_pulses(self,pt):
        if self.expt_cfg['ge_pi']:
            self.psb.append('pi', self.pulse_type)
        self.psb.append('general', self.pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.ef_sideband_freq)
        self.psb.append('pi', self.pulse_type)