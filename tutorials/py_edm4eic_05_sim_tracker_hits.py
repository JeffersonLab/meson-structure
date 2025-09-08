#!/usr/bin/env python3
"""
==============================================================================
TUTORIAL: Analyzing EDM4hep SimTrackerHit Data from ROOT Files
==============================================================================

What this tutorial demonstrates:
---------------------------------
1. How to open and explore ROOT files containing EDM4hep simulation data
2. How to find specific data types (vector<edm4hep::SimTrackerHitData>) in the file
3. How to access and read hit position data from detector components
4. Understanding the EDM4hep data structure for tracker hits

EDM4hep Background:
-------------------
EDM4hep (Event Data Model for HEP) is a common data format used in High Energy
Physics experiments. SimTrackerHitData contains Monte Carlo simulation hits
from tracking detectors, including:
- Position (x, y, z) where particles hit the detector
- Energy deposition
- Time information
- Links to the MC particle that created the hit

This script specifically looks for Silicon Barrel Vertex detector hits as an
example of how to access and analyze this data.

Usage:
------
python analyze_sim_tracker_hits.py <root_file>

Requirements:
-------------
- uproot: For reading ROOT files in Python
- awkward: For handling jagged arrays from ROOT
- rich: For pretty printing (optional but helpful)
==============================================================================
"""

import sys
import uproot


