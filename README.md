# DDMOGs!
This repository contains code for analyzing difference-distance magic oriented graphs (DDMOGs).

This work utilized the Ball State University beowulf cluster, which is supported
by The National Science Foundation (MRI-1726017) and Ball State University,
Muncie, Indiana.

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
There are multiple approaches to searching for DDMOGs implemented in this repository.
1. Brute force search through all oriented graphs of order n using `OrientedGraphIterator` in `magicutils/distance_magic/iterators.py`.
2. A backtracking search through all possible solutions to the weight equation using `DDMOGIterator` in `magicutils/distance_magic/ddmog_iterator.py`.
3. A SAT solver approach using `DDMOGStitcher` in `magicutils/distance_magic/ddmog_stitcher.py` that attempts to "stitch" together possible rows of an order n DDMOG's skew adjacency matrix.
4. A SAT solver approach 
using `ddmo_generator` in `magicutils/distance_magic/ddmo_generator.py`
that tries to find a valid DDM orientation and labeling of an unoriented graph.


### DDMOGIterator Tests
The program `find_all_ddmogs.py` uses `DDMOGIterator` to search for all
connected DDMOGs from order 5 upward.
The subset sum variation subproblem in this algorithm is a bottleneck.
The initial working implementation of the algorithm for finding all weakly connected DDMOGs of order n
had the following speed when running on my MacBook.
```
Found all 6 DDMOGs of order 5 in 0.35 seconds.
Found all 22 DDMOGs of order 6 in 0.00 seconds.
Found all 296 DDMOGs of order 7 in 0.08 seconds.
Found all 9930 DDMOGs of order 8 in 3.10 seconds.
Found all 754804 DDMOGs of order 9 in 320.36 seconds.
Found all 130528594 DDMOGs of order 10 in 79081.32 seconds.
```

Note that 6, 22, and 296 on order 5, 6, and 7 align with the final section of "Difference distance magic oriented graphs"
However, 9930 on order 8 is different from the reported 8240 in that paper.
They remark that they do not account for isomorphic graphs under rotations and reflections.

Using Musser's sumset algorithm for the subset sum subproblem provides a significant speedup.
Here is the current speed running on the same MacBook from before
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

The python program `find_sparsest_ddmogs.py` searches for DDMOGs with minimal
sparsity (ceil(3n/2) edges or ceil(3n/2) + 1 edges if n = 2 (mod 4)) and outputs
their adjacency matrices in the directory `sparsest_ddmogs`.  The results of
this program for orders up to 38 are available in the repository (when n > 38 we use too much memory...).  
Note that the program `create_ddmog_plot.py` can be used to create a png picture of a DDMOG
given the path to its adjacency matrix.

Note that if a DDMOG has n vertices and 3n/2 edges when n = 2 (mod 4)
then the graph is 3-regular. Adding up each label 3 times corresponds exactly
to the number of times each label appears in the weight equations.
It can be shown that this sum is an integer only when n = 0,3 (mod 4).

Some additional constraints that might interesting to explore are
- Searching for k-regular DDMO graphs when k > 3.
- Searching for the densest DDMOGs by maximizing the number of edges.
- Generalizing to labels taken from finitely generated abelian groups.

### Other potentially interesting questions
- How many different ways are there to label and orient a DDMO graph?
- Is there a fast way to check if a graph is DDMO?
- Is the base b representation of labels conducive to determining if a regular graph is DDMO?

## Constructing Sparse DDMOGs
Skolem sequences and near-Skolem sequences can be used to construct DDMOGs
with ceil(3n/2) edges whenever n >= 10 and n = 0,5,11 (mod 12).  
See `magicutils/distance_magic/graphs.py` for implementations.

I haven't implement the actual formulas for some of the sequences yet,
but in theory the constructions work.

When n > 138, a Langford sequence can be used to 
label an arbitrary number of pairs of K_{3,3}
added on to a DDMOG with n vertices.
The program `disconnected_conjecture.py` uses 
`ddmo_generator.py` in 
`magicutils/distance_magic/ddmo_generator.py`
to guess orientations and labelings of base graphs
found by `DDMOStitcher` in
`magicutils/distance_magic/ddmog_iterator.py`
with pairs of K_{3,3} added on to the base graph.
Results for n <= 138 can be found in the `disconnected_conjecture`
directory.

Note that these examples combined with examples in the `sparsest_ddmogs`
directory combined with the Langford sequence construction demonstrate
that minimal sparsity DDMOGs exist for all n >= 10.