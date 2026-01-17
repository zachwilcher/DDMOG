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

Sage thinks it wants `libgsl.25.dylib` (gsl version 2.6) but conda provides `libgsl.27.dylib` (gsl version 2.7).
We can "fix" this by creating a symbolic link from `libgsl.27.dylib` to `libgsl.25.dylib` with
```bash
cd ./.conda-env/lib
ln -s libgsl.27.dylib libgsl.25.dylib
```


## Notes
For graphs on 7 vertices, the sparsest connected DDMOG has 12 edges and starts
at graph number 1166308915 (index starts at 1 in this number) in the
`PossibleGraphIterator`.  Might be interesting to look at graphs with number:
- 1166309838
- 1181345436
- 1181346149
- 1181877911
- 1181878634