"""Unstructured 2D mesh around a NACA0012 -> SU2 format (needs: pip install gmsh)."""
import numpy as np
import gmsh

N = 80          # points per surface
R_FAR = 50.0    # far-field radius in chords
gmsh.initialize()
gmsh.model.add("naca0012")

x = (1 - np.cos(np.linspace(0, np.pi, N))) / 2          # cosine spacing
yt = 5 * 0.12 * (0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1036*x**4)  # closed TE

up = [gmsh.model.geo.addPoint(xi, yi, 0, 0.004) for xi, yi in zip(x, yt)]
lo = [gmsh.model.geo.addPoint(xi, -yi, 0, 0.004) for xi, yi in zip(x[1:-1], yt[1:-1])]
# loop: LE -> TE on the upper surface, TE -> LE on the lower
pts_up = up[::-1]                     # TE -> LE ordering fix below
sp_u = gmsh.model.geo.addSpline(up)                          # LE -> TE (upper)
sp_l = gmsh.model.geo.addSpline([up[0]] + lo + [up[-1]])      # LE -> TE (lower)
airfoil = [sp_u, sp_l]

c = gmsh.model.geo.addPoint(0.5, 0, 0, 5.0)
f = [gmsh.model.geo.addPoint(0.5 + R_FAR*np.cos(a), R_FAR*np.sin(a), 0, 5.0) for a in (0, np.pi/2, np.pi, 3*np.pi/2)]
arcs = [gmsh.model.geo.addCircleArc(f[i], c, f[(i+1) % 4]) for i in range(4)]
outer = gmsh.model.geo.addCurveLoop(arcs)
inner = gmsh.model.geo.addCurveLoop([sp_u, -sp_l])
surf = gmsh.model.geo.addPlaneSurface([outer, inner])
gmsh.model.geo.synchronize()

# size field: fine near the airfoil, coarse far away
d = gmsh.model.mesh.field.add("Distance"); gmsh.model.mesh.field.setNumbers(d, "CurvesList", airfoil)
gmsh.model.mesh.field.setNumber(d, "Sampling", 200)
t = gmsh.model.mesh.field.add("Threshold")
for k, v in dict(InField=d, SizeMin=0.004, SizeMax=6.0, DistMin=0.05, DistMax=30.0).items():
    gmsh.model.mesh.field.setNumber(t, k, v)
gmsh.model.mesh.field.setAsBackgroundMesh(t)

gmsh.model.addPhysicalGroup(1, airfoil, name="airfoil")
gmsh.model.addPhysicalGroup(1, arcs, name="farfield")
gmsh.model.addPhysicalGroup(2, [surf], name="fluid")
gmsh.model.mesh.generate(2)
gmsh.write("naca0012.su2")
print("cells:", len(gmsh.model.mesh.getElements(2)[1][0]))
gmsh.finalize()
