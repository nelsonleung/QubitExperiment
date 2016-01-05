__author__ = 'Nelson'

from slab.instruments.awg.PulseSequence import *
from numpy import arange, linspace
from slab.experiments.ExpLib.PulseSequenceBuilder import *
from slab.experiments.ExpLib.QubitPulseSequence import *

from liveplot import LivePlotClient


class RabiSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        if self.expt_cfg['sweep_amp']:
            self.psb.append('q','general', self.pulse_type, amp=pt, length=self.expt_cfg['length'],freq=self.expt_cfg['iq_freq'])
        else:
            self.psb.append('q','general', self.pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.expt_cfg['iq_freq'])




class RamseySequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','half_pi', self.pulse_type)
        self.psb.idle(pt)
        self.psb.append('q','half_pi', self.pulse_type, phase = 360.0*self.expt_cfg['ramsey_freq']*pt/(1.0e9))


class SpinEchoSequence(QubitPulseSequence):
    def __init__(self,name,cfg, expt_cfg,**kwargs):
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
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.ef_pulse_type = self.expt_cfg['ef_pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq)

    def define_pulses(self,pt):
        if self.expt_cfg['ge_pi']:
           self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q','general', self.ef_pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.ef_sideband_freq)
        #self.psb.append('q','general', self.pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.ef_sideband_freq)
        self.psb.append('q','pi', self.pulse_type)


class EFRamseySequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self, name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.ef_pulse_type = self.expt_cfg['ef_pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq + self.expt_cfg['ramsey_freq'])

    def define_pulses(self,pt):
        if self.expt_cfg['ge_pi']:
            self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q','general', self.pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.ef_sideband_freq)
        self.psb.append('q','general', self.ef_pulse_type,amp=self.expt_cfg['a'],length = self.expt_cfg['half_pi_ef'], freq=self.ef_sideband_freq )
        self.psb.idle(pt)
        self.psb.append('q','general', self.ef_pulse_type,amp=self.expt_cfg['a'],length = self.expt_cfg['half_pi_ef'],freq=self.ef_sideband_freq )
        self.psb.append('q','pi', self.pulse_type)


class EFT1Sequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters,self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.ef_pulse_type = self.expt_cfg['ef_pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq)

    def define_pulses(self,pt):
        if self.expt_cfg['ge_pi']:
            self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q','general', self.ef_pulse_type,amp=self.expt_cfg['a'],length = self.expt_cfg['pi_ef'], freq=self.ef_sideband_freq )
        self.psb.idle(pt)
        self.psb.append('q','pi', self.pulse_type)



class T1Sequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        # self.psb.append('q','general', 'square', amp=1, length=16,freq=150e6)
        self.psb.append('q','pi', self.pulse_type)
        self.psb.idle(pt)


class HalfPiXOptimizationSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        n = 2*pt+1
        i = 0
        while i< n:
            self.psb.append('q','half_pi', self.pulse_type)
            i += 1


class HalfPiXOptimizationSweepSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.pulse_cfg = cfg['pulse_info']
        self.expt_cfg = expt_cfg
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
            #print str(key) + ": " + str(value)
        self.pulse_length = self.extra_args['pulse_length']

        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        n = 2*pt+1
        i = 0
        while i< n:
            self.psb.append('q','general', self.pulse_type, amp=self.pulse_cfg[self.pulse_type]['a'], length=self.pulse_length,freq=self.pulse_cfg[self.pulse_type]['iq_freq'])
            i += 1


class PiXOptimizationSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        n = pt
        i = 0
        self.psb.append('q','half_pi', self.pulse_type)
        while i< n:
            self.psb.append('q','pi', self.pulse_type)
            i += 1

class HalfPiYPhaseOptimizationSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','half_pi', self.pulse_type)
        self.psb.append('q','general', self.pulse_type, amp=self.pulse_cfg[self.pulse_type]['a'], length=self.pulse_cfg[self.pulse_type]['half_pi_length'],freq=self.pulse_cfg[self.pulse_type]['iq_freq'],phase=pt)

class HalfPiYOptimizationSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        n = 2*pt+1
        i = 0
        while i< n:
            self.psb.append('q','half_pi_y', self.pulse_type)
            i += 1

class PiYOptimizationSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        n = pt
        i = 0
        self.psb.append('q','half_pi_y', self.pulse_type)
        while i< n:
            self.psb.append('q','pi_y', self.pulse_type)
            i += 1


class TomographySequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = np.array([0,1,2])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        ### Initiate states
        self.psb.append('q','half_pi', self.pulse_type)

        ### gates before measurement for tomography
        if pt == 0:
            # <X>
            self.psb.append('q','half_pi', self.pulse_type)
        elif pt == 1:
            # <Y>
            self.psb.append('q','half_pi_y', self.pulse_type)
        elif pt == 2:
            # <Z>
            pass


class HalfPiYOptimizationSweepSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.pulse_cfg = cfg['pulse_info']
        self.expt_cfg = expt_cfg
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
            #print str(key) + ": " + str(value)
        self.pulse_length = self.extra_args['pulse_length']

        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        n = 2*pt+1
        i = 0
        while i< n:
            self.psb.append('q','general', self.pulse_type, amp=self.pulse_cfg[self.pulse_type]['a'], length=self.pulse_length,freq=self.pulse_cfg[self.pulse_type]['iq_freq'],phase=self.pulse_cfg[self.pulse_type]['y_phase'])
            i += 1


class PiXOptimizationSweepSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.pulse_cfg = cfg['pulse_info']
        self.expt_cfg = expt_cfg
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
            #print str(key) + ": " + str(value)
        self.pulse_length = self.extra_args['pulse_length']

        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        n = pt
        i = 0
        self.psb.append('q','half_pi', self.pulse_type)
        while i< n:
            self.psb.append('q','general', self.pulse_type, amp=self.pulse_cfg[self.pulse_type]['a'], length=self.pulse_length,freq=self.pulse_cfg[self.pulse_type]['iq_freq'])
            i += 1


class PiYOptimizationSweepSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.pulse_cfg = cfg['pulse_info']
        self.expt_cfg = expt_cfg
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
            #print str(key) + ": " + str(value)
        self.pulse_length = self.extra_args['pulse_length']

        QubitPulseSequence.__init__(self,name, cfg, expt_cfg,self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        n = pt
        i = 0
        self.psb.append('q','half_pi_y', self.pulse_type)
        while i< n:
            self.psb.append('q','general', self.pulse_type, amp=self.pulse_cfg[self.pulse_type]['a'], length=self.pulse_length,freq=self.pulse_cfg[self.pulse_type]['iq_freq'],phase=self.pulse_cfg[self.pulse_type]['y_phase'])
            i += 1


class RabiSweepSequence(QubitPulseSequence):

    def __init__(self,name, cfg, expt_cfg, **kwargs):
        self.pulse_cfg = cfg['pulse_info']

        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses, **kwargs)


    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','general', self.pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.expt_cfg['iq_freq'])




