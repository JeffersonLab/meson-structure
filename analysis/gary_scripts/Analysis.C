//this needs to go before include mesonMC.h
//otherwise dont get correct path
//at compile time
#ifdef CTEQ_TBL_PATH
  #undef CTEQ_TBL_PATH
#endif
#define CTEQ_TBL_PATH "../../mesonSFgen/src/cteq-tbls"

#include "../../mesonSFgen/src/EIC_mesonMC.h"
//#include "../../mesonSFgen/src/EIC_mesonMC.cpp"
#include "../../mesonSFgen/src/functions/sf.h"

//#include "binning.C"
//#include "/home/garyp/eic/EPICStyle/EPICStyle.C"
#include "/home/garyp/eic/epic_plot_macro/ePIC_style.C"

using ROOT::VecOps::RVec;
using ROOT::Math::PxPyPzMVector;
using ROOT::Math::VectorUtil::boost;

const std::vector<EColor> kp6 = {kP6Violet, kP6Gray, kP6Grape, kP6Red, kP6Yellow, kP6Blue};
const std::vector<int> vEcom = {20, 45, 140};
const std::vector<string> vEset = {"5x41", "10x100", "18x275"};

void DrawTruRec(TH1D* h1, TH1D* h2, bool legend=false){

//all->SetLineColor(kBlack);
h1->SetLineColor(kp6[0]);
//h1->SetFillColorAlpha(kp6[0],0.8);
//h1->SetFillStyle(3004);
h2->SetLineColor(kp6[1]);
//h2->SetFillColorAlpha(kp6[1],0.8);
//h2->SetFillStyle(3005);
//all->SetMaximum(1.25*all->GetMaximum());
//all->DrawCopy("hist p");
auto h1c = h1->DrawCopy();
h1c->SetMinimum(0);
auto h2c = h2->DrawCopy("same");
if(legend){
TLegend *leg = new TLegend(0.6,0.6,0.7,0.75);
leg->AddEntry(h1c,"Truth","l");
leg->AddEntry(h2c,"Reconstructed","l");
leg->Draw();
}
}


