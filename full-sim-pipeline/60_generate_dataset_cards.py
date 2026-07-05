#!/usr/bin/env python3
"""
60_generate_dataset_cards.py

Write one small YAML "dataset card" per (flavor, energy) describing where the
reconstructed .edm4eic.root files live. Cards are compatible with
ai-epic-background/full-sim-pipeline/41_create_csv_eicrecon_jobs.py: point its
config `datasets_dir` at the output of this script to run the CSV conversion
on meson-structure data alongside the rucio-discovered datasets.

Unlike ai-epic-background's 42_create_datasets_list.py (which queries rucio
and lists root:// PFNs), meson-structure data is not on rucio: processing runs
on the same farm as the files, so cards simply list absolute paths. The
`dataset:` field plays the role of the rucio DID — here it is the absolute
per-energy directory; the `xrootd:` field records the equivalent public
XRootD location (root://dtn-eic.jlab.org/).

Card layout:

    dataset: /work/eic3/users/romanov/meson-structure-2026-07/reco/5x41
    xrootd: root://dtn-eic.jlab.org//work/.../reco/5x41
    slug: msf_2026-07_reco_5x41
    metadata:
      data_type: reconstructed
      campaign: 2026-07
      detector: epic_craterlake
      has_background: false
      beam_energy: 5x41
      q2: gt-1to500
      beam_effects: true
      generator: eic_mesonsf_generator
      physics: k-lambda
    rucio_metadata:      # pre-filled template for a future rucio registration
      ...
    n_files: 998
    files:
    - /work/.../msf_5x41_1000evt_0001.edm4eic.root

Config keys (campaign YAML)
---------------------------
    csv_eicrecon_input: "${eicrecon_output}"       # scanned per energy
    datasets_dir:       "${base_dir}/datasets"     # where cards are written
    q2_min: 1                                      # optional; EG q2 range
    q2_max: 500
    campaign: "2026-07"      # optional; default derived from base_dir name
    detector: "epic_craterlake"                    # optional
    generator: "eic_mesonsf_generator"             # optional
    physics: "k-lambda"                            # optional
    xrootd_prefix: "root://dtn-eic.jlab.org/"      # optional
    dataset_metadata: {...}  # optional; merged into every card's metadata

Run on the farm where the files live:
    python 60_generate_dataset_cards.py -c config-campaign-26-07.yaml
"""

import argparse
import os
import re
from glob import glob

import yaml
from omegaconf import OmegaConf

from job_creator import load_config, load_config_for_energy

ENERGY_RE = re.compile(r"^(\d+)x(\d+)$")           # 5x41 -> (5, 41)

XROOTD_PREFIX_DEFAULT = "root://dtn-eic.jlab.org/"
GENERATOR_DEFAULT = "eic_mesonsf_generator"        # github.com/JeffersonLab/eic_mesonsf_generator
PHYSICS_DEFAULT = "k-lambda"
DETECTOR_DEFAULT = "epic_craterlake"


def campaign_from_base_dir(base_dir):
    """Derive the campaign name from the base directory.

    /work/.../meson-structure-2026-07 -> 2026-07; anything else falls back to
    the full directory name (override with the `campaign` config key).
    """
    name = os.path.basename(os.path.normpath(base_dir))
    prefix = "meson-structure-"
    return name[len(prefix):] if name.startswith(prefix) else name


def software_release_from_container(container):
    """Extract the image tag from the container path.

    /cvmfs/.../eic_xl:26.06-stable/ -> 26.06-stable; local .sif images fall
    back to the file name.
    """
    if not container:
        return None
    name = os.path.basename(os.path.normpath(str(container)))
    return name.split(":", 1)[1] if ":" in name else name


def flavor_from_input_dir(input_dir, base_dir):
    """Flavor = the directory holding the per-energy dirs (reco, reco-background, ...)."""
    parent = os.path.dirname(os.path.normpath(input_dir))
    rel = os.path.relpath(parent, base_dir)
    return os.path.basename(parent) if rel.startswith("..") else rel.replace(os.sep, "_")


def make_slug(campaign, flavor, energy):
    """msf_<campaign>_<flavor>_<energy>, restricted to alnum . _ - characters."""
    slug = f"msf_{campaign}_{flavor}_{energy}"
    return re.sub(r"[^A-Za-z0-9._-]", "_", slug)


