# VarMINT
The **Var**iational **M**ultiscale **I**ncompressible **N**avier--Stokes **T**oolkit:  A small Python module with re-usable functionality for solving the Navier--Stokes equations in [FEniCS](https://fenicsproject.org/), using a variational multiscale (VMS) formulation.

The **S**olid **M**echanics **A**nd **N**onlinear **E**lasticity **R**outines module, **SalaMANdER**, provides a framework for implementing solid material models that avoids code duplication where possible.

The **C**onvert **M**esh utility, **ChaMeleon**, was written to convert meshes generated with [GMSH](gmsh.info) to FEniCS-compatible XDMF-format meshes using [meshio](https://pypi.org/project/meshio/).

To install these modules, do the following: 
```
pip3 install git+https://github.com/MehdiSaraeian/VarMINT.git
```

This module was originally written to support the following paper, submitted to a special issue on open-source software for partial differential equations:
```
@article{kamensky2021open,
  title={Open-source immersogeometric analysis of fluid--structure interaction using FEniCS and tIGAr},
  author={Kamensky, David},
  journal={Computers \& Mathematics with Applications},
  volume={81},
  pages={634--648},
  year={2021},
  publisher={Elsevier}
}
```

It has since been updated to be based on an Arbitrary Lagrangian-Eulerian (ALE) framework to facilitate fluid-structure interaction simulations for the below publication:
```
@article{neighbor2023leveraging,
  title={Leveraging code generation for transparent immersogeometric fluid--structure interaction analysis on deforming domains},
  author={Neighbor, Grant E and Zhao, Han and Saraeian, Mehdi and Hsu, Ming-Chen and Kamensky, David},
  journal={Engineering with Computers},
  volume={39},
  number={2},
  pages={1019--1040},
  year={2023},
  publisher={Springer}
}
```

VarMINT is intentionally lightweight and mainly intended to avoid needless duplication of UFL code defining the VMS formulation in different applications.  A more comprehensive FEniCS-based flow solver using a similar VMS formulation is described by Zhu and Yan [here](https://doi.org/10.1016/j.camwa.2019.07.034).



