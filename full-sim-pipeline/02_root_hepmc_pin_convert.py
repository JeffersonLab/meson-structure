#!/usr/bin/env python3
"""
convert_to_hepmc3.py

Reads 'Evnts' TTree from one or more large ROOT files (k-lambda events),
and converts them to HepMC3 format (ASCII output). Each output file can
contain at most --events-per-file events, so large samples are split
across multiple files, e.g. output_001.hepmc, output_002.hepmc, etc.

Features:
    - Chunked reading (uproot.iterate) to handle large files.
    - Each TTree entry -> one GenEvent with:
      * One GenVertex at (0,0,0,0).
      * Two incoming beam particles: (Proton, Electron).
      * Three outgoing final-state particles: (Scattered electron, Kaon, Lambda).
      * DIS invariants from 'invts' stored as DoubleAttributes with "dis_" prefix.
    - PDG codes guessed: Proton=2212, Electron=11, K+=321, Lambda=3122.
      Adjust if needed.

Usage Example:
  python root_hepmc_converter.py \
      --input-files file_5x41.root file_10x100.root \
      --chunk-size 50000 \
      --events 100000 \
      --output-prefix out_hepmc \
      --events-per-file 20000

Make sure to install uproot, awkward, and a proper HepMC3 w/ Python support:
  pip install uproot awkward
  # Then build/install HepMC3 from https://gitlab.cern.ch/hepmc/HepMC3
"""

import argparse
import os
import uproot
import awkward as ak
from pyHepMC3 import HepMC3 as hm
from pyHepMC3 import std as std

# PDG codes
PDG_PROTON = 2212
PDG_ELECTRON = 11
PDG_KAON_PLUS = 321
PDG_LAMBDA = 3122

class SplitHepMC3Writer:
    """
    A small helper class that writes GenEvents to multiple ASCII files,
    each file containing up to 'events_per_file' events.
    Filenames are prefixed by 'prefix_' and have an index like _001, _002, ...
    """
    def __init__(self, prefix: str, events_per_file: int):
        self.prefix = prefix
        self.events_per_file = events_per_file
        self.current_file_idx = 1
        self.events_in_current_file = 0
        self.current_writer = None

    def _open_new_file(self):
        """Open a new WriterAscii, incrementing the file index."""
        filename = f"{self.prefix}_{self.current_file_idx:03d}.hepmc"
        print(f"Opening new output file: {filename}")
        self.current_file_idx += 1
        return hm.WriterAscii(filename)

    def write_event(self, event: hm.GenEvent):
        # Check if the next event would exceed the limit
        if (self.events_in_current_file >= self.events_per_file) or not self.current_writer:
            self._next_file()
        self.current_writer.write_event(event)
        self.events_in_current_file += 1

    def _next_file(self):
        """Close the current file (if any) and open the next one."""
        if self.current_writer:
            self.current_writer.close()
        self.current_writer = self._open_new_file()
        self.events_in_current_file = 0

    def close(self):
        """Close the last open file, if any."""
        if self.current_writer:
            self.current_writer.close()
            self.current_writer = None


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert k-lambda TTree to multiple HepMC3 files."
    )
    parser.add_argument(
        "--input-files", "-i", nargs="+", required=True,
        help="List of ROOT files with 'Evnts' TTree."
    )
    parser.add_argument(
        "--events", type=int, default=None,
        help="Max number of events to process in total (default: no limit)."
    )
    parser.add_argument(
        "--chunk-size", type=int, default=50000,
        help="Number of TTree entries to read per chunk (default: 50000)."
    )
    parser.add_argument(
        "--output-prefix", "-o", default="output",
        help="Prefix for output HepMC3 ASCII files (default: 'output')."
    )
    parser.add_argument(
        "--events-per-file", type=int, default=20000,
        help="Number of events per each HepMC3 file (default: 20000)."
    )
    return parser.parse_args()


