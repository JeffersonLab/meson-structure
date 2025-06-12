// singularity exec -B /volatile/eic/romanov/meson-structure-2025-06:/volatile/eic/romanov/meson-structure-2025-06 /cvmfs/singularity.opensciencegrid.org/eicweb/eic_xl:nightly bash
// source /opt/detector/epic-main/bin/thisepic.sh
// root -x -l -b -q e01_edm4hep.cxx\(\"/volatile/eic/romanov/meson-structure-2025-06/analysis/cpp-example/data/DRICHPID.root\"\)
R__LOAD_LIBRARY(podioDict)
R__LOAD_LIBRARY(podioRootIO)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libedm4eicDict)
#include "podio/EventStore.h"
#include "podio/ROOTReader.h"
#include "edm4hep/utils/kinematics.h"

// #define _AEROGEL_

#define _NPE_REFERENCE_ 211
//#define _NPE_REFERENCE_ (11)
//#define _NPE_REFERENCE_ 321

void e01_edm4hep(const char *ifname, const char *ofname = nullptr)
{
  // open recon output .root file with podio
  podio::EventStore podio_store;
  podio::ROOTReader podio_reader;
  podio_reader.openFile(ifname);
  podio_store.setReader(&podio_reader);

  auto np = new TH1D("np", "Photon count",            50,       0,       50);


  // event loop
  for(unsigned ev=0; ev<podio_reader.getEntries(); ev++) {
    if(ev%100==0) printf("read event %d\n",ev);

    // get collections
    auto& cherenkovs = podio_store.get<edm4eic::CherenkovParticleIDCollection>("DRICHPID");
    auto& mctracks   = podio_store.get<edm4hep::MCParticleCollection>("MCParticles");

    // Then the Cherenkov-to-reconstructed mapping;
    // FIXME: may want to use Cherenkov-to-simulated mapping to start with, for the debugging purposes;
    // FIXME: if we loop over reconstructed tracks, rather than MC particles, then we
    // have the 1-1 relation edm4hep::ReconstructedParticle::getParticleIDUsed(),
    // which returns the type edm4hep::ParticleID
    std::map<edm4hep::MCParticle,edm4eic::CherenkovParticleID> rc2cherenkov;
    for(const auto &pid : cherenkovs)
      rc2cherenkov[pid.getAssociatedParticle()] = pid;

    // Loop through all MC tracks; 
    for(const auto &mctrack : mctracks) {
      // FIXME: consider only primaries for now?; equivalent to mctrack.getGeneratorStatus()==1?
      if (mctrack.parents_size()>0) continue;

      edm4eic::CherenkovParticleID cherenkov;
      if(rc2cherenkov.find(mctrack) != rc2cherenkov.end()) cherenkov = rc2cherenkov[mctrack];
      else continue;

      double pp = edm4hep::utils::p(mctrack);
      double m  = mctrack.getMass();

      //printf("m=%5.3f p=%5.1f (%4d) \n", m, pp, mctrack.getPDG());

      // Loop through all of the mass hypotheses available for this reconstructed track;
      {
        const edm4eic::CherenkovPdgHypothesis *best = 0;

        for(const auto &option : cherenkov.getOptions()) {

          if (option.radiator != id) continue;

          // Skip electron hypothesis; of no interest here;
          //if (abs(option.pdg) == 11) continue;

          if (abs(option.pdg) == _NPE_REFERENCE_) {
            np->Fill(option.npe);

            if (ofname) npvector.push_back(option.npe);
          } //if

          if (!best || option.weight > best->weight) best = &option;
          printf("radiator %3d (pdg %5d): weight %7.2f, npe %7.2f\n", 
              option.radiator, option.pdg, option.weight, option.npe);
        } //for option
        printf("\n");

        // Check whether the true PDG got a highest score;
        if (!best || best->pdg != mctrack.getPDG()) false_assignment_stat[best->npe >= 5 ? 0 : 1]++;

        // This assumes of course that at least one radiator was requested in juggler;
        double rindex = cherenkov.getAngles()[id].rindex;
        double theta  = cherenkov.getAngles()[id].theta;
        double lambda = cherenkov.getAngles()[id].wavelength;
        double argument = sqrt(pp*pp + m*m)/(rindex*pp);
        double thp = fabs(argument) <= 1.0 ? acos(argument) : theta;

        th->Fill(1000 * theta);
        //if (mctrack.getPDG() == 321)
        dt->Fill(1000* (theta - thp));
        ri->Fill(rindex - 1.0);
        wl->Fill(lambda);//rindex - 1.0);
        printf("<n> ~ %8.6f, <th> = %7.2f [mrad]\n", rindex - 1.0, 1000*thp);

        if (ofname) thvector.push_back(theta - thp);
      }
    } //for track

    // next event
    podio_store.clear();
    podio_reader.endOfEvent();
  } //for ev

  // end of event loop
  printf("%3d (%3d) false out of %d\n", false_assignment_stat[0], false_assignment_stat[1], podio_reader.getEntries());
  podio_reader.closeFile();

  // write
  if (ofname) {

    auto *ofdata = new TFile(ofname, "RECREATE");

    if (!ofdata) {
      printf("was not able to create output file '%s'\n", ofname);
      exit(0);
    } //if
    auto *ot = new TTree("t", "My tree");

    double thbff, npbff;
    ot->Branch("th", &thbff, "th/D");
    ot->Branch("np", &npbff, "np/D");

    for(unsigned iq=0; iq<thvector.size(); iq++) {
      thbff = thvector[iq];
      npbff = npvector[iq];

      ot->Fill();
    } //for iq

    ot->Write();
    ofdata->Close();
    exit(0);
  } else {
    auto cv = new TCanvas("cv", "", 1700, 500);
    cv->Divide(5, 1);
    cv->cd(1); np->Draw();       np->Fit("gaus");
    cv->cd(2); th->Draw("SAME"); th->Fit("gaus");
    cv->cd(3); ri->Draw();       ri->Fit("gaus");
    cv->cd(4); dt->Draw();       dt->Fit("gaus");
    cv->cd(5); wl->Draw();       //dt->Fit("gaus");
  } //if
} // evaluation()