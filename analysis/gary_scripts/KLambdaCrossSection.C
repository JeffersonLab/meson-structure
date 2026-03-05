std::vector<double> KLambdaCrossSection(const std::string filename="/w/work5/home/garyp/eic/eg-orig-kaon-lambda/k_lambda_crossing_0.000-18.0on275.0_x0.0001-1.0000_q1.0-500.0.root", 
					Long64_t nEntries=1e6    
					) {
  
  TBenchmark bench;
  bench.Start("Testing Cross Section Code");
  
  TFile *file = TFile::Open(filename.c_str());
  TTree *tree = (TTree*)file->Get("Process");
  TTree *meta = (TTree*)file->Get("Meta");
  
  
  // ---- Faster metadata ---- 
  Long64_t totalEntries = tree->GetEntriesFast();
  if (nEntries < 0 || nEntries > totalEntries) 
    nEntries = totalEntries;
  
  
  // --- Disable all branches, only enable needed ones ---
  tree->SetBranchStatus("*", 0);
  meta->SetBranchStatus("*", 0);
  
  
  // ---- Enable only required branches ---- 
  tree->SetBranchStatus("xsec_tagged_dis", 1);
  tree->SetBranchStatus("Q2", 1);
  tree->SetBranchStatus("xbj", 1);
  tree->SetBranchStatus("y_inelasticity", 1);
  tree->SetBranchStatus("k_int", 1);
  
  meta->SetBranchStatus("Jacob", 1);
  meta->SetBranchStatus("MC", 1);
  
  
  // ---- Branch setup ---- 
  Double_t xsec_tagged_dis, Q2, x, y, Jacob, k_int;
  tree->SetBranchAddress("xsec_tagged_dis", &xsec_tagged_dis);
  tree->SetBranchAddress("Q2", &Q2);
  tree->SetBranchAddress("xbj", &x);
  tree->SetBranchAddress("y_inelasticity", &y);
  tree->SetBranchAddress("k_int", &k_int);
  
  struct MCStruct {
    Int_t nEvts;
    Float_t PhSpFct;
  };
  MCStruct MC;
  meta->SetBranchAddress("Jacob", &Jacob);
  meta->SetBranchAddress("MC", &MC);
  
    
  double sumA = 0.0;
  double sumA2 = 0.0;
  
  for (Long64_t i = 0; i < nEntries; ++i) {
      
    tree->GetEntry(i);
    meta->GetEntry(i);
    
    if(TMath::IsNaN(Q2) || TMath::IsNaN(x) || TMath::IsNaN(y) || TMath::IsNaN(xsec_tagged_dis)){
      continue;
    }
    
    //unclear if these are still needed.
    // double ncalls = 147954175; //number of calls for 10m events, 18x275
    // double ngen =1e7;
    // double frac=ngen/ncalls;
    
    auto psf = MC.PhSpFct;
    double a = xsec_tagged_dis * Jacob * psf * k_int;
    sumA += a;
    sumA2 += a*a;
  }
  
  const long double M = static_cast<long double>(nEntries);
  
  
  // ---- Cross section value ---- 
  double xsec = static_cast<double>(sumA / M);
  
  // ---- MC statistical error ---- 
  double err = 0.0;
  if (M > 1) {
    long double var =
      (sumA2 - (sumA * sumA) / M) / (M * (M - 1));
    err = std::sqrt(static_cast<double>(var));
  }
  
  bench.Stop("Testing Cross Section Code");
  //bench.Print("Testing Cross Section Code");
  return {xsec, err};
}
