import cc3d
from cc3d.core.PySteppables import SteppableBasePy
#from cc3d.core.PyCoreSpecs import PixelTrackerPlugin, BoundaryPixelTrackerPlugin, NeighborTrackerPlugin
import numpy as np 
#import math

#important! need square domain from wound creation logic
grid_x = 252 #multiple of 12 bc of layers 
grid_y = grid_x


#woundMakerTime=100 #mcs when wound is created -- No longer needed with WoundMakerForce.py instead of Steppable_S.py
wR = 40 # wound radius in pixels 
target_volume, lambda_volume = 100, 1
wound_mcs = None
relaxation_mcs = 200 #after domain completely filled wait relaxation_mcs before opening wound 
force=1200

N=8 #repeated runs
t=100001 #not inclusive: last mcs = t-1 ----- Maximum MCS 

thick_f = 4
thick_w = 2
r_fc = (min(grid_x, grid_y) // 2) - (thick_w + thick_f)
N_expected = int(np.pi * r_fc**2 / target_volume)

domain_filled = False
domain_filled_mcs = None

