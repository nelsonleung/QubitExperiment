__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.experiments.ExpLib.QubitPulseSequenceExperiment import *
from numpy import mean, arange


class RabiExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Rabi', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=RabiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        self.drive.set_frequency(self.cfg['qubit']['frequency'] - self.cfg[self.expt_cfg_name]['iq_freq'])

    def post_run(self, expt_pts, expt_avg_data):
        if self.cfg[self.expt_cfg_name]['calibrate_pulse']:
            print "Analyzing Rabi Data"
            fitdata = fitdecaysin(expt_pts, expt_avg_data)

            pulse_type = self.cfg[self.expt_cfg_name]['pulse_type']
            # determine the start location of the rabi oscillation. +1 if it starts top; -1 if it starts bottom.
            start_signal = np.sign(180 - fitdata[2] % 360)
            if pulse_type is 'gauss':
                self.cfg['cal']['excited_signal'] = start_signal
            # time takes to have the rabi oscillation phase to +/- pi/2
            pi_length = (self.cfg['cal']['excited_signal'] * np.sign(fitdata[0]) * 0.5 * np.pi - fitdata[
                2] * np.pi / 180.) / (2 * np.pi * fitdata[1]) % (1 / fitdata[1])
            # time takes to have the rabi oscillation phase to 0/ pi
            half_pi_length = (self.cfg['cal']['excited_signal'] * np.sign(fitdata[0]) * np.pi - fitdata[
                2] * np.pi / 180.) / (2 * np.pi * fitdata[1]) % (0.5 / fitdata[1])

            from time import gmtime, strftime

            self.cfg['pulse_info'][pulse_type]['calibrated_time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            self.cfg['pulse_info'][pulse_type]['pi_length'] = pi_length
            self.cfg['pulse_info'][pulse_type]['half_pi_length'] = half_pi_length
            self.cfg['pulse_info'][pulse_type]['a'] = self.cfg[self.expt_cfg_name]['a']
            self.cfg['pulse_info'][pulse_type]['iq_freq'] = self.cfg[self.expt_cfg_name]['iq_freq']
            self.save_config()


class T1Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='T1', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=T1Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        pass

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing T1 Data"
        fitdata = fitexp(expt_pts, t1_avg_data)
        print "T1: " + str(fitdata[3]) + " ns"


class RamseyExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Ramsey', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=RamseySequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        self.drive.set_frequency(
            self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'] + self.cfg['ramsey'][
                'ramsey_freq'])

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing Ramsey Data"
        fitdata = fitdecaysin(expt_pts, expt_avg_data)
        suggested_qubit_freq = self.cfg['qubit']['frequency'] - (fitdata[1] * 1e9 - self.cfg['ramsey']['ramsey_freq'])
        print "Oscillation frequency: " + str(fitdata[1] * 1e3) + " MHz"
        print "T2*: " + str(fitdata[3]) + " ns"
        print "Suggested Qubit Frequency: " + str(suggested_qubit_freq)


class SpinEchoExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Spin_Echo', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=SpinEchoSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        self.drive.set_frequency(
            self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'] + self.cfg['ramsey'][
                'ramsey_freq'])

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing Spin Echo Data"
        fitdata = fitdecaysin(expt_pts, expt_avg_data)
        suggested_qubit_freq = self.cfg['qubit']['frequency'] - (fitdata[1] * 1e9 - self.cfg['ramsey']['ramsey_freq'])
        print "Oscillation frequency: " + str(fitdata[1] * 1e3) + " MHz"
        print "T2*: " + str(fitdata[3]) + " ns"
        print "Suggested Qubit Frequency: " + str(suggested_qubit_freq)


class EFRabiExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='EF_Rabi', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=EFRabiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run)

    def pre_run(self):
        self.drive.set_frequency(
            self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'])


    def post_run(self, expt_pts, expt_avg_data):
        pass


