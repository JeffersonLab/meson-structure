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

#include "KLambdaCrossSection.C"
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
auto h2c = h2->DrawCopy("same");
if(legend){
TLegend *leg = new TLegend(0.6,0.6,0.7,0.75);
leg->AddEntry(h1c,"Truth","l");
leg->AddEntry(h2c,"Reconstructed","l");
leg->Draw();
}
}

//infile = rad output tree for analysis
//genfile = MesonMC gen output file for cross section calculation
void Analysis(std::string infile="/w/work5/home/garyp/rad_trees/MCMatched_KLambda_18x275.root", std::string genfile="/w/work5/home/garyp/eic/eg-orig-kaon-lambda/k_lambda_crossing_0.000-18.0on275.0_x0.0001-1.0000_q1.0-500.0.root"){
  
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
  
  
  //get cross section value from generator file
  auto vxsec = KLambdaCrossSection(genfile,1e6); //1e6 events is enough
  auto xsec = vxsec[0];
  auto err_xsec = vxsec[1];

  initcteqpdf();
  ROOT::EnableImplicitMT(8);
  //ROOT::DisableImplicitMT();
  ROOT::RDataFrame df_raw("rad_tree",infile);
  
  //resolutions
  auto df = df_raw
    .Define("res_t","tru_t_bot-rec_t_bot")
    .Define("res_Q2","tru_Q2-rec_Q2")
    .Define("res_xbj","tru_xbj-rec_xbj");
  
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
    
  //spectator lambda
  df = df
    //tru
    .Define("tru_pmag_lambda","tru_pmag[Lambda]")
    .Define("tru_px_lambda","MCParticles_momentum_x[Lambda]")
    .Define("tru_py_lambda","MCParticles_momentum_y[Lambda]")
    .Define("tru_pz_lambda","MCParticles_momentum_z[Lambda]")
    .Define("tru_m_lambda","MCParticles_mass[Lambda]")
    .Define("tru_eta_lambda","tru_eta[Lambda]")
    .Define("tru_theta_lambda","tru_theta[Lambda]")
    .Define("tru_phi_lambda","tru_phi[Lambda]")
    //rec
    .Define("rec_pmag_lambda","rec_pmag[Lambda]")
    .Define("rec_px_lambda","ReconstructedParticles_momentum_x[Lambda]")
    .Define("rec_py_lambda","ReconstructedParticles_momentum_y[Lambda]")
    .Define("rec_pz_lambda","ReconstructedParticles_momentum_z[Lambda]")
    .Define("rec_m_lambda","ReconstructedParticles_mass[Lambda]")
    .Define("rec_eta_lambda","rec_eta[Lambda]")
    .Define("rec_theta_lambda","rec_theta[Lambda]")
    .Define("rec_phi_lambda","rec_phi[Lambda]")
    //resolution
    .Define("res_pmag_lambda","(tru_pmag_lambda-rec_pmag_lambda)/tru_pmag_lambda")
    .Define("res_theta_lambda","tru_theta_lambda-rec_theta_lambda")
    .Define("res_phi_lambda","tru_phi_lambda-rec_phi_lambda");
    
  
  double Mp = 0.938;
  double Mlambda = 1.115;
  double ebeamE = 18.0;
  double pbeamE = 275.0;
  //x_L
  df = df
    .Define("tru_xL",[](RVec<double> px, RVec<double> py, RVec<double> pz, RVec<double> mass, int ebeam_id, int pbeam_id, int lambda_id){
	PxPyPzMVector ebeam(px[ebeam_id],py[ebeam_id],pz[ebeam_id],mass[ebeam_id]);
	PxPyPzMVector pbeam(px[pbeam_id],py[pbeam_id],pz[pbeam_id],mass[pbeam_id]);
	PxPyPzMVector lambda(px[lambda_id],py[lambda_id],pz[lambda_id],mass[lambda_id]);
	auto xL = lambda.Dot(ebeam) / pbeam.Dot(ebeam);
	return xL;
      },{"MCParticles_momentum_x","MCParticles_momentum_y","MCParticles_momentum_z","MCParticles_mass","beam_ele","beam_ion","Lambda"})
    .Define("rec_xL",[](RVec<float> px, RVec<float> py, RVec<float> pz, RVec<float> mass, int ebeam_id, int pbeam_id, int lambda_id){
	PxPyPzMVector ebeam(px[ebeam_id],py[ebeam_id],pz[ebeam_id],mass[ebeam_id]);
	PxPyPzMVector pbeam(px[pbeam_id],py[pbeam_id],pz[pbeam_id],mass[pbeam_id]);
	PxPyPzMVector lambda(px[lambda_id],py[lambda_id],pz[lambda_id],mass[lambda_id]);
	auto xL = lambda.Dot(ebeam) / pbeam.Dot(ebeam);
	return xL;
      },{"ReconstructedParticles_momentum_x","ReconstructedParticles_momentum_y","ReconstructedParticles_momentum_z","ReconstructedParticles_mass","beam_ele","beam_ion","Lambda"});
    
  //xk
  df = df
    .Define("tru_xk",[](double xbj, double xL){
	return xbj / (1-xL);
      },{"tru_xbj","tru_xL"})
    .Define("rec_xk",[](double xbj, double xL){
	return xbj / (1-xL);
      },{"rec_xbj","rec_xL"});
  
  const auto nbin=4;
  const auto Q2_min=1;
  const auto Q2_max=500;
  const auto xbj_min=0.0001;
  const auto xbj_max=1.0;
  
  // Configure bins - later automate this in binning.C header
  std::vector<double> Q2_bins = {1, 25, 100, 250, 500};
  std::vector<double> x_bins  = {0.0001, 0.001, 0.01, 0.1, 1.0};

  
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
  
  
  df = df.Define("inucl","1");
  //here we need to split them to cut on xbj, to preserve the truth count
  //but also not crash the f2kZEUS and F2N functions with "bad" xbj values
  //kaon and nucleon structure functions
  auto df_tru = df
    .Filter("tru_xbj>0.0001 && tru_xbj<=1.0");
  df_tru = df_tru
    .Define("tru_F2k", f2kZEUS, {"tru_xbj","tru_Q2"})
    .Define("tru_F2N", F2N, {"tru_xbj","tru_Q2","inucl"});
  auto df_rec = df_tru
    .Filter("rec_xbj>0.0001 && rec_xbj<=1.0");
  df_rec = df_rec
    .Define("rec_F2k", f2kZEUS, {"rec_xbj","rec_Q2"})
    .Define("rec_F2N", F2N, {"rec_xbj","rec_Q2","inucl"});
  
  //limits and bins
  auto nx_t = 10;
  auto tmin = 0;
  auto tmax = 2.5;
  auto ny_f2 = 100;
  auto f2min = 0.0;
  auto f2max = 0.5;
  
  //scattered electron
  TCut good_scatele = "rec_pmag[scat_ele]>0";
  auto df_scatele = df_rec.Filter(good_scatele.GetTitle());
  //truth
  auto htru_Q2_scatele = df.Histo1D({"htru_Q2_scatel",";Q^{2} [GeV^{2}];Events",100,0,500},"tru_Q2");
  auto htru_pmag_scatele = df.Histo1D({"htru_pmag_scatele",";p [GeV/c]; Events",100,0,18},"tru_pmag_scatele");
  auto htru_pz_scatele = df.Histo1D({"htru_pz_scatele",";p_{z} [GeV/c]; Events",100,-18,18},"tru_pz_scatele");
  auto htru_eta_scatele = df.Histo1D({"htru_eta_scatele",";#eta; Events",100,-5,5},"tru_eta_scatele");
  auto htru_theta_scatele = df.Histo1D({"htru_theta_scatele",";#theta [rad]; Events",100,0,TMath::Pi()},"tru_theta_scatele");
  auto htru_phi_scatele = df.Histo1D({"htru_phi_scatele",";#phi [rad]; Events",100,0,TMath::Pi()},"tru_phi_scatele");
  //rec
  auto hrec_Q2_scatele = df_scatele.Histo1D({"hrec_Q2_scatel",";Q^{2} [GeV^{2}];Events",100,0,500},"rec_Q2");
  auto hrec_pmag_scatele = df_scatele.Histo1D({"hrec_pmag_scatele",";p [GeV/c]; Events",100,0,18},"rec_pmag_scatele");
  auto hrec_pz_scatele = df_scatele.Histo1D({"hrec_pz_scatele",";p_{z} [GeV/c]; Events",100,-18,18},"rec_pz_scatele");
  auto hrec_eta_scatele = df_scatele.Histo1D({"hrec_eta_scatele",";#eta; Events",100,-5,5},"rec_eta_scatele");
  auto hrec_theta_scatele = df_scatele.Histo1D({"hrec_theta_scatele",";#theta [rad]; Events",100,0,TMath::Pi()},"rec_theta_scatele");
  auto hrec_phi_scatele = df_scatele.Histo1D({"hrec_phi_scatele",";#phi [rad]; Events",100,0,TMath::Pi()},"rec_phi_scatele");
  //
  
  //scattered electron
  TCut good_lambda = "rec_pmag[Lambda]>0";
  auto df_lambda = df_rec.Filter(good_lambda.GetTitle());
  //truth
  auto htru_t_lambda = df.Histo1D({"htru_t_lambda",";|t| [GeV^{2}];Events",100,0,tmax},"tru_t_bot");
  auto htru_pmag_lambda = df.Histo1D({"htru_pmag_lambda",";p [GeV/c]; Events",100,0,275},"tru_pmag_lambda");
  auto htru_pz_lambda = df.Histo1D({"htru_pz_lambda",";p_{z} [GeV/c]; Events",100,-275,275},"tru_pz_lambda");
  auto htru_eta_lambda = df.Histo1D({"htru_eta_lambda",";#eta; Events",100,4,10},"tru_eta_lambda");
  auto htru_theta_lambda = df.Histo1D({"htru_theta_lambda",";#theta [rad]; Events",100,0,0.01},"tru_theta_lambda");
  auto htru_phi_lambda = df.Histo1D({"htru_phi_lambda",";#phi [rad]; Events",100,-TMath::Pi(),TMath::Pi()},"tru_phi_lambda");
  //rec
  auto hrec_t_lambda = df_lambda.Histo1D({"hrec_t_lambda",";|t| [GeV^{2}];Events",100,0,tmax},"rec_t_bot");
  auto hrec_pmag_lambda = df_lambda.Histo1D({"hrec_pmag_lambda",";p [GeV/c]; Events",100,0,275},"rec_pmag_lambda");
  auto hrec_pz_lambda = df_lambda.Histo1D({"hrec_pz_lambda",";p_{z} [GeV/c]; Events",100,-275,275},"rec_pz_lambda");
  auto hrec_eta_lambda = df_lambda.Histo1D({"hrec_eta_lambda",";#eta; Events",100,4,10},"rec_eta_lambda");
  auto hrec_theta_lambda = df_lambda.Histo1D({"hrec_theta_lambda",";#theta [rad]; Events",100,0,0.01},"rec_theta_lambda");
  auto hrec_phi_lambda = df_lambda.Histo1D({"hrec_phi_lambda",";#phi [rad]; Events",100,-TMath::Pi(),TMath::Pi()},"rec_phi_lambda");
  //
  
  
  TCut good_rec = good_scatele && good_lambda;
  auto df_good = df_rec.Filter(good_rec.GetTitle());
  //2D phase space
  auto htru_2d_x_Q2 = df_tru.Histo2D({"htru_2d_x_Q2","Generated Phase Space;x_{bj};Q^{2} [GeV^{2}]",20,0,1,20,0,500},"tru_xbj","tru_Q2");
  auto hrec_2d_x_Q2 = df_good.Histo2D({"hrec_2d_x_Q2","Reconstructed Phase Space;x_{bj};Q^{2} [GeV^{2}]",20,0,1,20,0,500},"rec_xbj","rec_Q2");
  
  //acc vs t
  auto t_res_cut=0.4;
  auto htru_t = df_tru.Histo1D({"htru_t","",100,0,tmax},"tru_t_bot");
  auto hrec_t = df_good.Histo1D({"hrec_t","",100,0,tmax},"rec_t_bot");
  auto hrec_t_rescut = df_good.Filter(Form("fabs(res_t)<%f",t_res_cut)).Histo1D({"hrec_t_rescut","",100,0,tmax},"rec_t_bot");
  
  //delta t vs t
  auto h2d_res_t = df_tru.Histo2D({"h2d_res_t",";|t|_{truth} [GeV^{2}];#Delta|t| [GeV^{2}]",100,0,tmax,100,-1,1},"tru_t_bot","res_t");
  
  //Lambda mass recon
  auto htru_m_lambda = df_tru.Histo1D({"htru_m_lambda",";M_{#Lambda} [GeV/c]",100,0,2},"tru_m_lambda");
  auto hrec_m_lambda = df_good.Histo1D({"hrec_m_lambda",";M_{#Lambda} [GeV/c]",100,0,2},"rec_m_lambda");
  
  //Lambda det eff as % vs variables
  
  //DeltaF2 vs -t 
  
  //std::vector<std::vector<ROOT::RDF::RResultPtr<TH2D>>> htru_2d_t_F2k;
  std::vector<std::vector<ROOT::RDF::RResultPtr<TH2D>>> htru_2d_t_F2k(nbin, std::vector<ROOT::RDF::RResultPtr<TH2D>>(nbin));
  //htru_2d_t_F2k.resize(nbin);
  //auto htru_2d_t_F2k[nbin][nbin];
  for (auto iq=0; iq<nbin; iq++){
      for (auto ix=0; ix<nbin; ix++){
	//htru_2d_t_F2k[iq][ix]= df.Filter(Form("htru_2d_t_F2k_%i_%i",iq,jx))Histo2D({Form("htru_2d_t_F2k","",100,0,2,100,0,1},"tru_t_bot","tru_F2k");
	
	
	auto view = df_rec.Filter([iq, ix](int qb, int xb){
	    return qb == iq && xb == ix;
	  }, {"Q2_bin", "x_bin"});
	
	// Unique histogram name & title
	std::string hname = Form("htru_2d_t_F2k_%d_%d", iq, ix);
	std::string htitle = Form("Q2 bin %d, x bin %d", iq, ix);
	gStyle->SetOptTitle(1);
	htru_2d_t_F2k[iq][ix] = view.Histo2D(ROOT::RDF::TH2DModel(hname.c_str(), 
							       htitle.c_str(), 
							       nx_t, 
							       tmin, tmax, 
							       ny_f2, 
							       f2min, f2max), 
					  "rec_t_bot", "tru_F2k");
	
      }
  }
  
  auto htru_F2k = df_tru.Histo1D({"htru_F2k",";F_{k};Events",100,0,1},"tru_F2k");
  auto hrec_F2k = df_rec.Histo1D({"hrec_F2k",";F_{k};Events",100,0,1},"rec_F2k");
  auto htru_F2N = df_tru.Histo1D({"htru_F2N",";F_{2}^{N};Events",100,0,1},"tru_F2N");
  auto hrec_F2N = df_rec.Histo1D({"hrec_F2N",";F_{2}^{N};Events",100,0,1},"rec_F2N");
  
  
  //rate vs -t
    
  //hit distributions from sullivan process particles in detectors
    
  //deviation of recon sullivan process track momentum from truth track
  auto hres_pmag_lambda = df_rec.Histo1D({"hres_pmag_lambda","",100,-10,10},"res_pmag_lambda");
    
  std::cout << "Everything is booked." << endl;
  auto trigger = *df.Count();
  
  //canvases
  TCanvas *c00 = new TCanvas("c00","Scattered Electron Acceptance (Single)",1920,1080);
  c00->Divide(3,2);
  c00->cd(1);
  DrawTruRec(htru_Q2_scatele.GetPtr(), hrec_Q2_scatele.GetPtr(),1);
  c00->cd(2);
  DrawTruRec(htru_pmag_scatele.GetPtr(), hrec_pmag_scatele.GetPtr());
  c00->cd(3);
  DrawTruRec(htru_pz_scatele.GetPtr(), hrec_pz_scatele.GetPtr());
  c00->cd(4);
  DrawTruRec(htru_eta_scatele.GetPtr(), hrec_eta_scatele.GetPtr());
  c00->cd(5);
  DrawTruRec(htru_theta_scatele.GetPtr(), hrec_theta_scatele.GetPtr());
  c00->cd(6);
  htru_phi_scatele->SetMinimum(0);
  DrawTruRec(htru_phi_scatele.GetPtr(), hrec_phi_scatele.GetPtr());
  c00->Print("scatele.png");
  c00->Close();
  
  TCanvas *c01 = new TCanvas("c01","Lambda Acceptance (Single)",1920,1080);
  c01->Divide(3,2);
  c01->cd(1)->SetLogy();
  htru_t_lambda->SetMinimum(1);
  DrawTruRec(htru_t_lambda.GetPtr(), hrec_t_lambda.GetPtr(),1);
  c01->cd(2)->SetLogy();
  htru_pmag_lambda->SetMinimum(1);
  DrawTruRec(htru_pmag_lambda.GetPtr(), hrec_pmag_lambda.GetPtr());
  c01->cd(3)->SetLogy();
  htru_pz_lambda->SetMinimum(1);
  DrawTruRec(htru_pz_lambda.GetPtr(), hrec_pz_lambda.GetPtr());
  c01->cd(4)->SetLogy();
  htru_eta_lambda->SetMinimum(1);
  DrawTruRec(htru_eta_lambda.GetPtr(), hrec_eta_lambda.GetPtr());
  c01->cd(5)->SetLogy();
  htru_theta_lambda->SetMinimum(1);
  DrawTruRec(htru_theta_lambda.GetPtr(), hrec_theta_lambda.GetPtr());
  c01->cd(6)->SetLogy();
  htru_phi_lambda->SetMinimum(1);
  DrawTruRec(htru_phi_lambda.GetPtr(), hrec_phi_lambda.GetPtr());
  c01->Print("lambda.png");
  
  TCanvas *c02 = new TCanvas("c02","|t| Acceptance and Resolution",1000,500);
  c02->Divide(2,1);
  c02->cd(1)->SetLogy();
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
  
  c02->cd(2);
  h2d_res_t->DrawCopy("colz");
  auto l_res_t_hi = new TLine(0,t_res_cut,tmax,t_res_cut);
  l_res_t_hi->SetLineStyle(7);
  l_res_t_hi->SetLineColor(kRed);
  l_res_t_hi->Draw();
  auto l_res_t_lo = new TLine(0,-t_res_cut,tmax,-t_res_cut);
  l_res_t_lo->SetLineStyle(7);
  l_res_t_lo->SetLineColor(kRed);
  l_res_t_lo->Draw();
  c02->Print("t_res_acc.png");
  c02->Close();
  
  // TCanvas *c01 = new TCanvas("c01","Lambda Mass Reconstruction",500,500);
  // htru_m_lambda->DrawCopy();
  // hrec_m_lambda->SetLineColor(kRed);
  // hrec_m_lambda->DrawCopy("same");
  // auto mass_leg = gPad->BuildLegend(0.2,0.7,0.4,0.8);


  TCanvas *c02a = new TCanvas("c02a","F2k",1000,500);
  c02a->Divide(2,1);
  c02a->cd(1);
  auto htru_F2kc = htru_F2k->DrawCopy();
  hrec_F2k->SetLineColor(kRed);
  auto hrec_F2kc = hrec_F2k->DrawCopy("same");
  TLegend *leg_sfs = new TLegend(0.5,0.5,0.75,0.7);
  //leg_sfs->SetTextSize(0.04);
  leg_sfs->AddEntry(htru_F2kc,"Truth Calculation","l");
  leg_sfs->AddEntry(hrec_F2kc,"Recon Calculation","l");
  leg_sfs->Draw();
  
  c02a->cd(2);
  //TCanvas *c02b = new TCanvas("c02b","F2N",500,500);
  htru_F2N->DrawCopy();
  hrec_F2N->SetLineColor(kRed);
  hrec_F2N->DrawCopy("same");
  c02a->Print("SFcalcs.png");
  
  TCanvas *c03a = new TCanvas("c03a","2D x,Q2 phase space");
  htru_2d_x_Q2->DrawCopy("colz");
  c03a->Print("htru_2d_xQ2.png");
  TCanvas *c03b = new TCanvas("c03b","2D x,Q2 phase space");
  hrec_2d_x_Q2->DrawCopy("colz");
  c03b->Print("hrec_2d_xQ2.png");
  TCanvas *c03 = new TCanvas("c03","2D x,Q2 phase space");
  auto hacc_2d_x_Q2 = (TH2D*) hrec_2d_x_Q2->Clone("hacc_2d_x_Q2");
  hacc_2d_x_Q2->SetTitle("Acceptance");
  hacc_2d_x_Q2->Divide(htru_2d_x_Q2.GetPtr());
  hacc_2d_x_Q2->Scale(1/xsec,"binwidth");
  hacc_2d_x_Q2->Draw("colz");
  c03->Print("hacc_2d_xQ2.png");
  
  TCanvas *c04a = new TCanvas("c04a","F2k vs t binned 2D");
  TCanvas *c04b = new TCanvas("c04b","F2k vs t binned");
  c04a->Divide(nbin,nbin);
  c04b->Divide(nbin,nbin);
  int idx=1;
  for(int iq=0; iq<nbin; iq++){
    for(int ix=0; ix< nbin; ix++){
      c04a->cd(idx);
      htru_2d_t_F2k[iq][ix]->FitSlicesY();
      htru_2d_t_F2k[iq][ix]->DrawCopy("colz");
      
      c04b->cd(idx);
      TH1D *htru_2d_t_F2k_1 = (TH1D*) gDirectory->Get(Form("htru_2d_t_F2k_%d_%d_1",iq,ix));
      htru_2d_t_F2k_1->SetTitle(";|t| [GeV^{2}]; F_{k}");
      htru_2d_t_F2k_1->SetMinimum(f2min);
      htru_2d_t_F2k_1->SetMaximum(f2max);
      htru_2d_t_F2k_1->DrawCopy();
      
      idx++;
    }
  }
  c04a->Print("F2k_t_2D.png");
  c04b->Print("F2k_t_bin.png");

}
