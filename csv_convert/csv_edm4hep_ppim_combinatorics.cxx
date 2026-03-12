#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif

// csv_edm4hep_ppim_combinatorics.cxx
//
// Produces a CSV of proton+pion candidate pairs for lambda combinatorics.
//   - Proton candidates: MCParticles leaving >= 2 hits in ForwardRomanPotHits
//   - Pion candidates:   MCParticles leaving >= 3 hits in B0TrackerHits
//   - Each row is one (proton_candidate, pion_candidate) pair per event.
//   - is_true_lam flag marks pairs that are truly p + pi- from a primary Lambda.

#include "podio/Frame.h"
#include "podio/ROOTReader.h"
#include <edm4hep/MCParticleCollection.h>
#include <edm4hep/SimCalorimeterHitCollection.h>
#include <edm4hep/SimTrackerHitCollection.h>
#include <edm4hep/CaloHitContributionCollection.h>
#include <edm4hep/SimTrackerHit.h>

#include <fmt/core.h>
#include <fmt/ostream.h>

#include <TFile.h>

#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <map>
#include <set>

using namespace edm4hep;

//------------------------------------------------------------------------------
// globals & helpers
//------------------------------------------------------------------------------
int events_limit = -1;
long total_evt_seen = 0;
std::ofstream csv;
bool header_written = false;

/**
 * @brief Formats a single particle's data into a comma-separated string.
 */
inline std::string particle_to_csv(const std::optional<MCParticle>& prt) {
    if (!prt) {
        return ",,,,,,,,,,,,,,"; // 14 commas for 15 empty fields
    }
    const auto mom = prt->getMomentum();
    const auto vtx = prt->getVertex();
    const auto ep = prt->getEndpoint();
    return fmt::format("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}",
                                         prt->getObjectID().index, // 01  id
                                         prt->getPDG(), // 02  pdg
                                         prt->getGeneratorStatus(), // 03  gen
                                         prt->getSimulatorStatus(), // 04  sim
                                         mom.x, // 05  px
                                         mom.y, // 06  py
                                         mom.z, // 07  pz
                                         vtx.x, // 08  vx
                                         vtx.y, // 09  vy
                                         vtx.z, // 10  vz
                                         ep.x, // 11  epx
                                         ep.y, // 12  epy
                                         ep.z, // 13  epz
                                         prt->getTime(), // 14  time
                                         prt->getDaughters().size() // 15  nd
    );
}

/**
 * @brief Creates a CSV header string for a particle with a given prefix.
 */
std::string make_particle_header(const std::string& prefix) {
    return fmt::format(""
        "{0}_id,"     // 01
        "{0}_pdg,"    // 02
        "{0}_gen,"    // 03
        "{0}_sim,"    // 04
        "{0}_px,"     // 05
        "{0}_py,"     // 06
        "{0}_pz,"     // 07
        "{0}_vx,"     // 08
        "{0}_vy,"     // 09
        "{0}_vz,"     // 10
        "{0}_epx,"    // 11
        "{0}_epy,"    // 12
        "{0}_epz,"    // 13
        "{0}_time,"   // 14
        "{0}_nd",     // 15 (no trailing comma)
        prefix
    );
}

//------------------------------------------------------------------------------
// Struct to hold a candidate with its first hit position
//------------------------------------------------------------------------------
struct Candidate {
    MCParticle particle;
    double first_hit_x{};
    double first_hit_y{};
    double first_hit_z{};
    int nhits{};
};

