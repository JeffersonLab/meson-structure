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

    // Write csv header?
    if (!header_written) {
        csv << "evt";
        for (const auto&name: kinDict | std::views::keys) {

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
        csv  << '\n';
        header_written = true;
    }

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