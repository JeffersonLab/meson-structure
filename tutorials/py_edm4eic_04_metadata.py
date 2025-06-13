description = """
Shows event-level metadata from EDM4eic files and builds 1D histograms of all numeric key-values.

Metadata from the original event generator files are copied through the simulation chain. 
There are file level metadata, and even level madata. Important for us values such as true Q2, Bjorken x, etc. 
The metadata is copied: from e.g. files to hepmc artifacts, then through DD4Hep output and then EICRecon output. 
Event level metadata comes in special branches of 'event' tree "GPStringKeys" and "GPStringValues" as strings.
This example shows how to decode the metadata and use in your project, here we build all metadata histograms.   
"""

import argparse
import os
import uproot
import awkward as ak
import math
import matplotlib.pyplot as plt
from hist import Hist


def create_hist_for_key(key: str, histo_val_min, histo_val_max) -> Hist:
    """
    Create a default 1D histogram for a given key name.

    In a real analysis, you might want special axis ranges for
    known keys (like xBj, Q2, etc.). Here we do something generic
    for demonstration: 100 bins from 0 to 1000.
    """
    # Fallback generic:
    return Hist.new.Reg(100, histo_val_min, histo_val_max, name=key, label=key).Double()


def process_chunk(chunk: dict, hists_by_key: dict):
    """
    Process one chunk of data from uproot.iterate() and fill histograms.

    Parameters
    ----------
    chunk : dict
        A dict from uproot (with keys 'GPStringKeys', 'GPStringValues').
    hists_by_key : dict
        A dictionary that maps 'string key' -> Hist instance.
    """

    # Extract the awkward arrays of keys and values
    keys_ak = chunk["GPStringKeys"]      # shape: (N_events * var)
    values_ak_str = chunk["GPStringValues"]  # shape: (N_events * var * var of strings)

    # Check we have some events
    if not len(keys_ak):
        return

    # Convert string to float64 (will fail if truly non-numeric):
    values_ak = ak.strings_astype(values_ak_str, "float64")

    # To get all names we take 1st event and use its values
    names = ak.to_list(ak.ravel(keys_ak[0]))

    # probably the first time here
    if not hists_by_key:
        print("Creating histograms")

        for name in names:
            values = values_ak[keys_ak == name]   # Select all values corresponding to this name
            histo_val_min = ak.min(values)
            histo_val_max = ak.max(values)
            add_edge = (histo_val_max - histo_val_min)*0.1  # Add 10% to min and max value in this sample
            if math.fabs(add_edge)>1e-7:                    # 0 means all values 0 or no values
                histo_val_min -= add_edge
                histo_val_max += add_edge
                print(f"   {name:<15} min: {histo_val_min:<10.3f} max: {histo_val_max:<10.3f}")
                hists_by_key[name] = create_hist_for_key(name, histo_val_min, histo_val_max)

    # Now fill the histograms by metadata name:
    for name in names:
        values = values_ak[keys_ak == name]   # Select all values corresponding to this name
        if name in hists_by_key:
            hists_by_key[name].fill(ak.ravel(values))

def main():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input_files", nargs="+", help="One or more EDM4eic ROOT files to process.")
    parser.add_argument("-e", "--events", type=int, default=None, help="If set, stop processing after this many events (across all files).")
    parser.add_argument("-o", "--output-dir", default="02_plots", help="Directory where output plots will be saved.")
    args = parser.parse_args()

    # Make sure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    print("Input files:", args.input_files)
    print("Output directory:", args.output_dir)

    # Dictionary that maps each unique key -> hist
    hists_by_key = {}

    # We'll track how many events have been processed in total
    total_processed = 0
    max_events = args.events if args.events is not None else float("inf")

    # For large files, we rely on uproot.iterate() to read in manageable chunks:
    #   - "events" is the TTree name
    #   - we specify the branches to load
    #   - step_size can be an integer (# of entries) or e.g. "100 MB"
    #   - we stop once we've read `args.events` if that was requested
    iter_chunks = uproot.iterate(
        files={name: "events" for name in args.input_files},
        expressions=["GPStringKeys", "GPStringValues"],
        treename="events",
        step_size="100MB",
    )

    for chunk in iter_chunks:
        # Count how many events in this chunk
        chunk_size = len(chunk["GPStringKeys"])
        # If adding this chunk exceeds our max_events, do partial
        if total_processed + chunk_size > max_events:
            # We only want part of this chunk (because of the user-specified limit)
            # We'll slice up front to a partial chunk:
            needed = max_events - total_processed
            partial_chunk = {
                "GPStringKeys": chunk["GPStringKeys"][:needed],
                "GPStringValues": chunk["GPStringValues"][:needed],
            }
            process_chunk(partial_chunk, hists_by_key)
            total_processed += needed
            break
        else:
            # Process entire chunk
            process_chunk(chunk, hists_by_key)
            total_processed += chunk_size

        # If we've reached or exceeded max_events, stop reading
        if total_processed >= max_events:
            break

    print(f"Finished reading {total_processed} events in total.")

    # Now create a plot for each key and save to the output directory
    for key, h in hists_by_key.items():
        fig, ax = plt.subplots()
        h.plot(ax=ax)

        ax.set_title(f"Key: {key}")
        ax.set_xlabel("Value (float)")
        ax.set_ylabel("Counts")

        out_name = os.path.join(args.output_dir, f"{key}.png")
        plt.savefig(out_name)
        plt.close(fig)

    print(f"Plots saved to: {args.output_dir}")

if __name__ == "__main__":
    main()
