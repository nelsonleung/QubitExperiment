__author__ = 'Nelson'

from EFRabiExperiment import *

efrabi=EFRabiExperiment(path=r"S:\_Data\150707 - 3D Qubit Chip Ar3D2 (Al cavity)\data",prefix='EF Rabi',config_file='..\\config.json')

if efrabi.ready_to_go:
    efrabi.go()
