#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif

// acceptance.cxx
// Reads edm4hep/edm4eic SimTrackerHit and SimCalorimeterHit collections,
// produces ROOT histograms + PNGs of:
//   - total number of tracker hits per event
//   - total number of calorimeter hits per event
//   - per-detector hit multiplicity for every tracker / calorimeter on the lists
//
// Input patterns support shell wildcards (e.g. "dir/*.root"), expanded via
// TChain::Add — see https://root.cern/root/html602/TChain.html#TChain:Add@1
//
// Usage (compiled):
//   ./acceptance [-n N] [-o output_dir] "input*.root" [more_patterns ...]
//
// Usage (ROOT macro, single pattern):
//   root -x -l -b -q 'acceptance.cxx("input.edm4hep.root","out_dir",100)'
//
// Usage (ROOT macro, wildcards and/or comma-separated patterns):
//   root -x -l -b -q 'acceptance.cxx("dir/*.root","out_dir",100)'
//   root -x -l -b -q 'acceptance.cxx("f1.root,dir/*.root","out_dir",100)'

// NOTE: we deliberately do NOT include edm4hep's SimTrackerHitCollection.h
// or SimCalorimeterHitCollection.h. In the edm4hep version installed here
// those headers pull in an inline `operator<` on MutableSimTrackerHit /
// MutableSimCalorimeterHit that references `podio::detail::getOrderKey` via
// an ADL customization point, and no matching `getOrderKey(...)` overload is
// declared for those hit types -> header parsing fails.
//
// We only need the hit count per event, and `podio::CollectionBase` already
// exposes `size()` as a virtual method. So we access collections through the
// non-template `Frame::get(name)` overload that returns a
// `const podio::CollectionBase*` and call `size()` directly.
#include "podio/Frame.h"
#include "podio/ROOTReader.h"
#include "podio/CollectionBase.h"

#include <fmt/core.h>
#include <fmt/ostream.h>

#include <TFile.h>
#include <TH1D.h>
#include <TCanvas.h>
#include <TSystem.h>
#include <TChain.h>
#include <TChainElement.h>
#include <TObjArray.h>

#include <map>
#include <string>
#include <vector>
#include <sstream>
#include <cstdlib>

//------------------------------------------------------------------------------
// globals
//------------------------------------------------------------------------------
int         events_limit  = -1;
long        total_evt_seen = 0;
std::string g_output_dir;

TFile* out_file = nullptr;

// List of trackers (taken from csv_edm4hep_acceptance_ppim.cxx)
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

// List of calorimeters (taken from csv_edm4hep_acceptance_npi0.cxx / ppim.cxx)
const std::vector<std::string> calorimeter_collections = {
    "EcalFarForwardZDCHits",
    "B0ECalHits",
    "EcalEndcapPHits",
    "EcalEndcapPInsertHits",
    "HcalFarForwardZDCHits",
    "HcalEndcapPInsertHits",
    "LFHCALHits"
};

//------------------------------------------------------------------------------
// Histograms
//------------------------------------------------------------------------------
TH1D* h_evt_total_tracker_hits = nullptr;
TH1D* h_evt_total_calo_hits    = nullptr;

// per-detector hit-count-per-event histograms, keyed by collection name
std::map<std::string, TH1D*> h_tracker_hits;
std::map<std::string, TH1D*> h_calo_hits;

//------------------------------------------------------------------------------
// coll_size: return the number of hits in the named collection, or 0 if the
// collection is not present in the event. Uses the non-template
// Frame::get(name) overload (returns const CollectionBase*) + virtual
// CollectionBase::size(), so we don't need the concrete collection type.
//------------------------------------------------------------------------------
inline long coll_size(const podio::Frame& frame, const std::string& name) {
    const podio::CollectionBase* base = frame.get(name);
    return base ? static_cast<long>(base->size()) : 0;
}

//------------------------------------------------------------------------------
// png_save: draw one histogram to a PNG in g_output_dir
//------------------------------------------------------------------------------
void png_save(TH1* h) {
    if (!h) return;
    TCanvas c("c_tmp", "", 800, 600);
    c.SetLeftMargin(0.12);
    if (h->InheritsFrom("TH2")) {
        c.SetRightMargin(0.14);
        h->Draw("COLZ");
    } else {
        h->Draw("HIST");
    }
    std::string path = g_output_dir + "/" + h->GetName() + ".png";
    c.SaveAs(path.c_str());
}

