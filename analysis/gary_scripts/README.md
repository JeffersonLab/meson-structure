# To Do:
- Update process macros to work with new RAD combinatorial framework.
- Fix bugs in 2D binning header for Q2 x binning of the structure functions.
- Implement New Lambda reconstruction algorithms (either post-hoc or direcly in rad header).
- Fold in cross section integration code for correct bin normalisation.
- Implement statistical projections to final plots of F2 binned in x Q2.



# RAD Usage
ProcessMCMatchedKLambda.C assumes a working local build of rad and epic-rad analysis framework. Currently the Process macro works for an "old" build of rad, prior to an overhaul that implemented combinatorial analysis in January 2026. As such the best builds to use are the following tags:

https://github.com/Garypenman/rad/releases/tag/v1.0.0

https://github.com/Garypenman/epic-rad/releases/tag/v1.0.0

RAD has no build or install stage, it is purely headers that are compiled at run time. As such the setup in the README of the main repo branches is accurate:


https://github.com/dglazier/rad


https://github.com/dglazier/epic-rad


Running PRocessMCMatchedKLambda.C produces an output rootfile containing a TTree named "rad_tree", which one then loads for physics analysis. In the future this will be replaced with a combinatorial analysis which will consider all reconstructed particle candidates, provide a flag for the truth match and output a TTree named "tree" containing all combinatorial reconstructed events and truth events.

# Post RAD Analysis
Analysis.C is intended as the main analysis macro (for now) and is still a continuous work in progress. Additional style and helper macros exist alongside this for convenience.

More later...
