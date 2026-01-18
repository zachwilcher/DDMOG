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
Dr. Aceska thinks that the sparsest DDMOG on order 9 has 16 edges.
Our code found a DDMOG of order 9 with 15 edges.

## Experiments

As of 16 Jan 2026, here is the speed of the current algorithm.

```
Found 6 DDMOGs out of 59049 possible oriented graphs of order 5 in 0.35 seconds.
Found 22 DDMOGs out of 14348907 possible oriented graphs of order 6 in 0.00 seconds.
Found 296 DDMOGs out of 10460353203 possible oriented graphs of order 7 in 0.08 seconds.
Found 9930 DDMOGs out of 22876792454961 possible oriented graphs of order 8 in 3.10 seconds.
Found 754804 DDMOGs out of 150094635296999121 possible oriented graphs of order 9 in 320.36 seconds.
Found 130528594 DDMOGs out of 2954312706550833698643 possible oriented graphs of order 10 in 79081.32 seconds.
```

Note that 6, 22, and 296 on order 5, 6, and 7 align with the final section of Difference distance magic oriented graphs by Alison Marr et al.
However, 9930 on order 8 is different from the reported 8240 in that paper.
They remark that they do not account for isomorphic graphs under rotations and reflections.

Conjecture: For each n \neq 6, there is a DDMOG with less than or equal to \ceil(3n/2) + 1 edges.
Data up to n = 11 supports it.