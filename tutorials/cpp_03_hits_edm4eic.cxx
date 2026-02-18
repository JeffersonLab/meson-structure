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
#include <edm4eic/MCRecoTrackerHitAssociationCollection.h>
#include <edm4eic/MCRecoTrackerHitAssociationCollection.h>
#include <edm4eic/MCRecoCalorimeterHitAssociationCollection.h>
#include <edm4eic/TrackerHitCollection.h>
#include <edm4eic/TrackerHit.h>

#include <fmt/core.h>
#include <fmt/ostream.h>

#include <TFile.h>

#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <map>
#include <expected>
#include <format>
#include <print>
using namespace edm4hep;

//------------------------------------------------------------------------------
// globals & helpers
//------------------------------------------------------------------------------
int events_limit = -1; // -n  <N>
long total_evt_processed = 0;
std::ofstream csv;
std::ofstream csv_trk_hits;
std::ofstream csv_cal_hits;
bool header_written = false;
bool trk_hits_header_written = false;



/// Struct representing a line in csv file
struct HitRecord {
    // Event and indexing
    uint64_t evt;                    // Event number
    uint64_t hit_index;              // Index of MCRecoTrackerHitAssociation in collection
    uint64_t prt_index;              // Index of MCParticle that created this hit

    // Particle identification
    int32_t prt_pdg;                 // PDG code of the particle (e.g., 11=e-, 211=pi+, 2212=proton)
    int32_t prt_status;              // Generator status: 1=stable from generator, 0=created by Geant4

    // Particle kinematics
    double prt_energy;               // Total energy of particle [GeV]
    float prt_charge;                // Electric charge [e]
    double prt_mom_x;                // Momentum x-component [GeV/c]
    double prt_mom_y;                // Momentum y-component [GeV/c]
    double prt_mom_z;                // Momentum z-component [GeV/c]

    // Particle vertex (production point)
    float prt_vtx_time;              // Time at production vertex [ns]
    float prt_vtx_pos_x;             // Production vertex x [mm]
    float prt_vtx_pos_y;             // Production vertex y [mm]
    float prt_vtx_pos_z;             // Production vertex z [mm]

    // Particle endpoint (decay/absorption point)
    float prt_end_time;              // Time at endpoint [ns] (Note: same as vtx_time in EDM4hep)
    float prt_end_pos_x;             // Endpoint x [mm]
    float prt_end_pos_y;             // Endpoint y [mm]
    float prt_end_pos_z;             // Endpoint z [mm]

    // Tracker hit detector info
    uint64_t trk_hit_cell_id;        // Full cell ID encoding detector hierarchy
    uint64_t trk_hit_system_id;      // Detector system ID (bits 0-7 of cell_id)
    std::string trk_hit_system_name; // Human-readable detector name (e.g., "SiBarrelVertex")

    // Tracker hit position and time
    float trk_hit_pos_x;             // Reconstructed hit position x [mm]
    float trk_hit_pos_y;             // Reconstructed hit position y [mm]
    float trk_hit_pos_z;             // Reconstructed hit position z [mm]
    float trk_hit_time;              // Reconstructed hit time [ns]

    // Tracker hit uncertainties (covariance matrix diagonal)
    float trk_hit_pos_err_xx;        // Position error variance in x [mm^2]
    float trk_hit_pos_err_yy;        // Position error variance in y [mm^2]
    float trk_hit_pos_err_zz;        // Position error variance in z [mm^2]
    float trk_hit_time_err;          // Time uncertainty [ns]

    // Tracker hit energy deposition
    float trk_hit_edep;              // Energy deposited in sensor [GeV]
    float trk_hit_edep_err;          // Energy deposition uncertainty [GeV]

    static std::string make_csv_header() {
        return "evt,hit_index,prt_index,"
               "prt_pdg,prt_status,prt_energy,prt_charge,"
               "prt_mom_x,prt_mom_y,prt_mom_z,"
               "prt_vtx_time,prt_vtx_pos_x,prt_vtx_pos_y,prt_vtx_pos_z,"
               "prt_end_time,prt_end_pos_x,prt_end_pos_y,prt_end_pos_z,"
               "trk_hit_cell_id,trk_hit_system_id,trk_hit_system_name,"
               "trk_hit_pos_x,trk_hit_pos_y,trk_hit_pos_z,trk_hit_time,"
               "trk_hit_pos_err_xx,trk_hit_pos_err_yy,trk_hit_pos_err_zz,trk_hit_time_err,"
               "trk_hit_edep,trk_hit_edep_err";
    }

