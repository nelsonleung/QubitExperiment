__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.experiments.General.PulseSequences.SingleQubitPulseSequences import T1Sequence
from numpy import mean, arange


class T1Experiment(Experiment):
    def __init__(self, path='', prefix='T1', config_file=None, use_cal=False, **kwargs):
        Experiment.__init__(self, path=path, prefix=prefix, config_file=config_file, **kwargs)

        self.pulse_type = self.cfg['t1']['pulse_type']

        self.pulse_sequence = T1Sequence(prefix, self.cfg['awgs'], self.cfg['t1'], self.cfg['readout'],self.cfg['pulse_info'])
        self.pulse_sequence.build_sequence()
        self.pulse_sequence.write_sequence(os.path.join(self.path, '../sequences/'), prefix, upload=True)

        self.expt_pts = self.pulse_sequence.expt_pts
        #self.cfg['alazar']['samplesPerRecord'] = self.pulse_sequence.waveform_length
        self.cfg['alazar']['recordsPerBuffer'] = self.pulse_sequence.sequence_length
        self.cfg['alazar']['recordsPerAcquisition'] = int(
            self.pulse_sequence.sequence_length * min(self.cfg['t1']['averages'], 100))

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

        self.drive.set_frequency(self.cfg['qubit']['frequency'] - self.cfg['pulse_info'][self.pulse_type]['iq_freq'])
        self.drive.set_power(self.cfg['drive']['power'])
        self.drive.set_ext_pulse(mod=True)
        self.drive.set_output(True)
        self.readout_atten.set_attenuator(self.cfg['readout']['dig_atten'])

        self.awg.set_amps_offsets(self.cfg['cal']['iq_amps'], self.cfg['cal']['iq_offsets'])

        print "Prep Card"
        adc = Alazar(self.cfg['alazar'])

        t1_data = None
        for ii in arange(max(1, self.cfg['t1']['averages'] / 100)):
            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=self.awg.stop_and_prep,
                                                                    start_function=self.awg.run,
                                                                    excise=self.cfg['readout']['window'])
            # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
            # if self.cfg.alazar["ch1_enabled"]: self.plotter.plot_xy('current ch1', tpts, ch1_pts)
            # if self.cfg.alazar["ch1_enabled"]: self.plotter.plot_xy('current ch2', tpts, ch2_pts)
            if t1_data is None:
                t1_data = ch1_pts
            else:
                t1_data = (t1_data * ii + ch1_pts) / (ii + 1.0)

            self.plotter.plot_z('t1 Data', t1_data.T)
            t1_avg_data = mean(t1_data, 1)
            self.plotter.plot_xy('t1 XY', self.expt_pts, t1_avg_data)

            print ii * min(self.cfg['t1']['averages'], 100)
            with self.datafile() as f:
                f.add('t1_2d', t1_data)
                f.add('t1_avg_data', t1_avg_data)
                f.add('t1_pts', self.expt_pts)
        self.post_run_analysis(self.expt_pts,t1_avg_data)


    def post_run_analysis(self,expt_pts,t1_avg_data):
        print "Analyzing T1 Data"
        fitdata = fitexp(expt_pts,t1_avg_data)
        print "T1: " + str(fitdata[3]) + " ns"