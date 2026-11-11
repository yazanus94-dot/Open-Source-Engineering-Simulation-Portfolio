"""3D linear elasticity: cantilever under self-weight, verified against Euler-Bernoulli.
Tested with DOLFINx 0.8/0.9 (conda-forge: fenics-dolfinx)."""
import numpy as np
from mpi4py import MPI
import ufl
from dolfinx import mesh, fem, io, default_scalar_type
from dolfinx.fem.petsc import LinearProblem

L, W = 1.0, 0.1                 # length, square section side [m]
E, nu, rho, g = 210e9, 0.3, 7850.0, 9.81
mu = E / (2 * (1 + nu))
lmbda = E * nu / ((1 + nu) * (1 - 2 * nu))


def solve(nx):
    domain = mesh.create_box(MPI.COMM_WORLD, [[0, 0, 0], [L, W, W]],
                             [nx, max(2, nx // 5), max(2, nx // 5)], mesh.CellType.hexahedron)
    V = fem.functionspace(domain, ("Lagrange", 1, (domain.geometry.dim,)))
    facets = mesh.locate_entities_boundary(domain, 2, lambda x: np.isclose(x[0], 0.0))
    dofs = fem.locate_dofs_topological(V, 2, facets)
    bc = fem.dirichletbc(np.zeros(3, dtype=default_scalar_type), dofs, V)

    def eps(u): return ufl.sym(ufl.grad(u))
    def sigma(u): return lmbda * ufl.tr(eps(u)) * ufl.Identity(3) + 2 * mu * eps(u)

    u, v = ufl.TrialFunction(V), ufl.TestFunction(V)
    f = fem.Constant(domain, default_scalar_type((0, 0, -rho * g)))
    a = ufl.inner(sigma(u), eps(v)) * ufl.dx
    Lf = ufl.dot(f, v) * ufl.dx
    prob = LinearProblem(a, Lf, bcs=[bc], petsc_options={"ksp_type": "preonly", "pc_type": "lu"})
    uh = prob.solve()
    uh.name = "Displacement"
    return domain, uh


if __name__ == "__main__":
    I = W**4 / 12
    analytic = rho * g * W * W * L**4 / (8 * E * I)
    print(f"Analytic tip deflection: {analytic*1e6:.2f} um")
    for nx in (10, 20, 40):
        domain, uh = solve(nx)
        tip = abs(uh.x.array.reshape(-1, 3)[:, 2].min())
        print(f"nx={nx:3d}  FE tip deflection = {tip*1e6:.2f} um   error = {100*(tip-analytic)/analytic:+.1f} %")
    with io.XDMFFile(domain.comm, "displacement.xdmf", "w") as xdmf:
        xdmf.write_mesh(domain)
        xdmf.write_function(uh)