    std::string get_csv_line() const {
        return fmt::format("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}",
            evt, hit_index, prt_index,
            prt_pdg, prt_status, prt_energy, prt_charge,
            prt_mom_x, prt_mom_y, prt_mom_z,
            prt_vtx_time, prt_vtx_pos_x, prt_vtx_pos_y, prt_vtx_pos_z,
            prt_end_time, prt_end_pos_x, prt_end_pos_y, prt_end_pos_z,
            trk_hit_cell_id, trk_hit_system_id, trk_hit_system_name,
            trk_hit_pos_x, trk_hit_pos_y, trk_hit_pos_z, trk_hit_time,
            trk_hit_pos_err_xx, trk_hit_pos_err_yy, trk_hit_pos_err_zz, trk_hit_time_err,
            trk_hit_edep, trk_hit_edep_err);
    }
};

// Name of collections for track associations, which associate:
// - edm4eic::RawTrackerHit rawHit       // reference to the digitized hit
// - edm4hep::SimTrackerHit simHit       // reference to the simulated hit
const std::vector<std::string> track_associations = {
    "B0TrackerRawHitAssociations",
    "BackwardMPGDEndcapRawHitAssociations",
    "ForwardMPGDEndcapRawHitAssociations",
    "ForwardOffMTrackerRawHitAssociations",
    "ForwardRomanPotRawHitAssociations",
    "MPGDBarrelRawHitAssociations",
    "OuterMPGDBarrelRawHitAssociations",
    "RICHEndcapNRawHitsAssociations",
    "SiBarrelRawHitAssociations",
    "SiBarrelVertexRawHitAssociations",
    "SiEndcapTrackerRawHitAssociations",
    "TOFBarrelRawHitAssociations",
    "TOFEndcapRawHitAssociations"//,
    //"TaggerTrackerRawHitAssociations" //, "DRICHRawHitsAssociations"
};

const std::map<std::string, std::string> tracker_names_by_assoc = {
    {"B0TrackerRawHitAssociations", "B0TrackerRecHits"},
    {"BackwardMPGDEndcapRawHitAssociations", "BackwardMPGDEndcapRecHits"},
    {"ForwardMPGDEndcapRawHitAssociations", "ForwardMPGDEndcapRecHits"},
    {"ForwardOffMTrackerRawHitAssociations", "ForwardOffMTrackerRecHits"},
    {"ForwardRomanPotRawHitAssociations", "ForwardRomanPotRecHits"},
    {"MPGDBarrelRawHitAssociations", "MPGDBarrelRecHits"},
    {"OuterMPGDBarrelRawHitAssociations", "OuterMPGDBarrelRecHits"},
    {"RICHEndcapNRawHitsAssociations", "RICHEndcapNRits"},
    {"SiBarrelRawHitAssociations", "SiBarrelTrackerRecHits"},
    {"SiBarrelVertexRawHitAssociations", "SiBarrelVertexRecHits"},
    {"SiEndcapTrackerRawHitAssociations", "SiEndcapTrackerRecHits"},
    {"TOFBarrelRawHitAssociations", "TOFBarrelRecHits"},
    {"TOFEndcapRawHitAssociations", "TOFEndcapRecHits"},
    // {"TaggerTrackerRawHitAssociations", "TaggerTrackerHit"} //,    {"DRICHRawHitsAssociations", ""}
};

const std::vector<std::string> cal_associations = {
    "B0ECalRawHitAssociations",
    "EcalBarrelImagingRawHitAssociations",
    "EcalBarrelScFiRawHitAssociations",
    "EcalEndcapNRawHitAssociations",
    "EcalEndcapPRawHitAssociations",
    "EcalFarForwardZDCRawHitAssociations",
    "EcalLumiSpecRawHitAssociations",
    "HcalBarrelRawHitAssociations",
    "HcalEndcapNRawHitAssociations",
    "HcalEndcapPInsertRawHitAssociations",
    "HcalFarForwardZDCRawHitAssociations",
    "LFHCALRawHitAssociations",

};

