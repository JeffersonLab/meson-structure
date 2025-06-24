// only inside the ROOT prompt / root -x
#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif

#include "podio/Frame.h"
#include "podio/ROOTReader.h"

#include <edm4hep/MCParticleCollection.h>
#include <edm4eic/ReconstructedParticleCollection.h>
#include <edm4eic/MCRecoClusterParticleAssociationCollection.h>
#include <edm4eic/ClusterCollection.h>

#include <fmt/core.h>
#include <fmt/format.h>

#include <TFile.h>

#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <map>

// Global variables for analysis configuration
int events_limit = -1;  // -1 means process all events
int total_evt_counter = 0;
int total_reco_lambdas = 0;
bool verbose_mode = false;

// Function declarations
void print_usage(const char* program_name);
void process_file(const std::string& filename);
void process_event(const podio::Frame& event, int event_number);
void print_mc_lambdas(const edm4hep::MCParticleCollection& mcParticles, int event_number);
void print_reco_lambdas(const edm4eic::ReconstructedParticleCollection&, int event_number);

int main(int argc, char* argv[]) {
    // Simple argument parsing - collect files and look for options
    std::vector<std::string> input_files;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        if (arg == "-n" && i + 1 < argc) {
            events_limit = std::atoi(argv[++i]);
            fmt::print("Event limit set to: {}\n", events_limit);
        } else if (arg == "-v" || arg == "--verbose") {
            verbose_mode = true;
            fmt::print("Verbose mode enabled\n");
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
}

void print_usage(const char* program_name) {
    fmt::print("Usage: {} [options] file1.root [file2.root ...]\n", program_name);
    fmt::print("Options:\n");
    fmt::print("  -n <number>  Process only <number> events (default: all)\n");
    fmt::print("  -v           Verbose mode - show all particles, not just Lambdas\n");
    fmt::print("  -h           Show this help message\n");
    fmt::print("\nExample: {} -n 10 -v file1.root file2.root\n", program_name);
}


void process_file(const std::string& filename) {
    try {
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

            // Read event from PODIO root file
            auto event = podio::Frame(reader.readNextEntry(podio::Category::Event));

            process_event(event, total_evt_counter);
            total_evt_counter++;
        }

        fmt::print("Analysis Summary so far");
        fmt::print("  Total events processed: {}\n", total_evt_counter);
        fmt::print("  Total reconstructed FF Lambdas found: {}\n", total_reco_lambdas);
        if (total_reco_lambdas > 0) {
            fmt::print("  Reco lambdas per event: {:.3f}\n",  total_reco_lambdas / static_cast<double>(total_evt_counter));
        }
    } catch (const std::exception& e) {
        fmt::print("Error processing file {}: {}\n", filename, e.what());
    }
}

void process_event(const podio::Frame& event, int event_number) {


    const auto& lambdas = event.get<edm4eic::ReconstructedParticleCollection>("ReconstructedFarForwardZDCLambdas");
    if (lambdas.empty()) {
        // not interested in events without reco lambdas fmt::print("  No reconstructed FF Lambdas in this event\n");
        return;
    }

    fmt::print("========== Event {} ==========\n", event_number);

    // look at MC Lambdas
    const auto& mcParticles = event.get<edm4hep::MCParticleCollection>("MCParticles");
    print_mc_lambdas(mcParticles, event_number);

    // 2. Then look at reconstructed FF Lambdas
    print_reco_lambdas(lambdas, event_number);

    fmt::print("\n");
}

void print_mc_lambdas(const edm4hep::MCParticleCollection& mcParticles, int event_number) {
    fmt::print("\n[MC Truth Lambdas]\n");

    int mc_lambda_count = 0;
    for (const auto& particle : mcParticles) {
        // Lambda PDG code is 3122
        if (particle.getPDG() == 3122) {
            mc_lambda_count++;

            fmt::print("  MC Lambda #{} (idx={}):\n", mc_lambda_count, particle.getObjectID().index);

            // Momentum and energy
            auto mom = particle.getMomentum();
            double p = std::sqrt(mom.x*mom.x + mom.y*mom.y + mom.z*mom.z);
            fmt::print("    Momentum: ({:.2f}, {:.2f}, {:.2f}) GeV, |p|={:.2f} GeV\n",
                      mom.x, mom.y, mom.z, p);
            fmt::print("    Mass: {:.3f} GeV\n", particle.getMass());

            // Vertex and endpoint
            auto vtx = particle.getVertex();
            auto end = particle.getEndpoint();
            fmt::print("    Vertex: ({:.1f}, {:.1f}, {:.1f}) mm\n", vtx.x, vtx.y, vtx.z);
            fmt::print("    Endpoint: ({:.1f}, {:.1f}, {:.1f}) mm\n", end.x, end.y, end.z);

            // Decay length
            double decay_length = std::sqrt(
                (end.x-vtx.x)*(end.x-vtx.x) +
                (end.y-vtx.y)*(end.y-vtx.y) +
                (end.z-vtx.z)*(end.z-vtx.z)
            );
            fmt::print("    Decay length: {:.1f} mm\n", decay_length);

            // Daughters
            fmt::print("    Daughters ({}):", particle.getDaughters().size());
            for (const auto& daughter : particle.getDaughters()) {
                fmt::print(" PDG={}", daughter.getPDG());
            }
            fmt::print("\n");
        } else if (verbose_mode && event_number < 3) {
            // In verbose mode, show other particles too (for first few events)
            fmt::print("  Other particle: PDG={}, idx={}\n",
                      particle.getPDG(), particle.getObjectID().index);
        }
    }

    if (mc_lambda_count == 0) {
        fmt::print("  No MC Lambdas found in this event\n");
    }
}

