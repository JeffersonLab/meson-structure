# Python EDM4EIC analysis

**Using uproot**

Corresponding python examples:

- [tutorials/py_edm4eic_01_uproot.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_01_uproot.py)
- [tutorials/py_edm4eic_02_plot_mcparticles.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_02_plot_mcparticles.py)
- [tutorials/py_edm4eic_03_references.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_03_references.py)
- [tutorials/py_edm4eic_04_metadata.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_04_metadata.py)
- [tutorials/py_edm4eic_05_sim_tracker_hits.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_05_sim_tracker_hits.py)


::: info
We use [uproot] to process reconstruction files saved in CERN ROOT format `.root`.
While python is a slow language if compared to C++, uproot can achieve comparable 
performance in event processing. It is based on [awkward-arrays][awkward] arrays which core
is written in C and uses vectorized data processing the same way as numpy. 
**uproot** can be easily installed via `pip install`, runs on all operating systems, 
very compatible with main python data science and AI tools. 
:::


## Prerequisites

Install these packages:

```bash
pip install uproot awkward numpy matplotlib hist
```

Related documentation: 

- [uproot]
- [awkward]


[uproot-github]: https://github.com/scikit-hep/uproot5
[uproot]: https://uproot.readthedocs.io/en/latest/basic.html
[awkward]: https://github.com/scikit-hep/awkward


## 01 Plot MCParticles

Code: 

- [tutorials/py_edm4eic_01_uproot.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_01_uproot.py)
- [tutorials/py_edm4eic_02_plot_mcparticles.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_02_plot_mcparticles.py)


- [tutorials/py_edm4eic_05_sim_tracker_hits.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_05_sim_tracker_hits.py)



### Reading root file

`uproot` provides several ways to open and read data from files.
Uproot tutorials start with `array` or `arrays` method which reads all required data at once. 
But it could easily take too much time and memory on e.g. a laptop if files are large. 

The most efficient way to develop analysis scripts and process large number of files/events is
to use `iterate` method which reads data in chunks, which could be
processed in a vectorized way (using numpy or better suited awkward array library)
So we e.g. read 1000 events at once, process them, add data to histos, process
next 1000 events, etc. 


