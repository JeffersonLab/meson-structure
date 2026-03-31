#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif

// mcpart_lambda.cxx
// Reads edm4hep/edm4eic MCParticles, finds Lambda decays,
// writes ROOT histograms + a flat TTree (same columns as mcpart_lambda CSV).
//
// Usage (compiled):
//   ./mcpart_lambda [-n N] [-o out.root] input1.root [input2.root ...]
//
// Usage (ROOT macro):
//   root -x -l -b -q 'mcpart_lambda.cxx("input.edm4hep.root","output.root",100)'

#include "podio/Frame.h"
#include "podio/ROOTReader.h"
#include <edm4hep/MCParticleCollection.h>

#include <fmt/core.h>
#include <fmt/ostream.h>

#include <TFile.h>
#include <TH1D.h>
#include <TH2D.h>
#include <TTree.h>
#include <TMath.h>

#include <string>
#include <vector>
#include <cstdlib>
#include <cmath>
#include <optional>

using namespace edm4hep;

//------------------------------------------------------------------------------
// globals
//------------------------------------------------------------------------------
int events_limit = -1;
long total_evt_seen = 0;

// Output ROOT file & tree
TFile* out_file = nullptr;
TTree* tree     = nullptr;

//------------------------------------------------------------------------------
// Tree branch variables  (same columns as CSV)
//------------------------------------------------------------------------------
struct ParticleBranch {
    int    id  = -1;
    int    pdg = 0;
    int    gen = 0;
    int    sim = 0;
    double px  = 0, py = 0, pz = 0;
    double vx  = 0, vy = 0, vz = 0;
    double epx = 0, epy = 0, epz = 0;
    double time = 0;
    int    nd  = 0;

    void clear() { id = -1; pdg = gen = sim = 0; px = py = pz = 0;
                    vx = vy = vz = 0; epx = epy = epz = 0; time = 0; nd = 0; }

    void fill(const MCParticle& p) {
        auto mom = p.getMomentum();
        auto vtx = p.getVertex();
        auto ep  = p.getEndpoint();
        id   = p.getObjectID().index;
        pdg  = p.getPDG();
        gen  = p.getGeneratorStatus();
        sim  = p.getSimulatorStatus();
        px   = mom.x; py = mom.y; pz = mom.z;
        vx   = vtx.x; vy = vtx.y; vz = vtx.z;
        epx  = ep.x;  epy = ep.y; epz = ep.z;
        time = p.getTime();
        nd   = p.getDaughters().size();
    }

    void attach(TTree* t, const std::string& pre) {
        t->Branch((pre + "_id").c_str(),   &id);
        t->Branch((pre + "_pdg").c_str(),  &pdg);
        t->Branch((pre + "_gen").c_str(),  &gen);
        t->Branch((pre + "_sim").c_str(),  &sim);
        t->Branch((pre + "_px").c_str(),   &px);
        t->Branch((pre + "_py").c_str(),   &py);
        t->Branch((pre + "_pz").c_str(),   &pz);
        t->Branch((pre + "_vx").c_str(),   &vx);
        t->Branch((pre + "_vy").c_str(),   &vy);
        t->Branch((pre + "_vz").c_str(),   &vz);
        t->Branch((pre + "_epx").c_str(),  &epx);
        t->Branch((pre + "_epy").c_str(),  &epy);
        t->Branch((pre + "_epz").c_str(),  &epz);
        t->Branch((pre + "_time").c_str(), &time);
        t->Branch((pre + "_nd").c_str(),   &nd);
    }
};

// Event-level branches
int    br_event     = 0;
int    br_lam_is_first = 0;
int    br_lam_decay = 0;

// Per-particle branches
ParticleBranch br_lam, br_prot, br_pimin, br_neut, br_pizero, br_gamone, br_gamtwo;

//------------------------------------------------------------------------------
// Histograms
//------------------------------------------------------------------------------
// Lambda kinematics
TH1D* h_lam_p      = nullptr;
TH1D* h_lam_pt     = nullptr;
TH1D* h_lam_pz     = nullptr;
TH1D* h_lam_eta    = nullptr;
TH1D* h_lam_phi    = nullptr;
TH1D* h_lam_mass   = nullptr;

