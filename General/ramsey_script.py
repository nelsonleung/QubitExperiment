print "Loading packages"

from slab import *
from slab.instruments import Tek5014Sequence
from numpy import *
from slab.instruments import Alazar, AlazarConfig
from slab.instruments.awg.awgpulses import *

print "Packages loaded"


def ramp_expt(amp, width, phase, cutoff, blockout_width, origin, total_length,
              measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):
    pulse = linspace(0, amp, floor(width))
    Ich = zeros(total_length)
    Qch = zeros(total_length)
    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich[origin - len(pulse):origin] = np.cos(phase) * pulse
    Qch[origin - len(pulse):origin] = np.sin(phase) * pulse
    blockout = ones(blockout_width)
    blockout_marker[origin - len(blockout) / 2: origin - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def T1_expt(amp, delay, flat_time, smooth_time, phase, blockout_width, origin, total_length,
            measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):
    pulse = smooth_square(origin - (flat_time / 2 + 2 * smooth_time + delay), smooth_time, flat_time, amp, total_length)

    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich = np.cos(phase) * pulse
    Qch = np.sin(phase) * pulse
    blockout = ones(blockout_width)
    blockout_marker[origin - (flat_time / 2 + 2 * smooth_time + delay) - len(blockout) / 2: origin - (
        flat_time / 2 + 2 * smooth_time + delay) - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker

def T1_expt_gauss(amp, delay, phase, sigma, cutoff, blockout_width, origin, total_length,
                  measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):
    pulse = gauss_new(origin - (cutoff + delay), sigma, pulse_height=amp, total_length=total_length,
                      cutoff_length=cutoff)

    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich = np.cos(phase) * pulse
    Qch = np.sin(phase) * pulse
    blockout = ones(blockout_width)
    blockout_marker[origin - (cutoff + delay) - len(blockout) / 2: origin - (
        cutoff + delay) - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def blue_sideband_rabi_expt_square(amp, delay, smooth_time, flat_time, blockout_width, origin, total_length,detuning_freq,
                  measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):

    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich = square_sideband(origin - (flat_time / 2 + 2 * smooth_time + delay), smooth_time, flat_time, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0)
    Qch = square_sideband(origin - (flat_time / 2 + 2 * smooth_time + delay), smooth_time, flat_time, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0.27*np.pi)
    blockout = ones(blockout_width)
    blockout_marker[origin - (flat_time / 2 + 2 * smooth_time + delay) - len(blockout) / 2: origin - (
        flat_time / 2 + 2 * smooth_time + delay) - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def red_sideband_rabi_expt_square(amp, delay, smooth_time, flat_time, blockout_width, origin, total_length,detuning_freq,
                  measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):

    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich = square_sideband(origin - (flat_time / 2 + 2 * smooth_time + delay), smooth_time, flat_time, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0.27*np.pi)
    Qch = square_sideband(origin - (flat_time / 2 + 2 * smooth_time + delay), smooth_time, flat_time, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0)
    blockout = ones(blockout_width)
    blockout_marker[origin - (flat_time / 2 + 2 * smooth_time + delay) - len(blockout) / 2: origin - (
        flat_time / 2 + 2 * smooth_time + delay) - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def blue_sideband_rabi_expt_gauss(amp, delay, sigma, cutoff, blockout_width, origin, total_length,detuning_freq,
                  measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):

    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich = gauss_sideband(origin - (cutoff + delay), sigma, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0,
                      cutoff_length=cutoff)
    Qch = gauss_sideband(origin - (cutoff + delay), sigma, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0.27*np.pi,
                      cutoff_length=cutoff)
    blockout = ones(blockout_width)
    blockout_marker[origin - (cutoff + delay) - len(blockout) / 2: origin - (
        cutoff + delay) - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def ef_rabi_expt_gauss(amp, delay, ef_rabi_sigma, ef_cutoff, origin, total_length,detuning_freq,
                  measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width, ge_pi_sigma):


    ge_pi_cutoff = ge_pi_sigma *3
    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    blockout_width = 2*ef_cutoff+4*ge_pi_cutoff+600

    Ich = gauss_sideband(origin - (ge_pi_cutoff + delay + 2*ge_pi_cutoff + 2*ef_cutoff), ge_pi_sigma, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0,
                      cutoff_length=ge_pi_cutoff)
    Qch = gauss_sideband(origin - (ge_pi_cutoff + delay + 2*ge_pi_cutoff + 2*ef_cutoff), ge_pi_sigma, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0.27*np.pi,
                      cutoff_length=ge_pi_cutoff)
    Ich += gauss_new(origin - (ef_cutoff + delay + 2*ge_pi_cutoff), ef_rabi_sigma, pulse_height=amp, total_length=total_length,
                      cutoff_length=ef_cutoff)
    Qch += gauss_new(origin - (ef_cutoff + delay + 2*ge_pi_cutoff), ef_rabi_sigma, pulse_height=amp, total_length=total_length,
                      cutoff_length=ef_cutoff)
    Ich += gauss_sideband(origin - (ge_pi_cutoff + delay), ge_pi_sigma, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0,
                      cutoff_length=ge_pi_cutoff)
    Qch += gauss_sideband(origin - (ge_pi_cutoff + delay), ge_pi_sigma, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0.27*np.pi,
                      cutoff_length=ge_pi_cutoff)

    blockout = ones(blockout_width)
    blockout_marker[origin - (ef_cutoff + delay + 2*ge_pi_cutoff + 300) - len(blockout) / 2: origin - (
        ef_cutoff + delay + 2*ge_pi_cutoff + 300) - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def ef_rabi_expt_gauss_no_ge(amp, delay, ef_rabi_sigma, ef_cutoff, origin, total_length,detuning_freq,
                  measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width, ge_pi_sigma):


    ge_pi_cutoff = ge_pi_sigma *3
    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    blockout_width = 2*ef_cutoff+2*ge_pi_cutoff+600

    Ich = gauss_new(origin - (ef_cutoff + delay + 2*ge_pi_cutoff), ef_rabi_sigma, pulse_height=amp, total_length=total_length,
                      cutoff_length=ef_cutoff)
    Qch = gauss_new(origin - (ef_cutoff + delay + 2*ge_pi_cutoff), ef_rabi_sigma, pulse_height=amp, total_length=total_length,
                      cutoff_length=ef_cutoff)
    Ich += gauss_sideband(origin - (ge_pi_cutoff + delay), ge_pi_sigma, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0,
                      cutoff_length=ge_pi_cutoff)
    Qch += gauss_sideband(origin - (ge_pi_cutoff + delay), ge_pi_sigma, pulse_height=amp, total_length=total_length,frequency=detuning_freq, phase = 0.27*np.pi,
                      cutoff_length=ge_pi_cutoff)

    blockout = ones(blockout_width)
    blockout_marker[origin - (ef_cutoff + delay + ge_pi_cutoff + 300) - len(blockout) / 2: origin - (
        ef_cutoff + delay + ge_pi_cutoff + 300) - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def rabi_expt(amp, width, phase, cutoff, blockout_width, origin, total_length,
              measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):
    if width == 0:
        pulse = zeros(1)
    else:
        pulse = gauss(amp, sigma=width, cutoff_length=cutoff)

    Ich = zeros(total_length)
    Qch = zeros(total_length)
    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich[origin - len(pulse) / 2:origin - len(pulse) / 2 + len(pulse)] = np.cos(phase) * pulse
    Qch[origin - len(pulse) / 2:origin - len(pulse) / 2 + len(pulse)] = np.sin(phase) * pulse
    blockout = ones(blockout_width)
    blockout_marker[origin - len(blockout) / 2: origin - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def rabi_expt_new(amp, delay, phase, sigma, cutoff, blockout_width, origin, total_length,
                  measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):
    pulse = gauss_new(origin - (cutoff + delay), sigma, pulse_height=amp, total_length=total_length,
                      cutoff_length=cutoff)

    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich = np.cos(phase) * pulse
    Qch = np.sin(phase) * pulse
    blockout = ones(blockout_width)
    blockout_marker[origin - (cutoff + delay) - len(blockout) / 2: origin - (
        cutoff + delay) - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def rabi_expt_vary_width(amp, delay, flat_time, smooth_time, phase, blockout_width, origin, total_length,
                         measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):
    pulse = smooth_square(origin - (flat_time / 2 + 2 * smooth_time + delay), smooth_time, flat_time, amp, total_length)

    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich = np.cos(phase) * pulse
    Qch = np.sin(phase) * pulse
    blockout = ones(blockout_width)
    blockout_marker[origin - (flat_time / 2 + 2 * smooth_time + delay) - len(blockout) / 2: origin - (
        flat_time / 2 + 2 * smooth_time + delay) - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def ramsey_expt(amp, width, phase, delay, cutoff, blockout_width, origin, total_length,
                measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):
    pulse = gauss(amp, sigma=width, cutoff_length=cutoff)
    Ich = zeros(total_length)
    Qch = zeros(total_length)
    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich[origin - len(pulse) / 2:origin - len(pulse) / 2 + len(pulse)] = np.cos(phase) * pulse
    Qch[origin - len(pulse) / 2:origin - len(pulse) / 2 + len(pulse)] = np.sin(phase) * pulse
    Ich[origin - delay - len(pulse) / 2:origin - delay - len(pulse) / 2 + len(pulse)] = np.cos(phase) * pulse
    Qch[origin - delay - len(pulse) / 2:origin - delay - len(pulse) / 2 + len(pulse)] = np.sin(phase) * pulse

    blockout = ones(blockout_width)
    blockout_marker[origin - len(blockout) / 2: origin - len(blockout) / 2 + len(blockout)] = blockout
    blockout_marker[origin - delay - len(blockout) / 2: origin - delay - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker


def ramsey_expt_squared(amp, flat_time, phase, delay, cutoff, blockout_width, origin, total_length,
                  measurement_pulse_delay, measurement_pulse_width, readout_delay, readout_pulse_width):
    smooth_time = 10
    pulse1 = smooth_square(origin - (flat_time / 2 + 2 * smooth_time), smooth_time, flat_time, amp, total_length)
    pulse2 = smooth_square(origin - (flat_time / 2 + 2 * smooth_time + delay), smooth_time, flat_time, amp, total_length)
    Ich = zeros(total_length)
    Qch = zeros(total_length)
    measurement_marker = zeros(total_length)
    card_marker = zeros(total_length)
    blockout_marker = zeros(total_length)

    Ich += pulse1
    Qch += pulse1
    Ich += pulse2
    Qch += pulse2

    blockout = ones(blockout_width)
    blockout_marker[origin - len(blockout) / 2: origin - len(blockout) / 2 + len(blockout)] = blockout
    blockout_marker[origin - delay - len(blockout) / 2: origin - delay - len(blockout) / 2 + len(blockout)] = blockout
    measurement_marker[
    origin + measurement_pulse_delay:origin + measurement_pulse_delay + measurement_pulse_width] = ones(
        measurement_pulse_width)
    card_marker[origin + readout_delay:origin + readout_delay + readout_pulse_width] = ones(
        readout_pulse_width)

    return Ich, Qch, card_marker, measurement_marker, blockout_marker

# expt.im=InstrumentManager('C:\_Lib\python\slab\instruments\instrument.cfg')

expt = Experiment("S:\\_Data\\150516 - 2D Multimode", prefix='2D_multimode')
expt.plotter.clear()
readout = expt.im.RF2
readout_shifter = expt.im.LBPHASE1
drive = expt.im.RF1
awg = expt.im.TEK
atten = expt.im.atten

####### setup the card

# configure card
azconfig = {'clock_edge': 'rising', 'trigger_edge1': 'rising', 'trigger_edge2': 'rising', 'ch1_filter': True,
            'ch2_filter': False,
            'trigger_coupling': 'DC', 'trigger_operation': 'or', 'trigger_level2': 0.5,
            'trigger_level1': 0.65, 'trigger_source2': 'disabled', 'trigger_source1': 'external',
            'clock_source': 'reference',
            'ch1_enabled': True, 'ch1_coupling': 'DC', 'ch1_range': 1,
            'ch2_enabled': False, 'ch2_range': 0.05, 'ch2_coupling': 'DC',
            'trigger_delay': 0,
            'sample_rate': 1000000, 'samplesPerRecord': 2048, 'recordsPerBuffer': 100, 'bufferCount': 20,
            'recordsPerAcquisition': 101,
            'timeout': 10000
            }




###### configure measurement

readout_power = 16
readout_pulse_width = 100
readout_recovery_time = 100
readout_frequency = 5.07535e9 #7.0846e9  # 7.05756e9
readout_phase = 90
phase_slope =  360.0 / 10.0e6

measurement_pulse_width = 6000

# Load pulses into AWG

pi_width = 100
pi_amp = 0.2
pi2_amp = 0.1
T1_width = 5000 #185
T1_width_gauss = 75
Ramsey_width = 7
Ramsey_freq = 5e6
measurement_pulse_delay = 20
readout_delay = measurement_pulse_delay - 1000

origin = 15000
total_length = 32768
blockout_width = 4 * pi_width

qubit_frequency = 4.2144e9
qubit_gf_2photons_frequency = 6.3328e9
qubit_ef_frequency = 2*qubit_gf_2photons_frequency - qubit_frequency

do_awg = True
do_T1 = False
do_T1_gauss = False
do_ef_rabi = False
do_ef_rabi_no_ge = False
do_sideband_rabi = False
do_blue_sideband_rabi_square= False
do_red_sideband_rabi_square= False
do_rabi = False
do_rabi_new = False
do_rabi_vary_width = False
do_freq = False
do_drive = False
do_drive_power = False
do_phase = False
do_power_freq = False
do_drive_atten = False
do_ramsey = True
do_ramsey_squared = False
do_histogram = False
do_histogram_2 = False
do_histogram_3 = False

# readout.set_ext_pulse(mod=True)
readout.set_power(readout_power)
readout.set_frequency(readout_frequency)
readout.set_output(True)

readout_shifter.set_phase(readout_phase, readout_frequency)

drive.set_frequency(qubit_frequency)
drive.set_ext_pulse(mod=True)
# drive.set_power(10)
# drive.set_output(True)


T1_pts = linspace(100, 45000, 100)
rabi_pts = linspace(0, 1., 100)
rabi_width_pts = linspace(10, 100, 100)
ef_rabi_width_pts = linspace(10, 200, 100)
ramsey_pts = linspace(40, 1000, 100)
ramp_pts = linspace(10., 100., 100)
histo_pts = [1, 75]

repeats = 1
azconfig['sample_rate'] = 500000
azconfig['samplesPerRecord'] = 4096
azconfig['recordsPerBuffer'] = len(rabi_width_pts) * repeats
avgs = 200
azconfig['recordsPerAcquisition'] = avgs * azconfig['recordsPerBuffer']
azconfig['timeout'] = 10000

fname = r'S:\_Data\150516 - 2D Multimode\sequences\optimize_readout.awg'
data_path = "S:\\_Data\\150516 - 2D Multimode\\"
print "Loading " + fname

expt.plotter.clear()

####### setup analysis

window = [0, 1000]
threshold = 0
num_bins = 1000
# prep card
print "Prep card"
adc = Alazar()
adc.configure(AlazarConfig(azconfig))


# start streaming experiment
awg.stop()
awg.prep_experiment()
awg.set_amps_offsets([0.1, 0.1, 0.1, 0.1], [-.012, -.006, 0, 0])  # CW settings

if do_awg and not (do_T1 or do_rabi or do_ramsey or do_histogram or do_histogram_2 or do_rabi_new) and False:
    print "Compiling sequence"
    expt.plotter.clear('seq')
    tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(T1_pts))
    for ii, d in enumerate(T1_pts):
        tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
        tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
        tseq.markers[1][1][ii] = T1_expt(0.5, 0, T1_width, 500, 0, T1_width + 4 * 500 + 1000,
                                         origin, total_length, measurement_pulse_delay,
                                         measurement_pulse_width, readout_delay,
                                         readout_pulse_width)
        expt.plotter.append_z('seq', tseq.waveforms[0][ii])
    tseq.load_into_awg(fname, None)
    awg.pre_load()
    awg.load_sequence_file(fname)

if do_histogram:
    if do_awg:
        print "Compiling sequence"

        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(histo_pts))

        for ii, sigma in enumerate(histo_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = rabi_expt_new(0.5, 0, 0, sigma, 3 * sigma, 6 * sigma + 300,
                                                   origin, total_length, measurement_pulse_delay,
                                                   measurement_pulse_width, readout_delay,
                                                   readout_pulse_width)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Histogram Experiment"
    prefix = "histogram"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    expt.im.atten.set_attenuator(-10)
    drive.set_frequency(qubit_frequency)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-15)
    awg.set_amps_offsets([0.5, 0.5, 0.5, 0.5], [-.012, -0.006, 0, 0])
    ss_data = zeros((len(histo_pts), num_bins))
    sss_data = zeros((len(histo_pts), num_bins))
    for ii in arange(1):
        # tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,excise=(1000,2000))
        #expt.plotter.plot_z("current",ch1_pts)

        ss1, ss2 = adc.acquire_singleshot_data(prep_function=awg.stop_and_prep, start_function=awg.run,
                                               excise=(1000, 2000))
        ss1 = reshape(ss1, (azconfig['recordsPerAcquisition'] / len(histo_pts), len(histo_pts))).T
        if ii == 0:
            histo_range = (ss1.min() / 1.5, ss1.max() * 1.5)
        for jj, ss in enumerate(ss1):
            sshisto, ssbins = np.histogram(ss, bins=num_bins, range=histo_range)
            ss_data[jj] += sshisto
            sss_data[jj] = cumsum(ss_data[[jj]])
            expt.plotter.plot_xy('histogram %d' % jj, ssbins[:-1], ss_data[jj])
            expt.plotter.plot_xy('cum histo %d' % jj, ssbins[:-1], sss_data[jj])
        expt.plotter.plot_xy('contrast', ssbins[:-1], (sss_data[0] - sss_data[1]) / ss_data[0].sum())

if do_histogram_2:
    if do_awg:
        print "Compiling sequence"

        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(histo_pts))

        for ii, sigma in enumerate(histo_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = rabi_expt_new(0.5, 0, 0, sigma, 3 * sigma, 6 * sigma + 300,
                                                   origin, total_length, measurement_pulse_delay,
                                                   measurement_pulse_width, readout_delay,
                                                   readout_pulse_width)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Histogram Optimizing Experiment"
    prefix = "histogram"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    expt.im.atten.set_attenuator(-10)
    drive.set_frequency(qubit_frequency)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-15)
    awg.set_amps_offsets([0.5, 0.5, 0.5, 0.5], [-.012, -0.006, 0, 0])
    ss_data = zeros((len(histo_pts), num_bins))
    sss_data = zeros((len(histo_pts), num_bins))
    attenpts = arange(0, -30, -0.5)
    max_contrast_data = zeros(len(attenpts))
    for xx, atten in enumerate(attenpts):
        expt.im.atten.set_attenuator(atten)
        # tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,excise=(1000,2000))
        #expt.plotter.plot_z("current",ch1_pts)

        ss1, ss2 = adc.acquire_singleshot_data(prep_function=awg.stop_and_prep, start_function=awg.run,
                                               excise=(1000, 1500))
        ss1 = reshape(ss1, (azconfig['recordsPerAcquisition'] / len(histo_pts), len(histo_pts))).T
        histo_range = (ss1.min() / 1.5, ss1.max() * 1.5)
        for jj, ss in enumerate(ss1):
            sshisto, ssbins = np.histogram(ss, bins=num_bins, range=histo_range)
            ss_data[jj] += sshisto
            sss_data[jj] = cumsum(ss_data[[jj]])
            expt.plotter.plot_xy('histogram %d' % jj, ssbins[:-1], ss_data[jj])
            expt.plotter.plot_xy('cum histo %d' % jj, ssbins[:-1], sss_data[jj])
        expt.plotter.plot_xy('contrast', ssbins[:-1], (sss_data[0] - sss_data[1]) / ss_data[0].sum())
        max_contrast_data[xx] = abs(((sss_data[0] - sss_data[1]) / ss_data[0].sum())).max()
        expt.plotter.plot_xy('max contrast', attenpts, max_contrast_data)

if do_histogram_3:
    if do_awg:
        print "Compiling sequence"

        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(histo_pts))

        for ii, sigma in enumerate(histo_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = rabi_expt_new(0.5, 0, 0, sigma, 3 * sigma, 6 * sigma + 300,
                                                   origin, total_length, measurement_pulse_delay,
                                                   measurement_pulse_width, readout_delay,
                                                   readout_pulse_width)
            # expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Histogram Optimizing Experiment 3"
    prefix = "histogram"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    expt.im.atten.set_attenuator(-10)
    drive.set_frequency(qubit_frequency)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-15)
    awg.set_amps_offsets([0.5, 0.5, 0.5, 0.5], [-.012, -0.006, 0, 0])
    attenpts = array([-3])
    # freqpts = [7.0846e9,7.0847e9 ]
    # attenpts = arange(0., -30., -0.5)
    #freqpts = arange(7.055e9, 7.065e9, 100e3)
    freqpts = arange(7.058e9, 7.062e9, 100e3)
    # print freqpts
    awg.run()
    for xx, atten in enumerate(attenpts):
        expt.im.atten.set_attenuator(atten)
        max_contrast_data = zeros(len(freqpts))
        expt.plotter.clear('max contrast')
        for yy, freq in enumerate(freqpts):
            readout.set_frequency(freq)
            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,excise=None)
            expt.plotter.plot_z("current",ch1_pts)
            ss_data = zeros((len(histo_pts), num_bins))
            sss_data = zeros((len(histo_pts), num_bins))

            ss1, ss2 = adc.acquire_singleshot_data(prep_function=None, start_function=None,
                                                   excise=(1000, 2000))


            ss1 = reshape(ss1, (azconfig['recordsPerAcquisition'] / len(histo_pts), len(histo_pts))).T
            histo_range = (ss1.min() / 1.5, ss1.max() * 1.5)
            for jj, ss in enumerate(ss1):
                sshisto, ssbins = np.histogram(ss, bins=num_bins, range=histo_range)
                ss_data[jj] += sshisto
                sss_data[jj] = cumsum(ss_data[[jj]])
                expt.plotter.plot_xy('histogram %d' % jj, ssbins[:-1], ss_data[jj])
                expt.plotter.plot_xy('cum histo %d' % jj, ssbins[:-1], sss_data[jj])

            expt.plotter.plot_xy('contrast', ssbins[:-1], (sss_data[0] - sss_data[1]) / ss_data[0].sum())
            max_contrast_data[yy] = abs(((sss_data[0] - sss_data[1]) / ss_data[0].sum())).max()
            expt.plotter.append_xy('max contrast', freq, max_contrast_data[yy])
        if len(attenpts)>1:
            print "plotting max contrast 2"
            expt.plotter.append_z('max contrast 2', max_contrast_data, start_step=(
             (attenpts[0], attenpts[1] - attenpts[0]),(freqpts[0] / 1.0e9, (freqpts[1] - freqpts[0]) / 1.0e9)))
        with SlabFile(data_fname) as f:
            f.append_pt('atten', atten)
            f.append_line('freq', freqpts)
            f.append_line('max_contrast_data', max_contrast_data)

if do_rabi:
    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(rabi_pts))
        for ii, d in enumerate(rabi_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = rabi_expt(d, pi_width, 0, 4 * pi_width, blockout_width,
                                               origin, total_length, measurement_pulse_delay,
                                               measurement_pulse_width, readout_delay,
                                               readout_pulse_width)
            # expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Rabi Experiment"
    prefix = "rabi"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(qubit_frequency)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-3)
    awg.set_amps_offsets([0.5, 0.5, 0.5, 0.5], [-.008, 0, 0, 0])
    for ii in arange(301):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', rabi_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('rabi_pts', rabi_pts)

if do_rabi_new:
    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(rabi_width_pts))
        for ii, sigma in enumerate(rabi_width_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = rabi_expt_new(1, 0, 0, sigma, 3 * sigma, 6 * sigma + 300,
                                                   origin, total_length, measurement_pulse_delay,
                                                   measurement_pulse_width, readout_delay,
                                                   readout_pulse_width)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Rabi Experiment New"
    prefix = "rabi"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(qubit_frequency)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(0)
    awg.set_amps_offsets([1, 1, 1, 1], [-0.008, -0.039, 0, 0])
    for ii in arange(501):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', rabi_width_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('rabi_pts', rabi_width_pts)

if do_ramsey:
    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(ramsey_pts))
        for ii, d in enumerate(ramsey_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = ramsey_expt(1, Ramsey_width, 0, d, None, blockout_width,
                                                 origin, total_length, measurement_pulse_delay,
                                                 measurement_pulse_width, readout_delay,
                                                 readout_pulse_width)
            # expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Ramsey Experiment"
    prefix = "ramsey"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(qubit_frequency + Ramsey_freq)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-6)
    awg.set_amps_offsets([1, 1, 1, 1], [-0.008, -0.039, 0, 0])
    for ii in arange(501):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', ramsey_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('rabi_pts', ramsey_pts)


if do_ramsey_squared:
    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(ramsey_pts))
        for ii, d in enumerate(ramsey_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = ramsey_expt_squared(1, Ramsey_width, 0, d, None, blockout_width,
                                                 origin, total_length, measurement_pulse_delay,
                                                 measurement_pulse_width, readout_delay,
                                                 readout_pulse_width)
            # expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Ramsey Experiment"
    prefix = "ramsey"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(qubit_frequency + Ramsey_freq)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-6)
    awg.set_amps_offsets([1, 1, 1, 1], [-0.008, -0.039, 0, 0])
    for ii in arange(501):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', ramsey_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('rabi_pts', ramsey_pts)


if do_rabi_vary_width:
    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(rabi_width_pts))
        for ii, rabi_width in enumerate(rabi_width_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = rabi_expt_vary_width(1, 0, rabi_width, 10, 0, rabi_width + 4 * 10 + 200,
                                                          origin, total_length, measurement_pulse_delay,
                                                          measurement_pulse_width, readout_delay,
                                                          readout_pulse_width)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Rabi Experiment Vary Width"
    prefix = "rabi"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(qubit_frequency)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(0)
    awg.set_amps_offsets([1, 1, 1, 1], [-0.008, -0.039, 0, 0])
    for ii in arange(101):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', rabi_width_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('rabi_pts', rabi_width_pts)

if do_ef_rabi:
    ge_sideband_pi_sigma = 45.86
    RF1_freq = qubit_ef_frequency
    detuning_freq = abs(qubit_frequency-RF1_freq)

    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(T1_pts))
        for ii, rabi_width in enumerate(ef_rabi_width_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = ef_rabi_expt_gauss(1, 0, rabi_width,3 * rabi_width,
                                                   origin, total_length, detuning_freq,measurement_pulse_delay,
                                                   measurement_pulse_width, readout_delay,
                                                   readout_pulse_width,ge_sideband_pi_sigma)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "EF Rabi Experiment"
    prefix = "EF Rabi"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(RF1_freq)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-3)
    awg.set_amps_offsets([1, 1, 1, 1], [-.012, -.006, 0, 0])
    for ii in arange(21):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', ef_rabi_width_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('ef_rabi_width_pts', ef_rabi_width_pts)

if do_ef_rabi_no_ge:
    ge_sideband_pi_sigma = 45.86
    RF1_freq = qubit_ef_frequency
    detuning_freq = abs(qubit_frequency-RF1_freq)

    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(T1_pts))
        for ii, rabi_width in enumerate(ef_rabi_width_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = ef_rabi_expt_gauss_no_ge(1, 0, rabi_width,3 * rabi_width,
                                                   origin, total_length, detuning_freq,measurement_pulse_delay,
                                                   measurement_pulse_width, readout_delay,
                                                   readout_pulse_width,ge_sideband_pi_sigma)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "EF Rabi Experiment"
    prefix = "EF Rabi"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(RF1_freq)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-3)
    awg.set_amps_offsets([1, 1, 1, 1], [-.012, -.006, 0, 0])
    for ii in arange(101):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', ef_rabi_width_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('ef_rabi_width_pts', ef_rabi_width_pts)

if do_sideband_rabi:
    RF1_freq = qubit_ef_frequency
    detuning_freq = abs(qubit_frequency-RF1_freq)

    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(T1_pts))
        for ii, rabi_width in enumerate(rabi_width_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = blue_sideband_rabi_expt_gauss(1, 0, rabi_width,3 * rabi_width, 6 * rabi_width + 300,
                                                   origin, total_length, detuning_freq,measurement_pulse_delay,
                                                   measurement_pulse_width, readout_delay,
                                                   readout_pulse_width)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Sideband Rabi Experiment"
    prefix = "Sideband Rabi"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(RF1_freq)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-3)
    awg.set_amps_offsets([1, 1, 1, 1], [-.012, -.006, 0, 0])
    for ii in arange(101):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', rabi_width_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('rabi_width_pts', rabi_width_pts)

if do_blue_sideband_rabi_square:
    RF1_freq = qubit_ef_frequency #6.4400e9 #6.5216e9
    detuning_freq = abs(qubit_frequency-RF1_freq)

    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(T1_pts))
        for ii, rabi_width in enumerate(rabi_width_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = blue_sideband_rabi_expt_square(1, 0,10, rabi_width, 4*10+ rabi_width + 300,
                                                   origin, total_length, detuning_freq,measurement_pulse_delay,
                                                   measurement_pulse_width, readout_delay,
                                                   readout_pulse_width)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Sideband Rabi Experiment"
    prefix = "Sideband Rabi"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(RF1_freq)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-3)
    awg.set_amps_offsets([1, 1, 1, 1], [-.012, -.006, 0, 0])
    for ii in arange(101):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', rabi_width_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('rabi_width_pts', rabi_width_pts)

