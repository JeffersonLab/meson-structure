#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif

// lambdas_to_csv.cxx
#include "podio/Frame.h"
#include "podio/ROOTReader.h"
#include <edm4hep/MCParticleCollection.h>

#include <fmt/core.h>
#include <fmt/ostream.h>

#include <TFile.h>

#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>

using namespace edm4hep;

//------------------------------------------------------------------------------
// globals & helpers
//------------------------------------------------------------------------------
int events_limit = -1; // -n  <N>
long total_evt_seen = 0;
std::ofstream csv;
bool header_written = false;

struct Vec3 {
    double x{}, y{}, z{};
};

/**
 * @brief Formats a single particle's data into a comma-separated string.
 * @param p A pointer to the MCParticle. If nullptr, returns empty fields.
 * @return A std::string containing the formatted particle data.
 */
inline std::string particle_to_csv(const MCParticle* p) {
    if (!p) {
        return ",,,,,,,,,,,,,,"; // 14 commas for 15 empty fields
    }
    const auto mom = p->getMomentum();
    const auto vtx = p->getVertex();
    const auto ep = p->getEndpoint();
    return fmt::format("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}",
                                         p->getObjectID().index, // 01  id
                                         p->getPDG(), // 02  pdg
                                         p->getGeneratorStatus(), // 03  gen
                                         p->getSimulatorStatus(), // 04  sim
                                         mom.x, // 05  px
                                         mom.y, // 06  py
                                         mom.z, // 07  pz
                                         vtx.x, // 08  vx
                                         vtx.y, // 09  vy
                                         vtx.z, // 10  vz
                                         ep.x, // 11  epx
                                         ep.y, // 12  epy
                                         ep.z, // 13  epz
                                         p->getTime(), // 14  time
                                         p->getDaughters().size() // 15  nd
    );
}

/**
 * @brief Creates a CSV header string for a particle with a given prefix.
 * @param prefix The prefix for each column name (e.g., "lam").
 * @return A string containing the formatted CSV header.
 */
std::string make_particle_header(const std::string&prefix) {
    return fmt::format(""
        "{0}_id,"     // 01  id
        "{0}_pdg,"    // 02  pdg
        "{0}_gen,"    // 03  gen
        "{0}_sim,"    // 04  sim
        "{0}_px,"     // 05  px
        "{0}_py,"     // 06  py
        "{0}_pz,"     // 07  pz
        "{0}_vx,"     // 08  vx
        "{0}_vy,"     // 09  vy
        "{0}_vz,"     // 10  vz
        "{0}_epx,"    // 11  epx
        "{0}_epy,"    // 12  epy
        "{0}_epz,"    // 13  epz
        "{0}_time,"   // 14  time
        "{0}_nd",     // 15  nd (no trailing comma)
        prefix
    );
}

//------------------------------------------------------------------------------
// event processing
//------------------------------------------------------------------------------
void process_event(const podio::Frame&event, int evt_id) {
    const auto&parts = event.get<MCParticleCollection>("MCParticles");

    for (const auto&lam: parts) {
        if (lam.getPDG() != 3122) continue; // not Λ⁰

        const auto&dtrs = lam.getDaughters();
        // if (dtrs.size() < 2) continue; // malformed

        // -----------------------------------------------------------------
        // classify decay channel & pick final-state pointers
        // -----------------------------------------------------------------
        const MCParticle *prot = nullptr, *pimin = nullptr, *neut = nullptr,
                *pi0 = nullptr, *gam1 = nullptr, *gam2 = nullptr;

        for (const auto&d: dtrs) {
            switch (d.getPDG()) {
                case 2212: prot = &d;
                    break; // p
                case -211: pimin = &d;
                    break; // π-
                case 2112: neut = &d;
                    break; // n
                case 111: pi0 = &d;
                    break; // π0
            }
        }

        int channel = -1;
        if (prot && pimin) {
            channel = 1; // Charged channel: Λ⁰ → p + π⁻
        }
        else if (neut && pi0) {
            channel = 2; // Neutral channel: Λ⁰ → n + π⁰

            // Use iterators to get stable addresses for daughter particles
            const auto&pi0_dtrs = pi0->getDaughters();
            auto it = pi0_dtrs.begin();
            if (it != pi0_dtrs.end()) {
                gam1 = &(*it); // First photon
                ++it;
                if (it != pi0_dtrs.end()) {
                    gam2 = &(*it); // Second photon
                }
            }
        }
        // if (channel == -1) continue; // skip rare channels

        // -----------------------------------------------------------------
        // output
        // -----------------------------------------------------------------
        if (!header_written) {
            csv << "event,"
                    << make_particle_header("lam") << ','
                    << make_particle_header("prot") << ','
                    << make_particle_header("pimin") << ','
                    << make_particle_header("neut") << ','
                    << make_particle_header("pizero") << ','
                    << make_particle_header("gamone") << ','
                    << make_particle_header("gamtwo") << '\n';
            header_written = true;
        }

        // Call the new string-returning function to build the output line
        csv << evt_id << ','
                << particle_to_csv(&lam) << ','
                << particle_to_csv(prot) << ','
                << particle_to_csv(pimin) << ','
                << particle_to_csv(neut) << ','
                << particle_to_csv(pi0) << ','
                << particle_to_csv(gam1) << ','
                << particle_to_csv(gam2) << '\n';
    }
}

//------------------------------------------------------------------------------
// file loop
//------------------------------------------------------------------------------
void process_file(const std::string&fname) {
    podio::ROOTReader rdr;
    try {
        rdr.openFile(fname);
    }
    catch (const std::runtime_error&e) {
        fmt::print(stderr, "Error opening file {}: {}\n", fname, e.what());
        return;
    }

    const auto nEv = rdr.getEntries(podio::Category::Event);

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
    std::string out_name = "mcpart_lambdas.csv";

    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "-n" && i + 1 < argc) events_limit = std::atoi(argv[++i]);
        else if (a == "-o" && i + 1 < argc) out_name = argv[++i];
        else if (a == "-h" || a == "--help") {
            fmt::print("usage: {} [-n N] [-o file] input1.root [...]\n", argv[0]);
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

    for (auto&f: infiles) {
        process_file(f);
        if (events_limit > 0 && total_evt_seen >= events_limit) break;
    }

    csv.close();
    fmt::print("Wrote data for {} Λ decays to {}\n", total_evt_seen, out_name);
    return 0;
}


// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt:  root -x -l -b -q 'csv_mcpart_lambda.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void csv_mcpart_lambda(const char* infile, const char* outfile, int events = -1)
{
    fmt::print("'csv_mcpart_lambda' entry point is used. Arguments:\n");
    fmt::print("  infile:  {}\n", infile);
    fmt::print("  outfile: {}\n", outfile);
    fmt::print("  events:  {} {}\n", events, (events == -1 ? "(process all)" : ""));

    csv.open(outfile);
    if (!csv) {
        fmt::print(stderr, "error: cannot open output file {}\n", outfile);
        exit(1);
    }

    events_limit = events;                // reuse the global controls
    process_file(infile);

    csv.close();
    fmt::print("\nWrote data for {} Λ decays to {}\n", total_evt_seen, outfile);
}