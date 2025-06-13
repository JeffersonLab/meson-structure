// only inside the ROOT prompt / root -x
#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif

#include "podio/Frame.h"
#include "podio/ROOTReader.h"
#include "podio/ROOTWriter.h"

#include <edm4hep/MCParticleCollection.h>

#include <fmt/core.h>
#include <fmt/format.h>

#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
// Global variables for analysis configuration
int events_limit = -1;  // -1 means process all events
int total_evt_counter = 0;

// Function declarations
void print_usage(const char* program_name);
void process_file(const std::string& filename);
void process_event(const podio::Frame& event, int event_number);



int main(int argc, char* argv[]) {
    // Simple argument parsing - collect files and look for -n option
    std::vector<std::string> input_files;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        if (arg == "-n" && i + 1 < argc) {
            events_limit = std::atoi(argv[++i]);
            fmt::print("Event limit set to: {}\n", events_limit);
        } else if (arg == "-h" || arg == "--help") {
            print_usage(argv[0]);
            return 0;
        } else if (arg[0] != '-') {
            input_files.push_back(arg);
        } else {
            fmt::print("Unknown option: {}\n", arg);
            print_usage(argv[0]);
            return 1;
        }
    }

    // Check if we have input files
    if (input_files.empty()) {
        fmt::print("Error: No input files provided\n");
        print_usage(argv[0]);
        return 1;
    }

    // Process each file
    fmt::print("Processing {} file(s)\n", input_files.size());
    for (const auto& filename : input_files) {
        fmt::print("\n=== Processing file: {} ===\n", filename);
        process_file(filename);

        // Check if we've reached the event limit
        if (events_limit > 0 && total_evt_counter >= events_limit) {
            fmt::print("\nReached event limit of {}, stopping.\n", events_limit);
            break;
        }
    }

    fmt::print("\nTotal events processed: {}\n", total_evt_counter);
    return 0;
}

void print_usage(const char* program_name) {
    fmt::print("Usage: {} [options] file1.root [file2.root ...]\n", program_name);
    fmt::print("Options:\n");
    fmt::print("  -n <number>  Process only <number> events (default: all)\n");
    fmt::print("  -h           Show this help message\n");
    fmt::print("\nNote: Options and files can be mixed in any order\n");
    fmt::print("Example: {} file1.root -n 100 file2.root file3.root\n", program_name);
}

void process_file(const std::string& filename) {
    try {
        // Open the ROOT file
        auto tfile = TFile::Open(filename.c_str());
        tfile->Print();
        fmt::print("=====here=======\n");

        auto reader = podio::ROOTReader();
        reader.openFile(filename);

        const auto nEvents = reader.getEntries(podio::Category::Event);
        fmt::print("File contains {} events\n", nEvents);

        // Process events
        for (unsigned i = 0; i < nEvents; ++i) {
            // Check event limit
            if (events_limit > 0 && total_evt_counter >= events_limit) {
                break;
            }

            auto event = podio::Frame(reader.readNextEntry(podio::Category::Event));

            // For the single event we show how to get access to event level parameters
            if (i==0) {
                const auto& cols = event.getParameterKeys<std::string>();
                fmt::print("===== Collections =====\n");
                for (const auto& col : cols) {
                    fmt::print("    {} {}\n", col, event.getParameter<std::string>(col).value_or("None"));
                }
                fmt::print("=======================\n");
            }
            process_event(event, i);
            total_evt_counter++;
        }
    } catch (const std::exception& e) {
        fmt::print("Error processing file {}: {}\n", filename, e.what());
    }
}

void process_event(const podio::Frame& event, int event_number) {
    // Get MCParticles collection
    try {
        auto& mcParticles = event.get<edm4hep::MCParticleCollection>("MCParticles");

        if (event_number < 5) {  // Debug output for first few events
            fmt::print("\n--- Event {} ---\n", event_number);
            fmt::print("Number of MCParticles: {}\n", mcParticles.size());

            // Print detailed information for first few particles
            int particle_count = 0;
            for (const auto& particle : mcParticles) {
                // if (particle_count >= 5) break;  // Only show first 5 particles

                fmt::print("\nParticle {}:\n", particle_count);
                fmt::print("  PDG: {}\n", particle.getPDG());
                fmt::print("  IDX: {}\n", particle.getObjectID().index);
                fmt::print("  Charge: {:.3f}\n", particle.getCharge());
                fmt::print("  Mass: {:.6f} GeV\n", particle.getMass());
                fmt::print("  GeneratorStatus: {}\n", particle.getGeneratorStatus());
                fmt::print("  SimulatorStatus: {}\n", particle.getSimulatorStatus());

                // Momentum
                auto momentum = particle.getMomentum();
                fmt::print("  Momentum: ({:.3f}, {:.3f}, {:.3f}) GeV\n",
                          momentum.x, momentum.y, momentum.z);

                // Vertex
                auto vertex = particle.getVertex();
                fmt::print("  Vertex: ({:.3f}, {:.3f}, {:.3f}) mm\n",
                          vertex.x, vertex.y, vertex.z);

                // Endpoint
                auto endpoint = particle.getEndpoint();
                fmt::print("  Endpoint: ({:.3f}, {:.3f}, {:.3f}) mm\n",
                          endpoint.x, endpoint.y, endpoint.z);

                // Time
                fmt::print("  Time: {:.3f} ns\n", particle.getTime());

                // Parent/daughter relationships
                fmt::print("  Number of parents: {}\n", particle.getParents().size());
                fmt::print("  Number of daughters: {}\n", particle.getDaughters().size());

                if (particle.getDaughters().size() > 1) {
                    for (const auto& daughter : particle.getDaughters())
                    fmt::print("      daughter: index: {} PDG: {}\n", daughter.getObjectID().index, daughter.getPDG());
                }


                particle_count++;
            }
        }

        // TODO: Add your analysis logic here
        // For example, finding Lambda particles, analyzing decays, etc.

    } catch (const std::exception& e) {
        fmt::print("Error accessing MCParticles in event {}: {}\n", event_number, e.what());
    }
}

// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt:  root -x -l -b -q 'cpp01_read_edm4eic.cxx("file.root",100)'
// ---------------------------------------------------------------------------
void cpp01_read_edm4eic(const char* infile,
                  int events = -1) {

    fmt::print("'test_edm4eic' entry point is used\n");
    fmt::print(" infile: {}", infile);
    fmt::print(" events: {}", events);

    events_limit      = events;                // reuse the global controls
    total_evt_counter = 0;

    process_file(infile);

    fmt::print("\nTotal events processed: {}\n", total_evt_counter);
}