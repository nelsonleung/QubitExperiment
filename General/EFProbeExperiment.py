__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.instruments.awg.StandardPulseSequences import EFProbeSequence
from numpy import mean, arange


class EFProbeExperiment(Experiment):
    def __init__(self, path='', prefix='EF Probe', config_file=None, use_cal=False, **kwargs):
        Experiment.__init__(self, path=path, prefix=prefix, config_file=config_file, **kwargs)

        self.pulse_type = self.cfg['efprobe']['pulse_type']

        self.ef_pulse_pts = arange(self.cfg['efprobe']['start'], self.cfg['efprobe']['stop'], self.cfg['efprobe']['step'])

        if self.cfg['pulse_info'][self.pulse_type] is None:
            print "This pulse type is not valid."
            self.ready_to_go = False
            return


        pulse_calibrated = self.cfg['pulse_info'][self.pulse_type]['rabi_calibrated']

        if not pulse_calibrated:
            print "This pulse type has not been calibrated."
            self.ready_to_go = False
            return

        self.pulse_sequence = EFProbeSequence(self.cfg['awgs'], self.cfg['efprobe'], self.cfg['readout'],self.cfg['pulse_info'][self.pulse_type])
        self.pulse_sequence.build_sequence()
        self.pulse_sequence.write_sequence(os.path.join(self.path, 'sequences/'), prefix, upload=True)

        #self.cfg['alazar']['samplesPerRecord'] = self.pulse_sequence.waveform_length
        self.cfg['alazar']['recordsPerBuffer'] = 200
        self.cfg['alazar']['recordsPerAcquisition'] = 20000

        self.ready_to_go = True
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


        self.drive.set_power(self.cfg['efrabi']['power'])
        self.drive.set_ext_pulse(mod=True)
        self.drive.set_output(True)
        self.readout_atten.set_attenuator(self.cfg['readout']['dig_atten'])

        self.awg.set_amps_offsets(self.cfg['cal']['iq_amps'], self.cfg['cal']['iq_offsets'])

        self.awg.run()

        print "Prep Card"
        adc = Alazar(self.cfg['alazar'])

        for ef_freq in self.ef_pulse_pts:
            self.drive.set_frequency(ef_freq)

            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data()

            self.plotter.append_xy('avg_ef_probe_freq_scan1', ef_freq, mean(ch1_pts[0:]))

            with self.datafile() as f:
                f.append_pt('ef_freq', ef_freq)
                f.append_pt('ch1_mean', mean(ch1_pts[0:]))

