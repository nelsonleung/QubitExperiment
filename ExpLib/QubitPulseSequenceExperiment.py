__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.experiments.General.PulseSequences.SingleQubitPulseSequences import *
from slab.experiments.Multimode.PulseSequences.MultimodePulseSequence import *
from numpy import mean, arange


class QubitPulseSequenceExperiment(Experiment):
    '''
    Parent class for all the single qubit pulse sequence experiment.
    '''
    def __init__(self, path='', prefix='SQPSE', config_file=None, PulseSequence=None, pre_run=None, post_run=None,
                 **kwargs):
        Experiment.__init__(self, path=path, prefix=prefix, config_file=config_file, **kwargs)

        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value

        if 'prep_tek2' in self.extra_args:
            self.prep_tek2 = extra_args['prep_tek2']
        else:
            self.prep_tek2 = False

        self.prefix = prefix
        self.expt_cfg_name = prefix.lower()

        self.pre_run = pre_run
        self.post_run = post_run

        self.pulse_type = self.cfg[self.expt_cfg_name]['pulse_type']

        self.pulse_sequence = PulseSequence(prefix, self.cfg, self.cfg[self.expt_cfg_name])
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
        self.drive.set_ext_pulse(mod=False)
        self.drive.set_output(True)
        self.readout_atten.set_attenuator(self.cfg['readout']['dig_atten'])

        try:
            self.cfg['freq_flux']['flux_volt']=self.extra_args['flux_volt']
        except:
            pass

        try:
            self.cfg['freq_flux']['slope']=self.extra_args['freq_flux_slope']
        except:
            pass

        try:
            self.cfg['freq_flux']['volt_offset']+=self.extra_args['volt_offset']
        except:
            pass

        self.flux_volt.ramp_volt(self.cfg['freq_flux']['flux_volt'])

        self.awg.set_amps_offsets(self.cfg['cal']['iq_amps'], self.cfg['cal']['iq_offsets'])

        if self.pre_run is not None:
            self.pre_run()

        print "Prep Card"
        adc = Alazar(self.cfg['alazar'])

        expt_data = None
        for ii in arange(max(1, self.cfg[self.expt_cfg_name]['averages'] / 100)):
            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=self.awg_prep,
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

    def awg_prep(self):
        self.awg.stop_and_prep()
        if self.prep_tek2:
            self.tek2.stop()
            self.tek2.prep_experiment()
            self.tek2.run()