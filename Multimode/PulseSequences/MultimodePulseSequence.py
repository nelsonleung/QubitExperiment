__author__ = 'Nelson'

from slab.instruments.awg.PulseSequence import *
from numpy import arange, linspace, sin, pi, sign
from slab.experiments.ExpLib.PulseSequenceBuilder import *
from slab.experiments.ExpLib.QubitPulseSequence import *

from liveplot import LivePlotClient


class MultimodeRabiSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.multimode_cfg = cfg['multimodes']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']

    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q,mm1','general', self.flux_pulse_type, amp=self.multimode_cfg[1]['a'], length=pt)

class MultimodeEFRabiSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        self.multimode_cfg = cfg['multimodes']
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
        self.psb.append('q','general', "gauss" ,amp = 1,length = 52, freq=self.ef_sideband_freq)
        self.psb.append('q:mm','general',"gauss", amp=self.multimode_cfg[0]['a_ef'], length=pt, freq=self.multimode_cfg[0]['flux_pulse_freq_ef'])
        #self.psb.append('q,mm2','general', self.flux_pulse_type, amp=self.multimode_cfg[2]['a_ef'], length=pt)
        self.psb.append('q','pi', self.pulse_type)




class MultimodeRamseySequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        self.multimode_cfg = cfg['multimodes']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']
        #print self.expt_cfg['iq_freq']

    def define_pulses(self,pt):
        self.psb.append('q','half_pi', self.pulse_type)
        self.psb.append('q,mm1','general', self.flux_pulse_type, amp=self.multimode_cfg[1]['a'], length=  self.multimode_cfg[1]['flux_pi_length'])
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=0, length= pt)
        self.psb.idle(pt)
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['pi_sb_ge'])
        self.psb.append('q,mm1','general', self.flux_pulse_type, amp=self.multimode_cfg[1]['a'], length= self.multimode_cfg[1]['flux_pi_length'],phase = 360.0*self.expt_cfg['offset_f']*pt/(1e9) )
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
        self.psb.append('q','general', "gauss" ,amp = 1,length = 56, freq=self.ef_sideband_freq)
        #self.psb.append('q','general', self.ef_pulse_type,amp=self.expt_cfg['a'],length = 59.6159, freq=self.ef_sideband_freq)
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length=pt)
        self.psb.append('q:mm','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.flux_freq)
        self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q','general', "gauss" ,amp = 1,length = 59.6159, freq=self.ef_sideband_freq)

class MultimodeT1Sequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        self.multimode_cfg = cfg['multimodes']
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
        self.psb.append('q,mm1','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.multimode_cfg[1]['flux_pi_length'])
        self.psb.idle(pt)
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['pi_sb_ge'])
        self.psb.append('q,mm1','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.multimode_cfg[1]['flux_pi_length'],phase = 360.0*(self.multimode_cfg[1]['dc_offset_freq_ge'])*pt/(1e9))
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
        #self.psb.append('q','general', self.pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.expt_cfg['iq_freq'])

        # Test of phase with 2pi sideband rotation with variation of the amplitude of guassian pulses

        #self.psb.append('q','general', self.pulse_type, amp=float(pt)/float(self.expt_cfg['stop']), length=100,freq=self.expt_cfg['iq_freq'])
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= 184, phase=0)
        #self.psb.append('q','general', self.pulse_type, amp=float(pt)/float(self.expt_cfg['stop']), length=100,freq=self.expt_cfg['iq_freq'])
        #print float(pt)/float(self.expt_cfg['stop'])



        # Phase from 2pi ef rotation

       #self.psb.append('q','pi', self.pulse_type)
       #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= pt, phase=0)
       #self.psb.append('q','general', "gauss" ,amp = 1,length = 50, freq=self.ef_sideband_freq)
        #self.psb.idle(110)
        #self.psb.append('q','general', "gauss" ,amp = 1,length = 110, freq=self.ef_sideband_freq)
       #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= pt, phase=0)

        #self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= pt)
        #self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= pt)

        self.psb.append('q','general', self.pulse_type, amp=self.expt_cfg['a'], length= 10.25,freq=self.expt_cfg['iq_freq'])
        # self.psb.idle(10*1.41)
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length=80, phase=0 )



        #C-phase
        #self.psb.append('q','general', "gauss" ,amp = 1,length = 24, freq=self.ef_sideband_freq)
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= 184, phase= 0)
        #self.psb.append('q','general', "gauss" ,amp = 1,length = 24, freq=self.ef_sideband_freq)
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= self.multimode_cfg[1]['flux_pi_length'] , phase= 360.0*(self.multimode_cfg[1]['dc_offset_freq_ge'])*24*6/(1e9))
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= self.multimode_cfg[0]['flux_pi_length'] )
        #self.psb.append('q','general', "gauss" ,amp = 1,length = 54, freq=self.ef_sideband_freq)
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length=80, phase=0 )
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= 180)
        #self.psb.append('q','general', "gauss" ,amp = 1,length = 54, freq=self.ef_sideband_freq)
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= self.multimode_cfg[1]['flux_pi_length'], phase=0)
        self.psb.append('q','general', self.pulse_type, amp=self.expt_cfg['a'], length=10.25,freq=self.expt_cfg['iq_freq'],phase= pt)


        #self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= (2*self.multimode_cfg[1]['flux_pi_length']-pt)%(2*self.multimode_cfg[1]['flux_pi_length']), phase = 0)
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= pt, phase = 180)
        #self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a_ef'], length= 2*self.multimode_cfg[1]['flux_pi_length_ef'], freq= self.multimode_cfg[1]['flux_pulse_freq_ef'])
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= (self.multimode_cfg[1]['flux_pi_length_ef']- pt)%)


        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length=  self.multimode_cfg[1]['flux_pi_length'])
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp= self.multimode_cfg[0]['a'], length=  self.multimode_cfg[0]['flux_pi_length'])
        #self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length=  self.multimode_cfg[1]['flux_pi_length'])