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
#include <edm4eic/InclusiveKinematicsCollection.h>
#include <edm4eic/ReconstructedParticleCollection.h>

#include <fmt/core.h>
#include <fmt/ostream.h>

#include <TFile.h>
#include <TLorentzVector.h>

#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <cmath>
#include <csignal>

using namespace edm4hep;
using namespace edm4eic;

//------------------------------------------------------------------------------
// globals & helpers
//------------------------------------------------------------------------------
int events_limit = -1; // -n  <N>
long total_evt_seen = 0;
std::ofstream csv;
bool header_written = false;

// Particle masses in GeV
constexpr double PROTON_MASS = 0.938272;
constexpr double LAMBDA_MASS = 1.115683;

//------------------------------------------------------------------------------
// Helper structures
//------------------------------------------------------------------------------
struct ParticleData {
    bool valid = false;
    double px = 0.0;
    double py = 0.0;
    double pz = 0.0;
    double energy = 0.0;
    double t_value = 0.0;
};

//------------------------------------------------------------------------------
// Helper functions
//------------------------------------------------------------------------------

/**
 * @brief Calculate Mandelstam t from two four-vectors
 * @param p1 First four-vector (incident)
 * @param p2 Second four-vector (outgoing)
 * @return t = (p1 - p2)^2
 */
inline double calculate_t(const TLorentzVector& p1, const TLorentzVector& p2) {
    TLorentzVector q = p1 - p2;
    return q.M2();
}

/**
 * @brief Create TLorentzVector from particle momentum and mass
 * @param px X-component of momentum
 * @param py Y-component of momentum
 * @param pz Z-component of momentum
 * @param mass Particle mass in GeV
 * @return TLorentzVector
 */
TLorentzVector create_lorentz_vector(double px, double py, double pz, double mass) {
    double energy = std::sqrt(px*px + py*py + pz*pz + mass*mass);
    TLorentzVector vec;
    vec.SetPxPyPzE(px, py, pz, energy);
    return vec;
}

/**
 * @brief Find beam proton and MC Lambda in particle collection and return ParticleData
 * @param mcParticles MC particle collection
 * @return pair of <beam_proton_data, mc_lambda_data>
 */
std::pair<ParticleData, ParticleData> find_mc_particles(const MCParticleCollection& mcParticles) {
    ParticleData beam_proton_data;
    ParticleData mc_lambda_data;
    TLorentzVector beam_proton_vec;
    bool found_beam_proton = false;

    // First pass: find beam proton
    for (const auto& p : mcParticles) {
        if (!found_beam_proton && p.getPDG() == 2212) {  // proton
            const auto mom = p.getMomentum();
            beam_proton_data.valid = true;
            beam_proton_data.px = mom.x;
            beam_proton_data.py = mom.y;
            beam_proton_data.pz = mom.z;
            beam_proton_vec = create_lorentz_vector(mom.x, mom.y, mom.z, PROTON_MASS);
            beam_proton_data.energy = beam_proton_vec.E();
            found_beam_proton = true;
            break;
        }
    }

    // Second pass: find Lambda and calculate t if beam proton was found
    if (found_beam_proton) {
        for (const auto& p : mcParticles) {
            if (p.getPDG() == 3122) {  // Lambda
                const auto mom = p.getMomentum();
                mc_lambda_data.valid = true;
                mc_lambda_data.px = mom.x;
                mc_lambda_data.py = mom.y;
                mc_lambda_data.pz = mom.z;

                TLorentzVector lam_vec = create_lorentz_vector(mom.x, mom.y, mom.z, LAMBDA_MASS);
                mc_lambda_data.energy = lam_vec.E();
                mc_lambda_data.t_value = calculate_t(beam_proton_vec, lam_vec);
                break;
            }
        }
    }

    return {beam_proton_data, mc_lambda_data};
}

/**
 * @brief Process reconstructed Lambda and calculate t
 * @param ff_lambdas Collection of reconstructed Lambdas
 * @param beam_proton_data Beam proton data with momentum
 * @return ParticleData with momentum and t value
 */
