#!/bin/bash
set -e
gmsh -2 plate.geo -o plate.msh
ElmerGrid 14 5 plate.msh -out mesh      # Gmsh -> Elmer mesh in ./mesh
ElmerSolver case.sif | tee solver.log
echo "Open heat.vtu in ParaView (Temperature field)."