def build_card(config, energy, input_dir, files):
    """Assemble one dataset-card dict (same shape as the ai-epic-background cards)."""
    base_dir = str(config.base_dir)
    campaign = str(config.get("campaign") or campaign_from_base_dir(base_dir))
    detector = str(config.get("detector", DETECTOR_DEFAULT))
    generator = str(config.get("generator", GENERATOR_DEFAULT))
    physics = str(config.get("physics", PHYSICS_DEFAULT))
    flavor = flavor_from_input_dir(input_dir, base_dir)
    has_background = "background" in flavor.lower()
    slug = make_slug(campaign, flavor, energy)

    xrootd_prefix = str(config.get("xrootd_prefix", XROOTD_PREFIX_DEFAULT))
    dataset = os.path.normpath(input_dir)

    metadata = {
        "data_type": "reconstructed",
        "campaign": campaign,
        "detector": detector,
        "has_background": has_background,
        "beam_energy": energy,
        "beam_effects": True,   # afterburner (crossing angle + beam effects) always applied
        "generator": generator,
        "physics": physics,
    }

    q2_min = config.get("q2_min")
    q2_max = config.get("q2_max")
    if q2_min is not None and q2_max is not None:
        metadata["q2"] = f"gt-{q2_min}to{q2_max}"

    extra = config.get("dataset_metadata")
    if extra:
        metadata.update(OmegaConf.to_container(extra, resolve=True))

    # Pre-filled template for a future rucio registration; server-side fields
    # (created_at, availability, ...) are omitted and null values are to-fill.
    e_beam, i_beam = (int(v) for v in ENERGY_RE.match(energy).groups())
    rucio_metadata = {
        "account": None,
        "scope": None,
        "name": dataset,
        "did_type": "DATASET",
        "data_level": "reconstruction",
        "electron_beam_energy_gev": e_beam,
        "ion_beam_energy_gev": i_beam,
        "ion_species": "p",
        "generator": generator,
        "geometry_config": f"craterlake_{energy}",
        "is_background_mixed": has_background,
        "requester_pwg": None,
        "software_release": software_release_from_container(config.get("container")),
    }
    if q2_min is not None:
        rucio_metadata["q2_min_gev2"] = q2_min
    if q2_max is not None:
        rucio_metadata["q2_max_gev2"] = q2_max

    return {
        "dataset": dataset,
        # xrootd URL form is root://host//abs/path (double slash before the path)
        "xrootd": xrootd_prefix.rstrip("/") + "/" + dataset,
        "slug": slug,
        "metadata": metadata,
        "rucio_metadata": rucio_metadata,
        "n_files": len(files),
        "files": files,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-c", "--config", required=True, help="Campaign config YAML")
    parser.add_argument("--max-files", type=int, default=0, help="Cap files per dataset (0 = all)")
    parser.add_argument("--clean", action="store_true", help="Remove existing *.yaml in datasets_dir first")
    args = parser.parse_args()

    config = load_config(args.config)
    base_dir = str(config.base_dir)
    datasets_dir = os.path.abspath(str(config.get("datasets_dir") or os.path.join(base_dir, "datasets")))

    os.makedirs(datasets_dir, exist_ok=True)
    if args.clean:
        for f in glob(os.path.join(datasets_dir, "*.yaml")):
            os.remove(f)

    print("=" * 70)
    print("MESON-STRUCTURE DATASET CARDS")
    print(f"  base_dir: {base_dir}")
    print(f"  output:   {datasets_dir}")
    if args.max_files:
        print(f"  max files/dataset: {args.max_files}")
    print("=" * 70)

    written = []
    for energy in config.energies:
        e_config = load_config_for_energy(args.config, energy)
        input_dir = os.path.abspath(str(e_config.csv_eicrecon_input))
        files = sorted(glob(os.path.join(input_dir, "*.edm4eic.root")))
        if args.max_files:
            files = files[: args.max_files]
        if not files:
            print(f"  WARN: no *.edm4eic.root in {input_dir} -- skipping {energy}")
            continue

        card = build_card(e_config, energy, input_dir, files)
        out_path = os.path.join(datasets_dir, f"{card['slug']}.yaml")
        with open(out_path, "w") as f:
            yaml.safe_dump(card, f, sort_keys=False, default_flow_style=False)
        written.append(out_path)
        print(f"  {card['slug']}  ({len(files)} files) -> {out_path}")

    print("=" * 70)
    print(f"Wrote {len(written)} dataset card(s) to {datasets_dir}")
    print("Next (in ai-epic-background, with its config datasets_dir pointing here):")
    print("  python 41_create_csv_eicrecon_jobs.py -c <config>")
    print("=" * 70)


if __name__ == "__main__":
    main()