const std::vector<std::string> cal_cluster_associations = {
    "B0ECalClusterAssociations",

    "EcalBarrelClusterAssociations",

    "EcalBarrelImagingClusterAssociations",

    "EcalBarrelScFiClusterAssociations",

    "EcalBarrelTruthClusterAssociations",

    "EcalEndcapNClusterAssociations",
    "EcalEndcapNSplitMergeClusterAssociations",
    "EcalEndcapNTruthClusterAssociations",

    "EcalEndcapPClusterAssociations",
    "EcalEndcapPSplitMergeClusterAssociations",
    "EcalEndcapPTruthClusterAssociations",

    "EcalFarForwardZDCClusterAssociations",
    "EcalFarForwardZDCTruthClusterAssociations",

    "HcalFarForwardZDCClusterAssociations",
    "HcalFarForwardZDCClusterAssociationsBaseline",
    "HcalFarForwardZDCTruthClusterAssociations",

    "EcalLumiSpecClusterAssociations",
    "EcalLumiSpecTruthClusterAssociations",

    "HcalBarrelClusterAssociations",
    "HcalBarrelSplitMergeClusterAssociations",
    "HcalBarrelTruthClusterAssociations",

    "HcalEndcapNClusterAssociations",
    "HcalEndcapNSplitMergeClusterAssociations",
    "HcalEndcapNTruthClusterAssociations",

    "HcalEndcapPInsertClusterAssociations",

    "LFHCALClusterAssociations",
    "LFHCALSplitMergeClusterAssociations",
};


// Dictionary from your definitions.xml
std::map<uint64_t, std::string> system_names_by_ids = {
    {10, "BeamPipe"},
    {11, "BeamPipeB0"},
    {25, "VertexSubAssembly_0"},
    {26, "VertexSubAssembly_1"},
    {27, "VertexSubAssembly_2"},
    {31, "VertexBarrel_0"},
    {32, "VertexBarrel_1"},
    {33, "VertexBarrel_2"},
    {34, "VertexEndcapN_0"},
    {35, "VertexEndcapN_1"},
    {36, "VertexEndcapN_2"},
    {37, "VertexEndcapP_0"},
    {38, "VertexEndcapP_1"},
    {39, "VertexEndcapP_2"},
    {40, "TrackerSubAssembly_0"},
    {41, "TrackerSubAssembly_1"},
    {42, "TrackerSubAssembly_2"},
    {43, "TrackerSubAssembly_3"},
    {44, "TrackerSubAssembly_4"},
    {45, "TrackerSubAssembly_5"},
    {46, "TrackerSubAssembly_6"},
    {47, "TrackerSubAssembly_7"},
    {48, "TrackerSubAssembly_8"},
    {49, "TrackerSubAssembly_9"},
    {50, "SVT_IB_Support_0"},
    {51, "SVT_IB_Support_1"},
    {52, "SVT_IB_Support_2"},
    {53, "SVT_IB_Support_3"},
    {59, "TrackerBarrel_0"},
    {60, "TrackerBarrel_1"},
    {61, "TrackerBarrel_2"},
    {62, "TrackerBarrel_3"},
    {63, "TrackerBarrel_4"},
    {64, "TrackerBarrel_5"},
    {65, "TrackerBarrel_6"},
    {66, "TrackerBarrel_7"},
    {67, "TrackerBarrel_8"},
    {68, "TrackerEndcapN_0"},
    {69, "TrackerEndcapN_1"},
    {70, "TrackerEndcapN_2"},
    {71, "TrackerEndcapN_3"},
    {72, "TrackerEndcapN_4"},
    {73, "TrackerEndcapN_5"},
    {74, "TrackerEndcapN_6"},
    {75, "TrackerEndcapN_7"},
    {76, "TrackerEndcapN_8"},
    {77, "TrackerEndcapP_0"},
    {78, "TrackerEndcapP_1"},
    {79, "TrackerEndcapP_2"},
    {80, "TrackerEndcapP_3"},
    {81, "TrackerEndcapP_4"},
    {82, "TrackerEndcapP_5"},
    {83, "TrackerEndcapP_6"},
    {84, "TrackerSupport_0"},
    {85, "TrackerSupport_1"},
    {90, "BarrelDIRC"},
    {91, "BarrelTRD"},
    {92, "BarrelTOF"},
    {93, "TOFSubAssembly"},
    {100, "EcalSubAssembly"},
    {101, "EcalBarrel"},
    {102, "EcalEndcapP"},
    {103, "EcalEndcapN"},
    {104, "CrystalEndcap"},
    {105, "EcalBarrel2"},
    {106, "EcalEndcapPInsert"},
    {110, "HcalSubAssembly"},
    {111, "HcalBarrel"},
    {113, "HcalEndcapN"},
    {114, "PassiveSteelRingEndcapP"},
    {115, "HcalEndcapPInsert"},
    {116, "LFHCAL"},
    {120, "ForwardRICH"},
    {121, "ForwardTRD"},
    {122, "ForwardTOF"},
    {131, "BackwardRICH"},
    {132, "BackwardTOF"},
    {140, "Solenoid"},
    {141, "SolenoidSupport"},
    {142, "SolenoidYoke"},
    {150, "B0Tracker_Station_1"},
    {151, "B0Tracker_Station_2"},
    {152, "B0Tracker_Station_3"},
    {153, "B0Tracker_Station_4"},
    {154, "B0Preshower_Station_1"},
    {155, "ForwardRomanPot_Station_1"},
    {156, "ForwardRomanPot_Station_2"},
    {157, "B0TrackerCompanion"},
    {158, "B0TrackerSubAssembly"},
    {159, "ForwardOffMTracker_station_1"},
    {160, "ForwardOffMTracker_station_2"},
    {161, "ForwardOffMTracker_station_3"},
    {162, "ForwardOffMTracker_station_4"},
    {163, "ZDC_1stSilicon"},
    {164, "ZDC_Crystal"},
    {165, "ZDC_WSi"},
    {166, "ZDC_PbSi"},
    {167, "ZDC_PbSci"},
    {168, "VacuumMagnetElement_1"},
    {169, "B0ECal"},
    {170, "B0PF"},
    {171, "B0APF"},
    {172, "Q1APF"},
    {173, "Q1BPF"},
    {174, "Q2PF"},
    {175, "B1PF"},
    {176, "B1APF"},
    {177, "B2PF"},
    {180, "Q0EF"},
    {181, "Q1EF"},
    {182, "B0Window"},
    {190, "LumiCollimator"},
    {191, "LumiDipole"},
    {192, "LumiWindow"},
    {193, "LumiSpecTracker"},
    {194, "LumiSpecCAL"},
    {195, "LumiDirectPCAL"},
    {197, "BackwardsBeamline"},
    {198, "TaggerTracker"},
    {199, "TaggerCalorimeter"}
};