ParticleData process_ff_lambda(const ReconstructedParticleCollection& ff_lambdas,
                               const ParticleData& beam_proton_data) {
    ParticleData data;

    // Only process if we have a valid beam proton
    if (!beam_proton_data.valid) {
        return data;
    }

    // Create beam proton TLorentzVector
    TLorentzVector beam_proton_vec = create_lorentz_vector(
        beam_proton_data.px,
        beam_proton_data.py,
        beam_proton_data.pz,
        PROTON_MASS
    );

    // Process first Lambda in collection
    for (const auto& lam : ff_lambdas) {
        data.valid = true;
        const auto mom = lam.getMomentum();
        data.px = mom.x;
        data.py = mom.y;
        data.pz = mom.z;
        data.energy = lam.getEnergy();

        TLorentzVector lam_vec = create_lorentz_vector(mom.x, mom.y, mom.z, LAMBDA_MASS);
        data.t_value = calculate_t(beam_proton_vec, lam_vec);
        break; // Only process first Lambda
    }

    return data;
}

/**
 * @brief Formats electron particle data into a comma-separated string.
 * @param scat The scattered electron from InclusiveKinematics
 * @param valid Whether the electron data is valid
 * @return A std::string containing the formatted particle data.
 */
inline std::string electron_to_csv(const edm4eic::InclusiveKinematics& ik, bool valid) {
    if (!valid || !ik.getScat().isAvailable()) {
        return ",,,,,,,,,,,,,,,,"; // 16 commas for 17 empty fields
    }

    const auto p = ik.getScat();
    const auto mom = p.getMomentum();
    const auto ref = p.getReferencePoint();

    return fmt::format("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}",
        p.getObjectID().index,           // 01 id
        p.getPDG(),                     // 02 pdg
        p.getCharge(),                  // 03 charge
        p.getEnergy(),                  // 04 energy
        p.getMass(),                    // 05 mass
        mom.x,                           // 06 px
        mom.y,                           // 07 py
        mom.z,                           // 08 pz
        ref.x,                           // 09 ref_x
        ref.y,                           // 10 ref_y
        ref.z,                           // 11 ref_z
        p.getGoodnessOfPID(),           // 12 pid_goodness
        p.getType(),                    // 13 type
        p.getClusters().size(),         // 14 n_clusters
        p.getTracks().size(),           // 15 n_tracks
        p.getParticles().size(),        // 16 n_particles
        p.getParticleIDs().size()       // 17 n_particle_ids
    );
}

