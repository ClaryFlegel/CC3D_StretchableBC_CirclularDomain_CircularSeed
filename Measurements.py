import cc3d
from cc3d.core.PySteppables import SteppableBasePy
#from WoundMakerForce import WoundMakerSteppable
import numpy as np 
import math

#from Parameters import *
import Parameters
from pathlib import Path

class Measurements(SteppableBasePy):
    def __init__(self, frequency=1, run_id=0):
        super().__init__(frequency=frequency)

        self.run_id=run_id
        self.wound_closed_flag = False # it is not yet opened really
        self.header_updated = False
        self.closed_counter = 0


    def start(self,run_id=0):
        self.run_dir = Path("Runs") / f"Lx{Parameters.grid_x}_Ly{Parameters.grid_y}" / f"R{Parameters.wR}"
        self.run_dir.mkdir(parents=True, exist_ok=True)

        # Optional: delete all old measurement files for this wound folder
        #for f in self.run_dir.glob("simulation_results_*.txt"):
        #    f.unlink()
            #print(f"[Measurements] Deleted old file {f.name}")

        # create file path
        self.output_file = self.run_dir / f"simulation_results_{self.run_id}.txt"

        #self.output_file = f"simulation_results_{run_id}.txt"
        #with open(self.output_file, "a") as f:
        #    f.write("mcs, wound Area\n")

        with open(self.output_file, "w") as f:
            f.write(f"# Domain Size: Lx={Parameters.grid_x}, Ly={Parameters.grid_y}\n")
            f.write(f"# Wound Radius Created: R={Parameters.wR}\n")
            f.write("# Wound created at mcs: {wound_mcs}\n")  # placeholder
            f.write("mcs,woundArea\n")
  
    def step(self,mcs):
        #print("wound_mcs seen by Measurements:", Parameters.wound_mcs)
        if not self.header_updated:
            #wound_steppable = self.get_steppable_by_class(WoundMakerSteppable)
            #wound_mcs = wound_steppable.wound_mcs

            if Parameters.wound_mcs is not None:
                self._update_wound_header(Parameters.wound_mcs)
                self.header_updated = True
        #print(f"Measurements step called at MCS={mcs}")  # Debug line
        # woundArea=0
        # occupiedArea=0
        # for cell in self.cell_list:
        #     occupiedArea += cell.volume
        # woundArea=(grid_x-3)*(grid_y-3) - occupiedArea
        woundArea = self.compute_wound_area()
        
        with open(self.output_file, "a") as f:
            f.write(f"{mcs},{woundArea}\n")
        
        if self.header_updated and not self.wound_closed_flag:
            if woundArea == 0:
                self.closed_counter += 1
            else:
                self.closed_counter = 0

            if self.closed_counter >= 3:
                print(f"Wound stably closed at mcs {mcs}")
                self.wound_closed_flag = True
                self.stop_simulation()


    def compute_wound_area(self):
        woundArea = 0
        for x in range(Parameters.grid_x):
            for y in range(Parameters.grid_y):
                if self.cellField[x, y, 0] is None:  # medium pixel
                    woundArea += 1
        return woundArea
    
    def _update_wound_header(self, wound_mcs):
        with open(self.output_file, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith("# Wound created at mcs:"):
                lines[i] = f"# Wound created at mcs: {wound_mcs}\n"
                break

        with open(self.output_file, "w") as f:
            f.writelines(lines)