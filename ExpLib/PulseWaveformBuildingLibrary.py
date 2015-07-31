from slab.experiments.ExpLib import awgpulses as ap
import numpy as np

def square(wtpts,mtpts,origin,marker_start_buffer,pulse_location,pulse,pulse_cfg):
    qubit_waveforms = ap.sideband(wtpts,
                             ap.square(wtpts, pulse.amp,
                                       origin - pulse_location - pulse.length - 3 *
                                       pulse_cfg['square']['ramp_sigma'], pulse.length,
                                       pulse_cfg['square']['ramp_sigma']),
                             np.zeros(len(wtpts)),
                             pulse.freq, pulse.phase)
    qubit_marker = ap.square(mtpts, 1, origin - pulse_location - pulse.length - 6 *
                                                              pulse_cfg['square'][
                                                                  'ramp_sigma'] - marker_start_buffer,
                                                              pulse.length + 6 * pulse_cfg['square'][
                                                                  'ramp_sigma'] + marker_start_buffer)
    flux_waveform = None
    return (qubit_waveforms,qubit_marker,flux_waveform)


def gauss(wtpts,mtpts,origin,marker_start_buffer,pulse_location,pulse):
    qubit_waveforms = ap.sideband(wtpts,
                             ap.gauss(wtpts, pulse.amp,
                                      origin - pulse_location - 3 * pulse.length,
                                      pulse.length), np.zeros(len(wtpts)),
                             pulse.freq, pulse.phase)
    qubit_marker = ap.square(mtpts, 1,
                                              origin - pulse_location - 6 * pulse.length - marker_start_buffer,
                                              6 * pulse.length + marker_start_buffer)
    flux_waveform = None
    return (qubit_waveforms,qubit_marker,flux_waveform)