// Lambda decay info
TH1D* h_lam_decay_type = nullptr;
TH1D* h_lam_nd         = nullptr;

// Lambda decay vertex
TH1D* h_lam_decay_z     = nullptr;
TH1D* h_lam_decay_r     = nullptr;
TH2D* h_lam_decay_rz    = nullptr;
TH2D* h_lam_decay_xy    = nullptr;

// Lambda 2D correlations
TH2D* h_lam_p_vs_eta    = nullptr;
TH2D* h_lam_pt_vs_eta   = nullptr;
TH2D* h_lam_pz_vs_pt    = nullptr;

// Proton daughters (p + pi- channel)
TH1D* h_prot_p    = nullptr;
TH1D* h_prot_pt   = nullptr;
TH1D* h_prot_eta  = nullptr;

// Pion- daughters (p + pi- channel)
TH1D* h_pimin_p   = nullptr;
TH1D* h_pimin_pt  = nullptr;
TH1D* h_pimin_eta = nullptr;

// Neutron daughters (n + pi0 channel)
TH1D* h_neut_p    = nullptr;
TH1D* h_neut_pt   = nullptr;
TH1D* h_neut_eta  = nullptr;

// Pi0 daughters (n + pi0 channel)
TH1D* h_pi0_p     = nullptr;
TH1D* h_pi0_pt    = nullptr;

// Gamma from pi0 decay
TH1D* h_gam_energy = nullptr;
TH1D* h_gam_eta    = nullptr;

// Opening angle between p and pi- in p+pi- decay
TH1D* h_ppi_opening_angle = nullptr;
// Invariant mass of p+pi- pair (should peak at Lambda mass)
TH1D* h_ppi_inv_mass      = nullptr;

// Generator status of lambda
TH1D* h_lam_gen_status = nullptr;

//------------------------------------------------------------------------------
// Helper: compute derived quantities
//------------------------------------------------------------------------------
inline double mag(double x, double y, double z) { return std::sqrt(x*x + y*y + z*z); }
inline double pt(double x, double y) { return std::sqrt(x*x + y*y); }

inline double pseudorapidity(double px, double py, double pz) {
    double p = mag(px, py, pz);
    if (p <= 0) return 0;
    double costh = pz / p;
    if (std::abs(costh) >= 1.0) return (costh > 0 ? 30.0 : -30.0);
    return -std::log(std::tan(std::acos(costh) / 2.0));
}