if do_red_sideband_rabi_square:
    RF1_freq = 6.4400e9 #6.5216e9
    detuning_freq = abs(qubit_frequency-RF1_freq)

    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(T1_pts))
        for ii, rabi_width in enumerate(rabi_width_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = red_sideband_rabi_expt_square(1, 0,10, rabi_width, 4*10+ rabi_width + 300,
                                                   origin, total_length, detuning_freq,measurement_pulse_delay,
                                                   measurement_pulse_width, readout_delay,
                                                   readout_pulse_width)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "Sideband Rabi Experiment"
    prefix = "Sideband Rabi"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(RF1_freq)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-3)
    awg.set_amps_offsets([1, 1, 1, 1], [-.012, -.006, 0, 0])
    for ii in arange(101):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', rabi_width_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('rabi_width_pts', rabi_width_pts)

if do_T1_gauss:
    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(T1_pts))
        for ii, d in enumerate(T1_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = T1_expt_gauss(0.5, d,0, T1_width_gauss,3 * T1_width_gauss, 6 * T1_width_gauss + 300,
                                                   origin, total_length, measurement_pulse_delay,
                                                   measurement_pulse_width, readout_delay,
                                                   readout_pulse_width)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "T1 Experiment"
    prefix = "T1"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(qubit_frequency)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-3)
    awg.set_amps_offsets([0.5, 0.5, 0.5, 0.5], [-.012, -.006, 0, 0])
    for ii in arange(101):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', T1_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('T1_pts', T1_pts)


