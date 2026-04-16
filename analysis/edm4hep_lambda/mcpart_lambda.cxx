#ifdef __CLING__
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#endif

// mcpart_lambda.cxx
// Reads edm4hep/edm4eic MCParticles, finds Lambda decays,
// writes ROOT histograms + PNGs + a flat TTree (same columns as mcpart_lambda CSV).
//
// Input patterns support shell wildcards (e.g. "dir/*.root").
// podio::ROOTReader::openFiles() passes each pattern to TChain::Add, which
// handles wildcard expansion natively.
//
// Usage (compiled):
//   ./mcpart_lambda [-n N] [-o output_dir] "input*.root" [more_patterns ...]
//
// Usage (ROOT macro, single pattern or wildcard):
//   root -x -l -b -q 'mcpart_lambda.cxx("input.edm4hep.root","out_dir",100)'
//   root -x -l -b -q 'mcpart_lambda.cxx("dir/*.root","out_dir",100)'
//
// Usage (ROOT macro, comma-separated patterns/wildcards):
//   root -x -l -b -q 'mcpart_lambda.cxx("f1.root,dir/*.root","out_dir",100)'

#include "podio/Frame.h"
#include "podio/ROOTReader.h"
#include "podio/CollectionBase.h"
#include <edm4hep/MCParticleCollection.h>

#include <fmt/core.h>
#include <fmt/ostream.h>

#include <TFile.h>
#include <TH1D.h>
#include <TH2D.h>
#include <TTree.h>
#include <TMath.h>
#include <TCanvas.h>
#include <TSystem.h>
#include <TStyle.h>

#include <string>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <cmath>
#include <optional>

using namespace edm4hep;

//------------------------------------------------------------------------------
// globals
//------------------------------------------------------------------------------
int         events_limit  = -1;
long        total_evt_seen = 0;
std::string g_output_dir;

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
int br_event      = 0;
int br_lam_is_first = 0;
int br_lam_decay  = 0;

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
TH1D* h_lam_decay_z  = nullptr;
TH1D* h_lam_decay_r  = nullptr;
TH2D* h_lam_decay_rz = nullptr;
TH2D* h_lam_decay_xy = nullptr;

// Lambda 2D correlations
TH2D* h_lam_p_vs_eta  = nullptr;
TH2D* h_lam_pt_vs_eta = nullptr;
TH2D* h_lam_pz_vs_pt  = nullptr;

// Proton daughters (p + pi- channel)
TH1D* h_prot_p   = nullptr;
TH1D* h_prot_pt  = nullptr;
TH1D* h_prot_eta = nullptr;

// Pion- daughters (p + pi- channel)
TH1D* h_pimin_p   = nullptr;
TH1D* h_pimin_pt  = nullptr;
TH1D* h_pimin_eta = nullptr;

// Neutron daughters (n + pi0 channel)
TH1D* h_neut_p   = nullptr;
TH1D* h_neut_pt  = nullptr;
TH1D* h_neut_eta = nullptr;

// Pi0 daughters (n + pi0 channel)
TH1D* h_pi0_p  = nullptr;
TH1D* h_pi0_pt = nullptr;

// Gamma from pi0 decay
TH1D* h_gam_energy = nullptr;
TH1D* h_gam_eta    = nullptr;

// p + pi- derived
TH1D* h_ppi_opening_angle = nullptr;
TH1D* h_ppi_inv_mass      = nullptr;

// Generator status
TH1D* h_lam_gen_status = nullptr;

// Event-level
TH1D* h_evt_nparticles = nullptr;

//------------------------------------------------------------------------------
// frame_get: workaround for a podio::Frame::get<T>() template instantiation
// issue observed on some builds. We go through the non-template overload that
// returns a const CollectionBase* and cast to the wanted collection type.
//------------------------------------------------------------------------------
template <typename CollT>
inline const CollT& frame_get(const podio::Frame& frame, const std::string& name) {
    const podio::CollectionBase* base = frame.get(name);
    if (!base) {
        static const CollT empty{};
        return empty;
    }
    const auto* typed = dynamic_cast<const CollT*>(base);
    if (!typed) {
        static const CollT empty{};
        return empty;
    }
    return *typed;
}

//------------------------------------------------------------------------------
// Helpers: kinematics
//------------------------------------------------------------------------------
inline double mag(double x, double y, double z) { return std::sqrt(x*x + y*y + z*z); }
inline double pt(double x, double y)             { return std::sqrt(x*x + y*y); }

