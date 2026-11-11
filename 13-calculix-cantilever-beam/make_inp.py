"""Generate a structured hexahedral cantilever mesh + CalculiX input deck (C3D8I elements)."""
import sys
L, W, H = 1000.0, 50.0, 50.0       # mm
E, NU = 210e3, 0.3                 # MPa
P = 1000.0                         # N total tip load (-z)
nx, ny, nz = (int(v) for v in (sys.argv[1:4] if len(sys.argv) == 4 else (40, 4, 4)))

nid = lambda i, j, k: i + (nx + 1) * (j + (ny + 1) * k) + 1
with open("beam.inp", "w") as f:
    f.write("*HEADING\nCantilever beam, tip load, C3D8I\n*NODE\n")
    for k in range(nz + 1):
        for j in range(ny + 1):
            for i in range(nx + 1):
                f.write(f"{nid(i,j,k)}, {L*i/nx:.6f}, {W*j/ny:.6f}, {H*k/nz:.6f}\n")
    f.write("*ELEMENT, TYPE=C3D8I, ELSET=EALL\n")
    e = 1
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                n = [nid(i, j, k), nid(i+1, j, k), nid(i+1, j+1, k), nid(i, j+1, k),
                     nid(i, j, k+1), nid(i+1, j, k+1), nid(i+1, j+1, k+1), nid(i, j+1, k+1)]
                f.write(f"{e}, " + ", ".join(map(str, n)) + "\n"); e += 1
    fixed = [nid(0, j, k) for k in range(nz + 1) for j in range(ny + 1)]
    tip = [nid(nx, j, k) for k in range(nz + 1) for j in range(ny + 1)]
    f.write("*NSET, NSET=FIXED\n" + ",\n".join(map(str, fixed)) + "\n")
    f.write("*NSET, NSET=TIP\n" + ",\n".join(map(str, tip)) + "\n")
    f.write(f"*MATERIAL, NAME=STEEL\n*ELASTIC\n{E}, {NU}\n*SOLID SECTION, ELSET=EALL, MATERIAL=STEEL\n")
    f.write("*BOUNDARY\nFIXED, 1, 3\n*STEP\n*STATIC\n*CLOAD\n")
    for n in tip:
        f.write(f"{n}, 3, {-P/len(tip):.6f}\n")
    f.write("*NODE FILE\nU\n*EL FILE\nS\n*NODE PRINT, NSET=TIP\nU\n*END STEP\n")
print(f"Wrote beam.inp: {(nx+1)*(ny+1)*(nz+1)} nodes, {nx*ny*nz} elements")
