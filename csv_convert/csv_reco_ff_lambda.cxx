#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif

#include "podio/Frame.h"
#include "podio/ROOTReader.h"
#include <edm4eic/ReconstructedParticleCollection.h>

#include <fmt/core.h>
#include <fmt/ostream.h>

#include <TFile.h>

#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>

using namespace edm4eic;

//------------------------------------------------------------------------------
// globals & helpers
//------------------------------------------------------------------------------
int events_limit = -1; // -n  <N>
long total_evt_seen = 0;
long total_lambdas_written = 0;
std::ofstream csv;
bool header_written = false;

//------------------------------------------------------------------------------
// event processing
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int evt_id) {

    // Write header if first time
    if (!header_written) {
        csv << "evt,"
            << "idx,"
            << "pdg,"
            << "charge,"
            << "energy,"
            << "mass,"
            << "px,"
            << "py,"
            << "pz,"
            << "ref_x,"
            << "ref_y,"
            << "ref_z,"
            << "pid_goodness,"
            << "type,"
            << "n_clusters,"
            << "n_tracks,"
            << "n_particles,"
            << "n_particle_ids,"
            << "cov_xx,"
            << "cov_xy,"
            << "cov_xz,"
            << "cov_yy,"
            << "cov_yz,"
            << "cov_zz,"
            << "cov_xt,"
            << "cov_yt,"
            << "cov_zt,"
            << "cov_tt\n";
        header_written = true;
    }

    // Get the reconstructed far-forward lambdas collection
    const auto& ffLambdas = event.get<ReconstructedParticleCollection>("ReconstructedFarForwardZDCLambdas");

    // Process each lambda in the collection
    int lam_idx = 0;
    for (const auto& lam : ffLambdas) {
        const auto mom = lam.getMomentum();
        const auto ref = lam.getReferencePoint();
        const auto cov = lam.getCovMatrix();

        // Calculate the number of associated objects
        const size_t n_clusters = lam.getClusters().size();
        const size_t n_tracks = lam.getTracks().size();
        const size_t n_particles = lam.getParticles().size();
        const size_t n_particleIDs = lam.getParticleIDs().size();

        csv << evt_id << ","
            << lam_idx << ","
            << lam.getPDG() << ","
            << lam.getCharge() << ","
            << lam.getEnergy() << ","
            << lam.getMass() << ","
            << mom.x << ","
            << mom.y << ","
            << mom.z << ","
            << ref.x << ","
            << ref.y << ","
            << ref.z << ","
            << lam.getGoodnessOfPID() << ","
            << lam.getType() << ","
            << n_clusters << ","
            << n_tracks << ","
            << n_particles << ","
            << n_particleIDs << ","
            << cov.xx << ","     //  xx
            << cov.xy << ","     //  xy
            << cov.xz << ","     //  xz
            << cov.xt << ","     //  xt
            << cov.yy << ","     //  yy
            << cov.yz << ","     //  yz
            << cov.yt << ","     //  yt
            << cov.zz << ","     //  zz
            << cov.zt << ","     //  zt
            << cov.tt << "\n";   //  tt

        if (n_particles > 0) {
            auto part1 = lam.getParticles().at(0);
        }

        total_lambdas_written++;
    }
}

//------------------------------------------------------------------------------
// file loop
//------------------------------------------------------------------------------
void process_file(const std::string& fname) {
    podio::ROOTReader rdr;
    try {
        rdr.openFile(fname);
    }
    catch (const std::runtime_error& e) {
        fmt::print(stderr, "Error opening file {}: {}\n", fname, e.what());
        return;
    }

    const auto nEv = rdr.getEntries(podio::Category::Event);
    fmt::print("Processing {} events from {}\n", nEv, fname);

    for (unsigned ie = 0; ie < nEv; ++ie) {
        if (events_limit > 0 && total_evt_seen >= events_limit) return;

        podio::Frame evt(rdr.readNextEntry(podio::Category::Event));
        process_event(evt, total_evt_seen);
        ++total_evt_seen;
    }
}

//------------------------------------------------------------------------------
// main
//------------------------------------------------------------------------------
int main(int argc, char* argv[]) {
    std::vector<std::string> infiles;
    std::string out_name = "reco_ff_lambdas.csv";

    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "-n" && i + 1 < argc) events_limit = std::atoi(argv[++i]);
        else if (a == "-o" && i + 1 < argc) out_name = argv[++i];
        else if (a == "-h" || a == "--help") {
            fmt::print("usage: {} [-n N] [-o file] input1.root [...]\n", argv[0]);
            fmt::print("  -n N     Process only N events (default: all)\n");
            fmt::print("  -o file  Output CSV file (default: reco_ff_lambdas.csv)\n");
            return 0;
        }
        else if (!a.empty() && a[0] != '-') infiles.emplace_back(a);
        else {
            fmt::print(stderr, "unknown option {}\n", a);
            return 1;
        }
    }

    if (infiles.empty()) {
        fmt::print(stderr, "error: no input files\n");
        return 1;
    }

    csv.open(out_name);
    if (!csv) {
        fmt::print(stderr, "error: cannot open output file {}\n", out_name);
        return 1;
    }

    fmt::print("Processing {} file(s)\n", infiles.size());
    for (auto& f : infiles) {
        fmt::print("\n=== Processing file: {} ===\n", f);
        process_file(f);
        if (events_limit > 0 && total_evt_seen >= events_limit) break;
    }

    csv.close();
    fmt::print("\n\nTotal events processed: {}\n", total_evt_seen);
    fmt::print("Total reconstructed far-forward lambdas written: {}\n", total_lambdas_written);
    fmt::print("Output written to: {}\n", out_name);
    return 0;
}

// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt: root -x -l -b -q 'csv_reco_ff_lambda.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void csv_reco_ff_lambda(const char* infile, const char* outfile = "reco_ff_lambdas.csv", int events = -1) {
    fmt::print("'csv_reco_ff_lambda' entry point is used. Arguments:\n");
    fmt::print("  infile:  {}\n", infile);
    fmt::print("  outfile: {}\n", outfile);
    fmt::print("  events:  {} {}\n", events, (events == -1 ? "(process all)" : ""));

    csv.open(outfile);
    if (!csv) {
        fmt::print(stderr, "error: cannot open output file {}\n", outfile);
        return;
    }

    events_limit = events;
    total_evt_seen = 0;
    total_lambdas_written = 0;
    header_written = false;

    process_file(infile);

    csv.close();
    fmt::print("\nTotal events processed: {}\n", total_evt_seen);
    fmt::print("Total reconstructed far-forward lambdas written: {}\n", total_lambdas_written);
    fmt::print("Output written to: {}\n", outfile);
}