if do_T1:
    if do_awg:
        print "Compiling sequence"
        tseq = Tek5014Sequence(waveform_length=total_length, sequence_length=len(T1_pts))
        for ii, d in enumerate(T1_pts):
            tseq.waveforms[0][ii], tseq.waveforms[1][ii], \
            tseq.markers[0][0][ii], tseq.markers[0][1][ii], \
            tseq.markers[1][1][ii] = T1_expt(0.5, d, T1_width, 10, 0, T1_width + 4 * 10 + 200,
                                             origin, total_length, measurement_pulse_delay,
                                             measurement_pulse_width, readout_delay,
                                             readout_pulse_width)
            expt.plotter.append_z('seq', tseq.waveforms[0][ii])
        tseq.load_into_awg(fname, None)
        awg.pre_load()
        awg.load_sequence_file(fname)

    print "T1 Experiment"
    prefix = "T1"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    rabi_data = None
    readout.set_frequency(readout_frequency)
    drive.set_frequency(qubit_frequency)
    drive.set_power(13)
    drive.set_output(True)
    expt.im.atten.set_attenuator(-3)
    awg.set_amps_offsets([0.5, 0.5, 0.5, 0.5], [-.012, -.006, 0, 0])
    for ii in arange(101):
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data_by_record(prep_function=awg.stop_and_prep, start_function=awg.run,
                                                                excise=(1000, 2000))
        # tpts, ch1_pts, ch2_pts = adc.acquire_data_by_record(start_function=awg.run, excise=None)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        if rabi_data is None:
            rabi_data = ch1_pts
        else:
            rabi_data = (rabi_data * ii + ch1_pts) / (ii + 1.0)
        if ii % 1 == 0:
            expt.plotter.plot_z('Rabi Data', rabi_data.T)
            rabi_avg_data = mean(rabi_data, 1)
            expt.plotter.plot_xy('Rabi XY', T1_pts, rabi_avg_data)

            print ii * avgs
        with SlabFile(data_fname) as f:
            f.append_line('rabi_avg_data', rabi_avg_data)
            f.append_line('T1_pts', T1_pts)

