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
    long gamone_zdc_ecal = 0;
    long gamtwo_zdc_ecal = 0;
    long gamone_b0_ecal = 0;
    long gamtwo_b0_ecal = 0;
    long gamone_ecalp = 0;
    long gamtwo_ecalp = 0;
    long gamone_ecalp_ins = 0;
    long gamtwo_ecalp_ins = 0;

    // All 3 particle per detector
    long gam_neut_in_zdc = 0;

    // When all three particles detected
    long all3_neut_zdc_hcal = 0;
    long all3_neut_pins_hcal = 0;
    long all3_neut_lf_hcal = 0;
    long all3_gamone_zdc_ecal = 0;
    long all3_gamtwo_zdc_ecal = 0;
    long all3_gamone_b0_ecal = 0;
    long all3_gamtwo_b0_ecal = 0;
    long all3_gamone_ecalp = 0;
    long all3_gamtwo_ecalp = 0;
    long all3_gamone_ecalp_ins = 0;
    long all3_gamtwo_ecalp_ins = 0;

    // Decay channel statistics (matches lam_decay codes)
    long decay_not_decayed = 0;   // 0
    long decay_p_piminus = 0;     // 1
    long decay_shower = 0;        // 3
    long decay_only_p = 0;        // 4
    long decay_only_piplus = 0;   // 5
    long decay_only_n = 0;        // 6
    long decay_only_pi0 = 0;      // 7
    long decay_other = 0;         // 8
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
        return ",,,,,,,,,,,,,,,"; // 15 commas for 16 empty fields
    }
    const auto mom = prt->getMomentum();
    const auto vtx = prt->getVertex();
    const auto ep = prt->getEndpoint();
    return fmt::format("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}",
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
                                         prt->getDaughters().size(), // 15  nd
                                         prt->getParents().size() // 16  np
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
        "{0}_nd,"     // 15  nd
        "{0}_np",     // 16  np (no trailing comma)
        prefix
    );
}

bool has_particle_hits(const auto& hit_collection, const MCParticle& particle,
                       const std::string& detector_name, const std::string& particle_name) {
    for (const auto& hit: hit_collection) {
        for (const auto& contrib: hit.getContributions()) {
            if (contrib.getParticle().getObjectID() == particle.getObjectID()) {
                // fmt::print("{} hit: id={:<5} z={:<10.2f} contrib={} is of {} \n",
                //           detector_name, hit.id().index, hit.getPosition().z,
                //           hit.contributions_size(), particle_name);
                return true;
            }
        }
    }
    return false;
}

struct DetectionFlags {
    // Neutron in HCALs
    bool neut_HcalFarForwardZDCHits = false;
    bool neut_HcalEndcapPInsertHits = false;
    bool neut_LFHCALHits = false;
    // Gamma-one in ECALs
    bool gamone_EcalFarForwardZDCHits = false;
    bool gamone_B0ECalHits = false;
    bool gamone_EcalEndcapPHits = false;
    bool gamone_EcalEndcapPInsertHits = false;
    // Gamma-two in ECALs
    bool gamtwo_EcalFarForwardZDCHits = false;
    bool gamtwo_B0ECalHits = false;
    bool gamtwo_EcalEndcapPHits = false;
    bool gamtwo_EcalEndcapPInsertHits = false;
};

