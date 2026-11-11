# Open-Source Engineering Simulation Portfolio

A curated portfolio of **18 open-source engineering, simulation, CAD, EDA, and scientific-computing projects**. The repository packages reproducible source inputs, scripts, configurations, and documentation across CFD, FEA, DFT/materials modeling, molecular dynamics, circuit/PCB/HDL workflows, meshing, and parametric design.

**Author:** [Yazan Aljabari](https://www.linkedin.com/in/yazan-aljabari-878202139/)  
**License:** [MIT](LICENSE)  
**Branch:** `main`

## Overview

This portfolio demonstrates practical, tool-oriented engineering workflows using widely adopted open-source ecosystems. Each project is organized as an independent module with its original source artifacts preserved, accompanied by comprehensive documentation describing objectives, prerequisites, execution, methodology, and limitations.

## Problem statement

Engineering and scientific simulation work is often difficult to evaluate because project inputs, toolchain assumptions, and reproducibility steps are scattered or undocumented. This repository addresses that gap by consolidating diverse domain workflows into a consistent, inspectable portfolio structure that emphasizes transparent setup, methodological clarity, and honest reporting (no fabricated simulation results).

## Objectives

- Showcase breadth across engineering simulation and design domains (CFD, FEA, materials/atomistics, MD, circuits, HDL/verification, PCB, CAD/meshing).
- Preserve original project source files while improving documentation and repository professionalism.
- Provide reproducible, tool-aware run instructions and validation guidance for each workflow.
- Communicate assumptions, dependencies, and limitations clearly for reviewers and recruiters.

## Features

- **18 self-contained projects** covering simulation, modeling, analysis, and design workflows.
- **Preserved source artifacts:** solver inputs/configs, meshes/scripts, netlists/RTL, CAD scripts, analysis utilities, and included tests where present.
- **Comprehensive per-project READMEs** (overview, problem statement, objectives, features, technologies, structure, installation, usage, methodology, results, testing, limitations, future improvements, references, license).
- **Portfolio-level documentation:** root README, results dashboard, landing page (`index.html`), and validation script.
- **Lightweight CI:** syntax/structure validation workflow that does not require heavyweight external solvers.
- **Transparent results policy:** no fabricated numerical outputs; generated results are produced by running the appropriate external tools.

## Technologies

Representative tools and libraries used across the portfolio:

- **CFD:** OpenFOAM (icoFoam, blockMesh), SU2, Gmsh
- **FEA / Multiphysics:** CalculiX, ElmerFEM, FEniCSx/DOLFINx, Gmsh
- **Materials / Atomistics / MD:** Quantum ESPRESSO, ASE, pymatgen, LAMMPS
- **Electrochemistry:** PyBaMM
- **Circuits / EDA / HDL:** ngspice, Xyce, Yosys, Icarus Verilog, Verilator, KiCad
- **CAD / Parametric design:** CadQuery, OpenSCAD
- **Scripting & analysis:** Python (NumPy, Matplotlib), Shell/Make, pytest (where applicable)

## Project structure

```text
.
├── 01-openfoam-lid-driven-cavity/
├── 02-elmer-plate-heat-conduction/
├── 03-cadquery-parametric-flange/
├── 04-fenicsx-cantilever-elasticity/
├── 05-openscad-parametric-enclosure/
├── 06-su2-naca0012-transonic/
├── 07-quantum-espresso-silicon/
├── 08-pymatgen-crystal-analysis/
├── 09-pybamm-battery-simulation/
├── 10-ngspice-analog-filters/
├── 11-xyce-bridge-rectifier/
├── 12-ase-surface-adsorption/
├── 13-calculix-cantilever-beam/
├── 14-lammps-argon-liquid/
├── 15-yosys-alu-synthesis/
├── 16-gmsh-adaptive-plate-with-hole/
├── 17-verilator-sync-fifo/
├── 18-kicad-555-astable-blinker/
├── docs/                        # Portfolio dashboard and assets
├── scripts/validate_portfolio.py
├── .github/workflows/ci.yml
├── index.html                   # Landing page
├── requirements.txt             # Lightweight Python deps for utilities/validation
├── pyproject.toml
├── LICENSE
└── README.md
```

### Project catalog

| # | Project | Domain | Key tools | Summary |
|---:|---|---|---|---|
| 1 | [OpenFOAM Lid-Driven Cavity](01-openfoam-lid-driven-cavity/) | CFD / Fluid Dynamics | OpenFOAM (icoFoam, blockMesh) | Incompressible laminar lid-driven cavity (Re=100) case setup and post-processing workflow. |
| 2 | [Elmer Plate Heat Conduction](02-elmer-plate-heat-conduction/) | FEA / Heat Transfer | ElmerFEM, Gmsh | Steady-state 2D heat conduction with Dirichlet/adiabatic boundaries. |
| 3 | [CadQuery Parametric Flange](03-cadquery-parametric-flange/) | CAD / Parametric Design | CadQuery, pytest | Parametric bolt-circle flange generation with STEP/STL export and tests. |
| 4 | [FEniCSx Cantilever Elasticity](04-fenicsx-cantilever-elasticity/) | FEA / Solid Mechanics | FEniCSx/DOLFINx, PETSc | 3D linear elasticity cantilever model with tip traction and theory comparison hook. |
| 5 | [OpenSCAD Parametric Enclosure](05-openscad-parametric-enclosure/) | CAD / Parametric Design | OpenSCAD, Make | Parametric electronics enclosure (base/lid, standoffs, vents) with STL export flow. |
| 6 | [SU2 NACA 0012 Transonic Flow](06-su2-naca0012-transonic/) | CFD / Aerodynamics | SU2, Gmsh, Python | Inviscid transonic NACA 0012 case (mesh/config/plot scripts). |
| 7 | [Quantum ESPRESSO Silicon](07-quantum-espresso-silicon/) | DFT / Materials Science | Quantum ESPRESSO, Python | Silicon SCF, cutoff convergence, and band-structure workflow inputs/scripts. |
| 8 | [Pymatgen Crystal Analysis](08-pymatgen-crystal-analysis/) | Materials Informatics | pymatgen, pytest | Crystal structure construction/analysis utilities with basic tests. |
| 9 | [PyBaMM Battery Simulation](09-pybamm-battery-simulation/) | Electrochemical Modeling | PyBaMM, Python | Lithium-ion discharge simulation workflow across operating conditions. |
| 10 | [ngspice Analog Filters](10-ngspice-analog-filters/) | Circuit Simulation / Analog | ngspice, Python | RLC low-pass AC analysis and RC-diode clipper transient simulation. |
| 11 | [Xyce Bridge Rectifier](11-xyce-bridge-rectifier/) | Circuit Simulation / Power Electronics | Xyce, Python | Full-wave bridge rectifier transient simulation and post-processing. |
| 12 | [ASE Surface Adsorption Workflow](12-ase-surface-adsorption/) | Atomistic Modeling | ASE, Python | Surface slab + adsorbate setup and relaxation/adsorption-energy workflow. |
| 13 | [CalculiX Cantilever Beam](13-calculix-cantilever-beam/) | FEA / Structural | CalculiX, Gmsh, Python | 3D cantilever static analysis with mesh/input generation and theory check script. |
| 14 | [LAMMPS Argon Liquid (LJ)](14-lammps-argon-liquid/) | Molecular Dynamics | LAMMPS, Python | Lennard-Jones liquid argon MD workflow with thermodynamic analysis script. |
| 15 | [Yosys ALU Synthesis](15-yosys-alu-synthesis/) | Digital Design / HDL | Yosys, Icarus Verilog | Parameterizable ALU RTL, self-checking testbench, and synthesis flow. |
| 16 | [Gmsh Adaptive Plate with Hole](16-gmsh-adaptive-plate-with-hole/) | Meshing / Preprocessing | Gmsh API, Python | Adaptive 2D mesh generation for stress-concentration-aware FEA preprocessing. |
| 17 | [Verilator Synchronous FIFO](17-verilator-sync-fifo/) | Digital Design / Verification | Verilator, Verilog, C++ | Synchronous FIFO RTL verified with a C++ Verilator testbench. |
| 18 | [KiCad 555 Astable Blinker](18-kicad-555-astable-blinker/) | PCB / Electronics Design | KiCad, Python | NE555 astable blinker design calculations, netlist/BOM utilities, and layout checklist. |

## Installation

### Prerequisites
- **Git** and a code editor/viewer.
- **Python 3.10+** (for included Python scripts/utilities, validation, and selected project tests).
- **Domain-specific external tools/solvers** required by individual projects (not bundled): e.g. OpenFOAM, ElmerFEM, Gmsh, SU2, FEniCSx, Quantum ESPRESSO, LAMMPS, CalculiX, ngspice, Xyce, Yosys, Icarus Verilog, Verilator, KiCad, OpenSCAD, and relevant Python packages (CadQuery, PyBaMM, ASE, pymatgen, etc.). Install via official documentation for your OS; many Linux workflows run well in WSL on Windows.

### Setup
```bash
# Clone the repository
git clone https://github.com/yazanus94-dot/Open-Source-Engineering-Simulation-Portfolio.git
cd Open-Source-Engineering-Simulation-Portfolio

# (Optional) Create a virtual environment for Python utilities/validation
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

Then install per-project toolchains/dependencies as described in each project's `README.md`.

## Usage

- Browse to a project directory (e.g. `01-openfoam-lid-driven-cavity/`) and follow its README for prerequisites, inputs, and run commands.
- Execute provided scripts (`run.sh`, `Allrun`, `Makefile`, Python entry points, input decks) in an environment with the required external tools installed.
- Post-process generated outputs with the recommended tools (ParaView, plotting scripts, waveform viewers, etc.).

Example (portfolio-level validation, no external solvers required):
```bash
python scripts/validate_portfolio.py
python -m compileall -q .
```

## Methodology

- **Source-preserving restructuring:** original project files are retained; portfolio and per-project documentation is added for clarity and reproducibility.
- **Domain-appropriate workflows:** each module captures the canonical inputs for its toolchain (solver dictionaries/input decks, meshes, netlists/RTL, CAD/parametric scripts, analysis code).
- **Reproducibility guidance:** prerequisites, execution steps, and expected artifact types are documented per project.
- **Evidence-based reporting:** included documentation distinguishes source/configuration from tool-generated outputs and does not fabricate numerical results.
- **Quality checks:** lightweight automated validation confirms structural completeness (project directories, READMEs, required root files, no leftover ZIP archives).

## Results

- **Portfolio build artifacts (this repository):** 18 documented project modules, comprehensive per-project READMEs, root documentation, results dashboard, landing page, and CI/validation configuration are included.
- **Simulation/design outputs:** numerical fields, plots, meshes, logs, waveforms, synthesized netlists, and exported CAD/EDA artifacts are **not fabricated** here. They are produced by running the included workflows with the appropriate external tools and environment. See [docs/results.md](docs/results.md) for the portfolio results/status dashboard and [docs/assets/portfolio_overview.svg](docs/assets/portfolio_overview.svg) for a domain coverage visual.

## Testing

### Portfolio-level (automated / lightweight)
```bash
python scripts/validate_portfolio.py
python -m compileall -q .
```
CI runs these checks on push/PR (`.github/workflows/ci.yml`).

### Project-level
- Projects that include Python tests (e.g. `03-cadquery-parametric-flange`, `08-pymatgen-crystal-analysis`) can be run with `pytest` when their specific dependencies are installed.
- Projects depending on external solvers/EDA tools are validated by configuration correctness, script integrity, and reproducible run instructions; full execution requires the corresponding toolchains.

## Limitations

- Many workflows require **external, domain-specific software** (and sometimes licensed or platform-specific builds) not included in this repository.
- Numerical/performance results depend on tool versions, solver settings, meshes/discretization, and hardware; outputs are therefore environment-dependent.
- Some modules are **educational/minimal** configurations intended to demonstrate workflow structure rather than production-grade validation/verification.
- No solver-generated logs/plots/meshes are claimed as included results unless explicitly present and documented.

## Future improvements

- Add pinned, containerized environments (Docker/Apptainer) per domain for deterministic execution.
- Capture and publish verified reference outputs (logs, metrics, figures) produced with documented tool versions.
- Expand automated tests and CI matrices for projects with lightweight/open dependencies.
- Add convergence/verification studies, parameter sweeps, and cross-tool benchmarks where appropriate.
- Provide unified post-processing notebooks and standardized artifact manifests.

## References

- Project-local documentation and source files within each numbered directory.
- Official documentation for the utilized open-source tools: OpenFOAM, ElmerFEM, Gmsh, SU2, FEniCSx/DOLFINx, PETSc, CalculiX, LAMMPS, Quantum ESPRESSO, ASE, pymatgen, PyBaMM, ngspice, Xyce, Yosys, Icarus Verilog, Verilator, KiCad, CadQuery, and OpenSCAD.

## License

This repository is licensed under the **MIT License**. See [LICENSE](LICENSE).

**Copyright (c) 2026 Yazan Aljabari** — [LinkedIn](https://www.linkedin.com/in/yazan-aljabari-878202139/)
