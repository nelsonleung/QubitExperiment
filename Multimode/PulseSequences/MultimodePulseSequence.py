__author__ = 'Nelson'

from slab.instruments.awg.PulseSequence import *
from numpy import arange, linspace, sin, pi, sign, append
from slab.experiments.ExpLib.PulseSequenceBuilder import *
from slab.experiments.ExpLib.QubitPulseSequence import *
from slab.experiments.ExpLib.PulseSequenceGroup import *

from liveplot import LivePlotClient


class MultimodeRabiSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.multimode_cfg = cfg['multimodes']
        # self.pulse_cfg = cfg['pulse_info']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.id = self.expt_cfg['id']
        self.flux_pulse_type = self.multimode_cfg[int(self.id)]['flux_pulse_type']

    def define_pulses(self,pt):
        # self.psb.append('q','pi', self.pulse_type)
        # self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length= self.multimode_cfg[int(self.id)]['flux_pi_length'])
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
        self.psb.append('q','general', self.pulse_type ,amp = self.pulse_cfg[self.pulse_type]['pi_ef_a'],length = self.pulse_cfg[self.pulse_type]['pi_ef_length'], freq=self.ef_sideband_freq)
        self.psb.append('q:mm','general', self.flux_pulse_type, amp=self.expt_cfg['a'], length=pt,freq=self.expt_cfg['freq'])
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
        self.id = self.expt_cfg['id']
        self.flux_pulse_type = self.multimode_cfg[int(self.id)]['flux_pulse_type']
        self.phase_freq = self.multimode_cfg[int(self.id)]['dc_offset_freq'] + self.expt_cfg['ramsey_freq']
        #print self.expt_cfg['iq_freq']

    def define_pulses(self,pt):
        ##to do: change the index of mm easier
        self.psb.append('q','half_pi', self.pulse_type)
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=  self.multimode_cfg[int(self.id)]['flux_pi_length'])
        self.psb.idle(pt)
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(+self.id)]['a'], length= self.multimode_cfg[int(self.id)]['flux_pi_length'],phase = 360.0*self.phase_freq*pt/(1.0e9) )

        self.psb.append('q','half_pi', self.pulse_type)#, phase= self.pulse_cfg[self.pulse_type]['phase'])


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
        self.psb.append('q','general', "gauss" ,amp = 1,length = self.expt_cfg['pi_ef_length'], freq=self.ef_sideband_freq)
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
        self.id = self.expt_cfg['id']
        self.flux_pulse_type = self.multimode_cfg[int(self.id)]['flux_pulse_type']

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
        self.id1 = self.expt_cfg['id1']
        self.id2 = self.expt_cfg['id2']
        self.idm = self.expt_cfg['idm']


    def define_pulses(self,pt):

        self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q,mm'+str(self.id1),'general', self.flux_pulse_type, amp= self.multimode_cfg[int(self.id1)]['a'], length= pt, phase=180)
        if self.expt_cfg['GHZ']:
           self.psb.append('q','pi', self.pulse_type)
        self.psb.append('q,mm'+str(self.id2),'general', self.flux_pulse_type, amp= self.multimode_cfg[int(self.id2)]['a'], length=  self.multimode_cfg[int(self.id2)]['flux_pi_length'], phase=180)
        self.psb.append('q,mm'+str(self.idm),'general', self.flux_pulse_type, amp= self.multimode_cfg[int(self.idm)]['a'], length=  self.multimode_cfg[int(self.idm)]['flux_pi_length'])



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
        self.idef = self.expt_cfg['idef']
        self.half_pi_offset = self.pulse_cfg[self.pulse_type]['offset_phase']


    def define_pulses(self,pt):

        if self.expt_cfg["tomography"]:
            par = self.expt_cfg["time_slice"]
        else:
            if self.expt_cfg["slice"]:
                par = self.expt_cfg["time_slice"]
            else:
                par = pt

        # Test of phase with 2pi sideband rotation with variation of the length of guassian qubit drive pulse

        if self.expt_cfg["test_2pisideband"]:
            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
            # self.psb.idle(100)
            if self.expt_cfg["include_2pisideband"]:
                # self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_2pi_length'])
                self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])
                self.psb.idle(100)
                self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'], phase = self.multimode_cfg[int(self.id)]['pi_pi_offset_phase'])
                self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])
                self.psb.idle(100)
                self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'], phase = self.multimode_cfg[int(self.id)]['pi_pi_offset_phase'])

            if self.expt_cfg["include_theta_offset_phase"]:
               self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'], phase = self.multimode_cfg[int(self.id)]['2pi_offset_phase'] )
            else:
                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'], phase = 0)

        # Finding offset phase for second theta pulse due to the 2pi sideband

        if self.expt_cfg["find_2pi_sideband_offset"]:
            self.psb.append('q','general', self.pulse_type, amp=1, length=self.expt_cfg['theta_length'], freq=self.expt_cfg['iq_freq'])
            self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_2pi_length'])
            self.psb.append('q','general', self.pulse_type, amp=1, length=self.expt_cfg['theta_length'], freq=self.expt_cfg['iq_freq'],phase=pt)


        #  Finding offset phase for second theta pulse due 2 pi sidebands

        if self.expt_cfg["find_pi_pi_sideband_offset"]:
            self.psb.append('q','half_pi',self.pulse_type)
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.idle(self.expt_cfg["pi_pi_idle"])
            self.psb.append('q,mm'+str(self.id),'pi_ge', phase=pt)
            self.psb.append('q','half_pi',self.pulse_type, self.half_pi_offset)


        # Testing 2pi ef rotation
        if self.expt_cfg["test_2pi_ef_rotation"]:

            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
            self.psb.append('q','general', self.ef_pulse_type, amp=1, length=self.expt_cfg['pi_ef_length'],freq=self.ef_sideband_freq)
            self.psb.idle(100)
            # self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])
            # self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])
            self.psb.append('q','general', self.ef_pulse_type, amp=1, length=self.expt_cfg['pi_ef_length'],freq=self.ef_sideband_freq, phase =self.expt_cfg['pi_ef_offset'] )
            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])

        if self.expt_cfg["test_ef_with_resonator_loaded"]:

            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])

            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q','general', self.ef_pulse_type, amp=1, length=par ,freq=self.ef_sideband_freq)
            self.psb.append('q','pi', self.pulse_type)


        if self.expt_cfg["find_2pi_ef_offset"]:
            self.psb.append('q','half_pi', self.pulse_type)
            self.psb.append('q','general', self.ef_pulse_type, amp=1, length=self.expt_cfg['pi_ef_length'],freq=self.ef_sideband_freq)
            self.psb.idle(138)
            self.psb.append('q','general', self.ef_pulse_type, amp=1, length=self.expt_cfg['pi_ef_length'],freq=self.ef_sideband_freq, phase = pt)
            self.psb.append('q','half_pi', self.pulse_type, self.half_pi_offset)

        if self.expt_cfg["test_2pi_ef_sideband_rotation"]:

            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])
            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.idef),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.idef)]['a'], length=par)
            self.psb.append('q','pi', self.pulse_type)


        if self.expt_cfg["test_cphase"]:

        #State preparation
            if  self.expt_cfg["prepare_state"] == 0:

                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
                self.psb.append('q,mm'+str(self.id1),'pi_ge')

            if  self.expt_cfg["prepare_state"] == 1:

                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
                self.psb.append('q,mm'+str(self.id2),'pi_ge')

            if  self.expt_cfg["prepare_state"] == 2:

                self.psb.append('q','pi', self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'pi_ge')
                self.psb.append('q','pi', self.pulse_type)
                self.psb.append('q,mm'+str(self.id2),'pi_ge')

            if  self.expt_cfg["prepare_state"] == 3:
                self.psb.append('q','pi', self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'pi_ge')
                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
                self.psb.append('q,mm'+str(self.id2),'pi_ge')

            # <XZ>

            if  self.expt_cfg["prepare_state"] == 4:
                self.psb.append('q','half_pi_y', self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'pi_ge')
                self.psb.append('q,mm'+str(self.id2),'pi_ge')


        # Cphase Gate



            if self.expt_cfg["cphase_on"]:

                if self.expt_cfg["cphase_type"]==0:


                    self.psb.append('q,mm'+str(self.id2),'pi_ge')
                    self.psb.append('q','general', self.ef_pulse_type, amp=1, length=self.expt_cfg['pi_ef_length'],freq=self.ef_sideband_freq)
                    self.psb.append('q,mm'+str(self.id1),'pi_ge')
                    self.psb.append('q,mm'+str(self.id1),'pi_ge')
                    self.psb.append('q','general', self.ef_pulse_type, amp=1, length=self.expt_cfg['pi_ef_length'],freq=self.ef_sideband_freq, phase = self.expt_cfg['pi_ef_offset'] )
                    self.psb.append('q,mm'+str(self.id2),'pi_ge')

                if self.expt_cfg["cphase_type"]==1:

                    cphase(self.psb,self.id1,self.id2)


            else:
                self.psb.idle(self.expt_cfg['no_cphase_idle'])

        #Reversing State preparation

            if  self.expt_cfg["prepare_state"] == 0:
                self.psb.append('q,mm'+str(self.id1),'pi_ge', phase = pt )
                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])

            if  self.expt_cfg["prepare_state"] == 1:
                self.psb.append('q,mm'+str(self.id2),'pi_ge', phase =   pt )
                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])

            if  self.expt_cfg["prepare_state"] == 2:

                pass

            if  self.expt_cfg["prepare_state"] == 3:
                self.psb.append('q,mm'+str(self.id2),'pi_ge', phase = pt)
                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])

            if  self.expt_cfg["prepare_state"] == 4:
                self.psb.append('q,mm'+str(self.id1),'pi_ge', phase = pt)
                self.psb.append('q','half_pi_y', self.pulse_type)

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