/// Gets detector system ID and name from full cellID

std::tuple<uint64_t, std::string> get_detector_info(uint64_t cell_id) {
    uint64_t system_id = cell_id & 0xFF;  // system_id is saved in the least significant 8 bits (ha!)

    auto it = system_names_by_ids.find(system_id);
    std::string system_name;
    if (it != system_names_by_ids.end()) {
        system_name = it->second;
    } else {
        auto err_msg = std::format("system_names_by_id not found for system: {} . Full cell ID: {}", system_id, cell_id);
        throw std::out_of_range(err_msg);
    }
    return {system_id, system_name};
}


/// Utility function, finds tracker_hit by raw_hit
std::expected<edm4eic::TrackerHit, std::string> get_tracker_hit(const edm4eic::RawTrackerHit & raw_hit, const edm4eic::TrackerHitCollection & tracker_hits) {
    for (const auto & tracker_hit: tracker_hits){
        if (tracker_hit.getRawHit().id() == raw_hit.id())
            return tracker_hit;
    }
    return std::unexpected(std::format("edm4eic::TrackerHit was not found for raw hit with index: {}", raw_hit.id().index));
}


// Specialized function for Tracker Hits
void process_tracker_hits(const podio::Frame& event, const std::string& assoc_col_name, int evt_id) {

    const auto& hit_assocs = event.get<edm4eic::MCRecoTrackerHitAssociationCollection>(assoc_col_name);

    // We get corresponding tracker hits collection before hits iteration. We will need it there.
    const auto& traker_col_name = tracker_names_by_assoc.at(assoc_col_name);
    const auto& tracker_hits = event.get<edm4eic::TrackerHitCollection>(traker_col_name);

    // Write header if needed
    if (!trk_hits_header_written) {
        csv_trk_hits << HitRecord::make_csv_header() << "\n";
        trk_hits_header_written = true;
    }

    for (const auto& hit_assoc : hit_assocs) {

        // Since all the warning are ~the same, we create this printing functions.
        auto warn = [&](std::string_view msg) {
            fmt::print("WARNING! process_tracker_hits event={} col={} hit_assoc.index:{}. {}\n",
                       evt_id, assoc_col_name, hit_assoc.id().index, msg);
        };

        // Check we have a RawHit
        if (!hit_assoc.getRawHit().isAvailable()) {
            warn("!hit_assoc.getRawHit().isAvailable()");
            continue;
        }

        // Check we have a SimHit
        if (!hit_assoc.getSimHit().isAvailable()) {
            warn("!hit_assoc.getSimHit().isAvailable()");
            continue;
        }

        // Check we have a MCParticle
        if (!hit_assoc.getSimHit().getParticle().isAvailable()) {
            warn("!hit_assoc.getSimHit().getParticle().isAvailable()");
            continue;
        }

        // Pull raw hit
        auto & raw_hit = hit_assoc.getRawHit();

        // Find TRacker hit for this raw hit
        auto find_result = get_tracker_hit(raw_hit, tracker_hits);
        if (!find_result) {
            warn(find_result.error());
            continue;
        }
        auto & trk_hit = find_result.value();

        // Pull sim hit and particle
        auto & sim_hit = hit_assoc.getSimHit();
        auto & particle = sim_hit.getParticle();

        // We now have all info to fill our CSV line!

        //
        if (sim_hit.getParticle().getGeneratorStatus() < 10) {
            fmt::print("evt_id:{:<5} col:{:<35} hit_idx:{:<7} prt_id:{:<7}, prt_pid:{:<5}, prt_gstat:{:<8}, prt_sstat:{:<6}, prt_e:{:.3}\n",
                evt_id,
                assoc_col_name,
                hit_assoc.id().index,

                sim_hit.getParticle().id().index,
                sim_hit.getParticle().getPDG(),
                sim_hit.getParticle().getGeneratorStatus(),
                sim_hit.getParticle().getSimulatorStatus(),
                sim_hit.getParticle().getEnergy()
                );
        }

        HitRecord record;
        record.evt = evt_id;
        record.hit_index = hit_assoc.id().index;
        record.prt_index = particle.id().index;
        record.prt_pdg = particle.getPDG();
        record.prt_status = particle.getGeneratorStatus();
        record.prt_energy = particle.getEnergy();
        record.prt_charge = particle.getCharge();
        record.prt_mom_x = particle.getMomentum().x;
        record.prt_mom_y = particle.getMomentum().y;
        record.prt_mom_z = particle.getMomentum().z;
        record.prt_vtx_time = particle.getTime();
        record.prt_vtx_pos_x = particle.getVertex().x;
        record.prt_vtx_pos_y = particle.getVertex().y;
        record.prt_vtx_pos_z = particle.getVertex().z;
        record.prt_end_time = particle.getTime();  // Note: EDM4hep doesn't have separate end time
        record.prt_end_pos_x = particle.getEndpoint().x;
        record.prt_end_pos_y = particle.getEndpoint().y;
        record.prt_end_pos_z = particle.getEndpoint().z;

        record.trk_hit_cell_id = trk_hit.getCellID();
        std::tie(record.trk_hit_system_id, record.trk_hit_system_name) = get_detector_info(record.trk_hit_cell_id);
        record.trk_hit_pos_x = trk_hit.getPosition().x;
        record.trk_hit_pos_y = trk_hit.getPosition().y;
        record.trk_hit_pos_z = trk_hit.getPosition().z;
        record.trk_hit_time = trk_hit.getTime();
        record.trk_hit_pos_err_xx = trk_hit.getPositionError().xx;
        record.trk_hit_pos_err_yy = trk_hit.getPositionError().yy;
        record.trk_hit_pos_err_zz = trk_hit.getPositionError().zz;
        record.trk_hit_time_err = trk_hit.getTimeError();
        record.trk_hit_edep = trk_hit.getEdep();
        record.trk_hit_edep_err = trk_hit.getEdepError();

        // Write record to CSV
        csv_trk_hits << record.get_csv_line() << "\n";
    }
}



