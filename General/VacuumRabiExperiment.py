__author__ = 'dave'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.instruments.awg.StandardPulseSequences import RabiSequence
from numpy import mean, arange


class VacuumRabiExperiment(Experiment):
    def __init__(self, path='', prefix='Rabi', config_file=None, use_cal=False, **kwargs):
        Experiment.__init__(self, path=path, prefix=prefix, config_file=config_file, **kwargs)

        #self.cfg['alazar']['samplesPerRecord'] = self.cfg['readout']['width']
        self.cfg['alazar']['recordsPerBuffer'] = 100
        self.cfg['alazar']['recordsPerAcquisition'] = 10000

        self.vacuum_rabi_pts = arange(self.cfg['vacuum_rabi']['start'], self.cfg['vacuum_rabi']['stop'], self.cfg['vacuum_rabi']['step'])

        return

    def go(self):
        self.plotter.clear()

        print "Prep Instruments"
        self.readout.set_output(True)
        self.readout.set_power(self.cfg['readout']['power'])
        self.readout.set_ext_pulse(mod=True)

        self.drive.set_output(False)
        self.drive.set_ext_pulse(mod=False)
        self.readout_atten.set_attenuator(self.cfg['readout']['dig_atten'])

        self.awg.set_amps_offsets(self.cfg['cw_drive']['iq_amps'], self.cfg['cw_drive']['iq_offsets'])
        # self.save_config()

        print "Prep Card"
        adc = Alazar(self.cfg['alazar'])


        for freq in self.vacuum_rabi_pts:
            self.readout.set_frequency(freq)
            self.readout_shifter.set_phase((self.cfg['readout']['start_phase'] + self.cfg['readout']['phase_slope'] * (freq - self.cfg['readout']['frequency']))%360, freq)
            print self.readout_shifter.get_phase()
            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data()

            self.plotter.append_xy('readout_avg_freq_scan1', freq, mean(ch1_pts[0:]))
            self.plotter.append_z('scope',ch1_pts)

            with self.datafile() as f:
                f.append_pt('freq', freq)
                f.append_pt('ch1_mean', mean(ch1_pts[0:]))



