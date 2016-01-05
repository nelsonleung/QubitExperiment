__author__ = 'Nelson'

from slab.instruments.awg.PulseSequence import *
from numpy import arange, linspace, sin, pi, sign, append
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
        self.id = self.expt_cfg['id']

    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=pt)

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
        self.id = self.expt_cfg['id']
        self.phase_freq = self.multimode_cfg[int(self.id)]['dc_offset_freq'] + self.expt_cfg['ramsey_freq']
        #print self.expt_cfg['iq_freq']

    def define_pulses(self,pt):
        ##to do: change the index of mm easier
        self.psb.append('q','half_pi', self.pulse_type)
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=  self.multimode_cfg[int(self.id)]['flux_pi_length'])
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=0, length= pt)
        # self.psb.idle(0)
        self.psb.idle(pt)
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['pi_sb_ge'])
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(+self.id)]['a'], length= self.multimode_cfg[int(self.id)]['flux_pi_length'],phase = 360.0*self.phase_freq*pt/(1.0e9) )
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
        self.id = self.expt_cfg['id']

    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        #self.psb.append('q,mm0','pi', self.pulse_type)
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(+self.id)]['a'], length= self.multimode_cfg[int(self.id)]['flux_pi_length'])
        self.psb.idle(pt)
        #self.psb.append('q,mm0','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length= self.expt_cfg['pi_sb_ge'])
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(+self.id)]['a'], length= self.multimode_cfg[int(self.id)]['flux_pi_length'],phase= 360.0*self.multimode_cfg[int(self.id)]['dc_offset_freq']*pt/(1.0e9))
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


    def define_pulses(self,pt):
        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length= pt)
        self.psb.append('q,mm6','general', self.flux_pulse_type, amp= self.multimode_cfg[6]['a'], length=  self.multimode_cfg[6]['flux_pi_length'])
        # self.psb.append('q,mm1','general', self.flux_pulse_type, amp= self.multimode_cfg[1]['a'], length=  self.multimode_cfg[1]['flux_pi_length'])
        self.psb.append('q,mm6','general', self.flux_pulse_type, amp= self.multimode_cfg[6]['a'], length=  self.multimode_cfg[6]['flux_pi_length'])



class MultimodeCPhaseTestsSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        self.multimode_cfg = cfg['multimodes']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)


    def define_points(self):
        if self.expt_cfg["tomography"]:
            self.expt_pts = np.array([0,1,2])
        else:
            self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']
        self.ef_pulse_type = self.expt_cfg['ef_pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq)
        self.id1 = self.expt_cfg['id1']
        self.id2 = self.expt_cfg['id2']
        self.id = self.expt_cfg['id']



    def define_pulses(self,pt):

        if self.expt_cfg["tomography"]:
            par = self.expt_cfg["time_slice"]
        else:
            par = pt

        # Test of phase with 2pi sideband rotation with variation of the length of guassian qubit drive pulse

        if self.expt_cfg["test_2pisideband"]:
            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
            self.psb.idle(100)
            if self.expt_cfg["include_2pisideband"]:
                self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_2pi_length'])
            if self.expt_cfg["include_theta_offset_phase"]:
               self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'], phase = self.multimode_cfg[int(self.id)]['2pi_offset_phase'] )
            else:
                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'], phase = 180)

        # Finding offset phase for second theta pulse due to the 2pi sideband

        if self.expt_cfg["find_2pi_sideband_offset"]:
            self.psb.append('q','general', self.pulse_type, amp=1, length=self.expt_cfg['theta_length'], freq=self.expt_cfg['iq_freq'])
            self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_2pi_length'])
            self.psb.append('q','general', self.pulse_type, amp=1, length=self.expt_cfg['theta_length'], freq=self.expt_cfg['iq_freq'],phase=pt)


        #  Finding offset phase for second theta pulse due 2 pi sidebands

        if self.expt_cfg["find_pi_pi_sideband_offset"]:
            self.psb.append('q','general', self.pulse_type, amp=1, length=self.expt_cfg['theta_length'], freq=self.expt_cfg['iq_freq'])
            self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])
            self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])
            self.psb.append('q','general', self.pulse_type, amp=1, length=self.expt_cfg['theta_length'], freq=self.expt_cfg['iq_freq'],phase = pt)


        # Testing 2pi ef rotation
        if self.expt_cfg["test_2pi_ef_rotation"]:
            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
            # self.psb.append('q','general', self.ef_pulse_type, amp=1, length=self.expt_cfg['2pi_ef_length'],freq=self.ef_sideband_freq)
            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])


        # Is there an offset phase required for the second theta pulse for 2pi ef tests

        if self.expt_cfg["find_2pi_ef_offset"]:
            self.psb.append('q','general', self.pulse_type, amp=1, length=self.expt_cfg['theta_length'], freq=self.expt_cfg['iq_freq'])
            self.psb.append('q','general', self.ef_pulse_type, amp=1, length=self.expt_cfg['2pi_ef_length'],freq=self.ef_sideband_freq)
            self.psb.append('q','general', self.pulse_type, amp=1, length=self.expt_cfg['theta_length'], freq=self.expt_cfg['iq_freq'], phase = pt)


        if self.expt_cfg["test_cphase"]:

        #State preparation

            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
            self.psb.append('q,mm'+str(self.id1),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id1)]['a'], length=self.multimode_cfg[int(self.id1)]['flux_pi_length'])

            # cum_phase1 = 0
            # cum_phase2 = 0
        # Cphase Gate
            if self.expt_cfg["cphase_on"]:
                # cum_phase2 += 360*(self.multimode_cfg[int(self.id1)]['flux_pi_length'] + 6*10)*self.multimode_cfg[int(self.id2)]['dc_offset_freq']/(1.0e9)
                self.psb.append('q,mm'+str(self.id2),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id2)]['a'], length=self.multimode_cfg[int(self.id2)]['flux_pi_length'])

                self.psb.append('q','general', self.ef_pulse_type, amp=1, length=self.expt_cfg['pi_ef_length'],freq=self.ef_sideband_freq)
                # cum_phase1 += 360*(self.expt_cfg['pi_ef_length']+ 12*10 + self.multimode_cfg[int(self.id2)]['flux_pi_length'])*self.multimode_cfg[int(self.id1)]['dc_offset_freq']/(1.0e9) + (self.multimode_cfg[int(self.id1)]['pi_pi_offset_phase'])

                self.psb.append('q,mm'+str(self.id1),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id1)]['a'], length=self.multimode_cfg[int(self.id1)]['flux_2pi_length'])
                # cum_phase1 += (self.multimode_cfg[int(self.id1)]['pi_pi_offset_phase'])

                # self.psb.append('q,mm'+str(self.id1),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id1)]['a'], length=self.multimode_cfg[int(self.id1)]['flux_pi_length'])
                self.psb.append('q','general', self.ef_pulse_type, amp=1, length=self.expt_cfg['pi_ef_length'],freq=self.ef_sideband_freq)
                # cum_phase2 += 360*(2*self.expt_cfg['pi_ef_length']+24*10 + 2*self.multimode_cfg[int(self.id1)]['flux_pi_length'])*self.multimode_cfg[int(self.id2)]['dc_offset_freq']/(1.0e9) + (self.multimode_cfg[int(self.id2)]['pi_pi_offset_phase'])

                self.psb.append('q,mm'+str(self.id2),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id2)]['a'], length=self.multimode_cfg[int(self.id2)]['flux_pi_length'])
                # cum_phase1 +=  360*(self.expt_cfg['pi_ef_length']+ 12*10 + self.multimode_cfg[int(self.id2)]['flux_pi_length'])*self.multimode_cfg[int(self.id1)]['dc_offset_freq']/(1.0e9) + (self.multimode_cfg[int(self.id1)]['pi_pi_offset_phase'])


        #Reversing State preparation


            self.psb.append('q,mm'+str(self.id1),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id1)]['a'], length=self.multimode_cfg[int(self.id1)]['flux_pi_length'])
            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'], phase = self.multimode_cfg[int(self.id1)]['pi_pi_offset_phase'])


        # Tomography at a given time slice

        if self.expt_cfg["tomography"]:
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



class MultimodePi_PiSequence(QubitPulseSequence):
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
        self.id1 = self.expt_cfg['id1']
        self.id2 = self.expt_cfg['id2']
        self.id = self.expt_cfg['id']



    def define_pulses(self,pt):

        self.psb.append('q','half_pi', self.pulse_type)
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])
        self.psb.append('q','half_pi', self.pulse_type, phase = pt)

        # Tomography at a given time slice


