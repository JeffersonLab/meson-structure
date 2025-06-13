# CPP01 Iterate EDM4EIC

To save reconstructed data EDM4EIC file is used. EDM stands for 
"Event Data Model". This data model is based on PODIO, where 
IO = Input Output, and [POD is Plain Old Data] - referencing passive data.
In HENP it is often called "Flat data format" highlighting that instead of 
saving complex C++ class hierarchies, the file stores data in a relational way 
using minimum nesting. 

The **flat files** are good as you can read parts of it generally without knowing 
full schema. You see a branch like "MCParticle.momentum.z" and with very high
probability know what is saved there. Then you can use the branch name 
to directly read the values. You don't need to load special library for this. 
This is the advantage of such flat files. 

But dealing directly with branches as described above might be more complex when
data has many connections to each other. Hits make Tracks, which make particle hypothesis,
connected to calorimeter clusters they are combined into Reconstructed Particles and 
if Monte-Carlo truth is known, these ReconstructedParticles can be connected to 
the original MC particles. There are decays, vertexes and lots of more connections possible. 

One can use EDM4EIC library directly from root macro or using compiled C++ code to 
conveniently read EDM4EIC files and navigating between different objects. 
This tutorial is about it. 

The downside of this approach is that the exact same version of libraries that were used 
to save the data should be used in your code. Otherwise EDM4EIC files will not be opened. 

## Goal

- Read **EDM4EIC** ROOT file with **podio::ROOTReader**.
- Optionally stops after `-n` events.
- Dumps high-level event meta-data and detailed `MCParticle` info for the first few events.
- Can be executed either:

  - as an **interpreted ROOT macro** thanks to the `R__LOAD_LIBRARY` guards, or
  - as a **native C++20 executable** built by CMake.

The same source therefore doubles as a hands-on tutorial on **mixed scripting / compiled workflows in modern ROOT**. ([root-forum.cern.ch][1], [root.cern][2])


---

## Installation

The easies way to start would be to use `eic_shell`. 
Here is [a tutorial on the eic_shell](https://eic.github.io/tutorial-setting-up-environment/aio/index.html)

Then you can run as a root macros or build it using the container.  

If you want to build the tutorials outside of eic-shell, the dependencies are: 
**CERN ROOT**, **podio**, **EDM4hep**, **EDM4EIC**, **fmt**, **CMake**

> **Tip:** If you use `eic-shell` you already have every bullet above.
> The container gives a consistent compiler (GCC 13) and linker setup across Linux/macOS clusters. ([eic.github.io][6])

---


## Running as a ROOT macro

```bash
root -x -l -b -q 'cpp_01_read_edm4eic.cxx("events.edm4eic.root",100)'
```

To make such scripts on your own the important parts are: 

```cpp
#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif
```

- R__LOAD_LIBRARY loads the required libraries to read the files
- The `#ifdef __CLING__` block makes CLING load dictionaries **before** 
  it JIT-compiles the rest of the file, so every EDM4hep class is known to the interpreter. 
  ([root-forum.cern.ch][1])



## build & run in *eic-shell*

```bash
# 1) fire up the standard EPIC / Key4hep environment
./eic-shell          # prompt changes to "jug_dev>"

# 2) grab the sources (assume you’re in ~/work)
git clone https://github.com/YOUR_USER/cpp_meson_structure.git
cd cpp_meson_structure

# 3) out-of-source build
cmake -S . -B build
cmake --build build -j

# 4) run on one or many input files
build/cpp01_read_edm4eic  reco1.edm4eic.root  -n 200
build/csv_mcpart_lambda   sample.edm4eic.root > lambdas.csv
```

`eic-shell` auto-sets `LD_LIBRARY_PATH` so that the executables can locate `libpodioRootIO.so`, `libedm4hepDict.so`, etc. No `ROOTSYS` needed. ([eic.github.io][3])

---

## Generic CMake workflow (outside eic-shell)

```bash
# load your own ROOT / podio / EDM4hep setup first, then:
mkdir -p build && cd build
cmake ..                                  # detects all dependencies via find_package
make -j$(nproc)

# run
./cpp01_read_edm4eic  myfile.root  -n 50
```


##   Code walk-through (what to copy into your own analysis)

### Event loop

```cpp
podio::ROOTReader reader;
reader.openFile(filename);                      // self-contained I/O backend
const auto nEvents = reader.getEntries(podio::Category::Event);

for (unsigned i=0; i<nEvents; ++i) {
  podio::Frame event(reader.readNextEntry());   // zero-copy view
  auto& mcp = event.get<edm4hep::MCParticleCollection>("MCParticles");
  // your physics logic...
}
```

`podio::Frame` gives schema-aware access; collections keep relations and parameters intact. ([indico.cern.ch][7], [indico.cern.ch][8])

[1]: https://root-forum.cern.ch/t/about-documenting-r-load-library-i-e-using-root-compiled-classes-in-root-scripts/33565?utm_source=chatgpt.com "About documenting R__LOAD_LIBRARY (i.e. using ROOT-compiled ..."
[2]: https://root.cern/manual/integrate_root_into_my_cmake_project/?utm_source=chatgpt.com "Integrating ROOT into CMake projects"
[3]: https://eic.github.io/tutorial-setting-up-environment/aio/index.html "
  EIC Tutorial: Setting Up Your Environment
  "
[4]: https://github.com/AIDASoft/podio/blob/master/src/ROOTReader.cc?utm_source=chatgpt.com "podio/src/ROOTReader.cc at master - GitHub"
[5]: https://cmake.org/cmake/help/latest/command/find_package.html?utm_source=chatgpt.com "find_package — CMake 4.0.3 Documentation"
[6]: https://eic.github.io/tutorial-setting-up-environment/02-eic-shell/index.html "
  The EIC Software Environment – EIC Tutorial: Setting Up Your Environment
  "
[7]: https://indico.cern.ch/event/903696/contributions/3803479/attachments/2016028/3369629/2020-03-09-CLICWS-EDM4hep-1.pdf?utm_source=chatgpt.com "[PDF] KEY4HEP & EDM4HEP - Common Software for Future Colliders"
[8]: https://indico.cern.ch/event/1298458/contributions/5977790/attachments/2876449/5037555/20240612-key4hep-carceller.pdf?utm_source=chatgpt.com "[PDF] FCC Core Software: Key4hep - CERN Indico"
[9]: https://arxiv.org/abs/1804.03326?utm_source=chatgpt.com "Increasing Parallelism in the ROOT I/O Subsystem"
[10]: https://root-forum.cern.ch/t/integrating-root-in-a-cmake-project-find-package-options/21786?utm_source=chatgpt.com "Integrating ROOT in a CMake Project: find_package options"
[11]: https://arxiv.org/abs/2312.08206?utm_source=chatgpt.com "Towards podio v1.0 -- A first stable release of the EDM toolkit"
[12]: https://github.com/key4hep/key4hep-tutorials/blob/main/edm4hep_analysis/edm4hep_api_intro.md?utm_source=chatgpt.com "key4hep-tutorials/edm4hep_analysis/edm4hep_api_intro.md at main"
[13]: https://www.youtube.com/watch?v=Y0Mg24XLomY&utm_source=chatgpt.com "Setting up the EIC software environment (09/01/2022) - YouTube"
[14]: https://hepsoftwarefoundation.org/gsoc/blogs/2024/blog_Key4hep_BraulioRivas.html?utm_source=chatgpt.com "Any collection in Data Model Explorer - HEP Software Foundation"