//------------------------------------------------------------------------------
// create_histograms
//------------------------------------------------------------------------------
void create_histograms() {
    // Lambda kinematics
    h_lam_p    = new TH1D("h_lam_p",    "#Lambda |#vec{p}|;|#vec{p}| [GeV/c];Counts",  100,  0,  50);
    h_lam_pt   = new TH1D("h_lam_pt",   "#Lambda p_{T};p_{T} [GeV/c];Counts",           100,  0,   5);
    h_lam_pz   = new TH1D("h_lam_pz",   "#Lambda p_{z};p_{z} [GeV/c];Counts",           120, -10, 50);
    h_lam_eta  = new TH1D("h_lam_eta",  "#Lambda #eta;#eta;Counts",                      100, -6,   6);
    h_lam_phi  = new TH1D("h_lam_phi",  "#Lambda #phi;#phi [rad];Counts",                100, -TMath::Pi(), TMath::Pi());
    h_lam_mass = new TH1D("h_lam_mass", "#Lambda mass;mass [GeV/c^{2}];Counts",          100, 1.0, 1.3);

    // Decay classification
    h_lam_decay_type = new TH1D("h_lam_decay_type", "Decay type;type;Counts", 5, -0.5, 4.5);
    h_lam_decay_type->GetXaxis()->SetBinLabel(1, "No decay");
    h_lam_decay_type->GetXaxis()->SetBinLabel(2, "p+#pi^{-}");
    h_lam_decay_type->GetXaxis()->SetBinLabel(3, "n+#pi^{0}");
    h_lam_decay_type->GetXaxis()->SetBinLabel(4, "Shower");
    h_lam_decay_type->GetXaxis()->SetBinLabel(5, "Other");

    h_lam_nd = new TH1D("h_lam_nd", "#Lambda N daughters;N daughters;Counts", 10, -0.5, 9.5);

    // Decay vertex
    h_lam_decay_z  = new TH1D("h_lam_decay_z",  "#Lambda decay z;z [mm];Counts", 150, -5000, 40000);
    h_lam_decay_r  = new TH1D("h_lam_decay_r",  "#Lambda decay r;r [mm];Counts", 100, 0,     2000);
    h_lam_decay_rz = new TH2D("h_lam_decay_rz", "#Lambda decay vertex r vs z;z [mm];r [mm]",
                               150, -5000, 40000, 100, 0, 2000);
    h_lam_decay_xy = new TH2D("h_lam_decay_xy", "#Lambda decay vertex x vs y;x [mm];y [mm]",
                               200, -2000, 2000, 200, -2000, 2000);

    // Lambda 2D correlations
    h_lam_p_vs_eta  = new TH2D("h_lam_p_vs_eta",  "#Lambda |p| vs #eta;#eta;|p| [GeV/c]",
                                100, -6, 6, 100, 0, 50);
    h_lam_pt_vs_eta = new TH2D("h_lam_pt_vs_eta", "#Lambda p_{T} vs #eta;#eta;p_{T} [GeV/c]",
                                100, -6, 6, 100, 0, 5);
    h_lam_pz_vs_pt  = new TH2D("h_lam_pz_vs_pt",  "#Lambda p_{z} vs p_{T};p_{T} [GeV/c];p_{z} [GeV/c]",
                                100, 0, 5, 120, -10, 50);

    // Proton daughters
    h_prot_p   = new TH1D("h_prot_p",   "Proton |#vec{p}|;|#vec{p}| [GeV/c];Counts", 100, 0, 50);
    h_prot_pt  = new TH1D("h_prot_pt",  "Proton p_{T};p_{T} [GeV/c];Counts",          100, 0,  5);
    h_prot_eta = new TH1D("h_prot_eta", "Proton #eta;#eta;Counts",                     100, -6, 6);

    // Pion- daughters
    h_pimin_p   = new TH1D("h_pimin_p",   "#pi^{-} |#vec{p}|;|#vec{p}| [GeV/c];Counts", 100, 0, 20);
    h_pimin_pt  = new TH1D("h_pimin_pt",  "#pi^{-} p_{T};p_{T} [GeV/c];Counts",          100, 0,  5);
    h_pimin_eta = new TH1D("h_pimin_eta", "#pi^{-} #eta;#eta;Counts",                     100, -6, 6);

    // Neutron daughters
    h_neut_p   = new TH1D("h_neut_p",   "Neutron |#vec{p}|;|#vec{p}| [GeV/c];Counts", 100, 0, 50);
    h_neut_pt  = new TH1D("h_neut_pt",  "Neutron p_{T};p_{T} [GeV/c];Counts",          100, 0,  5);
    h_neut_eta = new TH1D("h_neut_eta", "Neutron #eta;#eta;Counts",                     100, -6, 6);

    // Pi0 daughters
    h_pi0_p  = new TH1D("h_pi0_p",  "#pi^{0} |#vec{p}|;|#vec{p}| [GeV/c];Counts", 100, 0, 20);
    h_pi0_pt = new TH1D("h_pi0_pt", "#pi^{0} p_{T};p_{T} [GeV/c];Counts",          100, 0,  5);

    // Gammas from pi0
    h_gam_energy = new TH1D("h_gam_energy", "#gamma energy from #pi^{0};E [GeV];Counts", 100, 0, 20);
    h_gam_eta    = new TH1D("h_gam_eta",    "#gamma #eta from #pi^{0};#eta;Counts",      100, -6, 6);

    // p + pi- channel derived
    h_ppi_opening_angle = new TH1D("h_ppi_opening_angle",
        "Opening angle p-#pi^{-};#theta [rad];Counts", 100, 0, TMath::Pi());
    h_ppi_inv_mass = new TH1D("h_ppi_inv_mass",
        "Invariant mass p+#pi^{-};M [GeV/c^{2}];Counts", 200, 1.0, 1.3);

    // Generator status
    h_lam_gen_status = new TH1D("h_lam_gen_status", "#Lambda generator status;status;Counts", 10, -0.5, 9.5);
}