DetectionFlags process_calo_hits_npi0(const podio::Frame& event, const MCParticle& neut,
                            const MCParticle& gam1, const MCParticle& gam2) {
    DetectionFlags flags;

    // Check for gamma particles in various ECALs
    const auto& zdc_ecal_hits = event.get<edm4hep::SimCalorimeterHitCollection>("EcalFarForwardZDCHits");
    flags.gamone_EcalFarForwardZDCHits = has_particle_hits(zdc_ecal_hits, gam1, "EcalFarForwardZDC", "gamone");
    flags.gamtwo_EcalFarForwardZDCHits = has_particle_hits(zdc_ecal_hits, gam2, "EcalFarForwardZDC", "gamtwo");

    const auto& b0_hits = event.get<edm4hep::SimCalorimeterHitCollection>("B0ECalHits");
    flags.gamone_B0ECalHits = has_particle_hits(b0_hits, gam1, "B0ECal", "gamone");
    flags.gamtwo_B0ECalHits = has_particle_hits(b0_hits, gam2, "B0ECal", "gamtwo");

    const auto& ecalp_hits = event.get<edm4hep::SimCalorimeterHitCollection>("EcalEndcapPHits");
    flags.gamone_EcalEndcapPHits = has_particle_hits(ecalp_hits, gam1, "EcalEndcapP", "gamone");
    flags.gamtwo_EcalEndcapPHits = has_particle_hits(ecalp_hits, gam2, "EcalEndcapP", "gamtwo");

    const auto& ecalpins_hits = event.get<edm4hep::SimCalorimeterHitCollection>("EcalEndcapPInsertHits");
    flags.gamone_EcalEndcapPInsertHits = has_particle_hits(ecalpins_hits, gam1, "EcalEndcapPInsert", "gamone");
    flags.gamtwo_EcalEndcapPInsertHits = has_particle_hits(ecalpins_hits, gam2, "EcalEndcapPInsert", "gamtwo");

    // Check for neutron in various HCALs
    const auto& zdc_hcal_hits = event.get<edm4hep::SimCalorimeterHitCollection>("HcalFarForwardZDCHits");
    flags.neut_HcalFarForwardZDCHits = has_particle_hits(zdc_hcal_hits, neut, "HcalFarForwardZDC", "NEUTRON");

    const auto& pins_hcal_hits = event.get<edm4hep::SimCalorimeterHitCollection>("HcalEndcapPInsertHits");
    flags.neut_HcalEndcapPInsertHits = has_particle_hits(pins_hcal_hits, neut, "HcalEndcapPInsert", "NEUTRON");

    const auto& lf_hcal_hits = event.get<edm4hep::SimCalorimeterHitCollection>("LFHCALHits");
    flags.neut_LFHCALHits = has_particle_hits(lf_hcal_hits, neut, "LFHCAL", "NEUTRON");

    // Check if neutron in any HCAL
    bool neut_in_any = flags.neut_HcalFarForwardZDCHits || flags.neut_HcalEndcapPInsertHits || flags.neut_LFHCALHits;
    if (neut_in_any) stats.neut_in_any_hcal++;

    // Check if both gammas detected anywhere
    bool gamone_detected = flags.gamone_EcalFarForwardZDCHits || flags.gamone_B0ECalHits || flags.gamone_EcalEndcapPHits || flags.gamone_EcalEndcapPInsertHits;
    bool gamtwo_detected = flags.gamtwo_EcalFarForwardZDCHits || flags.gamtwo_B0ECalHits || flags.gamtwo_EcalEndcapPHits || flags.gamtwo_EcalEndcapPInsertHits;

    if (neut_in_any && gamone_detected && gamtwo_detected) {
        stats.neut_and_both_gammas++;
    }

    // Update per-detector counts
    if (flags.neut_HcalFarForwardZDCHits) stats.neut_zdc_hcal++;
    if (flags.neut_HcalEndcapPInsertHits) stats.neut_pins_hcal++;
    if (flags.neut_LFHCALHits) stats.neut_lf_hcal++;

    if (flags.gamone_EcalFarForwardZDCHits) stats.gamone_zdc_ecal++;
    if (flags.gamtwo_EcalFarForwardZDCHits) stats.gamtwo_zdc_ecal++;
    if (flags.gamone_B0ECalHits) stats.gamone_b0_ecal++;
    if (flags.gamtwo_B0ECalHits) stats.gamtwo_b0_ecal++;
    if (flags.gamone_EcalEndcapPHits) stats.gamone_ecalp++;
    if (flags.gamtwo_EcalEndcapPHits) stats.gamtwo_ecalp++;
    if (flags.gamone_EcalEndcapPInsertHits) stats.gamone_ecalp_ins++;
    if (flags.gamtwo_EcalEndcapPInsertHits) stats.gamtwo_ecalp_ins++;

    // Check if all three particles detected
    if (neut_in_any && gamone_detected && gamtwo_detected) {
        stats.all_three_detected++;

        if (flags.neut_HcalFarForwardZDCHits && flags.gamone_EcalFarForwardZDCHits && flags.gamtwo_EcalFarForwardZDCHits) {
            stats.gam_neut_in_zdc++;
        }

        // Update all3 per-detector counts
        if (flags.neut_HcalFarForwardZDCHits) stats.all3_neut_zdc_hcal++;
        if (flags.neut_HcalEndcapPInsertHits) stats.all3_neut_pins_hcal++;
        if (flags.neut_LFHCALHits) stats.all3_neut_lf_hcal++;

        if (flags.gamone_EcalFarForwardZDCHits) stats.all3_gamone_zdc_ecal++;
        if (flags.gamtwo_EcalFarForwardZDCHits) stats.all3_gamtwo_zdc_ecal++;
        if (flags.gamone_B0ECalHits) stats.all3_gamone_b0_ecal++;
        if (flags.gamtwo_B0ECalHits) stats.all3_gamtwo_b0_ecal++;
        if (flags.gamone_EcalEndcapPHits) stats.all3_gamone_ecalp++;
        if (flags.gamtwo_EcalEndcapPHits) stats.all3_gamtwo_ecalp++;
        if (flags.gamone_EcalEndcapPInsertHits) stats.all3_gamone_ecalp_ins++;
        if (flags.gamtwo_EcalEndcapPInsertHits) stats.all3_gamtwo_ecalp_ins++;
    }

    return flags;
}