class MultimodeCPhaseSequence(QubitPulseSequence):
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
        self.idef = self.expt_cfg['idef']
        self.half_pi_offset = self.pulse_cfg[self.pulse_type]['offset_phase']
        self.halfpicounter1 = 0
        self.halfpicounter2 = 0


    def define_pulses(self,pt):

        if self.expt_cfg["tomography"]:
            par = self.expt_cfg["time_slice"]
        else:
            if self.expt_cfg["slice"]:
                par = self.expt_cfg["time_slice"]
            else:
                par = pt


        if self.expt_cfg["test_cphase"]:

        #State preparation
            if  self.expt_cfg["prepare_state"] == 0:

                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
                self.psb.append('q,mm'+str(self.id1),'pi_ge')

            if  self.expt_cfg["prepare_state"] == 1:

                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
                self.psb.append('q,mm'+str(self.id2),'pi_ge')

            if  self.expt_cfg["prepare_state"] == 2:

                self.psb.append('q','pi', self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'pi_ge')
                self.psb.append('q','pi', self.pulse_type)
                self.psb.append('q,mm'+str(self.id2),'pi_ge')

            if  self.expt_cfg["prepare_state"] == 3:
                self.psb.append('q','pi', self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'pi_ge')
                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
                self.psb.append('q,mm'+str(self.id2),'pi_ge')

            # <XZ>

            if  self.expt_cfg["prepare_state"] == 4:
                self.halfpicounter1 = 0
                self.halfpicounter2 = 0
                self.psb.append('q','half_pi_y', self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'pi_ge')
                self.halfpicounter1+=1
                # self.psb.idle(168.5)
                # self.psb.append('q','pi',self.pulse_type)
                # self.psb.append('q,mm'+str(self.id2),'pi_ge')

            # <YZ>

            if  self.expt_cfg["prepare_state"] == 5:
                self.halfpicounter1 = 0
                self.halfpicounter2 = 0

                self.psb.append('q','half_pi', self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'pi_ge')
                self.halfpicounter1+=1
                self.psb.append('q','pi',self.pulse_type)
                self.psb.append('q,mm'+str(self.id2),'pi_ge')


            #<ZX>

            if  self.expt_cfg["prepare_state"] == 6:
                self.halfpicounter1 = 0
                self.halfpicounter2 = 0
                self.psb.append('q','half_pi_y', self.pulse_type)
                self.psb.append('q,mm'+str(self.id2),'pi_ge')
                self.halfpicounter2+=1
                self.psb.append('q','pi',self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'pi_ge')

            #<ZY>

            if  self.expt_cfg["prepare_state"] == 7:
                self.halfpicounter1 = 0
                self.halfpicounter2 = 0
                self.psb.append('q','half_pi', self.pulse_type)
                self.psb.append('q,mm'+str(self.id2),'pi_ge')
                self.halfpicounter2+=1
                self.psb.append('q','pi',self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'pi_ge')

            #<IX>
            if  self.expt_cfg["prepare_state"] == 8:
                self.halfpicounter1 = 0
                self.halfpicounter2 = 0
                self.psb.append('q','half_pi_y', self.pulse_type)
                self.psb.append('q,mm'+str(self.id2),'pi_ge')
                self.halfpicounter2+=1
                self.psb.append('q','pi',self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'pi_ge')

            #phi bell
            if  self.expt_cfg["prepare_state"] == 9:
                self.halfpicounter1 = 0
                self.halfpicounter2 = 0
                self.psb.append('q','pi', self.pulse_type)
                self.psb.append('q,mm'+str(self.id1),'general', self.flux_pulse_type, amp= self.multimode_cfg[int(self.id1)]['a'], length= self.expt_cfg['time_slice'], phase=180)
                self.psb.append('q','pi', self.pulse_type)
                self.psb.append('q,mm'+str(self.id2),'pi_ge', phase=180)



        # Cphase Gate


            if self.expt_cfg["cphase_on"]:

                cphase(self.psb,self.id1,self.id2)

            else:
                self.psb.idle(self.expt_cfg['no_cphase_idle'])

        #Reversing State preparation

            if  self.expt_cfg["measure_state"] == 0:
                self.psb.append('q,mm'+str(self.id1),'pi_ge', phase = pt )
                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])

            if  self.expt_cfg["measure_state"] == 1:
                self.psb.append('q,mm'+str(self.id2),'pi_ge', phase =   pt )
                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])

            if  self.expt_cfg["measure_state"] == 2:
                pass

            if  self.expt_cfg["measure_state"] == 3:
                self.psb.append('q,mm'+str(self.id2),'pi_ge', phase = pt)
                self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])

            #<XZ>
            if  self.expt_cfg["measure_state"] == 4:
                self.psb.append('q,mm'+str(self.id1),'pi_ge', phase = self.expt_cfg['final_offset'] + pt)
                self.psb.append('q','half_pi_y', self.pulse_type, phase = 90 + self.halfpicounter1*self.half_pi_offset)
            #<YZ>
            if  self.expt_cfg["measure_state"] == 5:
                self.psb.append('q,mm'+str(self.id1),'pi_ge', phase = self.expt_cfg['final_offset'] + pt)
                self.psb.append('q','half_pi', self.pulse_type, phase = self.halfpicounter1*self.half_pi_offset)
            #<ZX>
            if  self.expt_cfg["measure_state"] == 6:
                self.psb.append('q,mm'+str(self.id2),'pi_ge', phase = self.expt_cfg['final_offset2'] + pt)
                self.psb.append('q','half_pi_y', self.pulse_type, phase = 90 + self.halfpicounter2*self.half_pi_offset)
            #<ZY>
            if  self.expt_cfg["measure_state"] == 7:
                self.psb.append('q,mm'+str(self.id2),'pi_ge', phase = self.expt_cfg['final_offset2'] + pt)
                self.psb.append('q','half_pi', self.pulse_type, phase = self.halfpicounter2*self.half_pi_offset)

            #<IX>
            if  self.expt_cfg["measure_state"] == 8:
                self.psb.append('q,mm'+str(self.id2),'pi_ge', phase = self.expt_cfg['final_offset_t'] + pt)
                self.psb.append('q','half_pi_y', self.pulse_type, phase = self.halfpicounter2*self.half_pi_offset)

            #<IY>
            if  self.expt_cfg["measure_state"] == 9:
                self.psb.append('q,mm'+str(self.id2),'pi_ge', phase = self.expt_cfg['final_offset_t'] + pt)
                self.psb.append('q','half_pi', self.pulse_type, phase = self.halfpicounter2*self.half_pi_offset)

            #<IZ>
            if  self.expt_cfg["measure_state"] == 10:
                self.psb.append('q,mm'+str(self.id2),'pi_ge', phase = self.expt_cfg['final_offset_t'] + pt)

            #<XI>
            if  self.expt_cfg["measure_state"] == 11:
                self.psb.append('q,mm'+str(self.id1),'pi_ge', phase = self.expt_cfg['final_offset_t'] + pt)
                self.psb.append('q','half_pi_y', self.pulse_type, phase = self.halfpicounter1*self.half_pi_offset)
            #<YI>
            if  self.expt_cfg["measure_state"] == 12:
                self.psb.append('q,mm'+str(self.id1),'pi_ge', phase = self.expt_cfg['final_offset_t'] + pt)
                self.psb.append('q','half_pi', self.pulse_type, phase = self.halfpicounter1*self.half_pi_offset)

             #<ZI>
            if  self.expt_cfg["measure_state"] == 13:
                self.psb.append('q,mm'+str(self.id1),'pi_ge', phase = self.expt_cfg['final_offset_t'] + pt)
                self.psb.append('q','half_pi', self.pulse_type, phase = self.halfpicounter1*self.half_pi_offset)



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