inline double pseudorapidity(double px, double py, double pz) {
    double p = mag(px, py, pz);
    if (p <= 0) return 0;
    double costh = pz / p;
    if (std::abs(costh) >= 1.0) return (costh > 0 ? 30.0 : -30.0);
    return -std::log(std::tan(std::acos(costh) / 2.0));
}

//------------------------------------------------------------------------------
// png_save: draw one histogram to a PNG in g_output_dir
//------------------------------------------------------------------------------
void png_save(TH1* h) {
    if (!h) return;
    TCanvas c("c_tmp", "", 800, 600);
    c.SetLeftMargin(0.12);
    if (h->InheritsFrom("TH2")) {
        c.SetRightMargin(0.14); // room for colour-z axis
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
    // entries + mean + stddev + integral
    gStyle->SetOptStat(1001111);

    h_lam_p    = new TH1D("h_lam_p",    "#Lambda |#vec{p}|;|#vec{p}| [GeV/c];Counts",  100,  0, 200);
    h_lam_pt   = new TH1D("h_lam_pt",   "#Lambda p_{T};p_{T} [GeV/c];Counts",           100,  0,   5);
    h_lam_pz   = new TH1D("h_lam_pz",   "#Lambda p_{z};p_{z} [GeV/c];Counts",           120, -10, 200);
    h_lam_eta  = new TH1D("h_lam_eta",  "#Lambda #eta;#eta;Counts",                      100, -6,   6);
    h_lam_phi  = new TH1D("h_lam_phi",  "#Lambda #phi;#phi [rad];Counts",                100, -TMath::Pi(), TMath::Pi());
    h_lam_mass = new TH1D("h_lam_mass", "#Lambda mass;mass [GeV/c^{2}];Counts",          100, 1.0, 1.3);

    h_lam_decay_type = new TH1D("h_lam_decay_type", "Decay type;type;Counts", 5, -0.5, 4.5);
    h_lam_decay_type->GetXaxis()->SetBinLabel(1, "No decay");
    h_lam_decay_type->GetXaxis()->SetBinLabel(2, "p+#pi^{-}");
    h_lam_decay_type->GetXaxis()->SetBinLabel(3, "n+#pi^{0}");
    h_lam_decay_type->GetXaxis()->SetBinLabel(4, "Shower");
    h_lam_decay_type->GetXaxis()->SetBinLabel(5, "Other");

    h_lam_nd = new TH1D("h_lam_nd", "#Lambda N daughters;N daughters;Counts", 10, -0.5, 9.5);

    h_lam_decay_z  = new TH1D("h_lam_decay_z",  "#Lambda decay z;z [mm];Counts",        150, -5000, 40000);
    h_lam_decay_r  = new TH1D("h_lam_decay_r",  "#Lambda decay r;r [mm];Counts",        100,     0,  500);
    h_lam_decay_rz = new TH2D("h_lam_decay_rz", "#Lambda decay vertex;z [mm];r [mm]",   150, -5000, 40000, 100, 0, 500);
    h_lam_decay_xy = new TH2D("h_lam_decay_xy", "#Lambda decay vertex;x [mm];y [mm]",   200, -500, 500, 200, -500, 500);

    h_lam_p_vs_eta  = new TH2D("h_lam_p_vs_eta",  "#Lambda |p| vs #eta;#eta;|p| [GeV/c]",    100, -6, 6, 100, 0, 200);
    h_lam_pt_vs_eta = new TH2D("h_lam_pt_vs_eta", "#Lambda p_{T} vs #eta;#eta;p_{T} [GeV/c]",100, -6, 6, 100, 0,  5);
    h_lam_pz_vs_pt  = new TH2D("h_lam_pz_vs_pt",  "#Lambda p_{z} vs p_{T};p_{T} [GeV/c];p_{z} [GeV/c]", 100, 0, 5, 120, -10, 200);

    h_prot_p   = new TH1D("h_prot_p",   "Proton |#vec{p}|;|#vec{p}| [GeV/c];Counts", 100, 0, 300);
    h_prot_pt  = new TH1D("h_prot_pt",  "Proton p_{T};p_{T} [GeV/c];Counts",          100, 0,  5);
    h_prot_eta = new TH1D("h_prot_eta", "Proton #eta;#eta;Counts",                     100, -6, 6);

    h_pimin_p   = new TH1D("h_pimin_p",   "#pi^{-} |#vec{p}|;|#vec{p}| [GeV/c];Counts", 100, 0, 40);
    h_pimin_pt  = new TH1D("h_pimin_pt",  "#pi^{-} p_{T};p_{T} [GeV/c];Counts",          100, 0,  5);
    h_pimin_eta = new TH1D("h_pimin_eta", "#pi^{-} #eta;#eta;Counts",                     100, -6, 6);

    h_neut_p   = new TH1D("h_neut_p",   "Neutron |#vec{p}|;|#vec{p}| [GeV/c];Counts", 100, 0, 50);
    h_neut_pt  = new TH1D("h_neut_pt",  "Neutron p_{T};p_{T} [GeV/c];Counts",          100, 0,  5);
    h_neut_eta = new TH1D("h_neut_eta", "Neutron #eta;#eta;Counts",                     100, -6, 6);

    h_pi0_p  = new TH1D("h_pi0_p",  "#pi^{0} |#vec{p}|;|#vec{p}| [GeV/c];Counts", 100, 0, 20);
    h_pi0_pt = new TH1D("h_pi0_pt", "#pi^{0} p_{T};p_{T} [GeV/c];Counts",          100, 0,  5);

    h_gam_energy = new TH1D("h_gam_energy", "#gamma energy from #pi^{0};E [GeV];Counts", 100, 0, 20);
    h_gam_eta    = new TH1D("h_gam_eta",    "#gamma #eta from #pi^{0};#eta;Counts",      100, -6, 6);

    h_ppi_opening_angle = new TH1D("h_ppi_opening_angle",
        "Opening angle p-#pi^{-};#theta [rad];Counts", 200, 0, 0.15);
    h_ppi_inv_mass = new TH1D("h_ppi_inv_mass",
        "Invariant mass p+#pi^{-};M [GeV/c^{2}];Counts", 200, 1.0, 1.3);

    h_lam_gen_status = new TH1D("h_lam_gen_status", "#Lambda generator status;status;Counts", 10, -0.5, 9.5);

    h_evt_nparticles = new TH1D("h_evt_nparticles", "Total MC particles per event;N particles;Events", 100, 0-0.5, 100-0.5);
}

//------------------------------------------------------------------------------
// save_all_pngs: call after filling, before closing the file
//------------------------------------------------------------------------------
void save_all_pngs() {
    fmt::print("\nSaving PNG images to {}/\n", g_output_dir);
    // 1D
    for (auto* h : {h_lam_p, h_lam_pt, h_lam_pz, h_lam_eta, h_lam_phi, h_lam_mass,
                    h_lam_decay_type, h_lam_nd,
                    h_lam_decay_z, h_lam_decay_r,
                    h_prot_p, h_prot_pt, h_prot_eta,
                    h_pimin_p, h_pimin_pt, h_pimin_eta,
                    h_neut_p, h_neut_pt, h_neut_eta,
                    h_pi0_p, h_pi0_pt,
                    h_gam_energy, h_gam_eta,
                    h_ppi_opening_angle, h_ppi_inv_mass,
                    h_lam_gen_status,
                    h_evt_nparticles}) {
        png_save(h);
    }
    // 2D
    for (auto* h : {(TH1*)h_lam_decay_rz, (TH1*)h_lam_decay_xy,
                    (TH1*)h_lam_p_vs_eta,  (TH1*)h_lam_pt_vs_eta, (TH1*)h_lam_pz_vs_pt}) {
        png_save(h);
    }
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
// fill_daughter_hists helper
//------------------------------------------------------------------------------
void fill_daughter_hists(TH1D* h_p, TH1D* h_pt_h, TH1D* h_eta_h,
                         double px, double py, double pz) {
    if (h_p)     h_p->Fill(mag(px, py, pz));
    if (h_pt_h)  h_pt_h->Fill(pt(px, py));
    if (h_eta_h) h_eta_h->Fill(pseudorapidity(px, py, pz));
}

//------------------------------------------------------------------------------
// process_event
//------------------------------------------------------------------------------
void process_event(const podio::Frame& event, int evt_id) {
    const auto& particles = frame_get<MCParticleCollection>(event, "MCParticles");

    h_evt_nparticles->Fill(static_cast<double>(particles.size()));

    bool is_first_lambda = true;

    for (const auto& lam : particles) {
        if (lam.getPDG() != 3122) continue;

        int decay_type = 4;
        std::optional<MCParticle> prot_opt, pimin_opt, neut_opt, pi0_opt, gam1_opt, gam2_opt;

        auto daughters = lam.getDaughters();

        if (daughters.size() == 0) {
            decay_type = 0;
        } else if (daughters.size() == 2) {
            if (daughters.at(0).getPDG() == 2212 && daughters.at(1).getPDG() == -211) {
                decay_type = 1; prot_opt = daughters.at(0); pimin_opt = daughters.at(1);
            }
            if (daughters.at(1).getPDG() == 2212 && daughters.at(0).getPDG() == -211) {
                decay_type = 1; prot_opt = daughters.at(1); pimin_opt = daughters.at(0);
            }
            if (daughters.at(0).getPDG() == 2112 && daughters.at(1).getPDG() == 111) {
                decay_type = 2; neut_opt = daughters.at(0); pi0_opt = daughters.at(1);
            }
            if (daughters.at(1).getPDG() == 2112 && daughters.at(0).getPDG() == 111) {
                decay_type = 2; neut_opt = daughters.at(1); pi0_opt = daughters.at(0);
            }
        } else {
            // nd == 1 or nd > 2: anything with more than 2 daughters is a hadronic shower
            if (daughters.size() > 2) decay_type = 3;
            // nd == 1 stays at 4 (other)
        }

        if (neut_opt && pi0_opt) {
            if (pi0_opt->getDaughters().size() > 0) gam1_opt = pi0_opt->getDaughters().at(0);
            if (pi0_opt->getDaughters().size() > 1) gam2_opt = pi0_opt->getDaughters().at(1);
        }

        if (neut_opt && prot_opt)
            fmt::print("(!!!) WARNING: neut && prot at evt_id={}\n", evt_id);

        // ---- fill tree ----
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

        // ---- fill histograms ----
        auto lam_mom = lam.getMomentum();
        auto lam_ep  = lam.getEndpoint();
        double lam_p_val  = mag(lam_mom.x, lam_mom.y, lam_mom.z);
        double lam_pt_val = pt(lam_mom.x, lam_mom.y);
        double lam_eta    = pseudorapidity(lam_mom.x, lam_mom.y, lam_mom.z);

        h_lam_p->Fill(lam_p_val);
        h_lam_pt->Fill(lam_pt_val);
        h_lam_pz->Fill(lam_mom.z);
        h_lam_eta->Fill(lam_eta);
        h_lam_phi->Fill(std::atan2(lam_mom.y, lam_mom.x));
        h_lam_mass->Fill(lam.getMass());
        h_lam_gen_status->Fill(lam.getGeneratorStatus());
        h_lam_decay_type->Fill(decay_type);
        h_lam_nd->Fill(static_cast<double>(daughters.size()));

        h_lam_p_vs_eta->Fill(lam_eta, lam_p_val);
        h_lam_pt_vs_eta->Fill(lam_eta, lam_pt_val);
        h_lam_pz_vs_pt->Fill(lam_pt_val, lam_mom.z);

        if (daughters.size() > 0) {
            double dec_r = pt(lam_ep.x, lam_ep.y);
            h_lam_decay_z->Fill(lam_ep.z);
            h_lam_decay_r->Fill(dec_r);
            h_lam_decay_rz->Fill(lam_ep.z, dec_r);
            h_lam_decay_xy->Fill(lam_ep.x, lam_ep.y);
        }

        if (prot_opt && pimin_opt) {
            auto pmom  = prot_opt->getMomentum();
            auto pimom = pimin_opt->getMomentum();
            fill_daughter_hists(h_prot_p,  h_prot_pt,  h_prot_eta,  pmom.x,  pmom.y,  pmom.z);
            fill_daughter_hists(h_pimin_p, h_pimin_pt, h_pimin_eta, pimom.x, pimom.y, pimom.z);

            double p1 = mag(pmom.x, pmom.y, pmom.z);
            double p2 = mag(pimom.x, pimom.y, pimom.z);
            if (p1 > 0 && p2 > 0) {
                double cosA = (pmom.x*pimom.x + pmom.y*pimom.y + pmom.z*pimom.z) / (p1*p2);
                cosA = std::clamp(cosA, -1.0, 1.0);
                h_ppi_opening_angle->Fill(std::acos(cosA));
            }

            constexpr double M_PROTON = 0.938272;
            constexpr double M_PION   = 0.139570;
            double E_p   = std::sqrt(p1*p1 + M_PROTON*M_PROTON);
            double E_pi  = std::sqrt(p2*p2 + M_PION*M_PION);
            double E_tot = E_p + E_pi;
            double pxtot = pmom.x + pimom.x, pytot = pmom.y + pimom.y, pztot = pmom.z + pimom.z;
            double m2 = E_tot*E_tot - (pxtot*pxtot + pytot*pytot + pztot*pztot);
            if (m2 > 0) h_ppi_inv_mass->Fill(std::sqrt(m2));
        }

        if (neut_opt) {
            auto nmom = neut_opt->getMomentum();
            fill_daughter_hists(h_neut_p, h_neut_pt, h_neut_eta, nmom.x, nmom.y, nmom.z);
        }
        if (pi0_opt) {
            auto pimom = pi0_opt->getMomentum();
            h_pi0_p->Fill(mag(pimom.x, pimom.y, pimom.z));
            h_pi0_pt->Fill(pt(pimom.x, pimom.y));
        }
        if (gam1_opt) {
            auto gm = gam1_opt->getMomentum();
            h_gam_energy->Fill(mag(gm.x, gm.y, gm.z));
            h_gam_eta->Fill(pseudorapidity(gm.x, gm.y, gm.z));
        }
        if (gam2_opt) {
            auto gm = gam2_opt->getMomentum();
            h_gam_energy->Fill(mag(gm.x, gm.y, gm.z));
            h_gam_eta->Fill(pseudorapidity(gm.x, gm.y, gm.z));
        }

        is_first_lambda = false;
        // (!!!)
        break;  // (!!!) We want only the first Lambda in each event, i.e. sullivan lambda. Don't care about the rest. 
        //^^^^^ Look above!
    }
}

//------------------------------------------------------------------------------
// prepare_output_dir: create dir (ok if already exists)
//------------------------------------------------------------------------------
void prepare_output_dir(const std::string& dir) {
    gSystem->mkdir(dir.c_str(), kTRUE); // kTRUE = create parents; succeeds if already exists
}

//------------------------------------------------------------------------------
// split_csv: split a comma-separated string into a vector of strings
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
// run: shared logic for both entry points
//------------------------------------------------------------------------------
void run(const std::vector<std::string>& infiles) {
    prepare_output_dir(g_output_dir);

    fmt::print("Input pattern(s):\n");
    for (const auto& f : infiles) fmt::print("  {}\n", f);

    podio::ROOTReader rdr;
    try {
        // openFiles passes each pattern to TChain::Add, which expands wildcards.
        rdr.openFiles(infiles);
    } catch (const std::runtime_error& e) {
        fmt::print(stderr, "error opening files: {}\n", e.what());
        return;
    }

    const auto nEv  = rdr.getEntries(podio::Category::Event);
    const long limit = (events_limit > 0) ? events_limit : static_cast<long>(nEv);
    fmt::print("Total events in chain: {}  (will process: {})\n", nEv, limit);

    std::string root_out = g_output_dir + "/mcpart_lambda.root";
    out_file = TFile::Open(root_out.c_str(), "RECREATE");
    if (!out_file || out_file->IsZombie()) {
        fmt::print(stderr, "error: cannot open output file {}\n", root_out);
        return;
    }

    create_histograms();
    setup_tree();

    for (unsigned ie = 0; ie < nEv; ++ie) {
        if (events_limit > 0 && total_evt_seen >= events_limit) break;
        podio::Frame evt(rdr.readNextEntry(podio::Category::Event));
        process_event(evt, total_evt_seen);
        ++total_evt_seen;
        if (total_evt_seen % 1000 == 0)
            fmt::print("  ... {} / {} events processed\n", total_evt_seen, limit);
    }

    save_all_pngs();

    out_file->Write();
    out_file->Close();
    fmt::print("\nWrote {} events -> {}\n", total_evt_seen, root_out);
}

//------------------------------------------------------------------------------
// main  (compiled mode)
//   ./mcpart_lambda [-n N] [-o output_dir] <pattern> [<pattern> ...]
// Patterns may include shell wildcards (quote them to defer to TChain).
//------------------------------------------------------------------------------
int main(int argc, char* argv[]) {
    std::vector<std::string> patterns;
    g_output_dir = "mcpart_lambda_out";

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
//   root -x -l -b -q 'mcpart_lambda.cxx("input.edm4hep.root","out_dir",100)'
// Wildcards and/or comma-separated patterns:
//   root -x -l -b -q 'mcpart_lambda.cxx("dir/*.root","out_dir",100)'
//   root -x -l -b -q 'mcpart_lambda.cxx("f1.root,dir/*.root","out_dir",100)'
// ---------------------------------------------------------------------------
void mcpart_lambda(const char* infiles_csv,
                   const char* output_dir = "mcpart_lambda_out",
                   int events = -1)
{
    fmt::print("'mcpart_lambda' ROOT macro\n");
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
