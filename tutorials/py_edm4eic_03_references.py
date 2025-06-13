"""
Shows how references between different data blocks work.

By the "references" we mean:

- MCParticles referencing parents and daughters. And how to navigate them
- Tracks referencing corresponding Hits
- Reconstructed Tracks referencing related MonteCarlo particle. Etc.

"""

import argparse
import os

import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt

# The scikit-hep "hist" library:
from hist import Hist


data_hist = Hist.new.Regular(100, 0, 1000, name="value").Double()


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
    pass


def main():
    parser = argparse.ArgumentParser(description="Shows how references between different data blocks work")
    parser.add_argument(
        "input_files",
        nargs="+",
        help="One or more EDM4eic ROOT files to process."
    )
    parser.add_argument(
        "-e", "--events",
        type=int,
        default=None,
        help="If set, stop processing after this many events (across all files)."
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="plots",
        help="Directory where output plots will be saved."
    )

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
