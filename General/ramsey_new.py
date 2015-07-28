__author__ = 'Nelson'

from RamseyExperiment import *

ramsey=RamseyExperiment(path=r"S:\_Data\150707 - 3D Qubit Chip Ar3D2 (Al cavity)\data",prefix='Ramsey',config_file='..\\config.json')

if ramsey.ready_to_go:
    ramsey.go()
