__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.experiments.General.PulseSequences.StandardPulseSequences import RabiSequence
from numpy import mean, arange


class CWDriveExperiment(Experiment):
    def __init__(self, path='', prefix='CW Drive', config_file=None, use_cal=False, **kwargs):
        Experiment.__init__(self, path=path, prefix=prefix, config_file=config_file, **kwargs)

        #self.cfg['alazar']['samplesPerRecord'] = self.cfg['readout']['width']
        self.cfg['alazar']['recordsPerBuffer'] = 100
        self.cfg['alazar']['recordsPerAcquisition'] = 10000

        self.cw_drive_pts = arange(self.cfg['cw_drive']['start'], self.cfg['cw_drive']['stop'], self.cfg['cw_drive']['step'])

        return

    def go(self):
        self.plotter.clear()

        print "Prep Instruments"
        self.readout.set_output(True)
        self.readout.set_power(self.cfg['readout']['power'])
        self.readout.set_ext_pulse(mod=False)
        self.readout_atten.set_attenuator(self.cfg['readout']['dig_atten'])
        self.readout.set_frequency(self.cfg['readout']['frequency'])
        self.readout_shifter.set_phase((self.cfg['readout']['start_phase'])%360, self.cfg['readout']['frequency'])

        self.drive.set_output(True)
        self.drive.set_power(self.cfg['cal']['drive_power'])
        self.drive.set_ext_pulse(mod=False)

        self.awg.set_amps_offsets(self.cfg['cw_drive']['iq_amps'], self.cfg['cw_drive']['iq_offsets'])
        # self.save_config()

        print "Prep Card"
        adc = Alazar(self.cfg['alazar'])

        for freq in self.cw_drive_pts:
            self.drive.set_frequency(freq)

            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data()

            self.plotter.append_xy('avg_cw_drive_freq_scan1', freq, mean(ch1_pts[0:]))

            with self.datafile() as f:
                f.append_pt('freq', freq)
                f.append_pt('ch1_mean', mean(ch1_pts[0:]))



