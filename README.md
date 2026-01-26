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


## DDMOGIterator Tests
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

After some further optimization to the backtracking subset sum problem, here is the speed as of 19 Jan 2026.
```
Found all 6 DDMOGs of order 5 in 0.32 seconds.
Found all 22 DDMOGs of order 6 in 0.00 seconds.
Found all 296 DDMOGs of order 7 in 0.06 seconds.
Found all 9930 DDMOGs of order 8 in 2.34 seconds.
Found all 754804 DDMOGs of order 9 in 242.80 seconds.
```

Using Musser's sumset algorithm for the subset sum problem is even faster.
As of 25 Jan 2026, here is the speed.
```
Found all 6 DDMOGs of order 5 in 0.46 seconds.
Found all 22 DDMOGs of order 6 in 0.00 seconds.
Found all 296 DDMOGs of order 7 in 0.05 seconds.
Found all 9930 DDMOGs of order 8 in 2.13 seconds.
Found all 754804 DDMOGs of order 9 in 228.15 seconds.
```

# Stitching with SAT Solver
Using the SAT solver approach, some very interesting graphs were found.
It seems that for n >= 12, there is potentially a family of sparsest DDMOGs with exactly 3n/2 edges 
formed for n congruent to 0 mod 4. Each of these graphs are 3-regular!

## Ideas

Constrain the number of degree 4 vertices, not just the size of the graph.