def make_gen_event(event_number: int, invts_entry, p_inc, e_inc, e_scat, k_out, lamb_out):
    """
    Build a HepMC3 GenEvent for a single TTree entry.

    :param event_number: Unique integer for labeling the event
    :param invts_entry:  awkward record with fields e.g. Q2, xBj, W, ...
    :param p_inc, e_inc, e_scat, k_out, lamb_out:
                        each is an awkward record with structure
                        { "fP": { "fX","fY","fZ" }, "fE" }
    :return: HepMC3 GenEvent
    """
    event = hm.GenEvent()
    event.set_event_number(event_number)

    # Create a single GenVertex at (0,0,0,0).
    vertex = hm.GenVertex(hm.FourVector(0, 0, 0, 0))
    event.add_vertex(vertex)

    # 1) Incoming (beam) proton
    proton_in = hm.GenParticle(
        hm.FourVector(
            p_inc["fP"]["fX"],
            p_inc["fP"]["fY"],
            p_inc["fP"]["fZ"],
            p_inc["fE"]
        ),
        PDG_PROTON,
        4  # status=4 => beam
    )
    vertex.add_particle_in(proton_in)

    # 2) Incoming (beam) electron
    electron_in = hm.GenParticle(
        hm.FourVector(
            e_inc["fP"]["fX"],
            e_inc["fP"]["fY"],
            e_inc["fP"]["fZ"],
            e_inc["fE"]
        ),
        PDG_ELECTRON,
        4  # beam
    )
    vertex.add_particle_in(electron_in)

    # 3) Outgoing scattered electron
    electron_out = hm.GenParticle(
        hm.FourVector(
            e_scat["fP"]["fX"],
            e_scat["fP"]["fY"],
            e_scat["fP"]["fZ"],
            e_scat["fE"]
        ),
        PDG_ELECTRON,
        1  # final state
    )
    vertex.add_particle_out(electron_out)

    # 4) Outgoing kaon
    kaon_out = hm.GenParticle(
        hm.FourVector(
            k_out["fP"]["fX"],
            k_out["fP"]["fY"],
            k_out["fP"]["fZ"],
            k_out["fE"]
        ),
        PDG_KAON_PLUS,
        1
    )
    vertex.add_particle_out(kaon_out)

    # 5) Outgoing lambda
    lambda_out = hm.GenParticle(
        hm.FourVector(
            lamb_out["fP"]["fX"],
            lamb_out["fP"]["fY"],
            lamb_out["fP"]["fZ"],
            lamb_out["fE"]
        ),
        PDG_LAMBDA,
        1
    )
    vertex.add_particle_out(lambda_out)

    # Attach 'invts' struct fields as attributes
    for field_name in invts_entry.fields:
        val = invts_entry[field_name]
        attr_key = "dis_" + field_name.lower()  # e.g. "dis_q2" for Q2
        event.add_attribute(attr_key, hm.DoubleAttribute(float(val)))

    return event


def main():
    args = parse_args()

    # We'll create the "split writer" that can handle multiple output files.
    writer = SplitHepMC3Writer(args.output_prefix, args.events_per_file)

    branches = [
        "invts",
        "P_Inc.",
        "e_Inc.",
        "e_Scat.",
        "k.",
        "lamb_scat."
    ]

    event_counter = 0

    for root_file in args.input_files:
        print(f"\nProcessing file: {root_file}")
        for chunk in uproot.iterate(
                f"{root_file}:Evnts",
                expressions=branches,
                library="ak",
                step_size=args.chunk_size
        ):
            invts_array   = chunk["invts"]
            p_inc_array   = chunk["P_Inc."]
            e_inc_array   = chunk["e_Inc."]
            e_scat_array  = chunk["e_Scat."]
            k_array       = chunk["k."]
            lamb_scat_arr = chunk["lamb_scat."]

            n_chunk = len(invts_array)
            for i in range(n_chunk):
                if args.events and (event_counter >= args.events):
                    break

                invts_entry   = invts_array[i]
                p_inc_entry   = p_inc_array[i]
                e_inc_entry   = e_inc_array[i]
                e_scat_entry  = e_scat_array[i]
                k_out_entry   = k_array[i]
                lamb_out_entry = lamb_scat_arr[i]

                gen_evt = make_gen_event(
                    event_number=event_counter,
                    invts_entry=invts_entry,
                    p_inc=p_inc_entry,
                    e_inc=e_inc_entry,
                    e_scat=e_scat_entry,
                    k_out=k_out_entry,
                    lamb_out=lamb_out_entry
                )
                writer.write_event(gen_evt)
                event_counter += 1

            if args.events and (event_counter >= args.events):
                break
        if args.events and (event_counter >= args.events):
            break

    # Close the final output file
    writer.close()

    print(f"\nAll done! Processed {event_counter} events total.")


if __name__ == "__main__":
    main()
