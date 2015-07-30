__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.experiments.General.PulseSequences.PulseProbeSequence import *
from numpy import mean, arange


class PulseProbeExperiment(Experiment):
    def __init__(self, path='', prefix='Pulse_Probe', config_file=None, use_cal=False, **kwargs):
        Experiment.__init__(self, path=path, prefix=prefix, config_file=config_file, **kwargs)

        self.pulse_type = self.cfg['pulse_probe']['pulse_type']

        self.expt_pts = arange(self.cfg['pulse_probe']['start'], self.cfg['pulse_probe']['stop'], self.cfg['pulse_probe']['step'])


        pulse_calibrated = self.cfg['pulse_info'][self.pulse_type]['rabi_calibrated']

        self.pulse_sequence = PulseProbeSequence(self.cfg['awgs'], self.cfg['pulse_probe'], self.cfg['readout'],self.cfg['pulse_info'][self.pulse_type], self.cfg['buffer'])
        self.pulse_sequence.build_sequence()
        self.pulse_sequence.write_sequence(os.path.join(self.path, '../sequences/'), prefix, upload=True)

        self.cfg['alazar']['samplesPerRecord'] = 2 ** (self.cfg['readout']['width'] - 1).bit_length()
        self.cfg['alazar']['recordsPerBuffer'] = 200
        self.cfg['alazar']['recordsPerAcquisition'] = 20000

        return

    def go(self):
        self.plotter.clear()

        # self.save_config()

        print "Prep Instruments"
        self.readout.set_frequency(self.cfg['readout']['frequency'])
        self.readout.set_power(self.cfg['readout']['power'])
        self.readout.set_ext_pulse(mod=True)
        self.readout_shifter.set_phase(self.cfg['readout']['start_phase'] + self.cfg['readout']['phase_slope'] * (
            self.cfg['readout']['frequency'] - self.cfg['readout']['bare_frequency']), self.cfg['readout']['frequency'])


        self.drive.set_power(self.cfg['drive']['power'])
        self.drive.set_ext_pulse(mod=True)
        self.drive.set_output(True)
        self.readout_atten.set_attenuator(self.cfg['readout']['dig_atten'])

        self.awg.set_amps_offsets(self.cfg['cal']['iq_amps'], self.cfg['cal']['iq_offsets'])

        self.awg.run()

        print "Prep Card"
        adc = Alazar(self.cfg['alazar'])

        for freq in self.expt_pts:
            self.drive.set_frequency(freq)

            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data()

            self.plotter.append_xy('avg_pulse_probe_freq_scan1', freq, mean(ch1_pts[0:]))

            with self.datafile() as f:
                f.append_pt('freq', freq)
                f.append_pt('ch1_mean', mean(ch1_pts[0:]))

