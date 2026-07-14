# What?
This package contains various utility functions for working with labeled oriented simple graphs
that are difference distance magic (DDM).

Important modules:
- The checks module contains various tests for determining if a labeled oriented graph is DDM
- The text module contains functions for going back and forth from text representations.
- The sagemath module contains functions for going back and forth from Sage's directed graph type
to a numpy adjacency matrix-label vector pair.
- The ddmog_stitcher module uses Google's OR-tools SAT solver to find DDMOGs with specified order.
- The ddmo_generator module like ddmog_stitcher uses a SAT solver to find valid labelings and orientations of an undirected graph

