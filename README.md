# meson-structure

Meson Structure Analysis

[The full documentation](https://jeffersonlab.github.io/meson-structure/)

# Multi-Calo Λ Reconstruction & Kaon Structure Function Studies

This repository provides a lightweight and user-friendly Python framework to:

- Read reconstructed Λ candidates from EICrecon ROOT outputs  
- Compare reconstructed vs truth (MCParticles) and afterburner  
- Produce spectra, angular distributions, efficiencies, and kinematic maps  
- Propagate statistical uncertainties to the kaon structure function in  
  - (xB, Q²)  
  - (xK, Q²)

All plots are written to:

./outputs/

Reconstructed ROOT files must be available in:

./inputs/

---------------------------------------------------------------------

# 1) Generate Reconstructed ROOT Files (EICrecon)

The analysis requires reconstructed ROOT files produced with the custom branch:

reco/lambda-ff-multicalo

Below is the full procedure.

---------------------------------------------------------------------

Enter the EIC XL container:

singularity shell -B /volatile/eic/fraisse:/volatile/eic/fraisse -B /volatile/eic/romanov/meson-structure-2025-07:/volatile/eic/romanov/meson-structure-2025-07:ro /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:25.11-stable

Then load the ePIC detector environment:

source /opt/detector/epic-main/bin/thisepic.sh

Clone EICrecon and checkout the Lambda branch:

git clone https://github.com/eic/EICrecon.git
cd EICrecon
git checkout reco/lambda-ff-multicalo

Build EICrecon:

rm -rf build install
mkdir -p build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
make install

---------------------------------------------------------------------

Run reconstruction (example: beam 18x275, files 0001 → 0009, 5000 events each):

for i in $(seq -w 1 9); do for c in 18x275; do eicrecon -Pjana:nevents=5000 -Pnthreads=$(nproc) -Ppodio:output_file=/volatile/eic/fraisse/meson-structure/data/k_lambda_${c}_5000evt_00${i}_testall_calocalib_ZDConly.root /volatile/eic/romanov/meson-structure-2025-07/reco/k_lambda_${c}_5000evt_00${i}.edm4hep.root > /volatile/eic/fraisse/meson-structure/data/recon_${c}_00${i}.out 2> /volatile/eic/fraisse/meson-structure/data/recon_${c}_00${i}.err; done; done

This produces reconstructed files in:

/volatile/eic/fraisse/meson-structure/data/

Example output file:

k_lambda_18x275_5000evt_001_testall_calocalib_ZDConly.root

---------------------------------------------------------------------

# 2) Prepare the Analysis Folder

From the analysis directory (where run.py is located):

mkdir -p inputs outputs

You can symlink the reconstructed files:

ln -s /volatile/eic/fraisse/meson-structure/data/*.root inputs/

Or copy them:

cp /volatile/eic/fraisse/meson-structure/data/*.root inputs/

The analysis expects files with the pattern:

k_lambda_<beam>_5000evt_<idx:03d>_<suffix>.root

Example:

k_lambda_18x275_5000evt_001_testall_calocalib_verification.root

---------------------------------------------------------------------

# 3) Run the Analysis

Run all studies:

python -m run --task all --nfiles 10 --suffix testall_calocalib_verification

Parameters:

--task all  
Runs:
- Angular distributions  
- Energy spectra  
- Efficiencies  
- Kinematic maps  
- Statistical uncertainty propagation  

--nfiles 10  
Reads files 001 → 010  

--suffix testall_calocalib_verification  
Selects files matching:
k_lambda_<beam>_5000evt_<idx>_<suffix>.root

---------------------------------------------------------------------

Run specific tasks:

Only spectra:

python -m run --task spectra --nfiles 10 --suffix testall_calocalib_verification

Only angular distributions:

python -m run --task angles --nfiles 10 --suffix testall_calocalib_verification

Only efficiencies:

python -m run --task eff --nfiles 10 --suffix testall_calocalib_verification

Only kinematics:

python -m run --task kin --nfiles 10 --suffix testall_calocalib_verification

Only kaon structure function statistical uncertainty:

python -m run --task relerr --nfiles 10 --suffix testall_calocalib_verification --lumin-fb 1.0

---------------------------------------------------------------------

# 4) Output

All figures are automatically saved to:

./outputs/

Examples:

spectrum_18x275_testall_calocalib_verification.png  
kinematics_xB_Q2_18x275_verification.png  
relerr_xK_Q2_18x275_verification_L1fb_linQ2.png  

---------------------------------------------------------------------

# 5) Summary Workflow

1) Enter container  
2) Setup detector  
3) Clone + build EICrecon (reco/lambda-ff-multicalo)  
4) Run reconstruction  
5) Link ROOT files into ./inputs/  
6) Run:

python -m run --task all

All plots will appear in ./outputs/.