#include "ePICReaction.h"
#include "ParticleCreator.h"
#include "ePICParticleCreator.h"
#include "ParticleModifier.h"
#include "ePICParticleModifier.h"
#include "Indicing.h"
#include "Histogrammer.h"
#include "BasicKinematicsRDF.h"
#include "ReactionKinematicsRDF.h"
#include "ElectronScatterKinematicsRDF.h"
#include "gammaN_2_Spin0Spin0SpinHalfRDF.h"
#include <TBenchmark.h>
#include <TCanvas.h>
#include <TMath.h>


void ProcessMCMatchedKLambda(std::vector<std::string> infile={"/w/work0/home/rachel/TDISEIC/data/reco/k_lambda_18x275_5000evt_001.edm4eic.root"}, std::string outfile="/w/work5/home/garyp/rad_trees/MCMatched_KLambda_18x275.root"){
  using namespace rad::names::data_type; //for Rec(), Truth()
  ROOT::EnableImplicitMT(8);
  
  outfile="tempout.root";
  
  gBenchmark->Start("df total");
  infile="root://dtn-eic.jlab.org//volatile/eic/romanov/meson-structure-2025-08/reco/18x275/k_lambda_18x275_5000evt_2000.edm4eic.root";
  auto files = GetXRootDFiles("dtn-eic.jlab.org/","/volatile/eic/romanov/meson-structure-2025-08/reco/18x275/","edm4eic.root",1);
  for(auto file : files)
    std::cout << file << std::endl;
  rad::config::ePICReaction epic{"events",files};
  epic.SetBeamsFromMC(); //for this file 0=ebeam 1=pbeam
  
  epic.AliasColumnsAndMatchWithMC();
  
  //rad::indice::UseAsID(index, offset) offset in case beam particle included in record
  epic.setScatElectron(rad::indice::UseAsID(0,2), {"MCScatteredElectrons_objIdx.index"});
  //epic.setParticleIndex("pprime",rad::indice::UseAsID(0,2),{"MCScatteredProtons_objIdx.index"},2212);

  
  //particle creator
  rad::epic::ePICParticleCreator epic_particles{epic};
  rad::epic::ePICParticleModifier  epic_modifier(epic);
  
  //Lambda^0_s
  epic.setParticleIndex("Lambda",2,3122);
  epic_particles.MCMatchedZDCLambda("Lambda");
  //K^+ tagged meson - becomes inclusive missing X
  epic.setParticleIndex("K",1,321);
  
  epic.Particles().Miss("missX",{rad::names::ScatEle().data(),"Lambda"});
  
  epic.setMesonParticles({"missX"});
  epic.setBaryonParticles({"Lambda"});
 
  //must call this after all particles are configured
  epic.makeParticleMap();
  
  epic_modifier.UndoCrossAngle("Lambda");
  epic_modifier.Apply("LambdaCrossAngle");
  
  //option filtering of reconstructed tracks
  //epic.Filter("el_OK==1&&po_OK==1","partFilter");
  //epic.Filter("rec_pmag[scat_ele]>0.1","pmag_scat_ele_filt");
  //epic.Filter("rec_pmag[Lambda]>0.1","pmag_Lambda_filt");
  
  //////////////////////////////////////////////////////////
  // Now define calculated variables
  // Note reconstructed variables will have rec_ prepended
  // truth variables will have tru_ prepended
  //////////////////////////////////////////////////////////

  //masses column name, {+ve particles}, {-ve particles}
  rad::rdf::MissMass(epic,"Welec","{scat_ele}");
  rad::rdf::Mass(epic,"Whad","{missX,Lambda}");
  rad::rdf::Q2(epic,"Q2");

  //t distribution, column name
  rad::rdf::TTop(epic,"t_top");
  rad::rdf::TBot(epic,"t_bot");
  rad::rdf::TPrimeTop(epic,"tp_top");
  rad::rdf::TPrimeBot(epic,"tp_bot");
  
  //CM production angles
  rad::rdf::CMAngles(epic,"CM");

  //exlusivity
  rad::rdf::MissMass(epic,"MissMassX","{scat_ele,Lambda}");
  rad::rdf::MissP(epic,"MissP_X","{scat_ele,K}");
  rad::rdf::MissPt(epic,"MissPt_X","{scat_ele,K}");
  rad::rdf::MissPz(epic,"MissPz_X","{scat_ele,K}");
  rad::rdf::MissTheta(epic,"MissTheta_X","{scat_ele,K}");

  //decay angles
  rad::rdf::gn2s0s0s12::HelicityAngles(epic,"Heli");

  ///////////////////////////////////////////////////////////
  //Define histograms
  ///////////////////////////////////////////////////////////
  rad::histo::Histogrammer histo{"set1",epic};
  // we can create many histograms by splitting events into
  // bins, where the same histogram is produced for the given bin
  // e.g. create 10 bins in tru_W between 4 and 54 GeV 
  //histo.Splitter().AddRegularDimension(Truth()+"W", rad::histo::RegularSplits(10,4,14) );
  //can add as many split dimensions as we like
  //histo.Splitter().AddRegularDimension("xxx", rad::histo::RegularSplits(nbins,low,high) );
  histo.Init({Rec(),Truth()});//will create histograms for rec and truth

  histo.Create<TH1D,double>({"hQ2",";Q^{2} [GeV^{2}]",100,0,500.},{"Q2"});
  histo.Create<TH1D,double>({"hWelec",";W (electro miss mass) [GeV/c^{2}]",100,0,200.},{"Welec"});
  histo.Create<TH1D,double>({"hWhad",";W (hadro final state) [GeV/c^{2}]",100,0,200.},{"Whad"});
  histo.Create<TH1D,double>({"hMissMassX",";M_{miss} [GeV/c^{2}]",1000,-200,200},{"MissMassX"});
  
  histo.Create<TH1D,double>({"httop",";t(top vertex) [GeV^{2}]",100,-1,5},{"t_top"});
  histo.Create<TH1D,double>({"htbot",";t(bottom vertex) [GeV^{2}]",100,-1,5},{"t_bot"});
  histo.Create<TH1D,double>({"htptop",";t'(top vertex) [GeV^{2}]",100,-1,5},{"tp_top"});
  histo.Create<TH1D,double>({"htpbot",";t'(bottom vertex) [GeV^{2}]",100,-1,5},{"tp_bot"});
  
  histo.Create<TH1D,double>({"hcthCM",";cos(#theta_{CM})",100,-1,1},{"CM_CosTheta"});
  histo.Create<TH1D,double>({"hphCM",";#phi_{CM}",100,-TMath::Pi(),TMath::Pi()},{"CM_Phi"});
  
  histo.Create<TH1D,double>({"hmissP",";p_{miss}(e',K)",1000,-100,100},{"MissP_X"});
  histo.Create<TH1D,double>({"hmissPt",";p_{t,miss}(e',K)",100,0,10},{"MissPt_X"});
  histo.Create<TH1D,double>({"hmissPz",";p_{z,miss}(e',K)",1000,-100,100},{"MissPz_X"});
  histo.Create<TH1D,double>({"hmissTheta",";#theta_{miss}(e',K)",100,-TMath::Pi(),TMath::Pi()},{"MissTheta_X"});
 
  //particle momenta
  histo.Create<TH1D,double>({"hpmag_elec",";p_{e'} [GeV/c]",100,-1,20},{"pmag[scat_ele]"});
  histo.Create<TH1D,double>({"heta_elec",";#eta_{e'} ",100,-10,10},{"eta[scat_ele]"});
  histo.Create<TH1D,double>({"htheta_elec",";#theta_{e'} [rad]",100,-TMath::Pi(),TMath::Pi()},{"theta[scat_ele]"});
  histo.Create<TH1D,double>({"hphi_elec",";#phi_{e'} [rad]",100,-TMath::Pi(),TMath::Pi()},{"phi[scat_ele]"});
  
  histo.Create<TH1D,double>({"hpmag_Lambda",";p_{p'} [GeV/c]",100,-1,300},{"pmag[Lambda]"});
  histo.Create<TH1D,double>({"heta_Lambda",";#eta_{p'} ",100,-10,10},{"eta[Lambda]"});
  histo.Create<TH1D,double>({"htheta_Lambda",";#theta_{p'} [rad]",1000,0,1},{"theta[Lambda]"});
  histo.Create<TH1D,double>({"hphi_Lambda",";#phi_{p'} [rad]",100,-TMath::Pi(),TMath::Pi()},{"phi[Lambda]"});
  
  //finally, book lazy snapshot before processing
  //benchmark here will be zero if lazy snapshot
  //which now works and will be booked till trigger
  gBenchmark->Start("snapshot");
  epic.BookLazySnapshot(outfile);
  //epic.Snapshot("MCMatchedKLambda.root");
  gBenchmark->Stop("snapshot");
  gBenchmark->Print("snapshot");

  gBenchmark->Start("processing");
  ///////////////////////////////////////////////////////////
  //Draw histograms
  ///////////////////////////////////////////////////////////
  
  
  TCanvas *c00 = new TCanvas();
  c00->Divide(2,2);
  c00->cd(1)->SetLogy();
  histo.DrawSame("hQ2",gPad);
  c00->cd(2)->SetLogy();
  histo.DrawSame("hWelec",gPad);
  c00->cd(3)->SetLogy();
  histo.DrawSame("hWhad",gPad);
  c00->cd(4)->SetLogy();
  histo.DrawSame("hMissMassX",gPad);

  TCanvas *c01 = new TCanvas();
  c01->Divide(2,2);
  c01->cd(1)->SetLogy();
  histo.DrawSame("httop",gPad);
  c01->cd(2)->SetLogy();
  histo.DrawSame("htbot",gPad);
  c01->cd(3)->SetLogy();
  histo.DrawSame("htptop",gPad);
  c01->cd(4)->SetLogy();
  histo.DrawSame("htpbot",gPad);
  
  TCanvas *c02 = new TCanvas();
  c02->Divide(2,2);
  c02->cd(1)->SetLogy();
  histo.DrawSame("hmissP",gPad);
  c02->cd(2)->SetLogy();
  histo.DrawSame("hmissPt",gPad);
  c02->cd(3)->SetLogy();
  histo.DrawSame("hmissPz",gPad);
  c02->cd(4)->SetLogy();
  histo.DrawSame("hmissTheta",gPad);
  
  //reco elec kin
  TCanvas *c03 = new TCanvas();
  c03->Divide(2,2);
  c03->cd(1)->SetLogy();
  histo.DrawSame("hpmag_elec",gPad);
  c03->cd(2)->SetLogy();
  histo.DrawSame("heta_elec",gPad);
  c03->cd(3)->SetLogy();
  histo.DrawSame("htheta_elec",gPad);
  c03->cd(4)->SetLogy();
  histo.DrawSame("hphi_elec",gPad);
  
  //reco proton kin
  TCanvas *c04 = new TCanvas();
  c04->Divide(2,2);
  c04->cd(1)->SetLogy();
  histo.DrawSame("hpmag_Lambda",gPad);
  c04->cd(2)->SetLogy();
  histo.DrawSame("heta_Lambda",gPad);
  c04->cd(3)->SetLogy();
  histo.DrawSame("htheta_Lambda",gPad);
  c04->cd(4)->SetLogy();
  histo.DrawSame("hphi_Lambda",gPad);
  
  gBenchmark->Stop("processing");
  gBenchmark->Print("processing");

  //save all histograms to file
  //histo.File("MCMatchedKLambda_hists.root");

  gBenchmark->Stop("df total");
  gBenchmark->Print("df total");
  
  
}