//------------------------------------------------------------------------------
// create_histograms
//------------------------------------------------------------------------------
void create_histograms() {
    h_evt_total_tracker_hits = new TH1D("h_evt_total_tracker_hits",
        "Total tracker hits per event;N hits;Events", 200, 0, 20000);
    h_evt_total_calo_hits = new TH1D("h_evt_total_calo_hits",
        "Total calorimeter hits per event;N hits;Events", 200, 0, 20000);

    for (const auto& name : tracker_collections) {
        std::string hname = "h_tracker_" + name;
        std::string title = fmt::format("{} hits per event;N hits;Events", name);
        h_tracker_hits[name] = new TH1D(hname.c_str(), title.c_str(), 200, 0, 2000);
    }
    for (const auto& name : calorimeter_collections) {
        std::string hname = "h_calo_" + name;
        std::string title = fmt::format("{} hits per event;N hits;Events", name);
        h_calo_hits[name] = new TH1D(hname.c_str(), title.c_str(), 200, 0, 2000);
    }
}

//------------------------------------------------------------------------------
// save_all_pngs
//------------------------------------------------------------------------------
void save_all_pngs() {
    fmt::print("\nSaving PNG images to {}/\n", g_output_dir);
    png_save(h_evt_total_tracker_hits);
    png_save(h_evt_total_calo_hits);
    for (const auto& name : tracker_collections)    png_save(h_tracker_hits[name]);
    for (const auto& name : calorimeter_collections) png_save(h_calo_hits[name]);
}

//------------------------------------------------------------------------------
// process_event
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int /*evt_id*/) {
    long total_tracker = 0;
    long total_calo    = 0;

    for (const auto& name : tracker_collections) {
        const long n = coll_size(event, name);
        h_tracker_hits[name]->Fill(static_cast<double>(n));
        total_tracker += n;
    }

    for (const auto& name : calorimeter_collections) {
        const long n = coll_size(event, name);
        h_calo_hits[name]->Fill(static_cast<double>(n));
        total_calo += n;
    }

    h_evt_total_tracker_hits->Fill(static_cast<double>(total_tracker));
    h_evt_total_calo_hits->Fill(static_cast<double>(total_calo));
}

//------------------------------------------------------------------------------
// process_file
//------------------------------------------------------------------------------
void process_file(const std::string& fname) {
    podio::ROOTReader rdr;
    try {
        rdr.openFile(fname);
    } catch (const std::runtime_error& e) {
        fmt::print(stderr, "Error opening file {}: {}\n", fname, e.what());
        return;
    }
    const auto nEv = rdr.getEntries(podio::Category::Event);
    fmt::print("  File: {} ({} events)\n", fname, nEv);

    for (unsigned ie = 0; ie < nEv; ++ie) {
        if (events_limit > 0 && total_evt_seen >= events_limit) return;
        podio::Frame evt(rdr.readNextEntry(podio::Category::Event));
        process_event(evt, total_evt_seen);
        ++total_evt_seen;
    }
}

//------------------------------------------------------------------------------
// prepare_output_dir
//------------------------------------------------------------------------------
void prepare_output_dir(const std::string& dir) {
    gSystem->mkdir(dir.c_str(), kTRUE);
}

//------------------------------------------------------------------------------
// split_csv
//------------------------------------------------------------------------------
std::vector<std::string> split_csv(const std::string& s) {
    std::vector<std::string> result;
    std::istringstream ss(s);
    std::string token;
    while (std::getline(ss, token, ',')) {
        if (!token.empty()) result.push_back(token);
    }
    return result;
}