//------------------------------------------------------------------------------
// setup_tree
//------------------------------------------------------------------------------
void setup_tree() {
    tree = new TTree("lambda_decays", "MC truth Lambda decay tree");

    tree->Branch("event",        &br_event);
    tree->Branch("lam_is_first", &br_lam_is_first);
    tree->Branch("lam_decay",    &br_lam_decay);

    br_lam.attach(tree,    "lam");
    br_prot.attach(tree,   "prot");
    br_pimin.attach(tree,  "pimin");
    br_neut.attach(tree,   "neut");
    br_pizero.attach(tree, "pizero");
    br_gamone.attach(tree, "gamone");
    br_gamtwo.attach(tree, "gamtwo");
}

//------------------------------------------------------------------------------
// fill_particle_histograms  (helper for daughter particles)
//------------------------------------------------------------------------------
void fill_daughter_hists(TH1D* h_p, TH1D* h_pt_h, TH1D* h_eta_h,
                         double px, double py, double pz) {
    double p_val  = mag(px, py, pz);
    double pt_val = pt(px, py);
    double eta    = pseudorapidity(px, py, pz);
    if (h_p)     h_p->Fill(p_val);
    if (h_pt_h)  h_pt_h->Fill(pt_val);
    if (h_eta_h) h_eta_h->Fill(eta);
}

