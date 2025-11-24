#include "binning.C"
#include "/home/garyp/eic/epic-rad/examples/EPICStyle.C"

void Analysis(std::string infile="/w/work5/home/garyp/rad_trees/MCMatched_KLambda_18x275.root"){
  
  SetEPICStyle();
  
  ROOT::EnableImplicitMT(8);
  ROOT::RDataFrame dfraw("rad_tree",infile);
  auto df = dfraw.Define("res_t","tru_t_bot-rec_t_bot");
  df = df.Define("tru_lambda_mass", [](ROOT::VecOps::RVec<double>&var, int&id)
		 { return var[id]; }
		 ,{"MCParticles_mass","Lambda"});//
  df = df.Define("rec_lambda_mass", [](ROOT::VecOps::RVec<float>&var, int&id)
		 { return var[id]; }
		 ,{"ReconstructedParticles_mass","Lambda"});//
  
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

  //rate vs -t
    
  //hit distributions from sullivan process particles in detectors
    
  //deviation of recon sullivan process track momentum from truth track
    
    
  std::cout << "Everything is booked." << endl;
  auto trigger = *df.Count();
    
  //canvases
  TCanvas *c00 = new TCanvas("c00","|t| Acceptance and Resolution",1000,500);
  c00->Divide(2,1);
  c00->cd(1)->SetLogy();
  auto hacc_t = (TH1D*)hrec_t->Clone("hacc_t");
  hacc_t->SetTitle(";|t| [GeV^{2}]; Acceptance");
  hacc_t->Divide(htru_t.GetPtr());
  hacc_t->Draw();
  auto hacc_t_rescut = (TH1D*)hrec_t_rescut->Clone("hacc_t_rescut");
  hacc_t_rescut->SetTitle(";|t| [GeV^{2}]; Acceptance");
  hacc_t_rescut->Divide(htru_t.GetPtr());
  hacc_t_rescut->SetLineStyle(7);
  hacc_t_rescut->SetLineColor(kRed);
  hacc_t_rescut->Draw("same");
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
}
