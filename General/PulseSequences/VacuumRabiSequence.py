__author__ = 'Nelson'


from slab.instruments.awg.PulseSequence import *
from slab.experiments.ExpLib import awgpulses as ap
from numpy import arange, linspace
from slab.experiments.ExpLib.TEK1PulseOrganizer import *

class VacuumRabiSequence(PulseSequence):
    def __init__(self, awg_info, pulse_probe_cfg, readout_cfg,buffer_cfg):

        self.pulse_probe_cfg = pulse_probe_cfg

        self.start_end_buffer = buffer_cfg['tek1_start_end']
        self.marker_start_buffer = buffer_cfg['marker_start']

        PulseSequence.__init__(self, "Pulse Probe", awg_info, sequence_length=1)

        self.pulse_type = pulse_probe_cfg['pulse_type']
        self.pulse_probe_len = pulse_probe_cfg['pulse_probe_len']
        self.a = pulse_probe_cfg['a']
        self.measurement_delay = readout_cfg['delay']
        self.measurement_width = readout_cfg['width']
        self.card_delay = readout_cfg['card_delay']
        self.card_trig_width = readout_cfg['card_trig_width']


        self.max_length = round_samples((self.measurement_delay + self.measurement_width + 2*self.start_end_buffer))
        self.origin = self.max_length - (self.measurement_delay + self.measurement_width + self.start_end_buffer)

        self.set_all_lengths(self.max_length)
        self.set_waveform_length("qubit 1 flux", 1)

    def build_sequence(self):
        PulseSequence.build_sequence(self)

        wtpts = self.get_waveform_times('qubit drive I')
        mtpts = self.get_marker_times('qubit buffer')

        ii = 0
        self.markers['readout pulse'][ii] = ap.square(mtpts, 1, self.origin + self.measurement_delay,
                                                       self.measurement_width)
        self.markers['card trigger'][ii] = ap.square(mtpts, 1,
                                                      self.origin - self.card_delay + self.measurement_delay,
                                                      self.card_trig_width)

        pulse_probe_len = self.pulse_probe_len
        a = self.a


    def reshape_data(self, data):
        return np.reshape(data, (self.sequence_length, self.waveform_length))