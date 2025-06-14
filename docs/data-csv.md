# CSV Data

We provide the relevant part `*.EDM4EIC.root` data converted to the CSV format 

- The CVS files are located in the same place as `*.edm4eic.root` files
- File names correspond to each other. E.g. `k_lambda_5x41_5000evt_001.*`
- Access to the CSV files is the same. See [DATA ACCESS](data) page
- CSV table names are embedded in extension before `.csv` , 
  e.g. `*.mcdis.csv`, `*.mcpart_lambda.csv`
- Column names are listed in the first line of the file (standard for CSV)

Example file names: 

```bash
# Original file
k_lambda_5x41_5000evt_001.edm4eic.root

# Related CSV-s
k_lambda_5x41_5000evt_001.mcdis.csv
k_lambda_5x41_5000evt_001.mcpart_lambda.csv
```

All scripts that make EDM4HEP to CSV conversion are located at 
[csv_convert](https://github.com/JeffersonLab/meson-structure/tree/main/csv_convert) dir.

## Table definitions
 
For analyzing data, we can work with multiple CSV files that contain related information.
The files are linked relationally. The first columns of a CSV table is always 
a primary key (e.g. event number). Or a composite key (e.g. event number + particle index). 
For example, all data related to e.g. `k_lambda_5x41_5000evt_001.*` 
will refer the same events. 

```mermaid
erDiagram
    MC_Events {
        int event_id PK "Event Number"
        float xBj "True x"
        float Q2 "True Q2"
        float etc "True values"
    }
    Reconstructed_Events {
        int event_id PK "Event Number"
        float xBj "Reconstructed x"
        float Q2 "Reconstructed Q2"
        float etc "Reconstructed values"
    }
    Lambda_Decays {
        int event_id FK "Event Number"
        int lambda_id PK "Lambda Number"
        float info "Lambda reco data"
    }

    MC_Events ||--|| Reconstructed_Events : "links to"
    MC_Events ||--o{ Lambda_Decays : "links to"
```
These CSV files are essentially **database tables**, 
and understanding this relationship helps us organize and analyze data more effectively.

With python and pandas it is easy to organize them joined tables like 
`MCvsReconstructed events`

### mcdis

- Files: `*.mc_dis.csv`
- Conversion script: [csv_convert/csv_mc_dis.cxx](https://github.com/JeffersonLab/meson-structure/blob/main/csv_convert/csv_mc_dis.cxx)

True event level values that come from the event generator.
`evt` - evnet id in file, the rest of the names correspond to table: 
[mc-variables](mc-variables)

Columns: 

```
evt
alphas
mx2
nu
p_rt
pdrest
pperps
pperpz
q2
s_e,s_q
tempvar
tprime
tspectator
twopdotk
twopdotq
w
x_d
xbj
y_d
yplus
```

### reco_dis

- Files: `*.reco_dis.csv`
- Conversion script: [csv_convert/csv_reco_dis.cxx](https://github.com/JeffersonLab/meson-structure/blob/main/csv_convert/csv_reco_dis.cxx)

Reconstructed (and true MC) event kinematic parameters. 
EICRecon provides several algorithms calculating the DIS kinematics. 
We save them all to CSV. E.g. `jb_q2` correspond to Q2 obtained by Jacquet-Blondel method
and `electron_q2` corresponds to scattered electron method. 

Prefixes - EDM4EIC Collection name: 

1. `da`       - "InclusiveKinematicsDA"
2. `esigma`   - "InclusiveKinematicsESigma"
3. `electron` - "InclusiveKinematicsElectron"
4. `jb`       - "InclusiveKinematicsJB"
5. `ml`       - "InclusiveKinematicsML"
6. `sigma`    - "InclusiveKinematicsSigma"
7. `mc`       - True MC values same as in `mc_dis` table

For each method variables are saved like: 

1. `{}_x`
2. `{}_q2`
3. `{}_y`
4. `{}_nu`
5. `{}_w`

`evt` is the first column = event number. 

So the total column names are:

```
evt,
da_x,da_q2,da_y,da_nu,da_w,
esigma_x,esigma_q2,esigma_y,esigma_nu,esigma_w,
electron_x,electron_q2,electron_y,electron_nu,electron_w,
jb_x,jb_q2,jb_y,jb_nu,jb_w,
ml_x,ml_q2,ml_y,ml_nu,ml_w,
sigma_x,sigma_q2,sigma_y,sigma_nu,sigma_w,
mc_x,mc_q2,mc_y,mc_nu,mc_w
```

### mcpart_lambda

- Files: `*.mcpart_lambda.csv`
- Conversion script: [csv_convert/csv_mcpart_lambda.cxx](https://github.com/JeffersonLab/meson-structure/blob/main/csv_convert/csv_mcpart_lambda.cxx)

Full MC particles information for a lambda decays chain by using `MCParticles` EDM4EIC table. 
MCParticles has relations like daughters and parents. Those relations are 
flattened by lambda decay. 
The columns represent possible lambda decays are grouped by particles: 

Prefixes (each has the same parameters after)

1. `lam` - Λ 
2. `prot` - p (if pπ- decay or nulls)
3. `pimin` - π- (if pπ- decay or nulls)
4. `neut` - Neutron (if n π0 decay)
5. `pizero` - pi0 - (if n π0 decay)
6. `gamone` - γ one from π0 decay (if pi0 decays)
7. `gamtwo` - γ two from π0 decay (if pi0 decays)

For each particle prefix, the next columns are saved: 

1.  `{0}_id`     -   id - particle index in MCParticles table
2.  `{0}_pdg`    -   pdg - particle PDG
3.  `{0}_gen`    -   gen - Generator Status (1 stable... probably)
4.  `{0}_sim`    -   sim - Simulation Status (by Geant4)
5.  `{0}_px`     -   px - Momentum
6.  `{0}_py`     -   py
7.  `{0}_pz`     -   pz
8.  `{0}_vx`     -   vx - Origin vertex information
9.  `{0}_vy`     -   vy
10. `{0}_vz`     -   vz
11. `{0}_epx`    -   epx - End Point (decay, or out of detector)
12. `{0}_epy`    -   epy
13. `{0}_epz`    -   epz
14. `{0}_time`   -   time - Time of origin
15. `{0}_nd`     -   nd - Number of daughters

So in the end the columns are: 

```yaml
evt,
lam_id,lam_pdg,lam_gen,lam_sim,lam_px,lam_py,lam_pz,lam_vx,lam_vy,lam_vz,lam_epx,lam_epy,lam_epz,lam_time,lam_nd,
prot_id,prot_pdg,prot_gen,prot_sim,prot_px,prot_py,prot_pz,prot_vx,prot_vy,prot_vz,prot_epx,prot_epy,prot_epz,prot_time,prot_nd,
pimin_id,pimin_pdg,pimin_gen,pimin_sim,pimin_px,pimin_py,pimin_pz,pimin_vx,pimin_vy,pimin_vz,pimin_epx,pimin_epy,pimin_epz,pimin_time,pimin_nd,neut_id,
neut_pdg,neut_gen,neut_sim,neut_px,neut_py,neut_pz,neut_vx,neut_vy,neut_vz,neut_epx,neut_epy,neut_epz,neut_time,neut_nd,
pizero_id,pizero_pdg,pizero_gen,pizero_sim,pizero_px,pizero_py,pizero_pz,pizero_vx,pizero_vy,pizero_vz,pizero_epx,pizero_epy,pizero_epz,pizero_time,pizero_nd,
gamone_id,gamone_pdg,gamone_gen,gamone_sim,gamone_px,gamone_py,gamone_pz,gamone_vx,gamone_vy,gamone_vz,gamone_epx,gamone_epy,gamone_epz,gamone_time,gamone_nd,
gamtwo_id,gamtwo_pdg,gamtwo_gen,gamtwo_sim,gamtwo_px,gamtwo_py,gamtwo_pz,gamtwo_vx,gamtwo_vy,gamtwo_vz,gamtwo_epx,gamtwo_epy,gamtwo_epz,gamtwo_time,gamtwo_nd
```

Notes:

- Particles may not be decayed. E.g. Lambda may just go outside of detector designated volume, 
  in this case `lam_nd` - Number of daughters will be 0 and the rest of columns will be null 


## Combine Multiple Files

When we have multiple CSV files from different runs or datasets, 
each file starts its event numbering from 0:

```
File 1: evt = [0, 1, 2, 3, 4, ...]
File 2: evt = [0, 1, 2, 3, 4, ...]  ← ID Collision!
File 3: evt = [0, 1, 2, 3, 4, ...]  ← ID Collision!
```

**Problem**: Event 0 from File 1 is completely different from Event 0 from File 2, 
but they have the same ID if read in pandas directly!

Use functions like this to read multiple files in one DF

```python
import pandas as pd
import glob

def concat_csvs_with_unique_events(files):
    """Load and concatenate CSV files with globally unique event IDs"""
    dfs = []
    offset = 0
    
    for file in files:
        df = pd.read_csv(file)
        df['evt'] = df['evt'] + offset  # Make IDs globally unique
        offset = df['evt'].max() + 1    # Set offset for next file
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)

# Load both tables with unique event IDs
lambda_df = concat_csvs_with_unique_events(sorted(glob.glob("mcpart_lambda*.csv")))
dis_df = concat_csvs_with_unique_events(sorted(glob.glob("dis_parameters*.csv")))
```

**Result**: Now we have globally unique event IDs:
```
File 1: evt = [0, 1, 2, 3, 4]
File 2: evt = [5, 6, 7, 8, 9]     ← No collision!  
File 3: evt = [10, 11, 12, 13, 14] ← No collision!
```
