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
long total_parts_written = 0;
std::ofstream csv;
bool header_written = false;

// The collection holding the final reconstructed particles. Overridable with -c.
std::string collection_name = "ReconstructedParticles";

/**
 * @brief Counts the calorimeter hits attached to a particle through its clusters.
 *
 * Each ReconstructedParticle references Clusters; each Cluster references
 * CalorimeterHits via getHits(). We sum them to report how many calorimeter
 * hits ultimately feed this particle.
 */
inline std::size_t count_cluster_hits(const ReconstructedParticle& p) {
    std::size_t n = 0;
    for (const auto& cl : p.getClusters()) {
        n += cl.getHits().size();
    }
    return n;
}

/**
 * @brief Counts tracker measurements and the tracker hits behind them.
 *
 * Each ReconstructedParticle references Tracks; each Track references
 * Measurement2D objects via getMeasurements(); each Measurement2D references
 * TrackerHits via getHits(). We report both the measurement count and the
 * underlying tracker-hit count.
 */
inline void count_track_hits(const ReconstructedParticle& p,
                             std::size_t& n_measurements,
                             std::size_t& n_tracker_hits) {
    n_measurements = 0;
    n_tracker_hits = 0;
    for (const auto& tr : p.getTracks()) {
        for (const auto& m : tr.getMeasurements()) {
            ++n_measurements;
            n_tracker_hits += m.getHits().size();
        }
    }
}

/**
 * @brief Formats a single reconstructed particle's data (kinematics + relation
 *        multiplicities) into a comma-separated string.
 */
inline std::string reco_particle_to_csv(const ReconstructedParticle& p) {
    const auto mom = p.getMomentum();
    const auto ref = p.getReferencePoint();

    std::size_t n_measurements = 0, n_tracker_hits = 0;
    count_track_hits(p, n_measurements, n_tracker_hits);

    return fmt::format(
        "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}",
        p.getObjectID().index,        // 01 id
        p.getPDG(),                   // 02 pdg
        p.getCharge(),                // 03 charge
        p.getEnergy(),                // 04 energy
        p.getMass(),                  // 05 mass
        mom.x,                        // 06 px
        mom.y,                        // 07 py
        mom.z,                        // 08 pz
        ref.x,                        // 09 ref_x
        ref.y,                        // 10 ref_y
        ref.z,                        // 11 ref_z
        p.getGoodnessOfPID(),         // 12 pid_goodness
        p.getType(),                  // 13 type
        p.getClusters().size(),       // 14 n_clusters
        p.getTracks().size(),         // 15 n_tracks
        p.getParticles().size(),      // 16 n_particles (daughters)
        p.getParticleIDs().size(),    // 17 n_particle_ids
        count_cluster_hits(p),        // 18 n_cluster_hits (calorimeter hits)
        n_measurements,               // 19 n_track_measurements
        n_tracker_hits                // 20 n_tracker_hits
    );
}

/**
 * @brief Creates the CSV header (event column + one reconstructed particle).
 */
std::string make_header() {
    return
        "event,"
        "id,"                   // 01
        "pdg,"                  // 02
        "charge,"               // 03
        "energy,"               // 04
        "mass,"                 // 05
        "px,"                   // 06
        "py,"                   // 07
        "pz,"                   // 08
        "ref_x,"                // 09
        "ref_y,"                // 10
        "ref_z,"                // 11
        "pid_goodness,"         // 12
        "type,"                 // 13
        "n_clusters,"           // 14
        "n_tracks,"             // 15
        "n_particles,"          // 16
        "n_particle_ids,"       // 17
        "n_cluster_hits,"       // 18
        "n_track_measurements," // 19
        "n_tracker_hits";       // 20
}

//------------------------------------------------------------------------------
// event processing
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int evt_id) {

    const auto& parts = event.get<ReconstructedParticleCollection>(collection_name);

    if (!header_written) {
        csv << make_header() << '\n';
        header_written = true;
    }

    for (const auto& p : parts) {
        csv << evt_id << ',' << reco_particle_to_csv(p) << '\n';
        ++total_parts_written;
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
    std::string out_name = "reco_particles.csv";

    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "-n" && i + 1 < argc) events_limit = std::atoi(argv[++i]);
        else if (a == "-o" && i + 1 < argc) out_name = argv[++i];
        else if (a == "-c" && i + 1 < argc) collection_name = argv[++i];
        else if (a == "-h" || a == "--help") {
            fmt::print("usage: {} [-n N] [-o file] [-c collection] input1.root [...]\n", argv[0]);
            fmt::print("  -n N          Process only N events (default: all)\n");
            fmt::print("  -o file       Output CSV file (default: reco_particles.csv)\n");
            fmt::print("  -c collection Reconstructed particle collection (default: ReconstructedParticles)\n");
            fmt::print("\nWrites one row per reconstructed particle with kinematics and\n");
            fmt::print("the number of related clusters/tracks/cluster-hits/tracker-hits.\n");
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
    fmt::print("Collection: {}\n", collection_name);

    for (auto& f : infiles) {
        fmt::print("\n=== Processing file: {} ===\n", f);
        process_file(f);
        if (events_limit > 0 && total_evt_seen >= events_limit) break;
    }

    csv.close();
    fmt::print("\n\nTotal events processed: {}\n", total_evt_seen);
    fmt::print("Total reconstructed particles written: {}\n", total_parts_written);
    fmt::print("Output written to: {}\n", out_name);
    return 0;
}

// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Call it from the prompt:
//   root -x -l -b -q 'csv_reco_particles.cxx("file.root", "output.csv", 100)'
// ---------------------------------------------------------------------------
void csv_reco_particles(const char* infile,
                        const char* outfile = "reco_particles.csv",
                        int events = -1,
                        const char* collection = "ReconstructedParticles") {
    fmt::print("'csv_reco_particles' entry point is used. Arguments:\n");
    fmt::print("  infile:     {}\n", infile);
    fmt::print("  outfile:    {}\n", outfile);
    fmt::print("  events:     {} {}\n", events, (events == -1 ? "(process all)" : ""));
    fmt::print("  collection: {}\n", collection);

    csv.open(outfile);
    if (!csv) {
        fmt::print(stderr, "error: cannot open output file {}\n", outfile);
        return;
    }

    events_limit = events;
    total_evt_seen = 0;
    total_parts_written = 0;
    header_written = false;
    collection_name = collection;

    process_file(infile);

    csv.close();
    fmt::print("\nTotal events processed: {}\n", total_evt_seen);
    fmt::print("Total reconstructed particles written: {}\n", total_parts_written);
    fmt::print("Output written to: {}\n", outfile);
}