void print_reco_lambdas(const edm4eic::ReconstructedParticleCollection& lambdas, int event_number) {
    fmt::print("\n[Reconstructed Far-Forward Lambdas]\n");

    try {

        if (lambdas.empty()) {
            fmt::print("  No reconstructed FF Lambdas in this event\n");
            return;
        }

        int reco_idx = 0;
        for (const auto& lam : lambdas) {
            total_reco_lambdas++;

            fmt::print("  Reco Lambda #{}:\n", reco_idx);
            fmt::print("    PDG: {}, Charge: {:.1f}\n", lam.getPDG(), lam.getCharge());

            // Kinematics
            auto mom = lam.getMomentum();
            double p = std::sqrt(mom.x*mom.x + mom.y*mom.y + mom.z*mom.z);
            fmt::print("    Momentum: ({:.2f}, {:.2f}, {:.2f}) GeV, |p|={:.2f} GeV\n",
                      mom.x, mom.y, mom.z, p);
            fmt::print("    Energy: {:.2f} GeV, Mass: {:.3f} GeV\n",
                      lam.getEnergy(), lam.getMass());

            // Reference point
            auto ref = lam.getReferencePoint();
            fmt::print("    Reference point: ({:.1f}, {:.1f}, {:.1f}) mm\n",
                      ref.x, ref.y, ref.z);

            // Quality
            fmt::print("    GoodnessOfPID: {:.3f}, Type: {}\n",
                      lam.getGoodnessOfPID(), lam.getType());

            // Associated objects
            fmt::print("    Associated objects: {} clusters, {} tracks, {} particles\n",
                      lam.getClusters().size(),
                      lam.getTracks().size(),
                      lam.getParticles().size());

            // Daughter particles
            if (!lam.getParticles().empty()) {
                fmt::print("    Daughter particles:\n");
                int dtr_idx = 0;
                for (const auto& dtr : lam.getParticles()) {
                    fmt::print("      Daughter {}: PDG={}, Charge={:.1f}, E={:.2f} GeV\n",
                              dtr_idx, dtr.getPDG(), dtr.getCharge(), dtr.getEnergy());

                    auto dtr_mom = dtr.getMomentum();
                    fmt::print("        p=({:.2f}, {:.2f}, {:.2f}) GeV\n",
                              dtr_mom.x, dtr_mom.y, dtr_mom.z);

                    // Daughter's clusters
                    if (!dtr.getClusters().empty()) {
                        fmt::print("        {} cluster(s):", dtr.getClusters().size());
                        for (const auto& cl : dtr.getClusters()) {
                            fmt::print(" E={:.2f}", cl.getEnergy());
                        }
                        fmt::print(" GeV\n");
                    }
                    dtr_idx++;
                }
            }

            // Lambda's own clusters
            if (!lam.getClusters().empty()) {
                fmt::print("    Direct clusters:\n");
                for (const auto& cluster : lam.getClusters()) {
                    auto pos = cluster.getPosition();
                    fmt::print("      E={:.2f} GeV, pos=({:.0f}, {:.0f}, {:.0f}) mm, nhits={}\n",
                              cluster.getEnergy(), pos.x, pos.y, pos.z, cluster.getNhits());
                }
            }

            reco_idx++;
        }

    } catch (const std::exception& e) {
        fmt::print("  Error accessing ReconstructedFarForwardZDCLambdas: {}\n", e.what());
    }
}

// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt: root -x -l -b -q 'cpp_02_ff_lambda.cxx("file.root", 10)'
// ---------------------------------------------------------------------------
void cpp_02_ff_lambda(const char* infile, int events = -1, bool verbose = false) {
    fmt::print("cpp_02_ff_lambda tutorial\n");
    fmt::print("  infile: {}\n", infile);
    fmt::print("  events: {}\n", events);
    fmt::print("  verbose: {}\n", verbose ? "ON" : "OFF");

    events_limit = events;
    verbose_mode = verbose;
    total_evt_counter = 0;
    total_reco_lambdas = 0;

    process_file(infile);
}