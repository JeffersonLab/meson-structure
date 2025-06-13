"""Very basic example of how to iterate over EIC files

You may consider this file to be a skeleton of how to read multiple root files efficiently
"""

import argparse
import uproot
import awkward as ak


def main():
    """Main function to run the tutorial analysis"""
    parser = argparse.ArgumentParser(description="Very basic example to read EIC files")
    parser.add_argument("input_files", nargs="+", help="List of ROOT files containing MCParticles.")
    parser.add_argument("--step-size", default=100, type=int, help="Number of events to read per chunk.")
    parser.add_argument("-n", "--nevents", default=200, type=int, help="Number of events to process")
    args = parser.parse_args()

    print(f"Starting analysis of {len(args.input_files)} files")
    print(f"Using chunk size of {args.step_size} events")
    print(f"Will process up to {args.nevents} events")
    print(f"Processing files:\n", "\n    ".join(args.input_files))

    # Uproot can process groups of files. It needs an array of {file_name:tree_name} for this
    # In our case we always have "events" tree in each file:
    files_with_tree = [{filename: "events"} for filename in args.input_files]

    # It is much-much faster to read only what we need:
    branches = [
        "MCParticles.PDG",
        "MCParticles.momentum.z",
        "MCParticles.endpoint.z",
    ]

    # Read and process file in chunks
    for chunk_i, chunk in enumerate(uproot.iterate(files_with_tree, branches, step_size=args.step_size, entry_stop=args.nevents)):

        print(f"Сhunk {chunk_i} read")
        # print data verbose. Very verbose
        # chunk["MCParticles.PDG"].show()

        # Print data shape. It is going to be
        # [n-events-in-chunk]x{branch:[n-particles]}
        chunk.type.show()

        # Show a value of a single particle
        particle_pdg = chunk[0]["MCParticles.PDG"][2]
        print(f"  PDG of the 3d particle of the 1st event in this chunk: {particle_pdg}")

        # You can iterate event by event but it IS SLOW!!!
        # for event_i in range(len(chunk)):
        #    pdgs_in_event = chunk[event_i]["MCParticles.PDG"]

        # Vectorized way of processing the data
        lambda_filter = chunk["MCParticles.PDG"] == 3122
        lam_pz = ak.mean(chunk[lambda_filter]["MCParticles.momentum.z"])
        print(f"  Lambdas pz in this chunk: {lam_pz}")

        # Do analysis ...

    print("Analysis complete!")


if __name__ == "__main__":
    main()