[uproot iterate method](https://uproot.readthedocs.io/en/latest/uproot.behaviors.TBranch.iterate.html):

The minimal you need to iterate

```python
# The simplest way to process a file
for chunk in uproot.iterate(
        {file_name: "events"},      # File Name : TTree name (EDM4EIC ttree is "events")
        branches,                   # List of branches you want to process
        step_size=1000,             # How many events to process per chunk
        entry_stop=10_000           # On what event to stop (there is also etry_start) variable
    ):
    # process chunk by chunk here
```

See [tutorials/00_uproot.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/00_uproot.py)

Full code stub: 

```python
import uproot

# What branches to process
branches = [
    "MCParticles.PDG",
    "MCParticles.momentum.z",
    "MCParticles.endpoint.z",
]

# Read and process file in chunks
for chunk_i, chunk in enumerate(uproot.iterate(
        {"my_file.root": "events"}, 
        branches, 
        step_size=100, 
        entry_stop=200)):

    print(f"Сhunk {chunk_i} read")

    # Print data shape. It is going to be
    # [n-events-in-chunk]x{branch:[n-particles]}
    chunk.type.show()

    # Show a value of a single particle
    particle_pdg = chunk[0]["MCParticles.PDG"][2]
    print(f"  PDG of the 3d particle of the 1st event in this chunk: {particle_pdg}")
```

How data is organized:

```
chunk.type.show() output is: 

100 * {
"MCParticles.PDG": var * int32,
"MCParticles.momentum.z": var * float32,
"MCParticles.endpoint.z": var * float64
}
```

This means that data can be accessed as:

```python
chunk[event_index][branch_name][particle_index]

# Example: 3d particle of the 1st event: 
particle_pdg = chunk[0]["MCParticles.PDG"][2]
```

What is more important, that one can use `chunk[branch_name]` to get `[events]x[particle data]` 
awkward array that can be processed in vectorized way: 

```python
events_pdgs = chunk["MCParticles.PDG"]

# [event_0, event_1, ...] where event_0=[particle_0_pdg, particle_1_pdg, ... etc]
# e.g. [[2212, 11, 11, 321, 3122, 22, 22, 22], ..., [2212, 11, 11, ..., 11, 11, 11]]

# Vectorized way of processing the data
lambda_filter = chunk["MCParticles.PDG"] == 3122
lam_pz = ak.mean(chunk[lambda_filter]["MCParticles.momentum.z"])
print(f"  Lambdas pz in this chunk: {lam_pz}")
```

The key features are:
- Using uproot iterate to process data in chunks
- Using awkward arrays for vectorized operations
- Using boolean masks to select specific particle types

### Histograms

Look [tutorials/01_plot_mcparticles.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/01_plot_mcparticles.py)
for full details. 

We use [hist](https://hist.readthedocs.io/en/latest/user-guide/notebooks/Plots.html) library, 
which uses [boost-histogram](https://boost-histogram.readthedocs.io/en/latest/index.html)
under the hood and provides familiar for HENP way to create and fill histograms when iterating the 
file:

```python
# Create histograms
pz_hist = hist.Hist(hist.axis.Regular(100, -50, 50, name="momentum_z"))

# Fill histograms
pz_hist.fill(branch_pz[lambda_mask])
```

Hist package can plot its own histograms in jupyter. Here is an example how to save histogrms to file:

```python
import matplotlib.pyplot as plt

# Figure and Axes in matplotlib are analog of Canvas and Pad in ROOT
fig, ax = plt.subplots(figsize=(10, 6))
pz_hist.plot(ax=ax)
fig.savefig("lambda_pz.png")
```

### Tips for Efficiency

1. **Adjust chunk size**: Find the right balance between processing speed and memory usage.

2. **Use vectorized operations**: The awkward array library enables fast, NumPy-like operations on jagged arrays.

3. **Focus on what you need**: Only request the branches you actually need from the ROOT files.

4. **Use boolean masks**: They're much faster than loops for filtering particles.


## 2 Navigating EDM4eic relations 

with **uproot**, **awkward‑array**, and **Rich**

Code: 
- [tutorials/py_edm4eic_03_references.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_03_references.py)


EDM4eic is flat POD - struct of arrays. It follows philosophy:

**Each collection** (e.g. `MCParticles.momentum.x`, `MCParticles.momentum.y`, everything in `MCParticles`) 
appears as a branch of aligned‑length record arrays – one row per object.

But how collections reference each other? E.g. how 
`MCParticles` connected to `ReconstructedParticles` or if we have a `Hit` made by / connected
to `MCParticles` how we navigate from one to another? 

For this tutorial, we will use internal `MCParticles` relations between particles.

`MCParticles` - represent monte-carlo information about particles in the event and
each particle may have daughters and parents. 
If we have Lambda decaying to proton and pi-minus we should be able to navigate
back and forth between them. 

Technically **Each *relation*** (parents, daughters, hits, clusters, …) 
is *not* stored inline (it is not directly index of daughter in the same array).
Instead we get:

1. supplementary flattened vector – a separate branch whose name starts 
   with an underscore, e.g. `_MCParticles_daughters`.
2. *offset* arrays per object: `relation_begin` and `relation_end`;
   e.g.  `MCParticles.daughters_begin` and `MCParticles.daughters_end`

> (!!!) It is a very common pitfall. `MCParticles.daughters_begin` is not 
> an index inside `MCParticles.xxx` arrays but index inside `_MCParticles_daughters`

The object’s relations therefore live in the half‑open slice

```text
relation_indices = _SUPPLEMENTAL[b:e]  # where b = relation_begin[i], e = relation_end[i]
```

Exactly the same for **all** links in EDM4eic:

| Example relation                 | Offset fields on object            | Supplemental branch                   |
| -------------------------------- | ---------------------------------- | ------------------------------------- |
| MCParticle → *parents*           | `parents_begin`, `parents_end`     | `_MCParticles_parents.*`              |
| MCParticle → *daughters*         | `daughters_begin`, `daughters_end` | `_MCParticles_daughters.*`            |
| Track → *TrackerHits*            | `hits_begin`, `hits_end`           | `_Track_hits.*`                       |
| RecoParticle → *MCParticle* link | `particles_begin`, `particles_end` | `_ReconstructedParticles_particles.*` |

Once you grok one case, you can traverse them all.


## 03 Accessing Event Metadata 

in EDM4eic Files


Code:

- [tutorials/py_edm4eic_04_metadata.py](https://github.com/JeffersonLab/meson-structure/tree/main/tutorials/py_edm4eic_04_metadata.py)



## Understanding the Metadata Flow

Metadata in EDM4eic files contains important physics quantities from the event generation stage that propagate through the simulation chain. This includes true values like Q², Bjorken x, and other physics quantities crucial for analysis.

```mermaid
flowchart LR
    gen[Event Generator] -->|true values| hepmc[HepMC Converter]
    hepmc -->|as attributes| after[Afterburner]
    after -->|as attributes| dd4hep[DD4Hep]
    dd4hep -->|event metadata| eicrecon[EICRecon]
   

```

The diagram above illustrates how metadata travels through the simulation chain:
1. The event generator produces the true physics values
2. These values are converted to HepMC format and passed as "attributes"
3. After passing through afterburner and DD4Hep simulation
4. The metadata is preserved in the final EICRecon output

## Metadata in EDM4eic Files

Metadata in EDM4eic files exists at both file and event levels:

- **File-level metadata**: Global information about the dataset
- **Event-level metadata**: Physics quantities for each event

The event-level metadata is stored in special branches of the 'events' tree:
- `GPStringKeys`: Contains the metadata field names
- `GPStringValues`: Contains the corresponding values as strings

## Common Metadata Fields

Here are some common metadata fields you might find in EDM4eic files:

| Field Name | Description |
|------------|-------------|
| dis_Q2     | Four-momentum transfer squared (GeV²) |
| dis_xbj    | Bjorken x, the momentum fraction of the struck parton |
| dis_y      | Inelasticity, the fraction of energy transferred to the hadronic system |
| dis_W2     | Squared invariant mass of the hadronic system (GeV²) |
| dis_nu     | Energy transferred to the hadronic system (GeV) |
| projectile_energy | Energy of the projectile beam (GeV) |
| target_energy | Energy of the target beam (GeV) |


## Conclusion

Accessing metadata in EDM4eic files allows you to retrieve 
evnet level physics quantities from the event generation stage. 
This can be valuable for:

- Understanding the characteristics of your dataset
- Performing truth-level analyses
- Evaluating reconstruction performance by comparing with reconstructed quantities

The metadata values provide the "ground truth" for your analysis, 
allowing you to better understand and interpret your results.