//------------------------------------------------------------------------------
// process_event
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int evt_id) {
    const auto& particles = event.get<MCParticleCollection>("MCParticles");

    bool is_first_lambda = true;

    for (const auto& lam : particles) {
        if (lam.getPDG() != 3122) continue; // not Lambda

        int decay_type = 4; // 0-nodecay, 1-p+pi-, 2-n+pi0, 3-shower, 4-other

        // Classify decay channel & pick daughters
        std::optional<MCParticle> prot_opt, pimin_opt, neut_opt, pi0_opt, gam1_opt, gam2_opt;

        auto daughters = lam.getDaughters();

        if (daughters.size() == 0) {
            decay_type = 0;
        } else if (daughters.size() == 2) {
            if (daughters.at(0).getPDG() == 2212 && daughters.at(1).getPDG() == -211) {
                decay_type = 1;
                prot_opt  = daughters.at(0);
                pimin_opt = daughters.at(1);
            }
            if (daughters.at(1).getPDG() == 2212 && daughters.at(0).getPDG() == -211) {
                decay_type = 1;
                prot_opt  = daughters.at(1);
                pimin_opt = daughters.at(0);
            }
            if (daughters.at(0).getPDG() == 2112 && daughters.at(1).getPDG() == 111) {
                decay_type = 2;
                neut_opt = daughters.at(0);
                pi0_opt  = daughters.at(1);
            }
            if (daughters.at(1).getPDG() == 2112 && daughters.at(0).getPDG() == 111) {
                decay_type = 2;
                neut_opt = daughters.at(1);
                pi0_opt  = daughters.at(0);
            }
        } else {
            for (const auto& daughter : daughters) {
                if (daughter.getPDG() == 3122) {
                    decay_type = 3; // shower/recharge
                    break;
                }
            }
        }

        // For n+pi0: capture pi0 decay gammas
        if (neut_opt && pi0_opt) {
            if (pi0_opt->getDaughters().size() > 0)
                gam1_opt = pi0_opt->getDaughters().at(0);
            if (pi0_opt->getDaughters().size() > 1)
                gam2_opt = pi0_opt->getDaughters().at(1);
        }

        if (neut_opt && prot_opt) {
            fmt::print("(!!!) WARNING: neut && prot at evt_id={}\n", evt_id);
        }

        // -----------------------------------------------------------------
        // Fill tree branches
        // -----------------------------------------------------------------
        br_event        = evt_id;
        br_lam_is_first = static_cast<int>(is_first_lambda);
        br_lam_decay    = decay_type;

        br_lam.clear();    br_lam.fill(lam);
        br_prot.clear();   if (prot_opt)  br_prot.fill(*prot_opt);
        br_pimin.clear();  if (pimin_opt) br_pimin.fill(*pimin_opt);
        br_neut.clear();   if (neut_opt)  br_neut.fill(*neut_opt);
        br_pizero.clear(); if (pi0_opt)   br_pizero.fill(*pi0_opt);
        br_gamone.clear(); if (gam1_opt)  br_gamone.fill(*gam1_opt);
        br_gamtwo.clear(); if (gam2_opt)  br_gamtwo.fill(*gam2_opt);

        tree->Fill();

        // -----------------------------------------------------------------
        // Fill histograms
        // -----------------------------------------------------------------
        auto lam_mom = lam.getMomentum();
        auto lam_ep  = lam.getEndpoint();
        double lam_p_val  = mag(lam_mom.x, lam_mom.y, lam_mom.z);
        double lam_pt_val = pt(lam_mom.x, lam_mom.y);
        double lam_eta    = pseudorapidity(lam_mom.x, lam_mom.y, lam_mom.z);
        double lam_phi    = std::atan2(lam_mom.y, lam_mom.x);

        h_lam_p->Fill(lam_p_val);
        h_lam_pt->Fill(lam_pt_val);
        h_lam_pz->Fill(lam_mom.z);
        h_lam_eta->Fill(lam_eta);
        h_lam_phi->Fill(lam_phi);
        h_lam_mass->Fill(lam.getMass());
        h_lam_gen_status->Fill(lam.getGeneratorStatus());

        h_lam_decay_type->Fill(decay_type);
        h_lam_nd->Fill(static_cast<double>(daughters.size()));

        // 2D correlations
        h_lam_p_vs_eta->Fill(lam_eta, lam_p_val);
        h_lam_pt_vs_eta->Fill(lam_eta, lam_pt_val);
        h_lam_pz_vs_pt->Fill(lam_pt_val, lam_mom.z);

        // Decay vertex (only if decayed)
        if (daughters.size() > 0) {
            double dec_r = pt(lam_ep.x, lam_ep.y);
            h_lam_decay_z->Fill(lam_ep.z);
            h_lam_decay_r->Fill(dec_r);
            h_lam_decay_rz->Fill(lam_ep.z, dec_r);
            h_lam_decay_xy->Fill(lam_ep.x, lam_ep.y);
        }

        // Proton + Pi- daughters
        if (prot_opt && pimin_opt) {
            auto pmom = prot_opt->getMomentum();
            auto pimom = pimin_opt->getMomentum();

            fill_daughter_hists(h_prot_p,  h_prot_pt,  h_prot_eta,  pmom.x,  pmom.y,  pmom.z);
            fill_daughter_hists(h_pimin_p, h_pimin_pt, h_pimin_eta, pimom.x, pimom.y, pimom.z);

            // Opening angle
            double p1 = mag(pmom.x, pmom.y, pmom.z);
            double p2 = mag(pimom.x, pimom.y, pimom.z);
            if (p1 > 0 && p2 > 0) {
                double cosA = (pmom.x*pimom.x + pmom.y*pimom.y + pmom.z*pimom.z) / (p1*p2);
                cosA = std::clamp(cosA, -1.0, 1.0);
                h_ppi_opening_angle->Fill(std::acos(cosA));
            }

            // Invariant mass of p + pi-
            constexpr double M_PROTON = 0.938272;
            constexpr double M_PION   = 0.139570;
            double E_p  = std::sqrt(p1*p1 + M_PROTON*M_PROTON);
            double E_pi = std::sqrt(p2*p2 + M_PION*M_PION);
            double E_tot = E_p + E_pi;
            double px_tot = pmom.x + pimom.x;
            double py_tot = pmom.y + pimom.y;
            double pz_tot = pmom.z + pimom.z;
            double m2 = E_tot*E_tot - (px_tot*px_tot + py_tot*py_tot + pz_tot*pz_tot);
            if (m2 > 0) h_ppi_inv_mass->Fill(std::sqrt(m2));
        }

        // Neutron + Pi0 daughters
        if (neut_opt) {
            auto nmom = neut_opt->getMomentum();
            fill_daughter_hists(h_neut_p, h_neut_pt, h_neut_eta, nmom.x, nmom.y, nmom.z);
        }
        if (pi0_opt) {
            auto pimom = pi0_opt->getMomentum();
            double p_val  = mag(pimom.x, pimom.y, pimom.z);
            double pt_val = pt(pimom.x, pimom.y);
            h_pi0_p->Fill(p_val);
            h_pi0_pt->Fill(pt_val);
        }

        // Gammas from pi0 decay
        if (gam1_opt) {
            auto gmom = gam1_opt->getMomentum();
            h_gam_energy->Fill(mag(gmom.x, gmom.y, gmom.z)); // massless: E = |p|
            h_gam_eta->Fill(pseudorapidity(gmom.x, gmom.y, gmom.z));
        }
        if (gam2_opt) {
            auto gmom = gam2_opt->getMomentum();
            h_gam_energy->Fill(mag(gmom.x, gmom.y, gmom.z));
            h_gam_eta->Fill(pseudorapidity(gmom.x, gmom.y, gmom.z));
        }

        is_first_lambda = false;
    }
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
// main  (compiled mode)
//------------------------------------------------------------------------------
int main(int argc, char* argv[]) {
    std::vector<std::string> infiles;
    std::string out_name = "mcpart_lambda.root";

    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "-n" && i + 1 < argc) events_limit = std::atoi(argv[++i]);
        else if (a == "-o" && i + 1 < argc) out_name = argv[++i];
        else if (a == "-h" || a == "--help") {
            fmt::print("usage: {} [-n N] [-o file.root] input1.root [...]\n", argv[0]);
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

    out_file = TFile::Open(out_name.c_str(), "RECREATE");
    if (!out_file || out_file->IsZombie()) {
        fmt::print(stderr, "error: cannot open output file {}\n", out_name);
        return 1;
    }

    create_histograms();
    setup_tree();

    for (auto& f : infiles) {
        process_file(f);
        if (events_limit > 0 && total_evt_seen >= events_limit) break;
    }

    out_file->Write();
    out_file->Close();
    fmt::print("\nWrote {} events to {}\n", total_evt_seen, out_name);
    return 0;
}

// ---------------------------------------------------------------------------
// ROOT-macro entry point.
// root -x -l -b -q 'mcpart_lambda.cxx("input.edm4hep.root","output.root",100)'
// ---------------------------------------------------------------------------
void mcpart_lambda(const char* infile,
                   const char* outfile = "mcpart_lambda.root",
                   int events = -1)
{
    fmt::print("'mcpart_lambda' ROOT macro entry point\n");
    fmt::print("  infile:  {}\n", infile);
    fmt::print("  outfile: {}\n", outfile);
    fmt::print("  events:  {} {}\n", events, (events == -1 ? "(process all)" : ""));

    out_file = TFile::Open(outfile, "RECREATE");
    if (!out_file || out_file->IsZombie()) {
        fmt::print(stderr, "error: cannot open output file {}\n", outfile);
        return;
    }

    events_limit     = events;
    total_evt_seen   = 0;

    create_histograms();
    setup_tree();

    process_file(infile);

    out_file->Write();
    out_file->Close();
    fmt::print("\nWrote {} events to {}\n", total_evt_seen, outfile);
}
