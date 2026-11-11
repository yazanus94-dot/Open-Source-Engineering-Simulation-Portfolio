"""Plate with a hole: OpenCASCADE geometry, distance-based refinement, quality statistics (Gmsh Python API)."""
import sys
import numpy as np
import gmsh
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

W, H, R = 200.0, 100.0, 10.0
h_min, h_max = 1.0, 12.0
order = int(sys.argv[1]) if len(sys.argv) > 1 else 1

gmsh.initialize(); gmsh.model.add("plate")
occ = gmsh.model.occ
rect = occ.addRectangle(0, 0, 0, W, H)
hole = occ.addDisk(W / 2, H / 2, 0, R, R)
plate, _ = occ.cut([(2, rect)], [(2, hole)])
occ.synchronize()

curves = gmsh.model.getEntities(1)
left = [c[1] for c in curves if np.isclose(gmsh.model.occ.getCenterOfMass(1, c[1])[0], 0)]
right = [c[1] for c in curves if np.isclose(gmsh.model.occ.getCenterOfMass(1, c[1])[0], W)]
hole_c = [c[1] for c in curves if np.isclose(gmsh.model.occ.getCenterOfMass(1, c[1])[0], W / 2, atol=R)
          and gmsh.model.getBoundingBox(1, c[1])[3] - gmsh.model.getBoundingBox(1, c[1])[0] < 2 * R + 1e-6]
gmsh.model.addPhysicalGroup(1, left, name="clamped")
gmsh.model.addPhysicalGroup(1, right, name="load")
gmsh.model.addPhysicalGroup(1, hole_c, name="hole")
gmsh.model.addPhysicalGroup(2, [plate[0][1]], name="plate")

f_d = gmsh.model.mesh.field.add("Distance"); gmsh.model.mesh.field.setNumbers(f_d, "CurvesList", hole_c)
gmsh.model.mesh.field.setNumber(f_d, "Sampling", 100)
f_t = gmsh.model.mesh.field.add("Threshold")
for k, v in dict(InField=f_d, SizeMin=h_min, SizeMax=h_max, DistMin=R * 0.5, DistMax=W / 3).items():
    gmsh.model.mesh.field.setNumber(f_t, k, v)
gmsh.model.mesh.field.setAsBackgroundMesh(f_t)
gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
gmsh.option.setNumber("Mesh.Algorithm", 6)         # Frontal-Delaunay
gmsh.model.mesh.generate(2)
if order > 1: gmsh.model.mesh.setOrder(order)

tags, _ = gmsh.model.mesh.getElementsByType(2 if order == 1 else 9)
q = np.array(gmsh.model.mesh.getElementQualities(tags, "minSICN"))
print(f"elements: {len(tags)}  min quality: {q.min():.3f}  mean: {q.mean():.3f}")
plt.hist(q, bins=40); plt.xlabel("minSICN (1 = ideal)"); plt.ylabel("elements"); plt.title("Mesh quality")
plt.savefig("quality.png", dpi=200)

gmsh.option.setNumber("Mesh.MshFileVersion", 4.1)
gmsh.write("plate.msh"); gmsh.write("plate.vtk")
# gmsh.fltk.run()   # uncomment for the GUI
gmsh.finalize()