void Analysis(std::string infile="/w/work5/home/garyp/rad_trees/MCMatched_KLambda_18x275.root"){
  
  //SetEPICStyle();
  set_ePIC_style(); //official epic
  //style corrections needed for official epic
  gStyle->SetOptTitle(0);
  gStyle->SetOptFit(0);
  gStyle->SetPadRightMargin(0.1);
  TLatex tex;
  tex.SetTextSize(0.05);
  tex.SetTextAlign(13);
  tex.SetNDC();
  TGaxis::SetMaxDigits(3);

  initcteqpdf();
  ROOT::EnableImplicitMT(8);
  //ROOT::DisableImplicitMT();
  ROOT::RDataFrame df_raw("rad_tree",infile);
  auto df_filt = df_raw.Filter("tru_xbj<=1");
  
  auto df = df_filt.Define("res_t","tru_t_bot-rec_t_bot");
  df = df.Define("tru_lambda_mass", [](ROOT::VecOps::RVec<double>&var, int&id)
		 { return var[id]; }
		 ,{"MCParticles_mass","Lambda"});//
  df = df.Define("rec_lambda_mass", [](ROOT::VecOps::RVec<float>&var, int&id)
		 { return var[id]; }
		 ,{"ReconstructedParticles_mass","Lambda"});//
  
  df = df.Define("inucl","1");
  //needed for now as small number of events truth xbj calc > 1
  //debug and fix that later
  df = df.Define("tru_F2N", F2N, {"tru_xbj","tru_Q2","inucl"});
  
  df = df
    .Define("tru_pmag_lambda","tru_pmag[Lambda]")
    .Define("tru_px_lambda","MCParticles_momentum_x[Lambda]")
    .Define("tru_py_lambda","MCParticles_momentum_x[Lambda]")
    .Define("tru_pz_lambda","MCParticles_momentum_x[Lambda]")
    .Define("rec_pmag_lambda","rec_pmag[Lambda]")
    .Define("rec_px_lambda","ReconstructedParticles_momentum_x[Lambda]")
    .Define("rec_py_lambda","ReconstructedParticles_momentum_x[Lambda]")
    .Define("rec_pz_lambda","ReconstructedParticles_momentum_x[Lambda]");
  
  double Mp = 0.938;
  double Mlambda = 1.115;
  double ebeamE = 18.0;
  double pbeamE = 275.0;
  //x_L
  df = df
    .Define("tru_xL",[&pbeamE, &Mlambda](double px, double py, double pz){
      PxPyPzMVector vlambda(px,py,pz,Mlambda);
      auto lambdaE = vlambda.E();
      return lambdaE / pbeamE;
    },{"tru_px_lambda","tru_py_lambda","tru_pz_lambda"})
  .Define("rec_xL",[&pbeamE, &Mlambda](float px, float py, float pz){
      PxPyPzMVector vlambda(px,py,pz,Mlambda);
      auto lambdaE = vlambda.E();
      return lambdaE / pbeamE;
    },{"rec_px_lambda","rec_py_lambda","rec_pz_lambda"});
  
  //scat elec
  df = df
    //tru
    .Define("tru_pmag_scatele","tru_pmag[scat_ele]")
    .Define("tru_pz_scatele","MCParticles_momentum_z[scat_ele]")
    .Define("tru_eta_scatele","tru_eta[scat_ele]")
    .Define("tru_theta_scatele","tru_theta[scat_ele]")
    .Define("tru_phi_scatele","tru_phi[scat_ele]")
    //rec
    .Define("rec_pmag_scatele","rec_pmag[scat_ele]")
    .Define("rec_pz_scatele","ReconstructedParticles_momentum_z[scat_ele]")
    .Define("rec_eta_scatele","rec_eta[scat_ele]")
    .Define("rec_theta_scatele","rec_theta[scat_ele]")
    .Define("rec_phi_scatele","rec_phi[scat_ele]");
    
  
  //scattered electron
  auto df_scatele = df.Filter("rec_pmag[scat_ele]>0");
  //truth
  auto htru_Q2_scatele = df.Histo1D({"htru_Q2_scatel",";Q^{2} [GeV^{2}];Events",100,0,500},"tru_Q2");
  auto htru_pmag_scatele = df.Histo1D({"htru_pmag_scatele",";p [GeV/c]; Events",100,0,18},"tru_pmag_scatele");
  auto htru_pz_scatele = df.Histo1D({"htru_pz_scatele",";p_{z} [GeV/c]; Events",100,0,18},"tru_pz_scatele");
  auto htru_eta_scatele = df.Histo1D({"htru_eta_scatele",";#eta; Events",100,-6,6},"tru_eta_scatele");
  auto htru_theta_scatele = df.Histo1D({"htru_theta_scatele",";#theta [rad]; Events",100,-TMath::Pi(),TMath::Pi()},"tru_theta_scatele");
  auto htru_phi_scatele = df.Histo1D({"htru_phi_scatele",";#phi [rad]; Events",100,-TMath::Pi(),TMath::Pi()},"tru_phi_scatele");
  //rec
  auto hrec_Q2_scatele = df_scatele.Histo1D({"hrec_Q2_scatel",";Q^{2} [GeV^{2}];Events",100,0,500},"rec_Q2");
  auto hrec_pmag_scatele = df_scatele.Histo1D({"hrec_pmag_scatele",";p [GeV/c]; Events",100,0,18},"rec_pmag_scatele");
  auto hrec_pz_scatele = df_scatele.Histo1D({"hrec_pz_scatele",";p_{z} [GeV/c]; Events",100,0,18},"rec_pz_scatele");
  auto hrec_eta_scatele = df_scatele.Histo1D({"hrec_eta_scatele",";#eta; Events",100,-6,6},"rec_eta_scatele");
  auto hrec_theta_scatele = df_scatele.Histo1D({"hrec_theta_scatele",";#theta [rad]; Events",100,-TMath::Pi(),TMath::Pi()},"rec_theta_scatele");
  auto hrec_phi_scatele = df_scatele.Histo1D({"hrec_phi_scatele",";#phi [rad]; Events",100,-TMath::Pi(),TMath::Pi()},"rec_phi_scatele");
  //
  
  
  //acc vs t
  auto tmax=2.5;
  auto t_res_cut=0.4;
  auto htru_t = df.Histo1D({"htru_t","",100,0,tmax},"tru_t_bot");
  auto hrec_t = df.Histo1D({"hrec_t","",100,0,tmax},"rec_t_bot");
  auto hrec_t_rescut = df.Filter(Form("fabs(res_t)<%f",t_res_cut)).Histo1D({"hrec_t_rescut","",100,0,tmax},"rec_t_bot");
  
  //delta t vs t
  auto h2d_res_t = df.Histo2D({"h2d_res_t","Resolution;|t|_{truth} [GeV^{2}];#Delta|t| [GeV^{2}]",100,0,tmax,100,-1,1},"tru_t_bot","res_t");
  
  //Lambda mass recon
  auto htru_lambda_mass = df.Histo1D({"htru_lambda_mass","Truth;M_{#Lambda} [GeV/c]",100,0,2},"tru_lambda_mass");
  auto hrec_lambda_mass = df.Histo1D({"hrec_lambda_mass","Reconstructed;M_{#Lambda} [GeV/c]",100,0,2},"rec_lambda_mass");
  
  //Lambda det eff as % vs variables
  
  //DeltaF2 vs -t 
  const auto nbin=5;
  const auto Q2_min=0;
  const auto Q2_max=500;
  const auto xbj_min=0.001;
  const auto xbj_max=1.0;
  
  // Configure bins - later automate this in loop using nbin
  std::vector<double> Q2_bins = {0, 50, 100, 200, 350, 500};
  std::vector<double> x_bins  = {0.001, 0.01, 0.05, 0.1, 0.3, 1.0};

  
  // Build regions - integrate this fully later on
  //auto regions = makeRegions(Q2_bins, x_bins);
  
  
  // Capture Q2,xbj bins by value in lambdas
  df = df
    .Define("Q2_bin", [Q2_bins](double Q2){
	auto it = std::lower_bound(Q2_bins.begin(), Q2_bins.end(), Q2);
	int idx = std::max(0, int(it - Q2_bins.begin()) - 1);
	if (idx < 0 || idx >= int(Q2_bins.size()) - 1) return -1;
	return idx;
      }, {"tru_Q2"})
    .Define("x_bin", [x_bins](double x) {
	auto it = std::lower_bound(x_bins.begin(), x_bins.end(), x);
	int idx = std::max(0, int(it - x_bins.begin()) - 1);
	if (idx < 0 || idx >= int(x_bins.size()) - 1) return -1;
	return idx;
      }, {"tru_xbj"});
  
  
  auto nx_t = 20;
  auto tmin = 0;
  //auto tmax = 2;
  auto ny_f2 = 20;
  auto f2min = 0;
  auto f2max = 1;
  
  //std::vector<std::vector<ROOT::RDF::RResultPtr<TH2D>>> htru_2d_t_f2n;
  std::vector<std::vector<ROOT::RDF::RResultPtr<TH2D>>> htru_2d_t_f2n(nbin, std::vector<ROOT::RDF::RResultPtr<TH2D>>(nbin));
  //htru_2d_t_f2n.resize(nbin);
  //auto htru_2d_t_f2n[nbin][nbin];
  for (auto iq=0; iq<nbin; iq++){
      for (auto ix=0; ix<nbin; ix++){
	//htru_2d_t_f2n[iq][ix]= df.Filter(Form("htru_2d_t_f2n_%i_%i",iq,jx))Histo2D({Form("htru_2d_t_f2n","",100,0,2,100,0,1},"tru_t_bot","tru_F2N");
	
	
	auto view = df.Filter([iq, ix](int qb, int xb){
	    return qb == iq && xb == ix;
	  }, {"Q2_bin", "x_bin"});
	
	// Unique histogram name & title
	std::string hname = Form("htru_2d_t_f2n_%d_%d", iq, ix);
	std::string htitle = Form("F2N vs -t (Q2 bin %d, x bin %d)", iq, ix);
	
	htru_2d_t_f2n[iq][ix] = view.Histo2D(ROOT::RDF::TH2DModel(hname.c_str(), 
							       htitle.c_str(), 
							       nx_t, 
							       tmin, tmax, 
							       ny_f2, 
							       f2min, f2max), 
					  "tru_t_bot", "tru_F2N");
	
      }
  }
  
  auto htru_f2n = df.Histo1D({"htru_f2n","",100,0,1},"tru_F2N");
  
  
  //rate vs -t
    
  //hit distributions from sullivan process particles in detectors
    
  //deviation of recon sullivan process track momentum from truth track
    
    
  std::cout << "Everything is booked." << endl;
  auto trigger = *df.Count();
  
  //canvases
  TCanvas *c000 = new TCanvas("c000","Scattered electron acceptance",1500,1000);
  c000->Divide(3,2);
  c000->cd(1);
  DrawTruRec(htru_Q2_scatele.GetPtr(), hrec_Q2_scatele.GetPtr(),1);
  c000->cd(2);
  DrawTruRec(htru_pmag_scatele.GetPtr(), hrec_pmag_scatele.GetPtr());
  c000->cd(3);
  DrawTruRec(htru_pz_scatele.GetPtr(), hrec_pz_scatele.GetPtr());
  c000->cd(4);
  DrawTruRec(htru_eta_scatele.GetPtr(), hrec_eta_scatele.GetPtr());
  c000->cd(5);
  DrawTruRec(htru_theta_scatele.GetPtr(), hrec_theta_scatele.GetPtr());
  c000->cd(6);
  DrawTruRec(htru_phi_scatele.GetPtr(), hrec_phi_scatele.GetPtr());
  
  TCanvas *c00 = new TCanvas("c00","|t| Acceptance and Resolution",1000,500);
  c00->Divide(2,1);
  c00->cd(1)->SetLogy();
  auto hacc_t = (TH1D*)hrec_t->Clone("hacc_t");
  hacc_t->SetTitle(";|t| [GeV^{2}]; Acceptance");
  hacc_t->Divide(htru_t.GetPtr());
  hacc_t->DrawCopy();
  auto hacc_t_rescut = (TH1D*)hrec_t_rescut->Clone("hacc_t_rescut");
  hacc_t_rescut->SetTitle(";|t| [GeV^{2}]; Acceptance");
  hacc_t_rescut->Divide(htru_t.GetPtr());
  hacc_t_rescut->SetLineStyle(7);
  hacc_t_rescut->SetLineColor(kRed);
  hacc_t_rescut->DrawCopy("same");
  auto l_acc = new TLine(0,1,tmax,1);
  l_acc->SetLineStyle(7);
  l_acc->Draw();
  
  c00->cd(2);
  h2d_res_t->DrawCopy("colz");
  auto l_res_t_hi = new TLine(0,t_res_cut,tmax,t_res_cut);
  l_res_t_hi->SetLineStyle(7);
  l_res_t_hi->SetLineColor(kRed);
  l_res_t_hi->Draw();
  auto l_res_t_lo = new TLine(0,-t_res_cut,tmax,-t_res_cut);
  l_res_t_lo->SetLineStyle(7);
  l_res_t_lo->SetLineColor(kRed);
  l_res_t_lo->Draw();
  
  
  TCanvas *c01 = new TCanvas("c01","Lambda Mass Reconstruction",500,500);
  htru_lambda_mass->DrawCopy();
  hrec_lambda_mass->SetLineColor(kRed);
  hrec_lambda_mass->DrawCopy("same");
  auto mass_leg = gPad->BuildLegend(0.2,0.7,0.4,0.8);


  TCanvas *c02 = new TCanvas("c02","F2N",500,500);
  htru_f2n->SetTitle("Truth F2N Calculated Post-Hoc Simulation + Reconstruction");
  htru_f2n->DrawCopy();
  //htru_2d_t_f2n->DrawCopy("colz");
  
  TCanvas *c03 = new TCanvas("co3","F2N vs t binned");
  c03->Divide(nbin,nbin);
  int idx=1;
  for(int iq=0; iq<nbin; iq++){
    for(int ix=0; ix< nbin; ix++){
      c03->cd(idx);
      htru_2d_t_f2n[iq][ix]->FitSlicesY();
      TH1D *htru_2d_t_f2n_1 = (TH1D*) gDirectory->Get(Form("htru_2d_t_f2n_%d_%d_1",iq,ix));
      //htru_2d_t_f2n[iq][ix]->DrawCopy();
      htru_2d_t_f2n_1->DrawCopy();
      idx++;
    }
  }
  
}
