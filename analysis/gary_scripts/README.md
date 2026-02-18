# To Do:
- Flesh out RAD usage details, and specify the old rad branch which these process macros will work with.
- Update process macros to work with new RAD combinatorial framework.
- Fix bugs in 2D binning header for Q2 x binning of the structure functions.
- Implement New Lambda reconstruction algorithms (either post-hoc or direcly in rad header).
- Fold in cross section integration code for correct bin normalisation.
- Implement statistical projections to final plots of F2 binned in x Q2.



# RAD Usage
ProcessMCMatchedKLambda.C assumes a working local build of rad and epic-rad analysis framework


https://github.com/dglazier/rad


https://github.com/dglazier/epic-rad


This produces an output rootfile containing a TTree named "rad_tree", which one then loads for physics analysis.

# Post RAD Analysis
Analysis.C is intended as the main analysis macro (for now) and is still a continuous work in progress. Additional style and helper macros exist alongside this for convenience.

More later...
