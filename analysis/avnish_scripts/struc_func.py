import uproot
import argparse
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import sys
from barry_split_func_minimal import PP2LAMBDA_SPLITTING
import os
import glob
import argparse

def debug_res_structure(res, N=10):
    for i in range(min(N, len(res))):
        print(f"\n--- Entry {i} ---")
        keys = res["key"][i]
        values = res["value"][i]
        
        for k, v in zip(keys, values):
            key_str = k[0] if isinstance(k, (list, tuple)) and len(k) > 0 else k
            print(f"{key_str}: {v}")


def extract_values(array, name):
    # Remove completely empty sublists
    array = array[ak.num(array, axis=-1) > 0]
    
    # Flatten to 1D and convert to NumPy
    flat = ak.to_numpy(ak.flatten(array))
    
    # Remove NaNs and zeros (if desired)
    flat = flat[~np.isnan(flat)]
    flat = flat[flat != 0]
    
    print(f"{name} extracted: {len(flat)} values")
    return flat


def get_data(input_file, n_events):

    with uproot.open(input_file) as file:
        # Get the events tree from file
        tree = file["events"]

        # Process first 10 events
        n_events = min(n_events, tree.num_entries)
        metadata = tree.arrays(('GPStringKeys', 'GPStringValues'), entry_stop=n_events)

        # Convert values to float
        values = ak.strings_astype(metadata.GPStringValues, "float64")

        # If we look at dimensions of GPStringKeys and GPStringValues we see they mismatch
        # Somehow after all the copying of metadta vlues end up in a single dimension array, like:
        # "dis_q2: [1.2345]" while it should be "dis_q2: 1.2345"
        # DEBUG (optional)
        # metadata.GPStringKeys.type.show()
        # metadata.GPStringValues.type.show()
        # values.type.show()

        res = ak.zip(
            {
                "key": metadata.GPStringKeys,
                "value": values,
            }
        )

        debug_res_structure(res,3)

        xbj = extract_values(res[res.key == "dis_xbj"].value, "xbj")
        q2  = extract_values(res[res.key == "dis_q2"].value, "q2")
        t   = extract_values(res[res.key == "dis_tspectator"].value, "t")
        xL  = extract_values(res[res.key == "dis_alphas"].value, "xL")
        kT  = extract_values(res[res.key == "dis_pperps"].value, "kT")

        return xbj, q2, kT, t, xL

def get_structure_func(xL, kT):
    barry_function = PP2LAMBDA_SPLITTING(model = 'Cov exp')
    # Regulator parameter
    par = 0.774 # using "Cov exp" regulator
    kT2 = kT**2
    # return barry_function.get_fL(kT2, xL)
    return barry_function.get_theory(par, xL, kT)

def analyze_fL_t(input_file, n_events):
    xbj, q2, kT, t, xL = get_data(input_file, n_events)

    # define bin edges
    xbj_bins = np.linspace(0, 0.9, 4)
    q2_bins = np.linspace(0, 200, 4)

    fig, axes = plt.subplots(len(xbj_bins)-1, len(q2_bins)-1, figsize=(15,12), sharex=True, sharey=True)

    for i in range(len(xbj_bins)-1):
        for j in range(len(q2_bins)-1):
            ax = axes[i, j]

            # create bin mask
            mask = (
                    (xbj >= xbj_bins[i]) & (xbj < xbj_bins[i+1]) &
                    (q2 >= q2_bins[j]) & (q2 < q2_bins[j+1])
                )


            if not np.any(mask):
                ax.set_title(f"No events")
                continue

            # extract values for this bin
            kT_bin = kT[mask]
            xL_bin = xL[mask]
            t_bin = t[mask]

            # compute structure function
            F_bin = get_structure_func(xL_bin, kT_bin)

            # plot F vs -t
            ax.scatter(-t_bin, F_bin, alpha=0.6, s=10, c='b')
            ax.set_title(f"x_bj: {xbj_bins[i]:.2f}-{xbj_bins[i+1]:.2f}, Q²: {q2_bins[j]:.1f}-{q2_bins[j+1]:.1f}")
            ax.set_xlabel("-t")
            ax.set_ylabel("F")

    plt.tight_layout()
    plt.show()

def analyze_fL_t_multi(file_list, n_events):
    all_xbj, all_q2, all_kT, all_t, all_xL = [], [], [], [], []

    for f in sorted(file_list):
        try:
            xbj, q2, kT, t, xL = get_data(f, n_events)
            all_xbj.append(xbj)
            all_q2.append(q2)
            all_kT.append(kT)
            all_t.append(t)
            all_xL.append(xL)
        except Exception as e:
            print(f"Failed to process {f}: {e}")
            continue

    # Concatenate all data arrays
    xbj = np.concatenate(all_xbj)
    q2  = np.concatenate(all_q2)
    kT  = np.concatenate(all_kT)
    t   = np.concatenate(all_t)
    xL  = np.concatenate(all_xL)

    # define bin edges
    xbj_bins = np.linspace(0, 0.9, 4)
    q2_bins = np.linspace(0, 200, 4)

    fig, axes = plt.subplots(len(xbj_bins)-1, len(q2_bins)-1, figsize=(15,12), sharex=True, sharey=True)

    for i in range(len(xbj_bins)-1):
        for j in range(len(q2_bins)-1):
            ax = axes[i, j]

            # create bin mask
            mask = (
                (xbj >= xbj_bins[i]) & (xbj < xbj_bins[i+1]) &
                (q2  >= q2_bins[j])  & (q2  < q2_bins[j+1])
            )

            if not np.any(mask):
                ax.set_title(f"No events")
                continue

            # extract values for this bin
            kT_bin = kT[mask]
            xL_bin = xL[mask]
            t_bin = t[mask]

            # compute structure function
            F_bin = get_structure_func(xL_bin, kT_bin)

            # plot F vs -t
            ax.scatter(-t_bin, F_bin, alpha=0.6, s=10, c='b')
            ax.set_title(f"x_bj: {xbj_bins[i]:.2f}-{xbj_bins[i+1]:.2f}, Q²: {q2_bins[j]:.1f}-{q2_bins[j+1]:.1f}")
            ax.set_xlabel("-t")
            ax.set_ylabel("F")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Path to input ROOT file or directory containing segmented files")
    parser.add_argument("--events", "-e", type=int, default=1000, help="Number of events to read (per file)")
    parser.add_argument("--beam", type=str, default="5x41", help="Beam energy tag (e.g., 5x41) for segmented files")
    args = parser.parse_args()

    if os.path.isfile(args.input_path):
        analyze_fL_t(args.input_path, args.events)

    elif os.path.isdir(args.input_path):
        pattern = os.path.join(args.input_path, f"k_lambda_{args.beam}_5000evt_*.edm4eic.root")
        file_list = glob.glob(pattern)
        if not file_list:
            print(f"No matching files found with pattern: {pattern}")
        else:
            print(f"Found {len(file_list)} files to process.")
            analyze_fL_t_multi(file_list, args.events)
    else:
        print("Invalid input path. Provide a ROOT file or a directory containing segmented ROOT files.")






