awg.run()
time.sleep(.5)
if do_freq:
    print "Scan readout"
    prefix = "vacuum_rabi"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    fpts = linspace(5.075e9, 5.085e9, 101)#linspace(readout_frequency - 5e6, readout_frequency + 40e6, 101)
    # print fpts[185]
    drive.set_output(True)
    drive.set_mod(False)
    readout.set_mod(True)
    expt.im.atten.set_attenuator(0)
    awg.set_amps_offsets([0,0,0,0],[.5,.5,.5,.5])
    for freq in fpts:
        #print (readout_phase + phase_slope * (freq - readout_frequency))%360
        readout_shifter.set_phase((readout_phase + phase_slope * (freq - readout_frequency))%360, freq)
        readout.set_frequency(freq)
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data()  # excise=(320, -1))
        # print freq
        #expt.plotter.append_z('readout_freq_scan', ch1_pts)
        expt.plotter.plot_xy('current1', tpts, ch1_pts)
        expt.plotter.append_xy('readout_avg_freq_scan1', freq, mean(ch1_pts[0:]))
        expt.plotter.append_xy('readout_avg_freq_scan2', freq, mean(ch2_pts[0:]))
        with SlabFile(data_fname) as f:
            f.append_pt('freq', freq)
            f.append_pt('ch1_mean', mean(ch1_pts[0:]))

