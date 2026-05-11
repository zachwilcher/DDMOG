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
Once the environment is activated, python programs in the project's main directory can be executed with
```bash
python ./program.py
```

If `conda-environment.yml` is edited, the environment needs to be updated. To do this run
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
1. A backtracking search through all possible solutions to the weight equation using `DDMOGIterator` in `magicutils/distance_magic/ddmog_iterator.py`.
2. A C++ implementation of the `DDMOGIterator` algorithm is in the `ddmog_counter` directory that simply
counts the number
2. A SAT solver approach using `DDMOGStitcher` in `magicutils/distance_magic/ddmog_stitcher.py` that attempts to "stitch" together possible rows of an order n DDMOG's skew adjacency matrix.
3. A SAT solver approach 
using `ddmo_generator` in `magicutils/distance_magic/ddmo_generator.py`
that tries to find a valid DDM orientation and labeling of an unoriented graph.


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


## Building ddmog_counter
CMake will need to be installed on your local system.

Make sure the conda environment is created and initialized with
```bash
conda env create --prefix .conda-env -f conda-environment.yml
conda activate ./.conda-env
```

Create the build system in `./build` with cmake.
```bash
cmake -B build
```

Finally, enter the build directory, compile the executable, and execute.
```bash
cd build
make
./ddmog_counter
```

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


## Questions and Work TBD
Some questions that someone might want to explore.
- How many different ways are there to label and orient a DDMO graph?
- Is there a fast way to check if a graph is DDMO?
- Is the base b representation of labels conducive to determining if a regular graph is DDMO?

In the `langford` module, there are several half implemented constructions.
It might be worth aggregating together all the different constructions
in one place as they are split up in multiple papers.
Also, there are fast ways to find a langford sequence given some defect and order.
Implementing these algorithms would make the module more complete.
