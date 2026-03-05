struct Region {
  double Q2min, Q2max;
  double xmin, xmax;
  TH1D* h_t;
  TH2D* htru_2d_t_f2n;
};


std::vector<Region> makeRegions(const std::vector<double>& Q2_bins,
                                const std::vector<double>& x_bins)
{
  std::vector<Region> regions;
  const auto nq = Q2_bins.size() - 1;
  const auto nx = x_bins.size() - 1;
  regions.reserve(nq * nx);

  for (size_t iq = 0; iq < nq; ++iq) {
    for (size_t ix = 0; ix < nx; ++ix) {
      Region r{};
      r.Q2min = Q2_bins[iq];
      r.Q2max = Q2_bins[iq+1];
      r.xmin  = x_bins[ix];
      r.xmax  = x_bins[ix+1];
      r.h_t   = nullptr; // we'll fill this later, or keep it unused
      r.htru_2d_t_f2n = nullptr;
      regions.emplace_back(r);
    }
  }
  return regions;
}


void drawGrid(const std::vector<Region>& regions,
              const std::vector<double>& Q2_bins,
              const std::vector<double>& x_bins){
  
  
  double mL = 0.15, mR = 0.1, mT = 0.1, mB = 0.1;
  int nQ2 = Q2_bins.size()-1;
  int nx  = x_bins.size()-1;
  
  double W = (1.0 - mL - mR)/ nQ2; // target drawable width
  double H = (1.0 - mT - mB) / nx;  // target drawable height
  double padW, padH;
  
  TCanvas* c = new TCanvas("c","Matrix of |t| distributions",1200,1000);
  
  //c->Divide(nQ2, nx); // thin margins
  
  int idx=0;
  
  double x_cursor = 0.0;
  double y_cursor = 1.0;
  
  for (int iy=0; iy<nx; iy++) {      // loop over x bins (rows)
    x_cursor = 0.0;
    for (int ix=0; ix<nQ2; ix++) { // loop over Q2 bins (columns)
      c->cd();
      //if(idx>0) continue;
      bool isLeft   = (ix == 0);
      bool isRight  = (ix == nQ2 - 1);
      bool isTop    = (iy == 0);
      bool isBottom = (iy == nx - 1);
      
      padW = isLeft ? W + mL/nQ2 : isRight ? W + mR/nQ2 : W;
      padH = isTop ? H + mT/nx : isBottom ? H + mB/nx : H;
      
      double xlow = x_cursor;
      double xup = x_cursor + padW;
      double yup = y_cursor;
      double ylow = y_cursor - padH;
      cout << xlow << " " << xup << " " << yup << " " << ylow << endl;
      cout << padW << " " << padH << endl;
      // // Clamp to [0, 1]
      // xlow = std::max(0.0, xlow);
      // xup  = std::min(1.0, xup);
      // ylow = std::max(0.0, ylow);
      // yup  = std::min(1.0, yup);
      
      TString padName = Form("pad_%d", idx);
      TPad* pad = new TPad(padName, padName, xlow, ylow, xup, yup);
	
      // pad->SetLeftMargin(isLeft ? mL : 0.0);
      // pad->SetRightMargin(isRight ? mR : 0.0);
      // pad->SetTopMargin(isTop ? mT : 0.0);
      // pad->SetBottomMargin(isBottom ? mB : 0.0);
      pad->SetLeftMargin(0.0);
      pad->SetRightMargin( 0.0);
      pad->SetTopMargin(0.0);
      pad->SetBottomMargin(0.0);
      
      pad->Draw();
      pad->cd();
      
      int regIndex = iy*nQ2 + ix; // index in regions vector
      TH1D* h = regions[regIndex].h_t;
      
      // Draw histogram
      h->SetStats(0);
      h->SetTitle("");
      h->GetXaxis()->SetLabelSize(0.05);
      h->GetXaxis()->SetTitleSize(0.05);
      h->GetYaxis()->SetLabelSize(0.05);
      h->GetYaxis()->SetTitleSize(0.05);
      //h->SetMaximum(0.1);
      
      if (!isBottom){ 
	h->GetXaxis()->SetLabelSize(0); // only bottom row has x labels
	h->GetXaxis()->SetTitleSize(0);
      }
	    
      if (!isLeft){    
	h->GetYaxis()->SetLabelSize(0); // only left column has y labels
	h->GetYaxis()->SetTitleSize(0);
      }
      
      TLatex *num = new TLatex(0.5,0.5,Form("%i",idx));
      num->SetNDC();
      num->SetTextSize(0.1);
      
      h->Draw("pe");
      num->Draw();
      
      // Bin labels
      if (isTop) { // top row: Q2 label
	TLatex *lab = new TLatex(0.5,0.95,Form("%.1f < Q^{2} < %.1f", Q2_bins[ix], Q2_bins[ix+1]));
	lab->SetNDC();
	lab->SetTextAlign(22);
	lab->SetTextSize(0.06);
	//c->cd();
	lab->Draw();
      }
      if (isRight) { // rightmost column: x label
	TLatex *lab = new TLatex(0.95,0.5,Form("%.3f < x < %.3f", x_bins[iy], x_bins[iy+1]));
	lab->SetNDC();
	lab->SetTextAngle(-90);
	lab->SetTextAlign(22);
	lab->SetTextSize(0.06);
	//c->cd();
	lab->Draw();
      }
      x_cursor += padW;
      idx++;
    }
    y_cursor -= padH;
  }
  // Global axis labels
  c->cd();
  // TLatex lab;
  // lab.SetTextAlign(22);
  // lab.SetTextSize(0.04);
  // lab.DrawLatexNDC(0.5, 0.03, "|t| [GeV^{2}]");
  // lab.SetTextAngle(90);
  // lab.DrawLatexNDC(0.04, 0.5, "Events");
  // c->SaveAs("matrix_t_plots.pdf");
}