void print_stats() {
    fmt::print("\n=== DETECTION STATISTICS ===\n");
    fmt::print("Total first lambdas: {}\n", stats.total_lambdas);
    auto pct = [&](long n) {
        return stats.total_lambdas > 0 ? 100.0 * n / stats.total_lambdas : 0.0;
    };
    fmt::print("Lambda decay channels:\n");
    fmt::print("  0 Not decayed:     {} ({:.2f}%)\n", stats.decay_not_decayed, pct(stats.decay_not_decayed));
    fmt::print("  1 p + π⁻:          {} ({:.2f}%)\n", stats.decay_p_piminus,   pct(stats.decay_p_piminus));
    fmt::print("  2 n + π⁰:          {} ({:.2f}%)\n", stats.total_npi0_decays, pct(stats.total_npi0_decays));
    fmt::print("  3 Shower (>2):     {} ({:.2f}%)\n", stats.decay_shower,      pct(stats.decay_shower));
    fmt::print("  4 Only p:          {} ({:.2f}%)\n", stats.decay_only_p,      pct(stats.decay_only_p));
    fmt::print("  5 Only π⁺:         {} ({:.2f}%)\n", stats.decay_only_piplus, pct(stats.decay_only_piplus));
    fmt::print("  6 Only n:          {} ({:.2f}%)\n", stats.decay_only_n,      pct(stats.decay_only_n));
    fmt::print("  7 Only π⁰:         {} ({:.2f}%)\n", stats.decay_only_pi0,    pct(stats.decay_only_pi0));
    fmt::print("  8 Other:           {} ({:.2f}%)\n", stats.decay_other,       pct(stats.decay_other));

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

        fmt::print("Gamone detections:\n");
        fmt::print("  EcalFarForwardZDC: {}\n", stats.gamone_zdc_ecal);
        fmt::print("  B0ECal: {}\n", stats.gamone_b0_ecal);
        fmt::print("  EcalEndcapP: {}\n", stats.gamone_ecalp);
        fmt::print("  EcalEndcapPInsert: {}\n", stats.gamone_ecalp_ins);

        fmt::print("Gamtwo detections:\n");
        fmt::print("  EcalFarForwardZDC: {}\n", stats.gamtwo_zdc_ecal);
        fmt::print("  B0ECal: {}\n", stats.gamtwo_b0_ecal);
        fmt::print("  EcalEndcapP: {}\n", stats.gamtwo_ecalp);
        fmt::print("  EcalEndcapPInsert: {}\n", stats.gamtwo_ecalp_ins);

        if (stats.all_three_detected > 0) {
            fmt::print("\n--- Per-Detector Counts (All 3 Particles Detected) ---\n");
            fmt::print("Total events with all 3 particles: {}\n", stats.all_three_detected);
            fmt::print("Neutron detections:\n");
            fmt::print("  HcalFarForwardZDC: {}\n", stats.all3_neut_zdc_hcal);
            fmt::print("  HcalEndcapPInsert: {}\n", stats.all3_neut_pins_hcal);
            fmt::print("  LFHCAL: {}\n", stats.all3_neut_lf_hcal);

            fmt::print("Gamone detections:\n");
            fmt::print("  EcalFarForwardZDC: {}\n", stats.all3_gamone_zdc_ecal);
            fmt::print("  B0ECal: {}\n", stats.all3_gamone_b0_ecal);
            fmt::print("  EcalEndcapP: {}\n", stats.all3_gamone_ecalp);
            fmt::print("  EcalEndcapPInsert: {}\n", stats.all3_gamone_ecalp_ins);

            fmt::print("Gamtwo detections:\n");
            fmt::print("  EcalFarForwardZDC: {}\n", stats.all3_gamtwo_zdc_ecal);
            fmt::print("  B0ECal: {}\n", stats.all3_gamtwo_b0_ecal);
            fmt::print("  EcalEndcapP: {}\n", stats.all3_gamtwo_ecalp);
            fmt::print("  EcalEndcapPInsert: {}\n", stats.all3_gamtwo_ecalp_ins);
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

        // Decay classification:
        //  0 - no daughters, 1 - p π⁻, 2 - n π⁰, 3 - shower (>2 daughters),
        //  4 - only p, 5 - only π⁺, 6 - only n, 7 - only π⁰, 8 - other
        int decay_type = 8;

        // -----------------------------------------------------------------
        // classify decay channel & pick final-state pointers
        // -----------------------------------------------------------------
        std::optional<MCParticle> prot, pimin, neut, pi0, gam1, gam2;

        auto daughters = lam.getDaughters();
        const auto nd = daughters.size();

        if (nd == 0) {
            decay_type = 0;
            stats.decay_not_decayed++;
        } else if (nd == 1) {
            switch (daughters.at(0).getPDG()) {
                case 2212: decay_type = 4; stats.decay_only_p++;      break;
                case 211:  decay_type = 5; stats.decay_only_piplus++; break;
                case 2112: decay_type = 6; stats.decay_only_n++;      break;
                case 111:  decay_type = 7; stats.decay_only_pi0++;    break;
                default:   decay_type = 8; stats.decay_other++;       break;
            }
        } else if (nd == 2) {
            const int pdg0 = daughters.at(0).getPDG();
            const int pdg1 = daughters.at(1).getPDG();
            if (pdg0 == 2212 && pdg1 == -211) {
                decay_type = 1;
                prot = daughters.at(0);
                pimin = daughters.at(1);
            } else if (pdg1 == 2212 && pdg0 == -211) {
                decay_type = 1;
                prot = daughters.at(1);
                pimin = daughters.at(0);
            } else if (pdg0 == 2112 && pdg1 == 111) {
                decay_type = 2;
                neut = daughters.at(0);
                pi0 = daughters.at(1);
            } else if (pdg1 == 2112 && pdg0 == 111) {
                decay_type = 2;
                neut = daughters.at(1);
                pi0 = daughters.at(0);
            } else {
                decay_type = 8;
                stats.decay_other++;
            }
        } else {
            decay_type = 3; // shower (>2 daughters)
            stats.decay_shower++;
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

            // fmt::print("---------------------------------------\n looking hits at event {}\n", evt_id);
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
                    << "neut_HcalFarForwardZDCHits,neut_HcalEndcapPInsertHits,neut_LFHCALHits,"
                    << "gamone_EcalFarForwardZDCHits,gamtwo_EcalFarForwardZDCHits,"
                    << "gamone_B0ECalHits,gamtwo_B0ECalHits,"
                    << "gamone_EcalEndcapPHits,gamtwo_EcalEndcapPHits,"
                    << "gamone_EcalEndcapPInsertHits,gamtwo_EcalEndcapPInsertHits"
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
                << flags.neut_HcalFarForwardZDCHits << ','
                << flags.neut_HcalEndcapPInsertHits << ','
                << flags.neut_LFHCALHits << ','
                << flags.gamone_EcalFarForwardZDCHits << ','
                << flags.gamtwo_EcalFarForwardZDCHits << ','
                << flags.gamone_B0ECalHits << ','
                << flags.gamtwo_B0ECalHits << ','
                << flags.gamone_EcalEndcapPHits << ','
                << flags.gamtwo_EcalEndcapPHits << ','
                << flags.gamone_EcalEndcapPInsertHits << ','
                << flags.gamtwo_EcalEndcapPInsertHits
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
// Call it from the prompt:  root -x -l -b -q 'csv_edm4hep_acceptance_npi0.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void csv_edm4hep_acceptance_npi0(const char* infile, const char* outfile, int events = -1)
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