__author__ = 'Nelson'

from slab.instruments.awg.PulseSequence import *
from numpy import arange, linspace, sin, pi
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

class MultimodeEFRabiSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']
        self.ef_pulse_type = self.expt_cfg['ef_pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq)


    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q','general', "gauss" ,amp = 1,length = 59.6159, freq=self.ef_sideband_freq)
        self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length=pt)
        self.psb.append('q','pi', self.pulse_type)
        print self.expt_cfg['a']



class MultimodeRamseySequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']
        #print self.expt_cfg['iq_freq']

    def define_pulses(self,pt):
        self.psb.append('q','half_pi', self.pulse_type)
        self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['pi_sb_ge'])
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=0, length= pt)
        self.psb.idle(pt)
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['pi_sb_ge'])
        self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['pi_sb_ge'],phase = 360.0*self.expt_cfg['offset_f']*pt/(1e9) )
        self.psb.append('q','half_pi', self.pulse_type)
        #self.psb.append('q','half_pi', self.pulse_type, phase = 360.0*self.expt_cfg['offset_f']*pt/(1e9))
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['half_pi_sb_ge'])

        #print self.expt_cfg['a']


class MultimodeEFRamseySequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq+ self.expt_cfg['ramsey_freq'])

    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q','general', "gauss" ,amp = 1,length = 59.6159, freq=self.ef_sideband_freq)
        self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['half_pi_sb_ef'])
        self.psb.idle(pt)
        self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['half_pi_sb_ef'])
        self.psb.append('q','pi', self.pulse_type)



class MultimodeRabiSweepSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg, **kwargs):
        self.extra_args={}
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']

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
        print self.expt_cfg['a']

class MultimodeEFRabiSweepSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg, **kwargs):
        self.extra_args={}
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
            #print str(key) + ": " + str(value)
        self.flux_freq = self.extra_args['flux_freq']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses, **kwargs)


    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.ef_pulse_type = self.expt_cfg['ef_pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq)

    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q','general', "gauss" ,amp = 1,length = 59.6159, freq=self.ef_sideband_freq)
        #self.psb.append('q','general', self.ef_pulse_type,amp=self.expt_cfg['a'],length = 59.6159, freq=self.ef_sideband_freq)
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length=pt)
        self.psb.append('q:mm','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.flux_freq)
        self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q','general', "gauss" ,amp = 1,length = 59.6159, freq=self.ef_sideband_freq)

class MultimodeT1Sequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        #self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q,mm0','pi', self.pulse_type)
        self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['pi_sb_ge'])
        print self.expt_cfg['pi_sb_ge']
        self.psb.idle(pt)
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['pi_sb_ge'])
        self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['pi_sb_ge'],phase = 360.0*self.expt_cfg['offset_f']*pt/(1e9))
        #self.psb.append('q,mm0','pi', self.pulse_type)


class MultimodeEntanglementSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        self.multimode_cfg = cfg['multimodes']
        #self.multimode_cfg = cfg['multimodes']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']
        self.ef_pulse_type = self.expt_cfg['ef_pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq)


    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= pt)
        self.psb.append('q,mm0','general', self.flux_pulse_type, amp= self.multimode_cfg[0]['a'], length=  self.multimode_cfg[0]['flux_pi_length'])
        self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length=  self.multimode_cfg[1]['flux_pi_length'])
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp= self.multimode_cfg[0]['a'], length=  self.multimode_cfg[0]['flux_pi_length'])



class MultimodeCPhaseQbitResTestSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        self.multimode_cfg = cfg['multimodes']
        #self.multimode_cfg = cfg['multimodes']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']
        self.ef_pulse_type = self.expt_cfg['ef_pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq)


    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= pt)
        self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a_ef'], length= 2*self.multimode_cfg[1]['flux_pi_length_ef'], freq= self.multimode_cfg[1]['flux_pulse_freq_ef'])
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= (self.multimode_cfg[1]['flux_pi_length_ef']- pt)%)


        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length=  self.multimode_cfg[1]['flux_pi_length'])
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp= self.multimode_cfg[0]['a'], length=  self.multimode_cfg[0]['flux_pi_length'])
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length=  self.multimode_cfg[1]['flux_pi_length'])