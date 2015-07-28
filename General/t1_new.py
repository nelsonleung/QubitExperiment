__author__ = 'Nelson'

from T1Experiment import *

t1=T1Experiment(path=r"S:\_Data\150707 - 3D Qubit Chip Ar3D2 (Al cavity)\data",prefix='T1',config_file='..\\config.json')

if t1.ready_to_go:
    t1.go()
