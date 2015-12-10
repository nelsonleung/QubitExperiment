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
        #self.drive.set_frequency(self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'])

        pass

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing T1 Data"
        fitdata = fitexp(expt_pts, expt_avg_data)
        print "T1: " + str(fitdata[3]) + " ns"


class RamseyExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Ramsey', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=RamseySequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        self.drive.set_frequency(
            self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'] + self.cfg['ramsey']['ramsey_freq'])
        print self.cfg['pulse_info'][self.pulse_type]['iq_freq']

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing Ramsey Data"
        fitdata = fitdecaysin(expt_pts, expt_avg_data)

        self.offset_freq =self.cfg['ramsey']['ramsey_freq'] - fitdata[1] * 1e9

        self.flux = self.cfg['freq_flux']['flux']
        self.freq_flux_slope = self.cfg['freq_flux']['freq_flux_slope']

        suggested_qubit_freq = self.cfg['qubit']['frequency'] - (fitdata[1] * 1e9 - self.cfg['ramsey']['ramsey_freq'])
        print "Oscillation frequency: " + str(fitdata[1] * 1e3) + " MHz"
        print "T2*: " + str(fitdata[3]) + " ns"

        print "Suggested Qubit Frequency: " + str(suggested_qubit_freq)
        print "Or Suggested Flux: " +str(self.flux -self.offset_freq/ self.freq_flux_slope)


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

class EFRamseyExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='EF_Ramsey', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=EFRamseySequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        self.drive.set_frequency(
            self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'] )

    def post_run(self, expt_pts, expt_avg_data):
        pass
        print "Analyzing EF Ramsey Data"
        fitdata = fitdecaysin(expt_pts, expt_avg_data)

        #self.offset_freq =self.cfg['ramsey']['ramsey_freq'] - fitdata[1] * 1e9
        #self.flux_volt = self.cfg['freq_flux']['flux_volt']
        #self.freq_flux_slope = self.cfg['freq_flux']['slope']

        suggested_anharm = self.cfg['qubit']['alpha'] + (+fitdata[1] * 1e9 - self.cfg['ef_ramsey']['ramsey_freq'])
        print "Oscillation frequency: " + str(fitdata[1] * 1e3) + " MHz"
        print "T2*ef: " + str(fitdata[3]) + " ns"
        #if round(self.offset_freq/ self.freq_flux_slope,4)==0.0000:
         #   print "Qubit frequency is well calibrated."
        #else:
        print "Suggested Anharmonicity: " + str(suggested_anharm)
          #  print "Or Suggested Flux Voltage: " +str(round(self.flux_volt -self.offset_freq/ self.freq_flux_slope,4))


class EFT1Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='EF_T1', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=EFT1Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        self.drive.set_frequency(self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'])

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing EF T1 Data"
        fitdata = fitexp(expt_pts, expt_avg_data)
        print "EF T1: " + str(fitdata[3]) + " ns"


class EFT1Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='EF_T1', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=EFT1Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        self.drive.set_frequency(self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'])

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing EF T1 Data"
        fitdata = fitexp(expt_pts, expt_avg_data)
        print "EF T1: " + str(fitdata[3]) + " ns"


class EFT1Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='EF_T1', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=EFT1Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        self.drive.set_frequency(self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'])

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing EF T1 Data"
        fitdata = fitexp(expt_pts, expt_avg_data)
        print "EF T1: " + str(fitdata[3]) + " ns"


class HalfPiXPulseOptimizationExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='HalfPiXPulseOptimization', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=HalfPiXPulseOptimizationSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        pass

    def post_run(self, expt_pts, expt_avg_data):
        pass


class PiXPulseOptimizationExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='PiXPulseOptimization', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=PiXPulseOptimizationSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        pass

    def post_run(self, expt_pts, expt_avg_data):
        pass


class RabiSweepExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Rabi_Sweep', config_file='..\\config.json', **kwargs):
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
        self.drive_freq = self.extra_args['drive_freq']
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=RabiSweepSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run,**kwargs)



    def pre_run(self):
        self.drive.set_frequency(self.drive_freq)


    def post_run(self, expt_pts, expt_avg_data):
        #print self.data_file
        slab_file = SlabFile(self.data_file)
        with slab_file as f:
            f.append_pt('drive_freq', self.drive_freq)
            f.append_line('sweep_expt_avg_data', expt_avg_data)
            f.append_line('sweep_expt_pts', expt_pts)

            f.close()

class HalfPiXPulseOptimizationSweepExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='HalfPiXPulseOptimization_Sweep', config_file='..\\config.json', **kwargs):
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
        self.pulse_length = self.extra_args['pulse_length']

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=HalfPiXPulseOptimizationSweepSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        pass

    def post_run(self, expt_pts, expt_avg_data):
        slab_file = SlabFile(self.data_file)
        with slab_file as f:
            f.append_pt('pulse_length', self.pulse_length)
            f.append_line('sweep_expt_avg_data', expt_avg_data)
            f.append_line('sweep_expt_pts', expt_pts)
            f.close()


