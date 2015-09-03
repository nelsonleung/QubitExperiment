__author__ = 'Nelson'

from slab.instruments.awg.PulseSequence import *
from numpy import arange, linspace
from slab.experiments.ExpLib.PulseSequenceBuilder import *
from slab.experiments.ExpLib.QubitPulseSequence import *

from liveplot import LivePlotClient


class MultimodeRabiSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length=pt)


class MultimodeRabiSweepSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg, **kwargs):
        self.extra_args={}

        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
            #print str(key) + ": " + str(value)
        self.flux_freq = self.extra_args['flux_freq']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses, **kwargs)


    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length=pt)
        self.psb.append('q:mm','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.flux_freq)

class MultimodeT1Sequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q,mm0','pi', self.pulse_type)
        self.psb.idle(pt)
        self.psb.append('q,mm0','pi', self.pulse_type)