__author__ = 'Nitrogen'

from RabiExperiment import *

rabi=RabiExperiment(path=r"S:\_Data\150707 - 3D Qubit Chip Ar3D2 (Al cavity)\data",prefix='Rabi',config_file='..\\config.json')

if rabi.ready_to_go:
    rabi.go()
