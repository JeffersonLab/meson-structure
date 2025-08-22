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
constexpr double PROTON_MASS = 0.938272;    // GeV
constexpr double LAMBDA_MASS = 1.115683;    // GeV
constexpr double ELECTRON_MASS = 0.000511;  // GeV
//------------------------------------------------------------------------------
// Note: ParticleData struct removed - using TLorentzVector throughout
//------------------------------------------------------------------------------

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
 * @brief Create TLorentzVector from MCParticle
 * @param p MCParticle
 * @param mass Particle mass in GeV
 * @return TLorentzVector
 */
TLorentzVector mc_to_lorentz_vector(const MCParticle& p, double mass) {
    const auto mom = p.getMomentum();
    return create_lorentz_vector(mom.x, mom.y, mom.z, mass);
}

/**
 *
 * @param true_beam_prot approximate/average beam momentum as known in experiment
 * In real experiment, we don't know real beam particle momentum.
 * There might be 4 beam settings: 5x41, 10x100, 10x130, 18x275
 * Function checks if proton mass is close to known value e.g. 41,
 * if it is close we know we work in 5x41 mode. We use 41 as proton momentum.
 * Then we apply -25mrad in x axis and 600 microrads in y axis to the vector
 * @return TLorentzVector of resulting proton
 */
TLorentzVector calculate_approx_beam(const TLorentzVector& true_beam_prot) {
    // 1) Estimate which running configuration we're in from truth |true_beam_prot|

    const double true_beam_prot_mom = true_beam_prot.P();
    static constexpr double proton_modes[] = {41.0, 100.0, 130.0, 275.0}; // GeV/c
    double fixed_beam_prot_mag = 0.0;
    for (double mode : proton_modes) {
        if (std::abs(true_beam_prot_mom - mode) < 10) {
            fixed_beam_prot_mag = mode;
        }
    }
    // If we're way off any nominal setting, stop
    if (fixed_beam_prot_mag == 0.0) {
        throw std::runtime_error("Could not find nominal proton beam mode");
    }

    // Crossing angles from AfterburnerConfig
    constexpr double crossing_angle_hor = 25e-3;   // -25 mrad in X
    constexpr double crossing_angle_ver = 100e-6;  // 100 microrad in Y

    // Exact formulation for a beam with crossing angles:
    // Starting from +Z direction, apply rotations for crossing angles
    double px = fixed_beam_prot_mag * std::sin(crossing_angle_hor);
    double py = fixed_beam_prot_mag * std::sin(crossing_angle_ver) * std::cos(crossing_angle_hor);
    double pz = fixed_beam_prot_mag * std::cos(crossing_angle_hor) * std::cos(crossing_angle_ver);

    return create_lorentz_vector(px, py, pz, PROTON_MASS);
}

/**
 * @brief Find beam proton and MC Lambda in particle collection and return TLorentzVectors
 * @param mcParticles MC particle collection
 * @return tuple of <beam_proton, beam_electron, scattered_electron, mc_lambda>
 */
std::tuple<TLorentzVector, TLorentzVector, TLorentzVector, TLorentzVector> find_mc_particles(const MCParticleCollection& mcParticles) {
    TLorentzVector beam_proton_vec;
    TLorentzVector beam_elec_vec;
    TLorentzVector scat_elec_vec;
    TLorentzVector mc_lambda_vec;

    bool found_beam_proton = false;
    bool found_beam_elec = false;
    bool found_scat_elec = false;

    // First pass: find all particles
    for (const auto& p : mcParticles) {

        // first proton is beam proton
        if (!found_beam_proton && p.getPDG() == 2212) {
            beam_proton_vec = mc_to_lorentz_vector(p, PROTON_MASS);
            found_beam_proton = true;
        }

        // the first electron is beam electron
        if (!found_beam_elec && p.getPDG() == 11) {
            beam_elec_vec = mc_to_lorentz_vector(p, ELECTRON_MASS);
            found_beam_elec = true;
        }
        // 2nd electron is scattered electron
        else if (found_beam_elec && !found_scat_elec && p.getPDG() == 11) {
            scat_elec_vec = mc_to_lorentz_vector(p, ELECTRON_MASS);
            found_scat_elec = true;
        }

        if (p.getPDG() == 3122) {  // Lambda
            mc_lambda_vec = mc_to_lorentz_vector(p, LAMBDA_MASS);
            // Lambda goes last, if we found lambda, we may stop here
            break;
        }
    }

    return {beam_proton_vec, beam_elec_vec, scat_elec_vec, mc_lambda_vec};
}