// Specialized function for Calorimeter Hits
void process_calo_hits(const podio::Frame& event, const std::string& collection_name, int evt_id) {

    const auto& hit_assocs = event.get<edm4eic::MCRecoCalorimeterHitAssociationCollection>(collection_name);

    for (const auto& hit_assoc : hit_assocs) {
        //hit_assoc.getSimHit().getContributions()
        hit_assoc.getSimHit();

        // Since all the warning are ~the same, we create this printing functions.
        auto warn = [&](std::string_view msg) {
            fmt::print("WARNING! process_calo_hits event={} col={} hit_assoc.index:{}. {}\n",
                       evt_id, collection_name, hit_assoc.id().index, msg);
        };

        // Check we have a RawHit
        if (!hit_assoc.getRawHit().isAvailable()) {
            warn("!hit_assoc.getRawHit().isAvailable()");
            continue;
        }

        // Check we have a SimHit
        if (!hit_assoc.getSimHit().isAvailable()) {
            warn("!hit_assoc.getSimHit().isAvailable()");
            continue;
        }

        // Check we have a Contributions
        if (hit_assoc.getSimHit().getContributions().empty()) {
            warn("hit_assoc.getSimHit().getContributions().empty()");
            continue;
        }

        // Check we have at least one MCParticle
        if (!hit_assoc.getSimHit().getContributions().at(0).getParticle().isAvailable()) {
            warn("hit_assoc.getSimHit().getContributions().at(0).getParticle().isAvailable()");
            continue;
        }

        // Pull raw hit
        auto & raw_hit = hit_assoc.getRawHit();

        // Pull sim hit and particle
        auto & sim_hit = hit_assoc.getSimHit();

        auto [system_id, system_name] = get_detector_info(raw_hit.getCellID());

        if (evt_id < 3 && hit_assoc.id().index < 10) {
            fmt::print("evt_id:{:<5} col:{:<35} hit_idx:{:<7} sys_id:{:<7}, sys:{:<20}, amp:{:<8}, ts:{:<6}, nc:{:<6} c0_time:{:.5f} \n",
                evt_id,
                collection_name,
                hit_assoc.id().index,
                system_id,
                system_name,
                raw_hit.getAmplitude(),
                raw_hit.getTimeStamp(),
                sim_hit.getContributions().size(),
                sim_hit.getContributions().at(0).getTime()
                );
        }

    }


}


