# Analysis tutorials

Tutorials code examples are located at 
[meson-structure/tutorials](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials)
folder. 

### 01 Using uproot to process EDM4Hep 
- [py_edm4eic_01_uproot.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_01_uproot.py)
  Very basic tutorial of iterating over files and events in uproot

- [py_edm4eic_02_plot_mcparticles.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_02_plot_mcparticles.py)
  Analyzing EICrecon Data with Uproot library.
  Very basic example showing iteration over number of files and building histograms using pyhep `hist` package

### 02 Access metadata from event generator
- [02 Metadata Tutorials]() and [py_edm4eic_04_metadata.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_04_metadata.py)
  Shows event-level metadata from EDM4eic files and builds 1D histograms of all numeric key-values.

  Metadata from the original event generator files are copied through the simulation chain.
  There are file level metadata, and even level madata. Important for us values such as true Q2, Bjorken x, etc.
  The metadata is copied: from e.g. files to hepmc artifacts, then through DD4Hep output and then EICRecon output.
  Event level metadata comes in special branches of 'event' tree "GPStringKeys" and "GPStringValues" as strings.
  This example shows how to decode the metadata and use in your project, here we build all metadata histograms.

## EIC and external tutorials

- [EIC full chain tutorial for JLab users](https://github.com/JeffersonLab/eic-sftware-tutorial/blob/main/README.md)
- [EIC official tutorials](https://eic.github.io/documentation/tutorials.html)

