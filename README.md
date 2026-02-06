# DDMOGs!
This repository contains code and notes for analyzing difference-distance magic oriented graphs (DDMOGs).

## How the project was set up
This project uses a conda environment to manage dependencies.
See the `conda-environment.yml` file for the list of packages used.

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

### Hacks
When trying to plot graphs, the project's Sagemath version thinks it wants
`libgsl.25.dylib` (gsl version 2.6) but conda provides `libgsl.27.dylib` (gsl
version 2.7).  We can "fix" this by creating a symbolic link from
`libgsl.27.dylib` to `libgsl.25.dylib` with
```bash
cd ./.conda-env/lib
ln -s libgsl.27.dylib libgsl.25.dylib
```

## Searching for DDMOGs
There are three approaches to searching for DDMOGs implemented in this repository.
1. Brute force search through all oriented graphs of order n using `OrientedGraphIterator` in `magicutils/iterators.py`.
2. A backtracking search through all possible solutions to the weight equation using `DDMOGIterator` in `magicutils/ddmog_iterator.py`.
3. A SAT solver approach using `DDMOGStitcher` in `magicutils/ddmog_stitcher.py` that attempts to "stitch" together possible rows of an order n DDMOG's skew adjacency matrix.


### DDMOGIterator Tests
The subset sum variation subproblem in this algorithm is a bottleneck.
The initial working implementation of the algorithm for finding all weakly connected DDMOGs of order n
has the following speed when running on my macbook.
```
Found 6 DDMOGs out of 59049 possible oriented graphs of order 5 in 0.35 seconds.
Found 22 DDMOGs out of 14348907 possible oriented graphs of order 6 in 0.00 seconds.
Found 296 DDMOGs out of 10460353203 possible oriented graphs of order 7 in 0.08 seconds.
Found 9930 DDMOGs out of 22876792454961 possible oriented graphs of order 8 in 3.10 seconds.
Found 754804 DDMOGs out of 150094635296999121 possible oriented graphs of order 9 in 320.36 seconds.
Found 130528594 DDMOGs out of 2954312706550833698643 possible oriented graphs of order 10 in 79081.32 seconds.
```

Note that 6, 22, and 296 on order 5, 6, and 7 align with the final section of "Difference distance magic oriented graphs"
However, 9930 on order 8 is different from the reported 8240 in that paper.
They remark that they do not account for isomorphic graphs under rotations and reflections.

Using Musser's sumset algorithm for the subset sum subproblem provides a significant speedup.
Here is the speed running on the same macbook from before
```
Found all 6 DDMOGs of order 5 in 0.46 seconds.
Found all 22 DDMOGs of order 6 in 0.00 seconds.
Found all 296 DDMOGs of order 7 in 0.05 seconds.
Found all 9930 DDMOGs of order 8 in 2.13 seconds.
Found all 754804 DDMOGs of order 9 in 228.15 seconds.
```

### Stitching with SAT Solver
Adding maximum size constraints to the SAT solver allows for finding sparse DDMOGs with much higher vertex counts.
However, searching for all DDMOGs of a given order with this approach is marginally slower than `DDMOGIterator`.

Some additional constraints that might interesting to explore are
- Searching for k-regular DDMO graphs when k > 3.
- Searching for the "coarsest" DDMOGs by maximizing the number of edges.
- Generalizing to labels taken from finitely generated abelian groups.


### Future