/**
 * @brief Process reconstructed Lambda and return TLorentzVector
 * @param ff_lambdas Collection of reconstructed Lambdas
 * @return TLorentzVector of first Lambda (or empty if none found)
 */
TLorentzVector process_ff_lambda(const edm4eic::ReconstructedParticleCollection& ff_lambdas) {
    TLorentzVector lam_vec;

    // Process first Lambda in collection
    for (const auto& lam : ff_lambdas) {
        const auto mom = lam.getMomentum();
        lam_vec = create_lorentz_vector(mom.x, mom.y, mom.z, LAMBDA_MASS);
        break; // Only process first Lambda
    }

    return lam_vec;
}

inline std::string no_electron_to_csv() {
    // Return 13 commas; combined with the preceding comma at call site -> 14 empty fields
    return std::string(13, ',');
}

/**
 * @brief Formats electron particle data into a comma-separated string.
 * @param scat The scattered electron from InclusiveKinematics
 * @param valid Whether the electron data is valid
 * @return A std::string containing the formatted particle data.
 */
inline std::string electron_to_csv(const edm4eic::ReconstructedParticle& scat) {

    const auto mom = scat.getMomentum();
    const auto ref = scat.getReferencePoint();

    return fmt::format("{},{},{},{},{},{},{},{},{},{},{},{},{},{}",
        scat.getObjectID().index,          // 01 id
        scat.getEnergy(),                  // 02 energy
        mom.x,                             // 03 px
        mom.y,                             // 04 py
        mom.z,                             // 05 pz
        ref.x,                             // 06 ref_x
        ref.y,                             // 07 ref_y
        ref.z,                             // 08 ref_z
        scat.getGoodnessOfPID(),           // 09 pid_goodness
        scat.getType(),                    // 10 type
        scat.getClusters().size(),         // 11 n_clusters
        scat.getTracks().size(),           // 12 n_tracks
        scat.getParticles().size(),        // 13 n_particles
        scat.getParticleIDs().size()       // 14 n_particle_ids
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
      Get MC particles and find beam proton and Lambda - now returns TLorentzVectors
    ---------------------------------------------------------------------------*/
    const auto& mcParticles = event.get<MCParticleCollection>("MCParticles");
    auto [beam_proton_vec, beam_elec_vec, mc_scat_elec_vec, mc_lambda_vec] = find_mc_particles(mcParticles);

    // Skip event if no beam proton found
    if (beam_proton_vec.E() == 0) {
        fmt::print("Warning: No beam proton found in event {}, skipping...\n", evt_id);
        return;
    }

    // Calculate approximate beam proton (as in real experiment)
    TLorentzVector assumed_beam_proton_vec = calculate_approx_beam(beam_proton_vec);

    // Calculate t values
    double mc_lambda_t_tb = 0.0;   // MC Lambda with true beam
    double mc_lambda_t_exp = 0.0;  // MC Lambda with experimental beam
    if (mc_lambda_vec.E() > 0) {
        mc_lambda_t_tb = calculate_t(beam_proton_vec, mc_lambda_vec);
        mc_lambda_t_exp = calculate_t(assumed_beam_proton_vec, mc_lambda_vec);
    }

    /*---------------------------------------------------------------------------
      Process reconstructed far-forward Lambda
    ---------------------------------------------------------------------------*/
    const auto& ffLambdas = event.get<edm4eic::ReconstructedParticleCollection>("ReconstructedFarForwardZDCLambdas");
    TLorentzVector ff_lambda_vec = process_ff_lambda(ffLambdas);

    double ff_lambda_t_tb = 0.0;   // FF Lambda with true beam
    double ff_lambda_t_exp = 0.0;  // FF Lambda with experimental beam
    if (ff_lambda_vec.E() > 0) {
        ff_lambda_t_tb = calculate_t(beam_proton_vec, ff_lambda_vec);
        ff_lambda_t_exp = calculate_t(assumed_beam_proton_vec, ff_lambda_vec);
    }

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
        csv << "," << "mc_lam_tb_t";
        csv << "," << "mc_lam_exp_t";
        csv << "," << "ff_lam_tb_t";
        csv << "," << "ff_lam_exp_t";

        // Add electron particle columns
        csv << "," << "elec_id";
        csv << "," << "elec_energy";
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

        // MC true scattered electron
        csv << "," << "mc_elec_px";
        csv << "," << "mc_elec_py";
        csv << "," << "mc_elec_pz";

        // Add Lambda momentum columns
        // true MC lambda
        csv << "," << "mc_lam_px";
        csv << "," << "mc_lam_py";
        csv << "," << "mc_lam_pz";

        // far forward recontructed lambda
        csv << "," << "ff_lam_px";
        csv << "," << "ff_lam_py";
        csv << "," << "ff_lam_pz";

        // beam proton and electron momentums
        csv << "," << "mc_beam_prot_px";
        csv << "," << "mc_beam_prot_py";
        csv << "," << "mc_beam_prot_pz";
        csv << "," << "mc_beam_elec_px";
        csv << "," << "mc_beam_elec_py";
        csv << "," << "mc_beam_elec_pz";

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

    // Add t values (5 columns to match headers)
    std::string mc_true_t = event.getParameter<std::string>("dis_tspectator").value_or("");
    csv << "," << mc_true_t;  // mc_true_t
    csv << "," << (mc_lambda_vec.E() > 0 ? fmt::format("{}", mc_lambda_t_tb) : "");    // mc_lam_tb_t
    csv << "," << (mc_lambda_vec.E() > 0 ? fmt::format("{}", mc_lambda_t_exp) : "");   // mc_lam_exp_t
    csv << "," << (ff_lambda_vec.E() > 0 ? fmt::format("{}", ff_lambda_t_tb) : "");    // ff_lam_tb_t
    csv << "," << (ff_lambda_vec.E() > 0 ? fmt::format("{}", ff_lambda_t_exp) : "");   // ff_lam_exp_t

    // Add electron particle information

    if (kinElectron.size() == 1 && kinElectron.at(0).getScat().isAvailable()) {
        csv << "," << electron_to_csv(kinElectron.at(0).getScat());
    } else {
        csv << "," << no_electron_to_csv();  // 13 empty fields
    }

    // MC true scattered electron
    csv << "," << (mc_scat_elec_vec.E() > 0 ? fmt::format("{}", mc_scat_elec_vec.Px()) : "");
    csv << "," << (mc_scat_elec_vec.E() > 0 ? fmt::format("{}", mc_scat_elec_vec.Py()) : "");
    csv << "," << (mc_scat_elec_vec.E() > 0 ? fmt::format("{}", mc_scat_elec_vec.Pz()) : "");

    // Add Lambda momenta
    // true MC lambda
    csv << "," << (mc_lambda_vec.E() > 0 ? fmt::format("{}", mc_lambda_vec.Px()) : "");
    csv << "," << (mc_lambda_vec.E() > 0 ? fmt::format("{}", mc_lambda_vec.Py()) : "");
    csv << "," << (mc_lambda_vec.E() > 0 ? fmt::format("{}", mc_lambda_vec.Pz()) : "");

    // far forward reconstructed lambda
    csv << "," << (ff_lambda_vec.E() > 0 ? fmt::format("{}", ff_lambda_vec.Px()) : "");
    csv << "," << (ff_lambda_vec.E() > 0 ? fmt::format("{}", ff_lambda_vec.Py()) : "");
    csv << "," << (ff_lambda_vec.E() > 0 ? fmt::format("{}", ff_lambda_vec.Pz()) : "");

    // beam proton and electron momentums
    csv << "," << (beam_proton_vec.E() > 0 ? fmt::format("{}", beam_proton_vec.Px()) : "");
    csv << "," << (beam_proton_vec.E() > 0 ? fmt::format("{}", beam_proton_vec.Py()) : "");
    csv << "," << (beam_proton_vec.E() > 0 ? fmt::format("{}", beam_proton_vec.Pz()) : "");
    csv << "," << (beam_elec_vec.E() > 0 ? fmt::format("{}", beam_elec_vec.Px()) : "");
    csv << "," << (beam_elec_vec.E() > 0 ? fmt::format("{}", beam_elec_vec.Py()) : "");
    csv << "," << (beam_elec_vec.E() > 0 ? fmt::format("{}", beam_elec_vec.Pz()) : "");

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