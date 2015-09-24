__author__ = 'dave'

import numpy as np


def sideband(t, i, q, freq=0, phase=0):
    return ( np.cos(2 * np.pi * (freq/1.0e9 * t )+ phase*np.pi/180.0) * i - np.cos(2 * np.pi * (freq/1.0e9 * t) + phase*np.pi/180.0) * q,
             -np.sin(2 * np.pi * (freq/1.0e9 * t )+ phase*np.pi/180.0) * i - np.sin(2 * np.pi * (freq/1.0e9 * t ) + phase*np.pi/180.0) * q)


def getFreq(time,time_array,pulse,freq,offset_fit_lin=0,offset_fit_quad=0):
    #time is a point
    #pulse is an array
    time_idx = (np.abs(np.array(time_array)-time)).argmin()
    print time_idx
    offset = offset_fit_lin*pulse[time_idx]+offset_fit_quad*pulse[time_idx]**2
    print offset
    return freq-offset


def gauss(t, a, t0, sigma):
    if sigma >0:
        return a * np.exp(-1.0 * (t - t0) ** 2 / (2 * sigma ** 2))
    else:
        return 0*(t-t0)


def dgauss(t, a, t0, sigma):
    return a * np.exp(-1.0 * (t - t0) ** 2 / (2 * sigma ** 2)) * (t - t0) / sigma ** 2


def ramp(t, a, t0, w):
    return a * (t - t0) * (t >= t0) * (t < t0 + w)


def square(t, a, t0, w, sigma=0):
    if sigma>0:
        return a * (
            (t >= t0) * (t < t0 + w) +  # Normal square pulse
            (t < t0) * np.exp(-(t - t0) ** 2 / (2 * sigma ** 2)) +  # leading gaussian edge
            (t >= t0 + w) * np.exp(-(t - (t0 + w)) ** 2 / (2 * sigma ** 2))  # trailing edge
        )
    else:
        return a * (t >= t0) * (t < t0 + w)


def trapezoid(t, a, t0, w, edge_time=0):
    return a * (
        (t - t0) * (t >= t0) * (t < t0 + edge_time) + (t >= t0 + edge_time) * (t < t0 + edge_time + w) + (
            t0 - t) * (
            t >= t0 + w + edge_time) * (
            t >= t0 + w + 2 * edge_time) )


def get_pulse_span_length(cfg, type, length):
    if type == "gauss":
        return length * 6
    if type == "square":
        return length + 6 * cfg[type]['ramp_sigma']
