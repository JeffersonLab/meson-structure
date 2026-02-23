#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif

// csv_edm4hep_acceptance_ppim.cxx
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

using namespace edm4hep;

//------------------------------------------------------------------------------
// globals & helpers
//------------------------------------------------------------------------------
int events_limit = -1; // -n  <N>
long total_evt_seen = 0;
std::ofstream csv;
std::ofstream csv_prot_hits;
std::ofstream csv_pimin_hits;
bool header_written = false;
bool hits_header_written = false;

// List of trackers from edm4hep-tree.md
const std::vector<std::string> tracker_collections = {
    "B0TrackerHits",
    "BackwardMPGDEndcapHits",
    "DIRCBarHits",
    "DRICHHits",
    "ForwardMPGDEndcapHits",
    "ForwardOffMTrackerHits",
    "ForwardRomanPotHits",
    "LumiSpecTrackerHits",
    "MPGDBarrelHits",
    "OuterMPGDBarrelHits",
    "RICHEndcapNHits",
    "SiBarrelHits",
    "TOFBarrelHits",
    "TOFEndcapHits",
    "TaggerTrackerHits",
    "TrackerEndcapHits",
    "VertexBarrelHits"
};

// List of calorimeters from csv_edm4hep_acceptance_npi0.cxx
const std::vector<std::string> calorimeter_collections = {
    "EcalFarForwardZDCHits",
    "B0ECalHits",
    "EcalEndcapPHits",
    "EcalEndcapPInsertHits",
    "HcalFarForwardZDCHits",
    "HcalEndcapPInsertHits",
    "LFHCALHits"
};

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

// Specialized function for Tracker Hits
void process_tracker_hits(const podio::Frame& event, const std::string& collection_name,
                          const MCParticle& particle, std::ofstream& hits_csv,
                          int evt_id, int lam_id, std::map<std::string, bool>& detection_map,
                          const std::string& particle_prefix) {
    try {
        const auto& collection = event.get<edm4hep::SimTrackerHitCollection>(collection_name);
        bool detected = false;
        for (const auto& hit : collection) {
            if (hit.getParticle().isAvailable() && hit.getParticle().getObjectID() == particle.getObjectID()) {
                detected = true;
                
                // Write to detailed CSV
                // Format: event_id, lam_id, detector, hit_id, x, y, z, eDep, time, pathLength
                hits_csv << evt_id << "," << lam_id << "," << collection_name << ","
                         << hit.getObjectID().index << ","
                         << hit.getPosition().x << ","
                         << hit.getPosition().y << ","
                         << hit.getPosition().z << ","
                         << hit.getEDep() << ","
                         << hit.getTime() << ","
                         << hit.getPathLength() << "\n";
            }
        }
        detection_map[particle_prefix + "_" + collection_name] = detected;
    } catch (...) {
        // Collection might not exist or be of different type (unlikely if we stick to the list)
        detection_map[particle_prefix + "_" + collection_name] = false;
    }
}

// Specialized function for Calorimeter Hits
void process_calo_hits(const podio::Frame& event, const std::string& collection_name,
                       const MCParticle& particle, std::ofstream& hits_csv,
                       int evt_id, int lam_id, std::map<std::string, bool>& detection_map,
                       const std::string& particle_prefix) {
    try {
        const auto& collection = event.get<edm4hep::SimCalorimeterHitCollection>(collection_name);
        bool detected = false;
        for (const auto& hit : collection) {
            bool particle_contributed = false;
            float time = -1;
            
            for (const auto& contrib : hit.getContributions()) {
                if (contrib.getParticle().getObjectID() == particle.getObjectID()) {
                    particle_contributed = true;
                    time = contrib.getTime(); // Take time from contribution
                    break; // One contribution is enough to claim the hit belongs to particle
                }
            }
            
            if (particle_contributed) {
                detected = true;
                
                // Write to detailed CSV
                // Format: event_id, lam_id, detector, hit_id, x, y, z, energy, time, pathLength (0 for calo)
                hits_csv << evt_id << "," << lam_id << "," << collection_name << ","
                         << hit.getObjectID().index << ","
                         << hit.getPosition().x << ","
                         << hit.getPosition().y << ","
                         << hit.getPosition().z << ","
                         << hit.getEnergy() << ","
                         << time << ","
                         << "0" << "\n"; // 0 for pathLength
            }
        }
        detection_map[particle_prefix + "_" + collection_name] = detected;
    } catch (...) {
        detection_map[particle_prefix + "_" + collection_name] = false;
    }
}