if do_power_freq:
    print "Scan readout"
    prefix = "atten_freq_sweep"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    fpts = linspace(readout_frequency - 50e6, readout_frequency + 1e6, 101)
    # print fpts[185]
    # attenpts = [-20]
    attenpts = arange(0, -10, -0.5)
    # awg.set_amps_offsets([0, 0, 0, 0], [.5, .5, .5, .5])  #CW settings
    drive.set_power(-25)
    drive.set_output(False)
    readout.set_mod(True)
    for atten in attenpts:
        print "Scanning attenuation point: " + str(atten)
        expt.im.atten.set_attenuator(atten)
        expt.plotter.clear('ch1_readout_freq_scan')
        expt.plotter.clear('ch1 current')
        expt.plotter.clear('readout_avg_freq_scan ch1')
        Tx1pts = []
        Tx2pts = []
        for freq in fpts:
            readout.set_frequency(freq)
            readout_shifter.set_phase((readout_phase + phase_slope * (freq - readout_frequency))%360, freq)
            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data(excise=(0, -1))
            Tx1pts.append(mean(ch1_pts))
            Tx2pts.append(mean(ch2_pts))
            # print freq
            expt.plotter.append_z('ch1_readout_freq_scan', ch1_pts)
            #expt.plotter.append_z('ch2_readout_freq_scan', ch2_pts)
            expt.plotter.plot_xy('ch1 current', tpts, ch1_pts)
            #expt.plotter.plot_xy('ch2 current', tpts, ch2_pts)
            expt.plotter.append_xy('readout_avg_freq_scan ch1', freq, mean(ch1_pts))
            #expt.plotter.append_xy('readout_avg_freq_scan ch2', freq, mean(ch2_pts))

        expt.plotter.append_z('atten_freq_scan1', Tx1pts)
        # expt.plotter.append_z('atten_freq_scan2',Tx2pts)
        with SlabFile(data_fname) as f:
            f.append_line('tpts', tpts)
            f.append_line('fpts', fpts)
            f.append_line('mags1', Tx1pts)
            f.append_line('mags2', Tx2pts)
            f.append_pt('atten_pts', atten)

