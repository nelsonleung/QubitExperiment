__author__ = 'Nitrogen'

from CWDriveExperiment import *
from RabiExperiment import *
from RamseyExperiment import *
from T1Experiment import *
from VacuumRabiExperiment import *
from HistogramExperiment import *
from EFProbeExperiment import *
from EFRabiExperiment import *

datapath = r"S:\_Data\150716 - 2D multimode (Chip 1)\data"

#Do CW drive experiment
#expt=CWDriveExperiment(path=datapath,prefix='cw_drive',config_file='..\\config.json')

#Do Rabi Experiment
#expt=RabiExperiment(path=datapath,prefix='Rabi',config_file='..\\config.json')

#Do Histogram Experiment
#expt=HistogramExperiment(path=datapath,prefix='Histogram',config_file='..\\config.json')

#Do resonator sweep
#expt=VacuumRabiExperiment(path=datapath,prefix='Vacuum_Rabi',config_file='..\\config.json')

#Do T1 Experiment
#expt=T1Experiment(path=datapath,prefix='T1',config_file='..\\config.json')

#Do Ramsey Experiment
expt=RamseyExperiment(path=datapath,prefix='Ramsey',config_file='..\\config.json')

#Do EFProbe Experiment
#expt=EFProbeExperiment(path=datapath,prefix='EF Probe',config_file='..\\config.json')

#Do EF Rabi Experiment
#expt=EFRabiExperiment(path=datapath,prefix='EF Rabi',config_file='..\\config.json')


expt.go()