class MultimodeCNOTSequence(QubitPulseSequence):
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
        self.idef = self.expt_cfg['idef']
        self.half_pi_offset = self.pulse_cfg[self.pulse_type]['offset_phase']
        self.halfpicounter1 = 0
        self.halfpicounter2 = 0



    def define_pulses(self,pt):

        if self.expt_cfg["tomography"]:
            par = self.expt_cfg["time_slice"]
        else:
            if self.expt_cfg["slice"]:
                par = self.expt_cfg["time_slice"]
            else:
                par = pt


        #State preparation
        if  self.expt_cfg["prepare_state"] == 0:

            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
            self.psb.append('q,mm'+str(self.id1),'pi_ge')

        if  self.expt_cfg["prepare_state"] == 1:

            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
            self.psb.append('q,mm'+str(self.id2),'pi_ge')

        if  self.expt_cfg["prepare_state"] == 2:

            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id2),'pi_ge')

        if  self.expt_cfg["prepare_state"] == 3:
            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])
            self.psb.append('q,mm'+str(self.id2),'pi_ge')

        # <XX>

        if  self.expt_cfg["prepare_state"] == 4:
            self.halfpicounter1 = 0
            self.halfpicounter2 = 0

            self.psb.append('q','half_pi_y', self.pulse_type)
            self.halfpicounter1 +=1
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q','half_pi_y', self.pulse_type)
            self.halfpicounter2 +=1
            self.psb.append('q,mm'+str(self.id2),'pi_ge')


        # <XY>
        if  self.expt_cfg["prepare_state"] == 5:
            self.halfpicounter1 = 0
            self.halfpicounter2 = 0

            self.psb.append('q','half_pi_y', self.pulse_type)
            self.halfpicounter1 +=1
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q','half_pi', self.pulse_type, phase=0)
            self.halfpicounter2 +=1
            self.psb.append('q,mm'+str(self.id2),'pi_ge')

        # <YX>
        if  self.expt_cfg["prepare_state"] == 6:
            self.halfpicounter1 = 0
            self.halfpicounter2 = 0

            self.psb.append('q','half_pi', self.pulse_type)
            self.halfpicounter1 +=1
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q','half_pi_y', self.pulse_type)
            self.halfpicounter2 +=1
            self.psb.append('q,mm'+str(self.id2),'pi_ge')

        # <YY>
        if  self.expt_cfg["prepare_state"] == 7:
            self.halfpicounter1 = 0
            self.halfpicounter2 = 0

            self.psb.append('q','half_pi', self.pulse_type)
            self.halfpicounter1 +=1
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q','half_pi', self.pulse_type)
            self.halfpicounter2 +=1
            self.psb.append('q,mm'+str(self.id2),'pi_ge')

         # <ZZ>
        if  self.expt_cfg["prepare_state"] == 8:
            self.halfpicounter1 = 0
            self.halfpicounter2 = 0

            self.psb.append('q','pi')
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q','pi')
            self.psb.append('q,mm'+str(self.id2),'pi_ge')

        #phi bell
        if  self.expt_cfg["prepare_state"] == 9:
            self.halfpicounter1 = 0
            self.halfpicounter2 = 0
            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id1),'general', self.flux_pulse_type, amp= self.multimode_cfg[int(self.id1)]['a'], length= self.expt_cfg['time_slice'], phase=180)
            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id2),'pi_ge', phase=0)

        #psi bell
        if  self.expt_cfg["prepare_state"] == 10:
            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id1),'general', self.flux_pulse_type, amp= self.multimode_cfg[int(self.id1)]['a'], length= self.expt_cfg['time_slice'])
            self.psb.append('q,mm'+str(self.id2),'pi_ge')

        # CNOT Gate

        if self.expt_cfg["cnot_on"]:

            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q','pi_q_ef', phase=self.expt_cfg['pi_ef_offset'] )
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q,mm'+str(self.id1),'pi_ge',phase=180)

        elif self.expt_cfg["cy_on"]:

            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q','pi_q_ef', phase=self.expt_cfg['pi_ef_offset'] + 90)
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q,mm'+str(self.id1),'pi_ge',phase=180)

        else:
            self.psb.idle(self.expt_cfg['no_cnot_idle'])

        #Reversing State preparation

        if  self.expt_cfg["measure_state"] == 0:
            self.psb.append('q,mm'+str(self.id2),'pi_ge', phase = pt )
            # self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])

        if  self.expt_cfg["measure_state"] == 1:
            self.psb.append('q,mm'+str(self.id2),'pi_ge', phase =   pt )
            self.psb.append('q','general', self.pulse_type, amp=1, length=par, freq=self.expt_cfg['iq_freq'])

        if  self.expt_cfg["measure_state"] == 2:
            pass

        if  self.expt_cfg["measure_state"] == 3:
            self.psb.append('q,mm'+str(self.id2),'pi_ge', phase = 0)
 # <XX>
        if  self.expt_cfg["measure_state"] == 4:
            self.psb.append('q,mm'+str(self.id1),'pi_ge', phase=self.expt_cfg['final_offset'] +pt  )
            self.psb.append('q','half_pi_y', self.pulse_type, phase= self.halfpicounter1*self.half_pi_offset  + 90)

 # <XY>
        if  self.expt_cfg["measure_state"] == 5:
            self.psb.append('q,mm'+str(self.id1),'pi_ge', phase=self.expt_cfg['final_offset'] + pt)
            self.psb.append('q','half_pi_y', self.pulse_type, phase= self.halfpicounter1*self.half_pi_offset  + 90)
 # <YX>
        if  self.expt_cfg["measure_state"] == 6:
            self.psb.append('q,mm'+str(self.id1),'pi_ge', phase=self.expt_cfg['final_offset'] + pt)
            self.psb.append('q','half_pi', self.pulse_type, phase= self.halfpicounter1*self.half_pi_offset)
 # <YY>
        if  self.expt_cfg["measure_state"] == 7:
            self.psb.append('q,mm'+str(self.id1),'pi_ge', phase=self.expt_cfg['final_offset'] + pt)
            self.psb.append('q','half_pi', self.pulse_type, phase= self.halfpicounter1*self.half_pi_offset)
 # <ZZ>
        if  self.expt_cfg["measure_state"] == 8:
            self.psb.append('q,mm'+str(self.id2),'pi_ge', phase=self.expt_cfg['final_offset2'] + pt)


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
        self.half_pi_offset = self.pulse_cfg[self.pulse_type]['y_phase']-90


    def define_pulses(self,pt):

        self.psb.append('q','half_pi', self.pulse_type)
        #self.psb.idle(2*self.multimode_cfg[int(self.id)]['flux_pi_length']+18.0*2.0)
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'])
        self.psb.idle(100)
        self.psb.append('q,mm'+str(self.id),'general', self.flux_pulse_type, amp=self.multimode_cfg[int(self.id)]['a'], length=self.multimode_cfg[int(self.id)]['flux_pi_length'], phase = pt)
        self.psb.append('q','half_pi', self.pulse_type, phase=self.half_pi_offset)

        # Tomography at a given time slice

class CPhaseOptimizationSweepSequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        self.multimode_cfg = cfg['multimodes']
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
            #print str(key) + ": " + str(value)
        self.idle_time = self.extra_args['idle_time']

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
        self.half_pi_offset = self.pulse_cfg[self.pulse_type]['y_phase']-90


    def define_pulses(self,pt):

        self.psb.append('q','half_pi', self.pulse_type)
        # self.psb.append('q,mm'+str(self.id),'pi_ge')
        self.psb.idle(self.idle_time)
        # self.psb.append('q,mm'+str(self.id),'pi_ge', phase = pt)
        self.psb.append('q','half_pi', self.pulse_type, phase=pt)



class MultimodeSingleResonatorTomographySequence(QubitPulseSequence):
    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        self.multimode_cfg = cfg['multimodes']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)


    def define_points(self):
        ## we define
        self.states_num = 4
        self.operations_num = 1
        ## automauted
        self.tomography_pulse_num = 3

        sequence_num = self.states_num*self.operations_num*self.tomography_pulse_num
        self.expt_pts = np.arange(0,sequence_num)

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']
        self.id = self.expt_cfg['id']
        self.half_pi_offset = self.pulse_cfg[self.pulse_type]['y_phase']-90
        self.op_index =  self.expt_cfg['op_index']

    def define_pulses(self,pt):

        ### Initiate states
        self.define_states(pt)


    def define_states(self,pt):
        state_index = (pt/(self.tomography_pulse_num*self.operations_num)) % self.states_num
        if state_index == 0:
            # I
            pass
        elif state_index == 1:
            # Pi/2 X
            self.psb.append('q','half_pi', self.pulse_type)
        elif state_index == 2:
            # Pi/2 Y
            self.psb.append('q','half_pi_y', self.pulse_type)
        elif state_index == 3:
            # Pi X
            self.psb.append('q','pi', self.pulse_type)

        self.define_operations_pulse(pt)

    def define_operations_pulse(self,pt):
        # op_index = (pt/self.tomography_pulse_num) % self.operations_num
        op_index = self.op_index
        if op_index ==0:
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)

        if op_index ==1:
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)
            self.psb.append('q','half_pi', self.pulse_type, phase= 0)
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)

        if op_index ==2:
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)
            self.psb.append('q','half_pi_y', self.pulse_type, phase = self.half_pi_offset+self.pulse_cfg[self.pulse_type]['y_phase'])
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)



        self.define_tomography_pulse(pt)

    def define_tomography_pulse(self,pt):
        ### gates before measurement for tomography
        tomo_index = pt%self.tomography_pulse_num
        if tomo_index == 0:
            # <X>
            self.psb.append('q','half_pi', self.pulse_type, phase=self.half_pi_offset)
        elif tomo_index == 1:
            # <Y>
            self.psb.append('q','half_pi_y', self.pulse_type, phase = self.half_pi_offset+self.pulse_cfg[self.pulse_type]['y_phase']  )
        elif tomo_index == 2:
            # <Z>
            pass