//------------------------------------------------------------------------------
// event processing
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int evt_id) {
    using IKColl = edm4eic::InclusiveKinematicsCollection;

    /*---------------------------------------------------------------------------
      Grab the collections
    ---------------------------------------------------------------------------*/
    const auto& kinDA      = event.get<IKColl>("InclusiveKinematicsDA");
    const auto& kinESigma  = event.get<IKColl>("InclusiveKinematicsESigma");
    const auto& kinElectron= event.get<IKColl>("InclusiveKinematicsElectron");
    const auto& kinJB      = event.get<IKColl>("InclusiveKinematicsJB");
    const auto& kinML      = event.get<IKColl>("InclusiveKinematicsML");
    const auto& kinSigma   = event.get<IKColl>("InclusiveKinematicsSigma");

    /*---------------------------------------------------------------------------
      Dictionary: { name , &collection }
    ---------------------------------------------------------------------------*/
    const std::vector<std::pair<std::string_view,const IKColl*>> kinDict = {
        { "da"      , &kinDA       },
        { "esigma"  , &kinESigma   },
        { "electron", &kinElectron },
        { "jb"      , &kinJB       },
        { "ml"      , &kinML       },
        { "sigma"   , &kinSigma    },
    };

    /*---------------------------------------------------------------------------
      Get MC particles and find beam proton and Lambda - now returns ParticleData
    ---------------------------------------------------------------------------*/
    const auto& mcParticles = event.get<MCParticleCollection>("MCParticles");
    auto [beam_proton_data, mc_lambda_data] = find_mc_particles(mcParticles);

    // Skip event if no beam proton found
    if (!beam_proton_data.valid) {
        fmt::print("Warning: No beam proton found in event {}, skipping...\n", evt_id);
        return;
    }

    /*---------------------------------------------------------------------------
      Process reconstructed far-forward Lambda
    ---------------------------------------------------------------------------*/
    const auto& ffLambdas = event.get<ReconstructedParticleCollection>("ReconstructedFarForwardZDCLambdas");
    ParticleData ff_lambda_data = process_ff_lambda(ffLambdas, beam_proton_data);

    /*---------------------------------------------------------------------------
      Write CSV header
    ---------------------------------------------------------------------------*/
    if (!header_written) {
        csv << "evt";
        for (const auto& [name, coll] : kinDict) {

            csv << "," << fmt::format("{}_x",  name);
            csv << "," << fmt::format("{}_q2", name);
            csv << "," << fmt::format("{}_y",  name);
            csv << "," << fmt::format("{}_nu", name);
            csv << "," << fmt::format("{}_w",  name);
        }
        // For Meson-structure analysis we taking true variables from different place, not "InclusiveKinematics*" tables, so put these column names manually
        csv << "," << "mc_x";
        csv << "," << "mc_q2";
        csv << "," << "mc_y";
        csv << "," << "mc_nu";
        csv << "," << "mc_w";

        // Add t-value columns
        csv << "," << "mc_true_t";
        csv << "," << "mc_lam_t";
        csv << "," << "ff_lam_t";

        // Add Lambda momentum columns
        csv << "," << "mc_lam_px";
        csv << "," << "mc_lam_py";
        csv << "," << "mc_lam_pz";
        csv << "," << "ff_lam_px";
        csv << "," << "ff_lam_py";
        csv << "," << "ff_lam_pz";

        // Add electron particle columns
        csv << "," << "elec_id";
        csv << "," << "elec_pdg";
        csv << "," << "elec_charge";
        csv << "," << "elec_energy";
        csv << "," << "elec_mass";
        csv << "," << "elec_px";
        csv << "," << "elec_py";
        csv << "," << "elec_pz";
        csv << "," << "elec_ref_x";
        csv << "," << "elec_ref_y";
        csv << "," << "elec_ref_z";
        csv << "," << "elec_pid_goodness";
        csv << "," << "elec_type";
        csv << "," << "elec_n_clusters";
        csv << "," << "elec_n_tracks";
        csv << "," << "elec_n_particles";
        csv << "," << "elec_n_particle_ids";

        csv  << '\n';
        header_written = true;
    }

    /*---------------------------------------------------------------------------
      Write data
    ---------------------------------------------------------------------------*/
    csv << evt_id;
    for (const auto& [name, coll] : kinDict)
    {
        if (coll->size() != 1) {
            csv << ",,,,,";  // Empty CSV value (null-s)
            continue;
        }

        csv << "," << coll->at(0).getX();
        csv << "," << coll->at(0).getQ2();
        csv << "," << coll->at(0).getY();
        csv << "," << coll->at(0).getNu();
        csv << "," << coll->at(0).getW();
    }

    // Here we add truth information saved in parameters
    csv << "," << event.getParameter<std::string>("dis_xbj").value_or("");
    csv << "," << event.getParameter<std::string>("dis_q2").value_or("");
    csv << "," << event.getParameter<std::string>("dis_y_d").value_or("");
    csv << "," << event.getParameter<std::string>("dis_nu").value_or("");
    csv << "," << event.getParameter<std::string>("dis_w").value_or("");

    // Add t values
    csv << "," << event.getParameter<std::string>("dis_tspectator").value_or("");  // mc_true_t
    csv << "," << (mc_lambda_data.valid ? fmt::format("{}", mc_lambda_data.t_value) : "");
    csv << "," << (ff_lambda_data.valid ? fmt::format("{}", ff_lambda_data.t_value) : "");

    // Add Lambda momenta
    csv << "," << (mc_lambda_data.valid ? fmt::format("{}", mc_lambda_data.px) : "");
    csv << "," << (mc_lambda_data.valid ? fmt::format("{}", mc_lambda_data.py) : "");
    csv << "," << (mc_lambda_data.valid ? fmt::format("{}", mc_lambda_data.pz) : "");
    csv << "," << (ff_lambda_data.valid ? fmt::format("{}", ff_lambda_data.px) : "");
    csv << "," << (ff_lambda_data.valid ? fmt::format("{}", ff_lambda_data.py) : "");
    csv << "," << (ff_lambda_data.valid ? fmt::format("{}", ff_lambda_data.pz) : "");

    // Add electron particle information
    if (kinElectron.size() == 1) {
        csv << "," << electron_to_csv(kinElectron.at(0), true);
    } else {
        // Create a dummy InclusiveKinematics to pass, but with false flag
        csv << ",,,,,,,,,,,,,,,,";  // 17 empty fields
    }

    csv  << '\n';
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
    std::string out_name = "reco_dis.csv";

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
    fmt::print("Wrote data for {} events to {}\n", total_evt_seen, out_name);
    return 0;
}


// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt: root -x -l -b -q 'csv_reco_dis.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void csv_reco_dis(const char* infile, const char* outfile, int events = -1)
{
    fmt::print("'csv_reco_dis' entry point is used. Arguments:\n");
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
    fmt::print("\nDone for {} events {}\n", total_evt_seen, outfile);
}