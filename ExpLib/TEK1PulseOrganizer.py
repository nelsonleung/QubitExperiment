__author__ = 'Nelson'

from slab.instruments.awg.PulseSequence import *
from slab.experiments.ExpLib import awgpulses as ap
from numpy import arange, linspace

from liveplot import LivePlotClient


class Pulse():
    def __init__(self, name, type, amp, length, freq, phase, span_length):
        self.name = name
        self.type = type
        self.amp = amp
        self.length = length
        self.freq = freq
        self.phase = phase
        self.span_length = span_length


class TEK1PulseSequenceBuilder():
    def __init__(self, pulse_cfg, readout_cfg,buffer_cfg):
        self.start_end_buffer = buffer_cfg['tek1_start_end']
        self.marker_start_buffer = buffer_cfg['marker_start']
        self.pulse_cfg = pulse_cfg
        self.readout_cfg = readout_cfg
        self.pulse_sequence_list = []
        self.total_pulse_span_length = 0

    def append(self, name, type, amp=0, length=0, freq=0, phase=0):
        '''
        Append a pulse in the pulse sequence.
        '''
        if name == "pi":
            amp = self.pulse_cfg[type]['a']
            length = self.pulse_cfg[type]['pi_length']
            freq = self.pulse_cfg[type]['iq_freq']
        if name == "half_pi":
            amp = self.pulse_cfg[type]['a']
            length = self.pulse_cfg[type]['half_pi_length']
            freq = self.pulse_cfg[type]['iq_freq']

        pulse_span_length = ap.get_pulse_span_length(self.pulse_cfg, type, length)
        pulse = Pulse(name, type, amp, length, freq, phase, pulse_span_length)

        self.pulse_sequence_list.append(pulse)
        self.total_pulse_span_length += pulse_span_length

    def idle(self, length):
        '''
        Append an idle in the pulse sequence.
        '''
        pulse_info = Pulse('idle', 'idle', 0, length, 0, 0, length)

        self.pulse_sequence_list.append(pulse_info)
        self.total_pulse_span_length += length

    def get_pulse_sequence(self):
        '''
        Being called externally to obtain the pulse sequence.
        '''
        pulse_sequence_list = self.pulse_sequence_list
        self.pulse_sequence_list = []
        return pulse_sequence_list

    def get_total_pulse_span_length(self):
        '''
        Being called externally to obtain the total pulse span length.
        '''
        total_pulse_span_length = self.total_pulse_span_length
        self.total_pulse_span_length = 0
        return total_pulse_span_length

    def acquire_readout_cfg(self):
        '''
        Being called internally to obtain the readout parameters.
        '''
        self.measurement_delay = self.readout_cfg['delay']
        self.measurement_width = self.readout_cfg['width']
        self.card_delay = self.readout_cfg['card_delay']
        self.card_trig_width = self.readout_cfg['card_trig_width']

    def get_max_length(self, total_pulse_span_length_list):
        '''
        Calculate the maximum of total pulse + marker length, of all the sequences.
        '''
        self.acquire_readout_cfg()
        max_total_pulse_span_length = max(total_pulse_span_length_list)
        self.max_length = round_samples(
            (max_total_pulse_span_length + self.measurement_delay + self.measurement_width + 2 * self.start_end_buffer))
        return self.max_length

    def prepare_build(self, wtpts, mtpts, markers_readout, markers_card, waveforms_qubit_I, waveforms_qubit_Q,
                      markers_qubit_buffer):
        '''
        Being called internally to set the variables.
        '''
        self.wtpts = wtpts
        self.mtpts = mtpts
        self.markers_readout = markers_readout
        self.markers_card = markers_card
        self.waveforms_qubit_I = waveforms_qubit_I
        self.waveforms_qubit_Q = waveforms_qubit_Q
        self.markers_qubit_buffer = markers_qubit_buffer


    def build(self, pulse_sequence_matrix):
        '''
        Parse the pulse sequence matrix generated previously.
        For each pulse sequence, location of readout and card is fixed.
        Pulses are appended backward, from the last pulse to the first pulse.
        '''
        self.origin = self.max_length - (self.measurement_delay + self.measurement_width + self.start_end_buffer)
        for ii in range(len(pulse_sequence_matrix)):
            self.markers_readout[ii] = ap.square(self.mtpts, 1, self.origin + self.measurement_delay,
                                                 self.measurement_width)
            self.markers_card[ii] = ap.square(self.mtpts, 1,
                                              self.origin - self.card_delay + self.measurement_delay,
                                              self.card_trig_width)
            self.waveforms_qubit_I[ii], self.waveforms_qubit_Q[ii] = \
                ap.sideband(self.wtpts,
                            np.zeros(len(self.wtpts)), np.zeros(len(self.wtpts)),
                            0, 0)
            self.markers_qubit_buffer[ii] = ap.square(self.mtpts, 0, 0, 0)
            pulse_location = 0
            # The range defined in this way means having the for loop with index backward.
            for jj in range(len(pulse_sequence_matrix[ii]) - 1, -1, -1):
                pulse = pulse_sequence_matrix[ii][jj]
                pulse_recorded = False
                if pulse.type == "square":
                    pulse_recorded = True
                    pulse_waveform = ap.sideband(self.wtpts,
                                                 ap.square(self.wtpts, pulse.amp,
                                                           self.origin - pulse_location - pulse.length - 3 *
                                                           self.pulse_cfg['square']['ramp_sigma'], pulse.length,
                                                           self.pulse_cfg['square']['ramp_sigma']),
                                                 np.zeros(len(self.wtpts)),
                                                 pulse.freq, pulse.phase)
                    self.waveforms_qubit_I[ii] += pulse_waveform[0]
                    self.waveforms_qubit_Q[ii] += pulse_waveform[1]

                    self.markers_qubit_buffer[ii] += ap.square(self.mtpts, 1, self.origin - pulse_location - 6 *
                                                              self.pulse_cfg['square'][
                                                                  'ramp_sigma'] - self.marker_start_buffer,
                                                              pulse.length + 6 * self.pulse_cfg['square'][
                                                                  'ramp_sigma'] + self.marker_start_buffer)
                if pulse.type == "gauss":
                    pulse_recorded = True
                    pulse_waveform = ap.sideband(self.wtpts,
                                                 ap.gauss(self.wtpts, pulse.amp,
                                                          self.origin - pulse_location - 3 * pulse.length,
                                                          pulse.length), np.zeros(len(self.wtpts)),
                                                 pulse.freq, pulse.phase)
                    self.waveforms_qubit_I[ii] += pulse_waveform[0]
                    self.waveforms_qubit_Q[ii] += pulse_waveform[1]
                    self.markers_qubit_buffer[ii] += ap.square(self.mtpts, 1,
                                                              self.origin - pulse_location - 6 * pulse.length - self.marker_start_buffer,
                                                              6 * pulse.length + self.marker_start_buffer)

                high_values_indices = self.markers_qubit_buffer[ii] > 1
                self.markers_qubit_buffer[ii][high_values_indices] = 1

                if pulse.type == "idle":
                    pulse_recorded = True

                pulse_location += pulse.span_length
                if pulse_recorded == False:
                    raise ValueError('Pulse is not defined.')

        return (self.markers_readout,
                self.markers_card,
                self.waveforms_qubit_I,
                self.waveforms_qubit_Q,
                self.markers_qubit_buffer )
