__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.instruments.awg.StandardPulseSequences import EFRabiSequence
from numpy import mean, arange


class EFRabiExperiment(Experiment):
    def __init__(self, path='', prefix='EF Rabi', config_file=None, use_cal=False, **kwargs):
        Experiment.__init__(self, path=path, prefix=prefix, config_file=config_file, **kwargs)

        self.pulse_type = self.cfg['efrabi']['pulse_type']

        if self.cfg['pulse_info'][self.pulse_type] is None:
            print "This pulse type is not valid."
            self.ready_to_go = False
            return


        pulse_calibrated = self.cfg['pulse_info'][self.pulse_type]['rabi_calibrated']

        if not pulse_calibrated:
            print "This pulse type has not been calibrated."
            self.ready_to_go = False
            return

        self.pulse_sequence = EFRabiSequence(self.cfg['awgs'], self.cfg['efrabi'], self.cfg['readout'],self.cfg['pulse_info'][self.pulse_type])
        self.pulse_sequence.build_sequence()
        self.pulse_sequence.write_sequence(os.path.join(self.path, '../sequences/'), prefix, upload=True)

        self.efrabi_pts = self.pulse_sequence.efrabi_pts
        #self.cfg['alazar']['samplesPerRecord'] = self.pulse_sequence.waveform_length
        self.cfg['alazar']['recordsPerBuffer'] = self.pulse_sequence.sequence_length
        self.cfg['alazar']['recordsPerAcquisition'] = int(
            self.pulse_sequence.sequence_length * min(self.cfg['efrabi']['averages'], 100))

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

        self.drive.set_frequency(self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['freq'])
        self.drive.set_power(self.cfg['efrabi']['power'])
        self.drive.set_ext_pulse(mod=True)
        self.drive.set_output(True)
        self.readout_atten.set_attenuator(self.cfg['readout']['dig_atten'])

        self.awg.set_amps_offsets(self.cfg['cal']['iq_amps'], self.cfg['cal']['iq_offsets'])

        print "Prep Card"
        adc = Alazar(self.cfg['alazar'])

        efrabi_data = None
        for ii in arange(max(1, self.cfg['efrabi']['averages'] / 100)):
            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=self.awg.stop_and_prep,
                                                                    start_function=self.awg.run,
                                                                    excise=self.cfg['readout']['window'])
            # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
            # if self.cfg.alazar["ch1_enabled"]: self.plotter.plot_xy('current ch1', tpts, ch1_pts)
            # if self.cfg.alazar["ch1_enabled"]: self.plotter.plot_xy('current ch2', tpts, ch2_pts)
            if efrabi_data is None:
                efrabi_data = ch1_pts
            else:
                efrabi_data = (efrabi_data * ii + ch1_pts) / (ii + 1.0)

            self.plotter.plot_z('tefrabi Data', efrabi_data.T)
            efrabi_avg_data = mean(efrabi_data, 1)
            self.plotter.plot_xy('efrabi XY', self.pulse_sequence.efrabi_pts, efrabi_avg_data)

            print ii * min(self.cfg['efrabi']['averages'], 100)
            with self.datafile() as f:
                f.add('efrabi_2d', efrabi_data)
                f.add('efrabi_avg_data', efrabi_avg_data)
                f.add('efrabi_pts', self.efrabi_pts)