//------------------------------------------------------------------------------
// event processing
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int evt_id) {

    for (const auto& trk_assoc_name: track_associations) {
        process_tracker_hits(event, trk_assoc_name, evt_id);
    }

    for (const auto& cal_assoc_name: cal_associations) {
        //process_calo_hits(event, cal_assoc_name, evt_id);
    }


    // const auto& particles = event.get<MCParticleCollection>("MCParticles");
    //
    // for (const auto& lam: particles) {
    //     if (lam.getPDG() != 3122) continue; // not Λ⁰
    //
    //     // Check if it decays to p + pi-
    //     auto daughters = lam.getDaughters();
    //     if (daughters.size() != 2) continue;
    //
    //     std::optional<MCParticle> prot, pimin;
    //
    //     // Check decay products
    //     bool is_ppim = false;
    //     if (daughters.at(0).getPDG() == 2212 && daughters.at(1).getPDG() == -211) {
    //         is_ppim = true;
    //         prot = daughters.at(0);
    //         pimin = daughters.at(1);
    //     } else if (daughters.at(1).getPDG() == 2212 && daughters.at(0).getPDG() == -211) {
    //         is_ppim = true;
    //         prot = daughters.at(1);
    //         pimin = daughters.at(0);
    //     }
    //
    //     if (!is_ppim) continue;
    //
    //     // We found a Lambda -> p + pi- decay
    //     int lam_id = lam.getObjectID().index;
    //
    //     // Prepare detection map
    //     std::map<std::string, bool> detection_map;
    //
    //     // Process Proton
    //     if (prot) {
    //         for (const auto& name : tracker_collections) {
    //             process_tracker_hits(event, name, *prot, csv_prot_hits, evt_id, lam_id, detection_map, "prot");
    //         }
    //         for (const auto& name : calorimeter_collections) {
    //             process_calo_hits(event, name, *prot, csv_prot_hits, evt_id, lam_id, detection_map, "prot");
    //         }
    //     }
    //
    //     // Process Pion
    //     if (pimin) {
    //         for (const auto& name : tracker_collections) {
    //             process_tracker_hits(event, name, *pimin, csv_pimin_hits, evt_id, lam_id, detection_map, "pimin");
    //         }
    //         for (const auto& name : calorimeter_collections) {
    //             process_calo_hits(event, name, *pimin, csv_pimin_hits, evt_id, lam_id, detection_map, "pimin");
    //         }
    //     }
    //
    //     // Write Main CSV Header if needed
    //     if (!header_written) {
    //         csv << "event,lam_id,"
    //             << make_particle_header("lam") << ","
    //             << make_particle_header("prot") << ","
    //             << make_particle_header("pimin");
    //
    //         // Add columns for detection flags
    //         for (const auto& name : tracker_collections) {
    //             csv << ",prot_" << name;
    //         }
    //         for (const auto& name : calorimeter_collections) {
    //             csv << ",prot_" << name;
    //         }
    //          for (const auto& name : tracker_collections) {
    //             csv << ",pimin_" << name;
    //         }
    //         for (const auto& name : calorimeter_collections) {
    //             csv << ",pimin_" << name;
    //         }
    //         csv << "\n";
    //         header_written = true;
    //     }
    //
    //     // Write Main CSV Data
    //     csv << evt_id << "," << lam_id << ","
    //         << particle_to_csv(lam) << ","
    //         << particle_to_csv(prot) << ","
    //         << particle_to_csv(pimin);
    //
    //     // Write flags
    //     for (const auto& name : tracker_collections) csv << "," << detection_map["prot_" + name];
    //     for (const auto& name : calorimeter_collections) csv << "," << detection_map["prot_" + name];
    //     for (const auto& name : tracker_collections) csv << "," << detection_map["pimin_" + name];
    //     for (const auto& name : calorimeter_collections) csv << "," << detection_map["pimin_" + name];
    //
    //     csv << "\n";
    //
    //     // We only process the first lambda per event?
    //     // The requirement says "first two colums must be event id and lambda id".
    //     // It implies we might have multiple lambdas or we just need to identify them.
    //     // The npi0 script breaks after first lambda.
    //     // "break; // we only need first lambdas. One lambda per event."
    //     // I will follow the same pattern for consistency unless instructed otherwise.
    //     // But wait, the user said "first two colums must be event id and lambda id".
    //     // If I break, I only get one.
    //     // The npi0 script has:
    //     // if (!header_written) { ... }
    //     // csv << ...
    //     // is_first_lambda = false;
    //     // break;
    //     // So it strictly does one lambda per event. I will do the same.
    //     break;
    // }
}

