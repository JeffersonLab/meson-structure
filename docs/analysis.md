# Analysis

This section tries to provide helpful information to our analysis toolchain. 

- EIC plot macro [template from Results Committee ](https://github.com/eic/ResultsCommittee_templates/tree/main/plot_macro)
- Analysis scripts are located at  
  https://github.com/JeffersonLab/meson-structure/tree/main/analysis


When there is only one csv type going in

script.py input1.csv input2.csv .... --beam=10x100 -o output_folder

If multiple csvs are processed at the same time

script.py input_001_type1.cvs input_001_type2.csv input_002_type1.csv ...  -o output_folder

It is script responsivity to match input_001_type1.cvs input_001_type2.csv together.