//------------------------------------------------------------------------------
// event processing
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int evt_id) {
    const auto& particles = event.get<MCParticleCollection>("MCParticles");

    // ---- Step 1: Find primary Lambda and its daughters (if they exist) -------
    // Build a map of MCParticle by objectID index for quick lookup
    std::map<int, MCParticle> particle_by_id;
    for (const auto& p : particles) {
        particle_by_id[p.getObjectID().index] = p;
    }

    // Find primary Lambda -> p + pi-
    int true_prot_id = -1;   // objectID.index of true proton from Lambda
    int true_pimin_id = -1;  // objectID.index of true pi- from Lambda

    for (const auto& lam : particles) {
        if (lam.getPDG() != 3122) continue;

        auto daughters = lam.getDaughters();
        if (daughters.size() != 2) continue;

        if (daughters.at(0).getPDG() == 2212 && daughters.at(1).getPDG() == -211) {
            true_prot_id = daughters.at(0).getObjectID().index;
            true_pimin_id = daughters.at(1).getObjectID().index;
        } else if (daughters.at(1).getPDG() == 2212 && daughters.at(0).getPDG() == -211) {
            true_prot_id = daughters.at(1).getObjectID().index;
            true_pimin_id = daughters.at(0).getObjectID().index;
        }
        if (true_prot_id >= 0) break; // take the first primary Lambda
    }

    // ---- Step 2: ForwardRomanPotHits -> proton candidates (>= 2 hits) -------
    // Build a map: particle objectID index -> vector of hits
    std::map<int, std::vector<SimTrackerHit>> rp_hits_by_particle;
    try {
        const auto& rp_hits = event.get<edm4hep::SimTrackerHitCollection>("ForwardRomanPotHits");
        for (const auto& hit : rp_hits) {
            if (hit.getParticle().isAvailable()) {
                rp_hits_by_particle[hit.getParticle().getObjectID().index].push_back(hit);
            }
        }
    } catch (...) {}

    // Select proton candidates: particles with >= 2 RomanPot hits
    std::vector<Candidate> proton_candidates;
    for (auto& [pid, hits] : rp_hits_by_particle) {
        if (static_cast<int>(hits.size()) < 2) continue;
        if (particle_by_id.find(pid) == particle_by_id.end()) continue;

        Candidate c;
        c.particle = particle_by_id[pid];
        c.nhits = static_cast<int>(hits.size());
        // First registered hit (first in collection order)
        c.first_hit_x = hits[0].getPosition().x;
        c.first_hit_y = hits[0].getPosition().y;
        c.first_hit_z = hits[0].getPosition().z;
        proton_candidates.push_back(c);
    }

    // ---- Step 3: B0TrackerHits -> pion candidates (>= 3 hits) ---------------
    std::map<int, std::vector<SimTrackerHit>> b0_hits_by_particle;
    try {
        const auto& b0_hits = event.get<edm4hep::SimTrackerHitCollection>("B0TrackerHits");
        for (const auto& hit : b0_hits) {
            if (hit.getParticle().isAvailable()) {
                b0_hits_by_particle[hit.getParticle().getObjectID().index].push_back(hit);
            }
        }
    } catch (...) {}

    // Select pion candidates: particles with >= 3 B0Tracker hits
    std::vector<Candidate> pion_candidates;
    for (auto& [pid, hits] : b0_hits_by_particle) {
        if (static_cast<int>(hits.size()) < 3) continue;
        if (particle_by_id.find(pid) == particle_by_id.end()) continue;

        Candidate c;
        c.particle = particle_by_id[pid];
        c.nhits = static_cast<int>(hits.size());
        c.first_hit_x = hits[0].getPosition().x;
        c.first_hit_y = hits[0].getPosition().y;
        c.first_hit_z = hits[0].getPosition().z;
        pion_candidates.push_back(c);
    }

    // ---- Step 4: B0ECalHits -> flag pion candidates with ecal contribution --
    std::map<int, bool> pion_has_ecal;            // particle id -> has contribution
    std::map<int, double> pion_ecal_first_x;
    std::map<int, double> pion_ecal_first_y;
    std::map<int, double> pion_ecal_first_z;

    // Initialize flags for all pion candidates
    for (const auto& pc : pion_candidates) {
        int pid = pc.particle.getObjectID().index;
        pion_has_ecal[pid] = false;
    }

    try {
        const auto& ecal_hits = event.get<edm4hep::SimCalorimeterHitCollection>("B0ECalHits");
        for (const auto& hit : ecal_hits) {
            for (const auto& contrib : hit.getContributions()) {
                if (!contrib.getParticle().isAvailable()) continue;
                int cid = contrib.getParticle().getObjectID().index;
                if (pion_has_ecal.find(cid) != pion_has_ecal.end()) {
                    if (!pion_has_ecal[cid]) {
                        // First ecal hit for this pion candidate - save position
                        pion_has_ecal[cid] = true;
                        pion_ecal_first_x[cid] = hit.getPosition().x;
                        pion_ecal_first_y[cid] = hit.getPosition().y;
                        pion_ecal_first_z[cid] = hit.getPosition().z;
                    }
                }
            }
        }
    } catch (...) {}

    // ---- Step 5 & 6: Write combinatoric pairs to CSV ------------------------
    if (proton_candidates.empty() || pion_candidates.empty()) return;

    // Write header on first output
    if (!header_written) {
        csv << "evt,is_true_lam,"
            << make_particle_header("pi") << ","
            << "pi_nhits_b0,"
            << "pi_first_b0_x,pi_first_b0_y,pi_first_b0_z,"
            << "pi_ecal_contrib,"
            << "pi_first_ecal_x,pi_first_ecal_y,pi_first_ecal_z,"
            << make_particle_header("p") << ","
            << "p_nhits_rp,"
            << "p_first_rp_x,p_first_rp_y,p_first_rp_z"
            << "\n";
        header_written = true;
    }

    // Each row is a (proton_candidate, pion_candidate) pair
    for (const auto& pc : proton_candidates) {
        int pc_id = pc.particle.getObjectID().index;
        for (const auto& pic : pion_candidates) {
            int pic_id = pic.particle.getObjectID().index;

            // is_true_lam: both candidates match the true Lambda daughters
            bool is_true = (pc_id == true_prot_id && pic_id == true_pimin_id);

            // Pion MCParticle info
            std::optional<MCParticle> pi_opt = pic.particle;
            // Proton MCParticle info
            std::optional<MCParticle> p_opt = pc.particle;

            // Ecal info for pion
            bool has_ecal = pion_has_ecal.count(pic_id) && pion_has_ecal[pic_id];
            double ecal_x = has_ecal ? pion_ecal_first_x[pic_id] : 0.0;
            double ecal_y = has_ecal ? pion_ecal_first_y[pic_id] : 0.0;
            double ecal_z = has_ecal ? pion_ecal_first_z[pic_id] : 0.0;

            csv << evt_id << "," << (is_true ? 1 : 0) << ","
                << particle_to_csv(pi_opt) << ","
                << pic.nhits << ","
                << pic.first_hit_x << "," << pic.first_hit_y << "," << pic.first_hit_z << ","
                << (has_ecal ? 1 : 0) << ","
                << ecal_x << "," << ecal_y << "," << ecal_z << ","
                << particle_to_csv(p_opt) << ","
                << pc.nhits << ","
                << pc.first_hit_x << "," << pc.first_hit_y << "," << pc.first_hit_z
                << "\n";
        }
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
    std::string out_name = "ppim_combinatorics.csv";

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

    for (auto& f : infiles) {
        process_file(f);
        if (events_limit > 0 && total_evt_seen >= events_limit) break;
    }

    csv.close();
    fmt::print("Wrote combinatorics data for {} events to {}\n", total_evt_seen, out_name);

    return 0;
}

// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// root -x -l -b -q 'csv_edm4hep_ppim_combinatorics.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void csv_edm4hep_ppim_combinatorics(const char* infile, const char* outfile, int events = -1)
{
    fmt::print("'csv_edm4hep_ppim_combinatorics' entry point is used.\n");

    csv.open(outfile);
    if (!csv) {
        fmt::print(stderr, "error: cannot open output file {}\n", outfile);
        exit(1);
    }

    events_limit = events;
    process_file(infile);

    csv.close();
    fmt::print("\nWrote combinatorics data for {} events to {}\n", total_evt_seen, outfile);
}
