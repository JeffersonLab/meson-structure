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

/**
 * @brief Formats a single reconstructed particle's data into a comma-separated string.
 * @param p A pointer to the ReconstructedParticle. If nullptr, returns empty fields.
 * @return A std::string containing the formatted particle data.
 */
inline std::string reco_particle_to_csv(const ReconstructedParticle* p) {
    if (!p) {
        return ",,,,,,,,,,,,,,,,,,,,,,,,,"; // 25 commas for 26 empty fields
    }
    const auto mom = p->getMomentum();
    const auto ref = p->getReferencePoint();
    const auto cov = p->getCovMatrix();

    return fmt::format("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}",
        p->getObjectID().index,           // 01 id
        p->getPDG(),                     // 02 pdg
        p->getCharge(),                  // 03 charge
        p->getEnergy(),                  // 04 energy
        p->getMass(),                    // 05 mass
        mom.x,                           // 06 px
        mom.y,                           // 07 py
        mom.z,                           // 08 pz
        ref.x,                           // 09 ref_x
        ref.y,                           // 10 ref_y
        ref.z,                           // 11 ref_z
        p->getGoodnessOfPID(),           // 12 pid_goodness
        p->getType(),                    // 13 type
        p->getClusters().size(),         // 14 n_clusters
        p->getTracks().size(),           // 15 n_tracks
        p->getParticles().size(),        // 16 n_particles
        p->getParticleIDs().size(),      // 17 n_particle_ids
        cov.xx,                          // 18 cov_xx
        cov.xy,                          // 19 cov_xy
        cov.xz,                          // 20 cov_xz
        cov.yy,                          // 21 cov_yy
        cov.yz,                          // 22 cov_yz
        cov.zz,                          // 23 cov_zz
        cov.xt,                          // 24 cov_xt
        cov.yt,                          // 25 cov_yt
        cov.zt,                          // 26 cov_zt
        cov.tt                           // 27 cov_tt
    );
}

/**
 * @brief Creates a CSV header string for a reconstructed particle with a given prefix.
 * @param prefix The prefix for each column name (e.g., "lam").
 * @return A string containing the formatted CSV header.
 */
std::string make_reco_particle_header(const std::string& prefix) {
    return fmt::format(""
        "{0}_id,"              // 01 id
        "{0}_pdg,"             // 02 pdg
        "{0}_charge,"          // 03 charge
        "{0}_energy,"          // 04 energy
        "{0}_mass,"            // 05 mass
        "{0}_px,"              // 06 px
        "{0}_py,"              // 07 py
        "{0}_pz,"              // 08 pz
        "{0}_ref_x,"           // 09 ref_x
        "{0}_ref_y,"           // 10 ref_y
        "{0}_ref_z,"           // 11 ref_z
        "{0}_pid_goodness,"    // 12 pid_goodness
        "{0}_type,"            // 13 type
        "{0}_n_clusters,"      // 14 n_clusters
        "{0}_n_tracks,"        // 15 n_tracks
        "{0}_n_particles,"     // 16 n_particles
        "{0}_n_particle_ids,"  // 17 n_particle_ids
        "{0}_cov_xx,"          // 18 cov_xx
        "{0}_cov_xy,"          // 19 cov_xy
        "{0}_cov_xz,"          // 20 cov_xz
        "{0}_cov_yy,"          // 21 cov_yy
        "{0}_cov_yz,"          // 22 cov_yz
        "{0}_cov_zz,"          // 23 cov_zz
        "{0}_cov_xt,"          // 24 cov_xt
        "{0}_cov_yt,"          // 25 cov_yt
        "{0}_cov_zt,"          // 26 cov_zt
        "{0}_cov_tt",          // 27 cov_tt (no trailing comma)
        prefix
    );
}

//------------------------------------------------------------------------------
// event processing
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int evt_id) {

    // Get the reconstructed far-forward lambdas collection
    const auto& ffLambdas = event.get<ReconstructedParticleCollection>("ReconstructedFarForwardZDCLambdas");

    // Process each lambda in the collection
    for (const auto& lam : ffLambdas) {

        // Get daughter particles
        const auto& daughters = lam.getParticles();

        // Look for neutron + 2 gammas decay
        const ReconstructedParticle* neut = nullptr;
        const ReconstructedParticle* gam1 = nullptr;
        const ReconstructedParticle* gam2 = nullptr;

        int n_neutrons = 0;
        int n_gammas = 0;

        for (const auto& d : daughters) {
            if (d.getPDG() == 2112) { // neutron
                neut = &d;
                n_neutrons++;
            } else if (d.getPDG() == 22) { // gamma
                if (!gam1) {
                    gam1 = &d;
                } else if (!gam2) {
                    gam2 = &d;
                }
                n_gammas++;
            }
        }

        // Only process if we have exactly 1 neutron and 2 gammas
        if (n_neutrons != 1 || n_gammas != 2) {
            continue;
        }

        // Write header if first time
        if (!header_written) {
            csv << "event,"
                << make_reco_particle_header("lam") << ','
                << make_reco_particle_header("neut") << ','
                << make_reco_particle_header("gam1") << ','
                << make_reco_particle_header("gam2") << '\n';
            header_written = true;
        }

        // Write the data
        csv << evt_id << ','
            << reco_particle_to_csv(&lam) << ','
            << reco_particle_to_csv(neut) << ','
            << reco_particle_to_csv(gam1) << ','
            << reco_particle_to_csv(gam2) << '\n';

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
    std::string out_name = "reco_ff_lambdas_ngamgam.csv";

    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "-n" && i + 1 < argc) events_limit = std::atoi(argv[++i]);
        else if (a == "-o" && i + 1 < argc) out_name = argv[++i];
        else if (a == "-h" || a == "--help") {
            fmt::print("usage: {} [-n N] [-o file] input1.root [...]\n", argv[0]);
            fmt::print("  -n N     Process only N events (default: all)\n");
            fmt::print("  -o file  Output CSV file (default: reco_ff_lambdas_ngamgam.csv)\n");
            fmt::print("\nThis program extracts Lambda -> neutron + gamma + gamma decays\n");
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
    fmt::print("Extracting Lambda -> neutron + gamma + gamma decays only\n");

    for (auto& f : infiles) {
        fmt::print("\n=== Processing file: {} ===\n", f);
        process_file(f);
        if (events_limit > 0 && total_evt_seen >= events_limit) break;
    }

    csv.close();
    fmt::print("\n\nTotal events processed: {}\n", total_evt_seen);
    fmt::print("Total Lambda -> n + gamma + gamma decays written: {}\n", total_lambdas_written);
    fmt::print("Output written to: {}\n", out_name);
    return 0;
}

// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt: root -x -l -b -q 'csv_reco_ff_lambda.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void csv_reco_ff_lambda(const char* infile, const char* outfile = "reco_ff_lambdas_ngamgam.csv", int events = -1) {
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
    fmt::print("Total Lambda -> n + gamma + gamma decays written: {}\n", total_lambdas_written);
    fmt::print("Output written to: {}\n", outfile);
}