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
#include <edm4hep/SimCalorimeterHitCollection.h>
#include <edm4hep/CaloHitContributionCollection.h>

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

// Global counters for statistics
struct DetectorStats {
    long total_lambdas = 0;
    long total_npi0_decays = 0;  // ALL n+pi0 decays
    long npi0_with_observable_gammas = 0;  // n+pi0 where pi0 decayed to 2 gammas
    long neut_in_any_hcal = 0;
    long neut_and_both_gammas = 0;
    long all_three_detected = 0;

    // Per-detector counts for neutrons
    long neut_zdc_hcal = 0;
    long neut_pins_hcal = 0;
    long neut_lf_hcal = 0;

    // Per-detector counts for gammas
    long gam1_zdc_ecal = 0;
    long gam2_zdc_ecal = 0;
    long gam1_b0_ecal = 0;
    long gam2_b0_ecal = 0;
    long gam1_ecalp = 0;
    long gam2_ecalp = 0;
    long gam1_ecalp_ins = 0;
    long gam2_ecalp_ins = 0;

    // All 3 particle per detector
    long gam_neut_in_zdc = 0;

    // When all three particles detected
    long all3_neut_zdc_hcal = 0;
    long all3_neut_pins_hcal = 0;
    long all3_neut_lf_hcal = 0;
    long all3_gam1_zdc_ecal = 0;
    long all3_gam2_zdc_ecal = 0;
    long all3_gam1_b0_ecal = 0;
    long all3_gam2_b0_ecal = 0;
    long all3_gam1_ecalp = 0;
    long all3_gam2_ecalp = 0;
    long all3_gam1_ecalp_ins = 0;
    long all3_gam2_ecalp_ins = 0;

    // Decay channel statistics
    long decay_not_decayed = 0;
    long decay_p_piminus = 0;
    long decay_shower = 0;
    long decay_other = 0;
};

DetectorStats stats;

struct Vec3 {
    double x{}, y{}, z{};
};