if do_drive:
    "Scan drive"
    prefix = "drive"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    fpts = linspace(4.3e9, 4.5e9, 101)
    readout.set_frequency(readout_frequency)
    # drive.set_ext_pulse(mod=True)
    # readout.set_mod(False)
    readout.set_ext_pulse(mod=True)
    # drive.set_mod(False)
    #awg.set_amps_offsets([0, 0, 0, 0], [.25, .25, .25, .25])  #CW settings
    drive.set_power(13)
    expt.im.atten.set_attenuator(0)
    drive.set_output(True)
    for freq in fpts:
        drive.set_frequency(freq)
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data(excise=(1000, 2000))
        expt.plotter.append_z('drive_freq_scan', ch1_pts)
        expt.plotter.plot_xy('current', tpts, ch1_pts)
        expt.plotter.append_xy('drive_freq_avg_scan', freq / 1e9, mean(ch1_pts))
        with SlabFile(data_fname) as f:
            f.append_pt('ch1_pts_mean', mean(ch1_pts))
            f.append_pt('freq', freq)

if do_drive_power:
    "Scan drive"
    prefix = "drive_power"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    fpts = linspace(6.47e9, 6.49e9, 101)
    powpts = linspace(-35, 0, 36)
    readout.set_frequency(readout_frequency)
    # drive.set_ext_pulse(mod=False)
    readout.set_mod(False)
    drive.set_mod(False)
    awg.set_amps_offsets([0, 0, 0, 0], [.5, .5, .5, .5])  # CW settings
    expt.im.atten.set_attenuator(-3)
    drive.set_output(True)
    for pow in powpts:
        drive.set_power(pow)
        mag = []
        expt.plotter.clear('drive_freq_avg_scan')
        expt.plotter.clear('drive_freq_scan')
        for freq in fpts:
            drive.set_frequency(freq)
            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data(excise=(350, -1))
            mag.append(mean(ch1_pts))
            expt.plotter.append_z('drive_freq_scan', ch1_pts)
            expt.plotter.plot_xy('current', tpts, ch1_pts)
            expt.plotter.append_xy('drive_freq_avg_scan', freq / 1e9, mag[-1])
        expt.plotter.append_z('drive_power', array(mag))
        with SlabFile(data_fname) as f:
            f.append_pt('powpts', pow)
            f.append_line('mags', mag)
            f.append_line('fpts', fpts)

