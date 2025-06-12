// lambdas_to_csv.cxx
#include "podio/Frame.h"
#include "podio/ROOTReader.h"
#include <edm4hep/MCParticleCollection.h>

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
int  events_limit   = -1;                // -n  <N>
long total_evt_seen =  0;
std::ofstream csv;
bool header_written = false;

struct Vec3 { double x{}, y{}, z{}; };
inline void write_particle(std::ostream& out, const MCParticle* p) {
  if (!p) { out << ",,,,,,,,,,,,"; return; }                        // 13 empties
  auto m  = p->getMomentum();
  auto v  = p->getVertex();
  auto ep = p->getEndpoint();
  out << p->getPDG()           << ',' << p->getCharge()      << ','
      << p->getMass()          << ','
      << m.x << ',' << m.y << ',' << m.z << ','
      << v.x << ',' << v.y << ',' << v.z << ','
      << ep.x << ',' << ep.y << ',' << ep.z << ','
      << p->getTime();
}

void write_header() {
  csv <<
    "event_id,lam_idx,channel,"
    /*lambda*/ "lam_pdg,lam_charge,lam_mass,lam_px,lam_py,lam_pz,"
               "lam_vx,lam_vy,lam_vz,lam_ex,lam_ey,lam_ez,lam_time,"
    /*prot   */ "prot_pdg,prot_charge,prot_mass,prot_px,prot_py,prot_pz,"
               "prot_vx,prot_vy,prot_vz,prot_ex,prot_ey,prot_ez,prot_time,"
    /*pimin  */ "pimin_pdg,pimin_charge,pimin_mass,pimin_px,pimin_py,pimin_pz,"
               "pimin_vx,pimin_vy,pimin_vz,pimin_ex,pimin_ey,pimin_ez,pimin_time,"
    /*neutron*/ "n_pdg,n_charge,n_mass,n_px,n_py,n_pz,"
               "n_vx,n_vy,n_vz,n_ex,n_ey,n_ez,n_time,"
    /*pi0    */ "pizero_pdg,pizero_charge,pizero_mass,pizero_px,pizero_py,pizero_pz,"
               "pizero_vx,pizero_vy,pizero_vz,pizero_ex,pizero_ey,pizero_ez,pizero_time,"
    /*gam1   */ "g1_pdg,g1_charge,g1_mass,g1_px,g1_py,g1_pz,"
               "g1_vx,g1_vy,g1_vz,g1_ex,g1_ey,g1_ez,g1_time,"
    /*gam2   */ "g2_pdg,g2_charge,g2_mass,g2_px,g2_py,g2_pz,"
               "g2_vx,g2_vy,g2_vz,g2_ex,g2_ey,g2_ez,g2_time\n";
  header_written = true;
}

//------------------------------------------------------------------------------
// event processing
//------------------------------------------------------------------------------
void process_event(const podio::Frame& evt, int evt_id) {
  const auto& parts = evt.get<MCParticleCollection>("MCParticles");

  for (const auto& lam : parts) {
    if (lam.getPDG() != 3122) continue;                          // not Λ⁰

    const auto& dtrs = lam.getDaughters();
    if (dtrs.size() < 2) continue;                               // malformed

    // -----------------------------------------------------------------
    // classify decay channel & pick final-state pointers
    // -----------------------------------------------------------------
    const MCParticle *prot=nullptr,*pimin=nullptr,*neut=nullptr,
                     *pi0=nullptr,*gam1=nullptr,*gam2=nullptr;

    for (const auto& d : dtrs) {
      switch (d.getPDG()) {
        case  2212: prot  = &d; break;          // p
        case -211: pimin = &d; break;           // π-
        case  2112: neut = &d; break;           // n
        case  111:  pi0  = &d; break;           // π0
      }
    }

    int channel = -1;
    if (prot && pimin) { channel = 1; }
    else if (neut && pi0) {
      channel = 2;
      pi0->getDaughters();
      if (g.size() >= 1) gam1 = &g[0];
      if (g.size() >= 2) gam2 = &g[1];
    }
    if (channel == -1) continue;               // skip rare channels

    // -----------------------------------------------------------------
    // output
    // -----------------------------------------------------------------
    if (!header_written) write_header();
    csv << evt_id << ',' << lam.getObjectID().index << ',' << channel << ',';
    write_particle(csv, &lam);
    write_particle(csv, prot);
    write_particle(csv, pimin);
    write_particle(csv, neut);
    write_particle(csv, pi0);
    write_particle(csv, gam1);
    write_particle(csv, gam2);
    csv << '\n';
  }
}

//------------------------------------------------------------------------------
// file loop
//------------------------------------------------------------------------------
void process_file(const std::string& fname) {
  podio::ROOTReader rdr;
  rdr.openFile(fname);
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
int main(int argc,char* argv[]) {
  std::vector<std::string> infiles;
  std::string out_name = "mcpart_lambdas.csv";

  for (int i=1;i<argc;++i) {
    std::string a = argv[i];
    if (a=="-n" && i+1<argc) events_limit = std::atoi(argv[++i]);
    else if (a=="-o" && i+1<argc) out_name = argv[++i];
    else if (a=="-h"||a=="--help") {
      fmt::print("usage: {} [-n N] [-o file] input1.root [...]\n", argv[0]); return 0;}
    else if (!a.empty() && a[0]!='-') infiles.emplace_back(a);
    else { fmt::print("unknown option {}\n",a); return 1; }
  }
  if (infiles.empty()) { fmt::print("no input files\n"); return 1; }

  csv.open(out_name);
  if (!csv) { fmt::print("cannot open {}\n", out_name); return 1; }

  for (auto& f: infiles) {
    process_file(f);
    if (events_limit>0 && total_evt_seen>=events_limit) break;
  }
  fmt::print("wrote {} Λ decays to {}\n", total_evt_seen, out_name);
  return 0;
}
