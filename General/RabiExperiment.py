__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.experiments.General.PulseSequences.SingleQubitPulseSequences import *
from numpy import mean, arange


class RabiExperiment(Experiment):
    def __init__(self, path='', prefix='Rabi', config_file=None, use_cal=False, **kwargs):
        Experiment.__init__(self, path=path, prefix=prefix, config_file=config_file, **kwargs)

        self.pulse_type = self.cfg['rabi']['pulse_type']
        if self.cfg['pulse_info'][self.pulse_type] is None:
            print "This pulse type is not valid."
            self.ready_to_go = False
            return

        self.pulse_sequence = RabiSequence(prefix, self.cfg['awgs'], self.cfg['rabi'], self.cfg['readout'], self.cfg['pulse_info'])
        self.pulse_sequence.build_sequence()
        self.pulse_sequence.write_sequence(os.path.join(self.path, '../sequences/'), prefix, upload=True)

        self.expt_pts = self.pulse_sequence.expt_pts
        #self.cfg['alazar']['samplesPerRecord'] = self.cfg['readout']['width']
        self.cfg['alazar']['recordsPerBuffer'] = self.pulse_sequence.sequence_length
        self.cfg['alazar']['recordsPerAcquisition'] = int(
            self.pulse_sequence.sequence_length * min(self.cfg['rabi']['averages'], 100))

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

        self.drive.set_frequency(self.cfg['qubit']['frequency'] - self.cfg['rabi']['freq'])
        self.drive.set_power(self.cfg['rabi']['power'])
        self.drive.set_ext_pulse(mod=True)
        self.drive.set_output(True)
        self.readout_atten.set_attenuator(self.cfg['readout']['dig_atten'])

        self.awg.set_amps_offsets(self.cfg['cal']['iq_amps'], self.cfg['cal']['iq_offsets'])

        print "Prep Card"
        adc = Alazar(self.cfg['alazar'])

        rabi_data = None
        for ii in arange(max(1, self.cfg['rabi']['averages'] / 100)):
            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=self.awg.stop_and_prep,
                                                                    start_function=self.awg.run,
                                                                    excise=self.cfg['readout']['window'])
            # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
            # if self.cfg.alazar["ch1_enabled"]: self.plotter.plot_xy('current ch1', tpts, ch1_pts)
            # if self.cfg.alazar["ch1_enabled"]: self.plotter.plot_xy('current ch2', tpts, ch2_pts)
            if rabi_data is None:
                rabi_data = ch1_pts
            else:
                rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)

            self.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            self.plotter.plot_xy('Rabi XY', self.pulse_sequence.expt_pts, rabi_avg_data)

            print ii * min(self.cfg['rabi']['averages'], 100)
            with self.datafile() as f:
                f.add('rabi_2d', rabi_data)
                f.add('rabi_avg_data', rabi_avg_data)
                f.add('rabi_pts', self.expt_pts)

        if self.cfg['rabi']['calibrate']:
            self.post_run_analysis(self.rabi_pts,rabi_avg_data)

    def post_run_analysis(self,rabi_pts,rabi_avg_data):
        print "Analyzing Rabi Data"
        fitdata = fitdecaysin(rabi_pts,rabi_avg_data)
        excited_signal = np.sign(180-fitdata[2]%360)
        pulse_type = self.cfg['rabi']['pulse_type']
        if pulse_type is 'gauss':
            excited_signal = np.sign(180-fitdata[2]%360)
            self.cfg['cal']['excited_signal'] = excited_signal
        pi_length = (self.cfg['cal']['excited_signal']*np.sign(fitdata[0])*0.5*np.pi-fitdata[2]*np.pi/180.)/(2*np.pi*fitdata[1])%(1/fitdata[1])
        half_pi_length = (self.cfg['cal']['excited_signal']*np.sign(fitdata[0])*np.pi-fitdata[2]*np.pi/180.)/(2*np.pi*fitdata[1])%(0.5/fitdata[1])
        self.cfg['pulse_info'][pulse_type]['rabi_calibrated']=True
        self.cfg['pulse_info'][pulse_type]['pi_length'] = pi_length
        self.cfg['pulse_info'][pulse_type]['half_pi_length'] = half_pi_length
        self.cfg['pulse_info'][pulse_type]['a']=self.cfg['rabi']['a']
        if pulse_type is not 'gauss':
            self.cfg['pulse_info'][pulse_type]['ramp_sigma']=self.cfg['rabi']['ramp_sigma']
        self.cfg['pulse_info'][pulse_type]['phase']=self.cfg['rabi']['phase']
        self.cfg['pulse_info'][pulse_type]['freq']=self.cfg['rabi']['freq']
        self.save_config()








