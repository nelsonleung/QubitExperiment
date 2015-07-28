__author__ = 'Nitrogen'

from VacuumRabiExperiment import *

vacuum_rabi=VacuumRabiExperiment(path=r"S:\_Data\150629 - 3D Qubit Chip Ar3D2 (Al cavity)\data",prefix='Vacuum_Rabi',config_file='..\\config.json')

vacuum_rabi.go()