class MultimodeTwoResonatorTomographySequence(QubitPulseSequence):

    def __init__(self,name, cfg, expt_cfg,**kwargs):
        self.qubit_cfg = cfg['qubit']
        self.pulse_cfg = cfg['pulse_info']
        self.multimode_cfg = cfg['multimodes']
        QubitPulseSequence.__init__(self,name, cfg, expt_cfg, self.define_points, self.define_parameters, self.define_pulses)


    def define_points(self):
        ## we define
        self.states_num = 1
        ## automauted
        self.tomography_pulse_num = 15

        sequence_num = self.states_num*self.tomography_pulse_num
        self.expt_pts = np.arange(0,sequence_num)

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']
        self.flux_pulse_type = self.expt_cfg['flux_pulse_type']
        self.ef_pulse_type = self.expt_cfg['ef_pulse_type']
        ef_freq = self.qubit_cfg['frequency']+self.qubit_cfg['alpha']
        self.ef_sideband_freq = self.pulse_cfg[self.pulse_type]['iq_freq']-(self.qubit_cfg['frequency']-ef_freq)
        self.id1 = self.expt_cfg['id1']
        self.id2 = self.expt_cfg['id2']
        self.id = self.expt_cfg['id']
        self.half_pi_offset = self.pulse_cfg[self.pulse_type]['offset_phase']
        self.state_index =  self.expt_cfg['state_index']
        self.halfpicounter1 = 0
        self.halfpicounter2 = 0

    def define_pulses(self,pt):

        ### Initiate states
        self.define_states(pt)

    def define_states(self,pt):
        state_index = self.state_index
        self.halfpicounter1=0
        self.halfpicounter2=0
        if state_index ==0:
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)

        if state_index ==1:

            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)
            self.psb.append('q','half_pi', self.pulse_type)
            self.halfpicounter1+=1
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)

        if state_index ==2:

            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)
            self.psb.append('q','half_pi_y', self.pulse_type)
            self.halfpicounter1+=1
            self.psb.append('q,mm'+str(self.id),'pi_ge')
            self.psb.append('q,mm'+str(self.id),'pi_ge',phase=35)

        if state_index ==3:
            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id1),'general', self.flux_pulse_type, amp= self.multimode_cfg[int(self.id1)]['a'], length= self.expt_cfg['time_slice'])
            self.psb.append('q,mm'+str(self.id2),'pi_ge')

        if state_index ==4:
            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id1),'general', self.flux_pulse_type, amp= self.multimode_cfg[int(self.id1)]['a'], length= self.expt_cfg['time_slice'],phase=180)
            self.psb.append('q','pi', self.pulse_type)
            self.psb.append('q,mm'+str(self.id2),'pi_ge',phase=0)

        self.define_tomography_pulse(pt)

    def define_tomography_pulse(self,pt):
        ### gates before measurement for two resonaotor tomography
        tomo_index = pt%self.tomography_pulse_num
        if tomo_index == 0:
            # -<IX>
            self.psb.append('q,mm'+str(self.id2),'pi_ge')
            self.psb.append('q','half_pi_y', self.pulse_type, phase = 90 + self.halfpicounter2*self.half_pi_offset)
            # self.halfpicounter2+=1
        elif tomo_index == 1:
            # <IY>
            self.psb.append('q,mm'+str(self.id2),'pi_ge')
            self.psb.append('q','half_pi', self.pulse_type, phase =  self.halfpicounter2*self.half_pi_offset)
            # self.halfpicounter2+=1
        elif tomo_index == 2:
            # <IZ>
            self.psb.append('q,mm'+str(self.id2),'pi_ge')
        elif tomo_index == 3:
            # -<XI>
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q','half_pi_y', self.pulse_type, phase = 90 + self.halfpicounter1*self.half_pi_offset)
            # self.halfpicounter2+=1
        elif tomo_index == 4:
            # <XX>

            #CNOT
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q','pi_q_ef', phase=self.expt_cfg['pi_ef_offset'])
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q,mm'+str(self.id1),'pi_ge',phase=180)

            self.psb.append('q,mm'+str(self.id1),'pi_ge', phase=self.expt_cfg['final_offset_not'])
            self.psb.append('q','half_pi_y', self.pulse_type, phase= self.halfpicounter1*self.half_pi_offset  + 90)

        elif tomo_index == 5:
            # -<XY>

            #CY
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q','pi_q_ef', phase=self.expt_cfg['pi_ef_offset']+90)
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q,mm'+str(self.id1),'pi_ge',phase=180)


            self.psb.append('q,mm'+str(self.id1),'pi_ge', phase=self.expt_cfg['final_offset_not'])
            self.psb.append('q','half_pi_y', self.pulse_type, phase= self.halfpicounter1*self.half_pi_offset  + 90)


        elif tomo_index == 6:
            # <XZ>
            cphase(self.psb,self.id1,self.id2)
            self.psb.append('q,mm'+str(self.id1),'pi_ge', phase=self.expt_cfg['final_offset_z'])
            self.psb.append('q','half_pi_y', self.pulse_type, phase= self.halfpicounter1*self.half_pi_offset  + 90)

        elif tomo_index == 7:
            # <YI>
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q','half_pi', self.pulse_type)
        elif tomo_index == 8:
            # -<YX>

            #CNOT
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q','pi_q_ef', phase=self.expt_cfg['pi_ef_offset'])
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q,mm'+str(self.id1),'pi_ge',phase=180)


            self.psb.append('q,mm'+str(self.id1),'pi_ge', phase=self.expt_cfg['final_offset_not'])
            self.psb.append('q','half_pi', self.pulse_type, phase= self.halfpicounter1*self.half_pi_offset)


        elif tomo_index == 9:
            # <YY>

            #CY
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q','pi_q_ef', phase=self.expt_cfg['pi_ef_offset']+90)
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q,mm'+str(self.id1),'pi_ge',phase=180)

            self.psb.append('q,mm'+str(self.id1),'pi_ge', phase=self.expt_cfg['final_offset_not'])
            self.psb.append('q','half_pi', self.pulse_type, phase= self.halfpicounter1*self.half_pi_offset)


        elif tomo_index == 10:
            # -<YZ>
            cphase(self.psb,self.id1,self.id2)
            self.psb.append('q,mm'+str(self.id1),'pi_ge',phase=self.expt_cfg['final_offset_z'])
            self.psb.append('q','half_pi', self.pulse_type, phase= self.halfpicounter1*self.half_pi_offset)
        elif tomo_index == 11:
            # <ZI>
            self.psb.append('q,mm'+str(self.id1),'pi_ge')
        elif tomo_index == 12:
            # <ZX>
            cphase(self.psb,self.id1,self.id2)
            self.psb.append('q,mm'+str(self.id2),'pi_ge',phase=self.expt_cfg['final_offset2_z'])
            self.psb.append('q','half_pi_y', self.pulse_type, phase= self.halfpicounter2*self.half_pi_offset + 90 )
        elif tomo_index == 13:
            # <ZY>
            cphase(self.psb,self.id1,self.id2)
            self.psb.append('q,mm'+str(self.id2),'pi_ge',phase=self.expt_cfg['final_offset2_z'])
            self.psb.append('q','half_pi', self.pulse_type,phase= self.halfpicounter2*self.half_pi_offset)
        elif tomo_index == 14:
            # <ZZ>

            self.psb.append('q,mm'+str(self.id1),'pi_ge')
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q','pi_q_ef', phase=self.expt_cfg['pi_ef_offset'])
            self.psb.append('q,mm'+str(self.id2),'pi_ef')
            self.psb.append('q,mm'+str(self.id1),'pi_ge',phase=180)

            self.psb.append('q,mm'+str(self.id2),'pi_ge', phase=self.expt_cfg['final_offset_not'])
