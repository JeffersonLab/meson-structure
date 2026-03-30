# Analysis

This section tries to provide helpful information to our analysis toolchain. 

- Analysis scripts are located at [analysis](https://github.com/JeffersonLab/meson-structure/tree/main/analysis) folder
- This repository has no branch protection and all are welcome to collaborate
- EIC plot macro [template from Results Committee ](https://github.com/eic/ResultsCommittee_templates/tree/main/plot_macro)

## Analysis conventions

We run analyzes as a part of simulation campaigns. In order for farm runners to run an analysis it has to comply to CLI
flags convention:

Convention TLDR:

```bash
script.py input1.csv input2.csv .... --beam=10x100 -o output_folder
```

1. Scripts accept multiple input files. Scripts should be written so that they won't go out of memory if all
   files for particular energy are used (e.g. 200 files total is 1m events). 

2. Scripts provide `-o, --output` argument that sets the output Directory for plots and artifacts (e.g. statistics text, csvs)

3. Scripts provide `-b, --beam` argument where beam in form `(ElectionE)x(IonE)` e.g. `10x100` is provided. 
   this flag might be used e.g. for histogram axis limits. Or it might do nothing (but farm scripts will provide it)

4. Optional: `-e, --events`, Max number of events to process, not required, but is nice for debugging. None => process all

> If multiple csvs are processed at the same time
> The script is responsible to match input_001.type1.cvs input_001.type2.csv together
> ```bash 
>    script.py input_001_type1.cvs input_001_type2.csv input_002_type1.csv ...  -o output_folder
> ```


## Suggestions

A good example of python CSV analysis is considered: 

- `analysis/csv_reco_dis_analysis/scattered_electron.py`

