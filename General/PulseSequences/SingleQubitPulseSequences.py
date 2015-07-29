__author__ = 'Nelson'

from slab.instruments.awg.PulseSequence import *
from slab.instruments.awg import awgpulses2 as ap2
from numpy import arange, linspace
from slab.experiments.ExpLib.TEK1PulseOrganizer import *

from liveplot import LivePlotClient

# lp=LivePlotClient()


class SingleQubitPulseSequence(PulseSequence):
    def __init__(self, name, awg_info, expt_cfg, readout_cfg, pulse_cfg, define_points, define_parameters, define_pulses):

        self.expt_cfg = expt_cfg
        define_points()
        define_parameters()
        sequence_length = len(self.expt_pts)

        PulseSequence.__init__(self, name, awg_info, sequence_length)

        self.tek1psb = TEK1PulseSequenceBuilder(pulse_cfg, readout_cfg)
        self.pulse_sequence_matrix = []
        total_pulse_span_length_list = []

        for ii, pt in enumerate(self.expt_pts):
            define_pulses(pt)
            self.pulse_sequence_matrix.append(self.tek1psb.get_pulse_sequence())
            total_pulse_span_length_list.append(self.tek1psb.total_pulse_span_length)

        max_length = self.tek1psb.get_max_length(total_pulse_span_length_list)
        print max_length
        self.set_all_lengths(max_length)

    def build_sequence(self):
        PulseSequence.build_sequence(self)
        wtpts = self.get_waveform_times('qubit drive I')
        mtpts = self.get_marker_times('qubit buffer')
        markers_readout = self.markers['readout pulse']
        markers_card = self.markers['card trigger']
        waveforms_qubit_I = self.waveforms['qubit drive I']
        waveforms_qubit_Q = self.waveforms['qubit drive Q']
        markers_qubit_buffer = self.markers['qubit buffer']
        self.tek1psb.prepare_build(wtpts, mtpts, markers_readout, markers_card, waveforms_qubit_I, waveforms_qubit_Q,
                              markers_qubit_buffer)
        generated_sequences = self.tek1psb.build(self.pulse_sequence_matrix)

        self.markers['readout pulse'], self.markers['card trigger'], self.waveforms['qubit drive I'], self.waveforms[
            'qubit drive Q'], self.markers['qubit buffer'] = generated_sequences

    def reshape_data(self, data):
        return np.reshape(data, (self.sequence_length, self.waveform_length))

class RabiSequence(SingleQubitPulseSequence):
    def __init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg):
        SingleQubitPulseSequence.__init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        self.pulse_type =  self.expt_cfg['pulse_type']

    def define_pulses(self,pt):
        self.tek1psb.append('general', self.pulse_type, amp=1, length=pt)


class T1Sequence(SingleQubitPulseSequence):
    def __init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg):
        SingleQubitPulseSequence.__init__(self,name, awg_info, expt_cfg, readout_cfg, pulse_cfg, self.define_points, self.define_parameters, self.define_pulses)

    def define_points(self):
        self.expt_pts = arange(self.expt_cfg['start'], self.expt_cfg['stop'], self.expt_cfg['step'])

    def define_parameters(self):
        pass

    def define_pulses(self,pt):
        self.tek1psb.append('pi', 'gauss')
        self.tek1psb.idle(pt)