//------------------------------------------------------------------------------
// file loop
//------------------------------------------------------------------------------
void process_file(const std::string& file_name) {
    podio::ROOTReader reader;
    try {
        reader.openFile(file_name);
    }
    catch (const std::runtime_error&e) {
        fmt::print(stderr, "Error opening file {}: {}\n", file_name, e.what());
        return;
    }

    const auto event_count = reader.getEntries(podio::Category::Event);

    for (unsigned ie = 0; ie < event_count; ++ie) {
        if (events_limit > 0 && total_evt_processed >= events_limit) return;

        podio::Frame evt(reader.readNextEntry(podio::Category::Event));
        process_event(evt, total_evt_processed);
        ++total_evt_processed;
    }
}


// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt:  root -x -l -b -q 'cpp_03_hits_edm4eic.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void cpp_03_hits_edm4eic(const char* infile, const char* outfile, int events = -1)
{
    fmt::print("'cpp_03_hits_edm4eic' entry point is used.\n");

    csv.open(outfile);

    std::string out_str = outfile;
    std::string trk_hits_fname = out_str + "_trk_hits.csv";
    std::string cal_hits_fname = out_str + "_cal_hits.csv";

    if (out_str.size() > 4 && out_str.substr(out_str.size() - 4) == ".csv") {
        std::string base = out_str.substr(0, out_str.size() - 4);
        trk_hits_fname = base + "_trk_hits.csv";
        cal_hits_fname = base + "_cal_hits.csv";
    }

    csv_trk_hits.open(trk_hits_fname);
    csv_cal_hits.open(cal_hits_fname);

    if (!csv || !csv_trk_hits || !csv_cal_hits) {
        fmt::print(stderr, "error: cannot open output files\n");
        exit(1);
    }

    events_limit = events;
    process_file(infile);

    csv.close();
    csv_trk_hits.close();
    csv_cal_hits.close();

    fmt::print("\nWrote data for {} events to {}\n", total_evt_processed, outfile);
    fmt::print("Tracker hits written to: {}\n", trk_hits_fname);
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

    cpp_03_hits_edm4eic(infiles[0].c_str(), out_name.c_str(), events_limit);

    return 0;
}