if do_drive_atten:
    "Scan drive"
    prefix = "drive_power"
    data_fname = get_next_filename(data_path, prefix, suffix='.h5')
    fpts = linspace(6.47e9, 6.49e9, 101)
    powpts = arange(-10, -30, -0.5)
    readout.set_frequency(readout_frequency)
    drive.set_ext_pulse(mod=True)
    readout.set_ext_pulse(mod=True)
    # readout.set_mod(True)
    # drive.set_mod(True)
    # awg.set_amps_offsets([0, 0, 0, 0], [.5, .5, .5, .5])  #CW settings
    drive.set_power(-25)
    drive.set_output(True)
    for pow in powpts:
        expt.im.atten.set_attenuator(pow)
        mag = []
        expt.plotter.clear('drive_freq_avg_scan')
        expt.plotter.clear('drive_freq_scan')
        for freq in fpts:
            drive.set_frequency(freq)
            tpts, ch1_pts, ch2_pts = adc.acquire_avg_data(excise=(350, -1))
            mag.append(mean(ch1_pts))
            expt.plotter.append_z('drive_freq_scan', ch1_pts)
            expt.plotter.plot_xy('current', tpts, ch1_pts)
            expt.plotter.append_xy('drive_freq_avg_scan', freq / 1e9, mag[-1])
        expt.plotter.append_z('drive_power', array(mag))
        with SlabFile(data_fname) as f:
            f.append_pt('powpts', pow)
            f.append_line('mags', mag)
            f.append_line('fpts', fpts)

if do_phase:
    "Scan readout phase"
    phase_pts = linspace(0, 180, 181)
    readout.set_frequency(readout_frequency)
    drive.set_frequency(qubit_frequency)
    for phase in phase_pts:
        readout_shifter.set_phase(phase, frequency=readout_frequency)
        tpts, ch1_pts, ch2_pts = adc.acquire_avg_data()

        expt.plotter.append_z('phase_scan', ch1_pts)
        expt.plotter.plot_xy('current', tpts, ch1_pts)