/**
 * @brief Formats a single particle's data into a comma-separated string.
 * @param prt A pointer to the MCParticle. If nullptr, returns empty fields.
 * @return A std::string containing the formatted particle data.
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

bool has_particle_hits(const auto& hit_collection, const MCParticle& particle,
                       const std::string& detector_name, const std::string& particle_name) {
    for (const auto& hit: hit_collection) {
        for (const auto& contrib: hit.getContributions()) {
            if (contrib.getParticle().getObjectID() == particle.getObjectID()) {
                fmt::print("{} hit: id={:<5} z={:<10.2f} contrib={} is of {} \n",
                          detector_name, hit.id().index, hit.getPosition().z,
                          hit.contributions_size(), particle_name);
                return true;
            }
        }
    }
    return false;
}

struct DetectionFlags {
    bool neut_zdc_hcal = false;
    bool neut_pins_hcal = false;
    bool neut_lf_hcal = false;
    bool gam1_zdc_ecal = false;
    bool gam2_zdc_ecal = false;
    bool gam1_b0_ecal = false;
    bool gam2_b0_ecal = false;
    bool gam1_ecalp = false;
    bool gam2_ecalp = false;
    bool gam1_ecalp_ins = false;
    bool gam2_ecalp_ins = false;
};

DetectionFlags process_calo_hits_npi0(const podio::Frame& event, const MCParticle& neut,
                            const MCParticle& gam1, const MCParticle& gam2) {
    DetectionFlags flags;

    // Check for gamma particles in various ECALs
    const auto& zdc_ecal_hits = event.get<edm4hep::SimCalorimeterHitCollection>("EcalFarForwardZDCHits");
    flags.gam1_zdc_ecal = has_particle_hits(zdc_ecal_hits, gam1, "EcalFarForwardZDC", "gam1");
    flags.gam2_zdc_ecal = has_particle_hits(zdc_ecal_hits, gam2, "EcalFarForwardZDC", "gam2");

    const auto& b0_hits = event.get<edm4hep::SimCalorimeterHitCollection>("B0ECalHits");
    flags.gam1_b0_ecal = has_particle_hits(b0_hits, gam1, "B0ECal", "gam1");
    flags.gam2_b0_ecal = has_particle_hits(b0_hits, gam2, "B0ECal", "gam2");

    const auto& ecalp_hits = event.get<edm4hep::SimCalorimeterHitCollection>("EcalEndcapPHits");
    flags.gam1_ecalp = has_particle_hits(ecalp_hits, gam1, "EcalEndcapP", "gam1");
    flags.gam2_ecalp = has_particle_hits(ecalp_hits, gam2, "EcalEndcapP", "gam2");

    const auto& ecalpins_hits = event.get<edm4hep::SimCalorimeterHitCollection>("EcalEndcapPInsertHits");
    flags.gam1_ecalp_ins = has_particle_hits(ecalpins_hits, gam1, "EcalEndcapPInsert", "gam1");
    flags.gam2_ecalp_ins = has_particle_hits(ecalpins_hits, gam2, "EcalEndcapPInsert", "gam2");

    // Check for neutron in various HCALs
    const auto& zdc_hcal_hits = event.get<edm4hep::SimCalorimeterHitCollection>("HcalFarForwardZDCHits");
    flags.neut_zdc_hcal = has_particle_hits(zdc_hcal_hits, neut, "HcalFarForwardZDC", "NEUTRON");

    const auto& pins_hcal_hits = event.get<edm4hep::SimCalorimeterHitCollection>("HcalEndcapPInsertHits");
    flags.neut_pins_hcal = has_particle_hits(pins_hcal_hits, neut, "HcalEndcapPInsert", "NEUTRON");

    const auto& lf_hcal_hits = event.get<edm4hep::SimCalorimeterHitCollection>("LFHCALHits");
    flags.neut_lf_hcal = has_particle_hits(lf_hcal_hits, neut, "LFHCAL", "NEUTRON");

    // Check if neutron in any HCAL
    bool neut_in_any = flags.neut_zdc_hcal || flags.neut_pins_hcal || flags.neut_lf_hcal;
    if (neut_in_any) stats.neut_in_any_hcal++;

    // Check if both gammas detected anywhere
    bool gam1_detected = flags.gam1_zdc_ecal || flags.gam1_b0_ecal || flags.gam1_ecalp || flags.gam1_ecalp_ins;
    bool gam2_detected = flags.gam2_zdc_ecal || flags.gam2_b0_ecal || flags.gam2_ecalp || flags.gam2_ecalp_ins;

    if (neut_in_any && gam1_detected && gam2_detected) {
        stats.neut_and_both_gammas++;
    }

    // Update per-detector counts
    if (flags.neut_zdc_hcal) stats.neut_zdc_hcal++;
    if (flags.neut_pins_hcal) stats.neut_pins_hcal++;
    if (flags.neut_lf_hcal) stats.neut_lf_hcal++;

    if (flags.gam1_zdc_ecal) stats.gam1_zdc_ecal++;
    if (flags.gam2_zdc_ecal) stats.gam2_zdc_ecal++;
    if (flags.gam1_b0_ecal) stats.gam1_b0_ecal++;
    if (flags.gam2_b0_ecal) stats.gam2_b0_ecal++;
    if (flags.gam1_ecalp) stats.gam1_ecalp++;
    if (flags.gam2_ecalp) stats.gam2_ecalp++;
    if (flags.gam1_ecalp_ins) stats.gam1_ecalp_ins++;
    if (flags.gam2_ecalp_ins) stats.gam2_ecalp_ins++;

    // Check if all three particles detected
    if (neut_in_any && gam1_detected && gam2_detected) {
        stats.all_three_detected++;

        if (flags.neut_zdc_hcal && flags.gam1_zdc_ecal && flags.gam2_zdc_ecal) {
            stats.gam_neut_in_zdc++;
        }

        // Update all3 per-detector counts
        if (flags.neut_zdc_hcal) stats.all3_neut_zdc_hcal++;
        if (flags.neut_pins_hcal) stats.all3_neut_pins_hcal++;
        if (flags.neut_lf_hcal) stats.all3_neut_lf_hcal++;

        if (flags.gam1_zdc_ecal) stats.all3_gam1_zdc_ecal++;
        if (flags.gam2_zdc_ecal) stats.all3_gam2_zdc_ecal++;
        if (flags.gam1_b0_ecal) stats.all3_gam1_b0_ecal++;
        if (flags.gam2_b0_ecal) stats.all3_gam2_b0_ecal++;
        if (flags.gam1_ecalp) stats.all3_gam1_ecalp++;
        if (flags.gam2_ecalp) stats.all3_gam2_ecalp++;
        if (flags.gam1_ecalp_ins) stats.all3_gam1_ecalp_ins++;
        if (flags.gam2_ecalp_ins) stats.all3_gam2_ecalp_ins++;
    }

    return flags;
}

void print_stats() {
    fmt::print("\n=== DETECTION STATISTICS ===\n");
    fmt::print("Total first lambdas: {}\n", stats.total_lambdas);
    fmt::print("Lambda decay channels:\n");
    fmt::print("  Not decayed: {} ({:.2f}%)\n",
               stats.decay_not_decayed,
               stats.total_lambdas > 0 ? 100.0 * stats.decay_not_decayed / stats.total_lambdas : 0.0);
    fmt::print("  p + π⁻: {} ({:.2f}%)\n",
               stats.decay_p_piminus,
               stats.total_lambdas > 0 ? 100.0 * stats.decay_p_piminus / stats.total_lambdas : 0.0);
    fmt::print("  n + π⁰: {} ({:.2f}%)\n",
               stats.total_npi0_decays,
               stats.total_lambdas > 0 ? 100.0 * stats.total_npi0_decays / stats.total_lambdas : 0.0);
    fmt::print("  Shower/recharge: {} ({:.2f}%)\n",
               stats.decay_shower,
               stats.total_lambdas > 0 ? 100.0 * stats.decay_shower / stats.total_lambdas : 0.0);
    fmt::print("  Other: {} ({:.2f}%)\n",
               stats.decay_other,
               stats.total_lambdas > 0 ? 100.0 * stats.decay_other / stats.total_lambdas : 0.0);

    fmt::print("\n--- n+π⁰ Detection Analysis ---\n");
    fmt::print("Total n+π⁰ decays: {}\n", stats.total_npi0_decays);
    fmt::print("n+π⁰ with observable γγ: {} ({:.2f}%)\n",
               stats.npi0_with_observable_gammas,
               stats.total_npi0_decays > 0 ? 100.0 * stats.npi0_with_observable_gammas / stats.total_npi0_decays : 0.0);

    if (stats.npi0_with_observable_gammas > 0) {
        fmt::print("\nOf the {} n+π⁰ decays with observable γγ:\n", stats.npi0_with_observable_gammas);
        fmt::print("  Neutron in any HCAL: {} ({:.2f}%)\n",
                   stats.neut_in_any_hcal,
                   100.0 * stats.neut_in_any_hcal / stats.npi0_with_observable_gammas);
        fmt::print("  Neutron + both gammas detected: {} ({:.2f}%)\n",
                   stats.neut_and_both_gammas,
                   100.0 * stats.neut_and_both_gammas / stats.npi0_with_observable_gammas);

        fmt::print("  Neutron + both gammas in ZDC: {} ({:.2f}%)\n", stats.gam_neut_in_zdc, 100.0 * stats.gam_neut_in_zdc / stats.npi0_with_observable_gammas);

        fmt::print("\n--- Per-Detector Counts (Observable γγ Events) ---\n");
        fmt::print("Neutron detections:\n");
        fmt::print("  HcalFarForwardZDC: {}\n", stats.neut_zdc_hcal);
        fmt::print("  HcalEndcapPInsert: {}\n", stats.neut_pins_hcal);
        fmt::print("  LFHCAL: {}\n", stats.neut_lf_hcal);

        fmt::print("Gamma1 detections:\n");
        fmt::print("  EcalFarForwardZDC: {}\n", stats.gam1_zdc_ecal);
        fmt::print("  B0ECal: {}\n", stats.gam1_b0_ecal);
        fmt::print("  EcalEndcapP: {}\n", stats.gam1_ecalp);
        fmt::print("  EcalEndcapPInsert: {}\n", stats.gam1_ecalp_ins);

        fmt::print("Gamma2 detections:\n");
        fmt::print("  EcalFarForwardZDC: {}\n", stats.gam2_zdc_ecal);
        fmt::print("  B0ECal: {}\n", stats.gam2_b0_ecal);
        fmt::print("  EcalEndcapP: {}\n", stats.gam2_ecalp);
        fmt::print("  EcalEndcapPInsert: {}\n", stats.gam2_ecalp_ins);

        if (stats.all_three_detected > 0) {
            fmt::print("\n--- Per-Detector Counts (All 3 Particles Detected) ---\n");
            fmt::print("Total events with all 3 particles: {}\n", stats.all_three_detected);
            fmt::print("Neutron detections:\n");
            fmt::print("  HcalFarForwardZDC: {}\n", stats.all3_neut_zdc_hcal);
            fmt::print("  HcalEndcapPInsert: {}\n", stats.all3_neut_pins_hcal);
            fmt::print("  LFHCAL: {}\n", stats.all3_neut_lf_hcal);

            fmt::print("Gamma1 detections:\n");
            fmt::print("  EcalFarForwardZDC: {}\n", stats.all3_gam1_zdc_ecal);
            fmt::print("  B0ECal: {}\n", stats.all3_gam1_b0_ecal);
            fmt::print("  EcalEndcapP: {}\n", stats.all3_gam1_ecalp);
            fmt::print("  EcalEndcapPInsert: {}\n", stats.all3_gam1_ecalp_ins);

            fmt::print("Gamma2 detections:\n");
            fmt::print("  EcalFarForwardZDC: {}\n", stats.all3_gam2_zdc_ecal);
            fmt::print("  B0ECal: {}\n", stats.all3_gam2_b0_ecal);
            fmt::print("  EcalEndcapP: {}\n", stats.all3_gam2_ecalp);
            fmt::print("  EcalEndcapPInsert: {}\n", stats.all3_gam2_ecalp_ins);
        }
    }
    fmt::print("=============================\n");
}

//------------------------------------------------------------------------------
// event processing
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int evt_id) {
    const auto& particles = event.get<MCParticleCollection>("MCParticles");

    // The first lambda in event should be generated spectator lambda
    bool is_first_lambda = true;

    for (const auto& lam: particles) {
        if (lam.getPDG() != 3122) continue; // not Λ⁰

        // Count first lambdas
        stats.total_lambdas++;

        int decay_type = 4; // 0 - not decayed, 1 - p-piminus, 2 - n-pizero, 3 - shower/recharge, 4 - other (what?)

        // -----------------------------------------------------------------
        // classify decay channel & pick final-state pointers
        // -----------------------------------------------------------------
        std::optional<MCParticle> prot, pimin, neut, pi0, gam1, gam2;

        auto daughters = lam.getDaughters();

        if (daughters.size() == 0) {
            decay_type = 0;     // didn't decayed. Maybe went out of the volume
            stats.decay_not_decayed++;
        } else if (daughters.size() == 2) {
            if (daughters.at(0).getPDG() == 2212 && daughters.at(1).getPDG() == -211) {
                decay_type = 1; // p-piminus
                prot = daughters.at(0);
                pimin = daughters.at(1);
            }

            if (daughters.at(1).getPDG() == 2212 && daughters.at(0).getPDG() == -211) {
                decay_type = 1; // p-piminus
                prot = daughters.at(1);
                pimin = daughters.at(0);
            }

            if (daughters.at(0).getPDG() == 2112 && daughters.at(1).getPDG() == 111) {
                decay_type = 2; // n-pizero
                neut = daughters.at(0);
                pi0 = daughters.at(1);
            }

            if (daughters.at(1).getPDG() == 2112 && daughters.at(0).getPDG() == 111) {
                decay_type = 2; // n-pizero
                neut = daughters.at(1);
                pi0 = daughters.at(0);

            }
        } else {
            // ... so ... it is complicated...
            bool is_shower = false;
            for (const auto& daughter: daughters) {
                if (daughter.getPDG() == 3122) {
                    decay_type = 3;     // It is recharging lambda - shower
                    is_shower = true;
                    stats.decay_shower++;
                    break;
                }
            }
            if (!is_shower) {
                stats.decay_other++;
            }
        }

        // For neutron+pi0 we need to capture pi0 decay products if exists
        if (neut && pi0) {
            // For Geant4 you don't know how pi0 was decayed.
            // I.e. it doesn't go against physics but it can not save particle if it goes nowhere
            if (pi0->getDaughters().size() > 0) {
                gam1 = pi0->getDaughters().at(0);
            }

            if (pi0->getDaughters().size() > 1) {
                gam2 = pi0->getDaughters().at(1);
            }
            stats.total_npi0_decays++;  // Count ALL n+pi0 decays
        }

        if (prot && pimin) {
            stats.decay_p_piminus++;
        }

        // Sanity check!
        if (neut && prot) {
            fmt::print("(!!!) WARNING: I see neut && prot at evt_id={}\n", evt_id);
        }

        // Initialize detection flags with default values
        DetectionFlags flags;

        // Process hits only if this is first lambda with n+pi0 decay AND observable gammas
        if (neut && gam1 && gam2) {
            // Increment counter for n+pi0 decays with observable gammas
            stats.npi0_with_observable_gammas++;

            fmt::print("---------------------------------------\n looking hits at event {}\n", evt_id);
            flags = process_calo_hits_npi0(event, neut.value(), gam1.value(), gam2.value());
        }

        // -----------------------------------------------------------------
        // output
        // -----------------------------------------------------------------
        if (!header_written) {
            csv << "event,lam_is_first,lam_decay,"
                    << make_particle_header("lam") << ','
                    << make_particle_header("prot") << ','
                    << make_particle_header("pimin") << ','
                    << make_particle_header("neut") << ','
                    << make_particle_header("pizero") << ','
                    << make_particle_header("gamone") << ','
                    << make_particle_header("gamtwo") << ','
                    << "neut_zdc_hcal,neut_pins_hcal,neut_lf_hcal,"
                    << "gam1_zdc_ecal,gam2_zdc_ecal,gam1_b0_ecal,gam2_b0_ecal,"
                    << "gam1_ecalp,gam2_ecalp,gam1_ecalp_ins,gam2_ecalp_ins"
                    << '\n';
            header_written = true;
        }

        // Call the new string-returning function to build the output line
        csv     << evt_id << ','
                << static_cast<int>(is_first_lambda) << ','
                << decay_type << ','
                << particle_to_csv(lam) << ','
                << particle_to_csv(prot) << ','
                << particle_to_csv(pimin) << ','
                << particle_to_csv(neut) << ','
                << particle_to_csv(pi0) << ','
                << particle_to_csv(gam1) << ','
                << particle_to_csv(gam2) << ','
                << flags.neut_zdc_hcal << ','
                << flags.neut_pins_hcal << ','
                << flags.neut_lf_hcal << ','
                << flags.gam1_zdc_ecal << ','
                << flags.gam2_zdc_ecal << ','
                << flags.gam1_b0_ecal << ','
                << flags.gam2_b0_ecal << ','
                << flags.gam1_ecalp << ','
                << flags.gam2_ecalp << ','
                << flags.gam1_ecalp_ins << ','
                << flags.gam2_ecalp_ins
                << '\n';

        is_first_lambda = false;
        break; // we only need first lambdas. One lambda per event.
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

    // Print statistics
    print_stats();

    return 0;
}


// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt:  root -x -l -b -q 'csv_edm4hep_acceptance.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void csv_edm4hep_acceptance(const char* infile, const char* outfile, int events = -1)
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

    // Print statistics
    print_stats();
}