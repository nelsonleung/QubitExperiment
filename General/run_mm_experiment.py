__author__ = 'Nelson'

from MultimodeFluxSideBandRabiExperiment import *
from MultimodeFluxSideBandT1Experiment import *
from MultimodeFluxSideBandT2Experiment import *
from MultimodeFluxSideBandTwoModesSwapSweepExperiment import *
import gc
import json
from slab.instruments.Alazar import Alazar


path = r"S:\_Data\150716 - 2D multimode (Chip 1)\data"


config_file = os.path.join(path, "..\\config" + ".json")
with open(config_file, 'r') as fid:
    cfg_str = fid.read()

cfg = AttrDict(json.loads(cfg_str))

print "Prep Card"
adc = Alazar(cfg['alazar'])

## Rabi
#expt=MultimodeFluxSideBandRabiExperiment(path=path,prefix='MM_Flux_Sideband_Rabi',config_file='..\\config.json')

## T1
expt=MultimodeFluxSideBandT1Experiment(path=path,prefix='MM_Flux_Sideband_T1',config_file='..\\config.json')

## T2
#expt=MultimodeFluxSideBandT2Experiment(path=path,prefix='MM_Flux_Sideband_T2',config_file='..\\config.json')

## Two Modes Swap Sweep
#expt=MultimodeFluxSideBandTwoModesSwapSweepExperiment(path=path,prefix='MM_Flux_Sideband_Two_Modes_Swap_Sweep',config_file='..\\config.json')

expt.go(adc=adc)

