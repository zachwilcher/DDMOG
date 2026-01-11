# DDMOG

This repository contains code and notes for analyzing difference-distance magic oriented graphs (DDMOGs)
where labels are not necessarily just the positive integers but elements of finitely generated abelian groups.

## How the project was set up

A conda environment is created with
```bash
conda env create --prefix .conda-env -f conda-environment.yml
```

The environment can be activated with
```bash
conda activate ./.conda-env
```

If the environment needs to be updated, edit the `conda-environment.yml` file and run
```bash
conda env update --prefix .conda-env -f conda-environment.yml --prune
```

## Hacks

Sage thinks it wants libgsl.25.dylib (gsl version 2.6) but conda provides libgsl.27.dylib (gsl version 2.7).
We can "fix" this by symlinking libgsl.25.dylib to libgsl.27.dylib:
```bash
cd ./.conda-env/lib
ln -s libgsl.27.dylib libgsl.25.dylib
```
