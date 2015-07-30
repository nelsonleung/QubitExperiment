__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.experiments.General.PulseSequences.SingleQubitPulseSequences import *
from numpy import mean, arange


class SingleQubitPulseSequenceExperiment(Experiment):
    def __init__(self, path='', prefix='SQPSE', config_file=None, PulseSequence=None, pre_run=None, post_run=None,
                 **kwargs):
        Experiment.__init__(self, path=path, prefix=prefix, config_file=config_file, **kwargs)

        self.prefix = prefix
        self.expt_cfg_name = prefix.lower()

        self.pre_run = pre_run
        self.post_run = post_run

        self.pulse_type = self.cfg[self.expt_cfg_name]['pulse_type']

        self.pulse_sequence = PulseSequence(prefix, self.cfg['awgs'], self.cfg[self.expt_cfg_name], self.cfg['readout'],
                                            self.cfg['pulse_info'])
        self.pulse_sequence.build_sequence()
        self.pulse_sequence.write_sequence(os.path.join(self.path, '../sequences/'), prefix, upload=True)

        self.expt_pts = self.pulse_sequence.expt_pts
        self.cfg['alazar']['samplesPerRecord'] = 2 ** (self.cfg['readout']['width'] - 1).bit_length()
        self.cfg['alazar']['recordsPerBuffer'] = self.pulse_sequence.sequence_length
        self.cfg['alazar']['recordsPerAcquisition'] = int(
            self.pulse_sequence.sequence_length * min(self.cfg[self.expt_cfg_name]['averages'], 100))

        self.ready_to_go = True
        return

    def go(self):
        self.plotter.clear()

        print "Prep Instruments"
        self.readout.set_frequency(self.cfg['readout']['frequency'])
        self.readout.set_power(self.cfg['readout']['power'])
        self.readout.set_ext_pulse(mod=True)
        self.readout_shifter.set_phase(self.cfg['readout']['start_phase'] + self.cfg['readout']['phase_slope'] * (
            self.cfg['readout']['frequency'] - self.cfg['readout']['bare_frequency']), self.cfg['readout']['frequency'])

        self.drive.set_frequency(self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'])
        self.drive.set_power(self.cfg['drive']['power'])
        self.drive.set_ext_pulse(mod=True)
        self.drive.set_output(True)
        self.readout_atten.set_attenuator(self.cfg['readout']['dig_atten'])

        self.awg.set_amps_offsets(self.cfg['cal']['iq_amps'], self.cfg['cal']['iq_offsets'])

        if self.pre_run is not None:
            self.pre_run()

        print "Prep Card"
        adc = Alazar(self.cfg['alazar'])

        expt_data = None
        for ii in arange(max(1, self.cfg[self.expt_cfg_name]['averages'] / 100)):
            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=self.awg.stop_and_prep,
                                                                    start_function=self.awg.run,
                                                                    excise=self.cfg['readout']['window'])
            if expt_data is None:
                expt_data = ch1_pts
            else:
                expt_data = (expt_data * ii + ch1_pts) / (ii + 1.0)

            self.plotter.plot_z(self.prefix + ' Data', expt_data.T)
            expt_avg_data = mean(expt_data, 1)
            self.plotter.plot_xy(self.prefix + ' XY', self.pulse_sequence.expt_pts, expt_avg_data)

            print ii * min(self.cfg[self.expt_cfg_name]['averages'], 100)
            with self.datafile() as f:
                f.add('expt_2d', expt_data)
                f.add('expt_avg_data', expt_avg_data)
                f.add('expt_pts', self.expt_pts)

        if self.post_run is not None:
            self.post_run(self.expt_pts, expt_avg_data)


class RabiExperiment(SingleQubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Rabi', config_file=None, **kwargs):
        SingleQubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=RabiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        self.drive.set_frequency(self.cfg['qubit']['frequency'] - self.cfg[self.expt_cfg_name]['iq_freq'])

    def post_run(self, expt_pts, expt_avg_data):
        if self.cfg[self.expt_cfg_name]['calibrate_pulse']:
            print "Analyzing Rabi Data"
            fitdata = fitdecaysin(expt_pts, expt_avg_data)
            excited_signal = np.sign(180 - fitdata[2] % 360)
            pulse_type = self.cfg[self.expt_cfg_name]['pulse_type']

            if pulse_type is 'gauss':
                self.cfg['cal']['excited_signal'] = excited_signal
            pi_length = (self.cfg['cal']['excited_signal'] * np.sign(fitdata[0]) * 0.5 * np.pi - fitdata[
                2] * np.pi / 180.) / (2 * np.pi * fitdata[1]) % (1 / fitdata[1])
            half_pi_length = (self.cfg['cal']['excited_signal'] * np.sign(fitdata[0]) * np.pi - fitdata[
                2] * np.pi / 180.) / (2 * np.pi * fitdata[1]) % (0.5 / fitdata[1])

            from time import gmtime, strftime

            self.cfg['pulse_info'][pulse_type]['calibrated_time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            self.cfg['pulse_info'][pulse_type]['pi_length'] = pi_length
            self.cfg['pulse_info'][pulse_type]['half_pi_length'] = half_pi_length
            self.cfg['pulse_info'][pulse_type]['a'] = self.cfg[self.expt_cfg_name]['a']
            self.cfg['pulse_info'][pulse_type]['iq_freq'] = self.cfg[self.expt_cfg_name]['iq_freq']
            self.save_config()


class T1Experiment(SingleQubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='T1', config_file=None, **kwargs):
        SingleQubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=T1Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, **kwargs)

    def pre_run(self):
        pass

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing T1 Data"
        fitdata = fitexp(expt_pts, t1_avg_data)
        print "T1: " + str(fitdata[3]) + " ns"


class RamseyExperiment(SingleQubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Ramsey', config_file=None, **kwargs):
        SingleQubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
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


class SpinEchoExperiment(SingleQubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Spin_Echo', config_file=None, **kwargs):
        SingleQubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
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