def main():
    # =========================================================================
    # STEP 1: Command Line Argument Processing
    # =========================================================================
    # Check that user provided exactly one argument (the ROOT file path)
    if len(sys.argv) != 2:
        print("Usage: python analyze_sim_tracker_hits.py <root_file>")
        print("Example: python analyze_sim_tracker_hits.py simulation_output.root")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # =====================================================================
        # STEP 2: Open the ROOT File
        # =====================================================================
        # ROOT files are structured containers used in particle physics
        # They contain "trees" which hold the actual event data
        print(f"Opening ROOT file: {filename}")
        file = uproot.open(filename)

        # =====================================================================
        # STEP 3: Access the Event Tree
        # =====================================================================
        # In EDM4hep files, the main tree is typically called "events"
        # Each entry in this tree represents one physics event (e.g., one collision)
        tree = file["events"]
        print(f"Successfully opened tree with {tree.num_entries} events")

        # =====================================================================
        # STEP 4: Find SimTrackerHit Branches
        # =====================================================================
        # ROOT trees contain "branches" - each branch stores a different type of data
        # We're looking for branches that contain simulation tracker hit data
        # The typename "vector<edm4hep::SimTrackerHitData>" indicates a collection
        # of simulation hits for each event

        print("\nSearching for SimTrackerHit branches...")

        # typenames() returns a dictionary of branch_name: typename pairs
        # filter_typename parameter filters to only branches matching our type
        sim_tracker_branches = tree.typenames(
            recursive=False,  # Don't look into sub-branches
            full_paths=True,  # Return full branch paths
            filter_typename="vector<edm4hep::SimTrackerHitData>"
        )

        # =====================================================================
        # STEP 5: Display Found Branches
        # =====================================================================
        # Each branch typically corresponds to a different detector component
        # Common examples:
        # - SiBarrelVertexHits: Silicon vertex detector in barrel region
        # - SiBarrelTrackerHits: Silicon tracker in barrel region
        # - SiEndcapTrackerHits: Silicon tracker in endcap region

        print("\n" + "=" * 60)
        print("Branches with type 'vector<edm4hep::SimTrackerHitData>':")
        print("=" * 60)

        if not sim_tracker_branches:
            print("No branches found with the specified typename.")
            print("This file may not contain simulation data.")
        else:
            # List all found branches with numbering for clarity
            for i, branch_name in enumerate(sim_tracker_branches.keys(), 1):
                print(f"{i}. {branch_name}")

        print("\n" + "=" * 60)

        # =====================================================================
        # STEP 6: Access Specific Branch Data (SiBarrelVertexHits)
        # =====================================================================
        # Now we'll look at a specific detector's hits as an example
        # The Silicon Barrel Vertex detector is typically the innermost tracker

        branch_name = "SiBarrelHits"

        if branch_name in sim_tracker_branches:
            print(f"Analyzing '{branch_name}' branch")
            print("=" * 60)

            # =================================================================
            # STEP 7: Understanding the Data Structure
            # =================================================================
            # Each SimTrackerHit branch has sub-branches for different properties:
            # - {branch_name}.position.x/y/z : Hit positions in mm
            # - {branch_name}.EDep : Energy deposition in GeV
            # - {branch_name}.time : Time of hit in ns
            # - {branch_name}.cellID : Detector cell identifier
            # - {branch_name}.momentum.x/y/z : Particle momentum at hit
            # - {branch_name}.pathLength : Path length from vertex

            # We'll focus on position data for this tutorial

            # Limit to first 100 events to keep output manageable
            max_entries = min(100, tree.num_entries)

            try:
                # =============================================================
                # STEP 8: Construct Branch Paths for Position Data
                # =============================================================
                # In ROOT files with EDM4hep data, the naming convention is:
                # {BranchName}/{BranchName}.{field}.{component}
                # For example: SiBarrelVertexHits/SiBarrelVertexHits.position.x

                pos_x_branch = f'{branch_name}/{branch_name}.position.x'
                pos_y_branch = f'{branch_name}/{branch_name}.position.y'

                # Verify these branches exist before trying to read them
                if pos_x_branch not in tree.keys() or pos_y_branch not in tree.keys():
                    print(f"Error: Position branches not found for {branch_name}")
                    print(f"Available sub-branches: {[k for k in tree.keys() if k.startswith(branch_name)]}")
                    sys.exit(1)

                # =============================================================
                # STEP 9: Read the Data Arrays
                # =============================================================
                # Each array element corresponds to one event
                # Each event can have multiple hits (jagged array structure)
                # For example:
                #   Event 0: [hit1_x, hit2_x, hit3_x]  # 3 hits
                #   Event 1: [hit1_x]                   # 1 hit
                #   Event 2: []                          # no hits

                print(f"\nReading position data for first {max_entries} events...")

                pos_x_array = tree[pos_x_branch].array(entry_stop=max_entries)
                pos_y_array = tree[pos_y_branch].array(entry_stop=max_entries)

                # These are awkward arrays - they handle jagged data efficiently
                print(f"Data type: {type(pos_x_array)}")
                print(f"Number of events read: {len(pos_x_array)}")

                print("\n" + "-" * 60)
                print("Position data (x, y) in mm:")
                print("-" * 60)

                # =============================================================
                # STEP 10: Process and Display the Hit Data
                # =============================================================
                # We'll iterate through events and hits, displaying positions

                total_hit_count = 0  # Track the total number of hits displayed
                entry_idx = -1       # The last event number processed

                for entry_idx in range(len(pos_x_array)):
                    # Get hits for this specific event
                    event_pos_x = pos_x_array[entry_idx]
                    event_pos_y = pos_y_array[entry_idx]

                    # Only process events that actually have hits
                    if len(event_pos_x) > 0:
                        print(f"\nEvent {entry_idx}: {len(event_pos_x)} hits")

                        # Loop through each hit in this event
                        for hit_idx in range(len(event_pos_x)):
                            # Stop if we've displayed 100 hits total
                            if total_hit_count >= 100:
                                print(f"\n... (stopped at 100 hits total)")
                                break

                            # Extract x,y coordinates for this hit
                            x = event_pos_x[hit_idx]
                            y = event_pos_y[hit_idx]

                            # Display with formatting for readability
                            # Position units are typically in mm in EDM4hep
                            print(f"  Hit {hit_idx:3d}: x = {x:12.6f} mm, y = {y:12.6f} mm")
                            total_hit_count += 1

                    # Stop processing events if we've shown enough hits
                    if total_hit_count >= 100:
                        break

                # =============================================================
                # STEP 11: Summary Statistics
                # =============================================================
                if total_hit_count == 0:
                    print("No hits found in the first 100 events.")
                    print("This might indicate:")
                    print("  - Events with no particles hitting this detector")
                    print("  - Different branch naming in your file")
                else:
                    print(f"\nSummary:")
                    print(f"  Total hits displayed: {total_hit_count}")
                    print(f"  Events processed: {entry_idx + 1}")

                    # You could add more analysis here, such as:
                    # - Average hits per event
                    # - Position distributions
                    # - Radial distance calculations

            except Exception as e:
                print(f"Error reading position data: {e}")
                print("This might be due to unexpected data structure.")

        else:
            # =================================================================
            # STEP 12: Handle Missing Branch
            # =================================================================
            print(f"Branch '{branch_name}' not found in the file.")
            print("This detector might not be present in your simulation.")
            print("\nAvailable SimTrackerHit branches are listed above.")
            print("You can modify the script to analyze a different branch.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        print("Please check the file path and try again.")
        sys.exit(1)

    except KeyError as e:
        print(f"Error: The file doesn't contain an 'events' tree.")
        print(f"Available trees in file: {list(uproot.open(filename).keys())}")
        print("This might not be an EDM4hep ROOT file.")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Please check your ROOT file format.")
        sys.exit(1)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    # This ensures the script runs only when executed directly,
    # not when imported as a module
    main()