//------------------------------------------------------------------------------
// event processing
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int evt_id) {
    const auto& particles = event.get<MCParticleCollection>("MCParticles");

    for (const auto& lam: particles) {
        if (lam.getPDG() != 3122) continue; // not Λ⁰

        // Check if it decays to p + pi-
        auto daughters = lam.getDaughters();
        if (daughters.size() != 2) continue;

        std::optional<MCParticle> prot, pimin;
        
        // Check decay products
        bool is_ppim = false;
        if (daughters.at(0).getPDG() == 2212 && daughters.at(1).getPDG() == -211) {
            is_ppim = true;
            prot = daughters.at(0);
            pimin = daughters.at(1);
        } else if (daughters.at(1).getPDG() == 2212 && daughters.at(0).getPDG() == -211) {
            is_ppim = true;
            prot = daughters.at(1);
            pimin = daughters.at(0);
        }

        if (!is_ppim) continue;

        // We found a Lambda -> p + pi- decay
        int lam_id = lam.getObjectID().index;

        // Prepare detection map
        std::map<std::string, bool> detection_map;

        // Process Proton
        if (prot) {
            for (const auto& name : tracker_collections) {
                process_tracker_hits(event, name, *prot, csv_prot_hits, evt_id, lam_id, detection_map, "prot");
            }
            for (const auto& name : calorimeter_collections) {
                process_calo_hits(event, name, *prot, csv_prot_hits, evt_id, lam_id, detection_map, "prot");
            }
        }

        // Process Pion
        if (pimin) {
            for (const auto& name : tracker_collections) {
                process_tracker_hits(event, name, *pimin, csv_pimin_hits, evt_id, lam_id, detection_map, "pimin");
            }
            for (const auto& name : calorimeter_collections) {
                process_calo_hits(event, name, *pimin, csv_pimin_hits, evt_id, lam_id, detection_map, "pimin");
            }
        }

        // Write Main CSV Header if needed
        if (!header_written) {
            csv << "evt,lam_id,"
                << make_particle_header("lam") << ","
                << make_particle_header("prot") << ","
                << make_particle_header("pimin");
            
            // Add columns for detection flags
            for (const auto& name : tracker_collections) {
                csv << ",prot_" << name;
            }
            for (const auto& name : calorimeter_collections) {
                csv << ",prot_" << name;
            }
             for (const auto& name : tracker_collections) {
                csv << ",pimin_" << name;
            }
            for (const auto& name : calorimeter_collections) {
                csv << ",pimin_" << name;
            }
            csv << "\n";
            header_written = true;
        }

        // Write Main CSV Data
        csv << evt_id << "," << lam_id << ","
            << particle_to_csv(lam) << ","
            << particle_to_csv(prot) << ","
            << particle_to_csv(pimin);

        // Write flags
        for (const auto& name : tracker_collections) csv << "," << detection_map["prot_" + name];
        for (const auto& name : calorimeter_collections) csv << "," << detection_map["prot_" + name];
        for (const auto& name : tracker_collections) csv << "," << detection_map["pimin_" + name];
        for (const auto& name : calorimeter_collections) csv << "," << detection_map["pimin_" + name];
        
        csv << "\n";

        // We only process the first lambda per event? 
        // The requirement says "first two colums must be event id and lambda id".
        // It implies we might have multiple lambdas or we just need to identify them.
        // The npi0 script breaks after first lambda.
        // "break; // we only need first lambdas. One lambda per event."
        // I will follow the same pattern for consistency unless instructed otherwise.
        // But wait, the user said "first two colums must be event id and lambda id".
        // If I break, I only get one.
        // The npi0 script has:
        // if (!header_written) { ... }
        // csv << ...
        // is_first_lambda = false;
        // break; 
        // So it strictly does one lambda per event. I will do the same.
        break; 
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
    std::string out_name = "acceptance_ppim.csv";

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
    std::string prot_hits_name = out_name + "_prot_hits.csv";
    std::string pimin_hits_name = out_name + "_pimin_hits.csv";
    
    // Fix extension if present
    if (out_name.size() > 4 && out_name.substr(out_name.size() - 4) == ".csv") {
        std::string base = out_name.substr(0, out_name.size() - 4);
        prot_hits_name = base + "_prot_hits.csv";
        pimin_hits_name = base + "_pimin_hits.csv";
    }
    
    csv_prot_hits.open(prot_hits_name);
    csv_pimin_hits.open(pimin_hits_name);

    if (!csv || !csv_prot_hits || !csv_pimin_hits) {
        fmt::print(stderr, "error: cannot open output files\n");
        return 1;
    }
    
    // Write headers for hits files
    std::string hits_header = "event_id,lam_id,detector,hit_id,x,y,z,eDep,time,pathLength\n";
    csv_prot_hits << hits_header;
    csv_pimin_hits << hits_header;

    for (auto&f: infiles) {
        process_file(f);
        if (events_limit > 0 && total_evt_seen >= events_limit) break;
    }

    csv.close();
    csv_prot_hits.close();
    csv_pimin_hits.close();
    
    fmt::print("Wrote data for {} events to {}\n", total_evt_seen, out_name);
    fmt::print("Detailed proton hits: {}\n", prot_hits_name);
    fmt::print("Detailed pion hits: {}\n", pimin_hits_name);

    return 0;
}

// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt:  root -x -l -b -q 'csv_edm4hep_acceptance_ppim.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void csv_edm4hep_acceptance_ppim(const char* infile, const char* outfile, int events = -1)
{
    fmt::print("'csv_edm4hep_acceptance_ppim' entry point is used.\n");
    
    csv.open(outfile);
    
    std::string out_str = outfile;
    std::string prot_hits_name = out_str + "_prot_hits.csv";
    std::string pimin_hits_name = out_str + "_pimin_hits.csv";
    
     if (out_str.size() > 4 && out_str.substr(out_str.size() - 4) == ".csv") {
        std::string base = out_str.substr(0, out_str.size() - 4);
        prot_hits_name = base + "_prot_hits.csv";
        pimin_hits_name = base + "_pimin_hits.csv";
    }
    
    csv_prot_hits.open(prot_hits_name);
    csv_pimin_hits.open(pimin_hits_name);

    if (!csv || !csv_prot_hits || !csv_pimin_hits) {
        fmt::print(stderr, "error: cannot open output files\n");
        exit(1);
    }

    // Write headers for hits files
    std::string hits_header = "evt,lam_id,detector,hit_id,x,y,z,eDep,time,pathLength\n";
    csv_prot_hits << hits_header;
    csv_pimin_hits << hits_header;

    events_limit = events;
    process_file(infile);

    csv.close();
    csv_prot_hits.close();
    csv_pimin_hits.close();
    
    fmt::print("\nWrote data for {} events to {}\n", total_evt_seen, outfile);
}
