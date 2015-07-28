__author__ = 'Nelson'

from HistogramExperiment import *

histo=HistogramExperiment(path=r"S:\_Data\150707 - 3D Qubit Chip Ar3D2 (Al cavity)\data",prefix='Histogram',config_file='..\\config.json')

if histo.ready_to_go:
    histo.go()