//------------------------------------------------------------------------------
// expand_files_with_tchain: resolve a list of input patterns (which may
// contain shell wildcards like "dir/*.root") into a concrete list of file
// paths. We use TChain::Add purely for its wildcard-expansion machinery —
// the actual event reading still goes through podio::ROOTReader, because
// podio collections can't be read via the generic TTree interface.
//
// See https://root.cern/root/html602/TChain.html#TChain:Add@1
//------------------------------------------------------------------------------
std::vector<std::string> expand_files_with_tchain(const std::vector<std::string>& patterns) {
    // "events" is the tree name podio writes event data into. TChain just
    // stores it in each TChainElement; we never actually open the trees here.
    TChain chain("events");
    for (const auto& p : patterns) {
        chain.Add(p.c_str());
    }
    std::vector<std::string> result;
    TObjArray* files = chain.GetListOfFiles();
    if (!files) return result;
    for (int i = 0; i < files->GetEntries(); ++i) {
        auto* el = dynamic_cast<TChainElement*>(files->At(i));
        if (el) result.emplace_back(el->GetTitle());
    }
    return result;
}

//------------------------------------------------------------------------------
// run
//------------------------------------------------------------------------------
void run(const std::vector<std::string>& input_patterns) {
    prepare_output_dir(g_output_dir);

    // Expand shell wildcards through TChain before touching podio.
    auto infiles = expand_files_with_tchain(input_patterns);
    if (infiles.empty()) {
        fmt::print(stderr, "error: no input files matched the provided patterns\n");
        for (const auto& p : input_patterns) fmt::print(stderr, "  pattern: {}\n", p);
        return;
    }
    fmt::print("Resolved {} input file(s):\n", infiles.size());
    for (const auto& f : infiles) fmt::print("  {}\n", f);

    std::string root_out = g_output_dir + "/acceptance.root";
    out_file = TFile::Open(root_out.c_str(), "RECREATE");
    if (!out_file || out_file->IsZombie()) {
        fmt::print(stderr, "error: cannot open output file {}\n", root_out);
        return;
    }

    create_histograms();

    for (const auto& f : infiles) {
        process_file(f);
        if (events_limit > 0 && total_evt_seen >= events_limit) break;
    }

    save_all_pngs();

    out_file->Write();
    out_file->Close();
    fmt::print("\nWrote {} events -> {}\n", total_evt_seen, root_out);
}

//------------------------------------------------------------------------------
// main (compiled mode)
//   ./acceptance [-n N] [-o output_dir] <pattern> [<pattern> ...]
// Patterns may include shell wildcards (quote them to defer to TChain).
//------------------------------------------------------------------------------
int main(int argc, char* argv[]) {
    std::vector<std::string> patterns;
    g_output_dir = "acceptance_out";

    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "-n" && i + 1 < argc)      events_limit = std::atoi(argv[++i]);
        else if (a == "-o" && i + 1 < argc) g_output_dir = argv[++i];
        else if (a == "-h" || a == "--help") {
            fmt::print("usage: {} [-n N] [-o output_dir] <pattern> [<pattern> ...]\n", argv[0]);
            fmt::print("  Patterns may use shell wildcards (e.g. \"dir/*.root\").\n");
            return 0;
        }
        else if (!a.empty() && a[0] != '-') patterns.emplace_back(a);
        else { fmt::print(stderr, "unknown option {}\n", a); return 1; }
    }
    if (patterns.empty()) { fmt::print(stderr, "error: no input patterns\n"); return 1; }

    run(patterns);
    return 0;
}

// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// Single pattern:
//   root -x -l -b -q 'acceptance.cxx("input.edm4hep.root","out_dir",100)'
// Wildcards and/or comma-separated patterns:
//   root -x -l -b -q 'acceptance.cxx("dir/*.root","out_dir",100)'
//   root -x -l -b -q 'acceptance.cxx("f1.root,dir/*.root","out_dir",100)'
// ---------------------------------------------------------------------------
void acceptance(const char* infiles_csv,
                const char* output_dir = "acceptance_out",
                int events = -1)
{
    fmt::print("'acceptance' ROOT macro\n");
    fmt::print("  infiles:    {}\n", infiles_csv);
    fmt::print("  output_dir: {}\n", output_dir);
    fmt::print("  events:     {} {}\n", events, (events == -1 ? "(all)" : ""));

    g_output_dir   = output_dir;
    events_limit   = events;
    total_evt_seen = 0;

    auto patterns = split_csv(infiles_csv);
    if (patterns.empty()) {
        fmt::print(stderr, "error: no input patterns in '{}'\n", infiles_csv);
        return;
    }

    run(patterns);
}
