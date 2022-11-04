import ROOT
import os
import rootUtils as ut
import shipunit as u
h={}

path = "/eos/experiment/sndlhc/MonteCarlo/MuonBackground/muons_up/muonRates2/runNXX/sndLHC.Ntuple-TGeant4_dig.root"
cbmsim = ROOT.TChain('cbmsim')
for n in range(50,60):
       cbmsim.AddFile(os.environ['EOSSHIP']+path.replace('XX',str(n)))

scaleFactor = 1./0.04  # keV to QDC

ut.bookHist(h,'elossUS','eloss;[MeV]',1000,0.,10)
ut.bookHist(h,'elossDS','eloss;[MeV]',1000,0.,10)
ut.bookHist(h,'NelossUS','eloss;[qdc]',1000,0.,400)
ut.bookHist(h,'NelossDS','eloss;[qdc]',1000,0.,400)

def fit_langau(hist,o,bmin,bmax):
   params = {0:'Width(scale)',1:'mostProbable',2:'norm',3:'sigma'}
   F = ROOT.TF1('langau',langaufun,0,400,4)
   for p in params: F.SetParName(p,params[p])
   rc = hist.Fit('landau','S'+o,'',bmin,bmax)
   res = rc.Get()
   if not res: return res
   F.SetParameter(2,res.Parameter(0))
   F.SetParameter(1,res.Parameter(1))
   F.SetParameter(0,res.Parameter(2))
   F.SetParameter(3,res.Parameter(2))
   F.SetParLimits(0,0,10)
   F.SetParLimits(1,0,100)
   F.SetParLimits(3,0,10)
   rc = hist.Fit(F,'S','',bmin,bmax)
   res = rc.Get()
   return res


def  langaufun(x,par):
   #Fit parameters:
   #par[0]=Width (scale) parameter of Landau density
   #par[1]=Most Probable (MP, location) parameter of Landau density
   #par[2]=Total area (integral -inf to inf, normalization constant)
   #par[3]=Width (sigma) of convoluted Gaussian function
   #
   #In the Landau distribution (represented by the CERNLIB approximation),
   #the maximum is located at x=-0.22278298 with the location parameter=0.
   #This shift is corrected within this function, so that the actual
   #maximum is identical to the MP parameter.
#
      # Numeric constants
      invsq2pi = 0.3989422804014   # (2 pi)^(-1/2)
      mpshift  = -0.22278298       # Landau maximum location
#
      # Control constants
      np = 100.0      # number of convolution steps
      sc =   5.0      # convolution extends to +-sc Gaussian sigmas
#
      # Variables
      summe = 0.0
#
      # MP shift correction
      mpc = par[1] - mpshift * par[0]
#
      # Range of convolution integral
      xlow = x[0] - sc * par[3]
      xupp = x[0] + sc * par[3]
#
      step = (xupp-xlow) / np
#
      # Convolution integral of Landau and Gaussian by sum
      i=1.0
      while i<=np/2:
         i+=1
         xx = xlow + (i-.5) * step
         fland = ROOT.TMath.Landau(xx,mpc,par[0]) / par[0]
         summe += fland * ROOT.TMath.Gaus(x[0],xx,par[3])
#
         xx = xupp - (i-.5) * step
         fland = ROOT.TMath.Landau(xx,mpc,par[0]) / par[0]
         summe += fland * ROOT.TMath.Gaus(x[0],xx,par[3])
#
      return (par[2] * step * summe * invsq2pi / par[3])

for event in cbmsim:
   for X in event.MuFilterPoint:
           if not abs(X.PdgCode())==13: continue
           s = X.GetDetectorID()//10000
           dE = X.GetEnergyLoss()/u.MeV
           if s==2:
               rc  = h['elossUS'].Fill(dE)
               rc  = h['NelossUS'].Fill(dE*scaleFactor)
           if s==3:
               rc  = h['elossDS'].Fill(dE)
               rc  = h['NelossDS'].Fill(dE*scaleFactor)

ut.bookCanvas(h,'E','',1600,900,2,1)
ut.bookCanvas(h,'NE','',1600,900,2,1)

for t in ['','N']:
  k=1
  for hist in [h[t+'elossUS'],h[t+'elossDS']]:
       tc = h[t+'E'].cd(k)
       k+=1
       if t=='': res = fit_langau(hist,'L',1.,3.)
       else: res = fit_langau(hist,'L',30.,150.)
       tc.Update()
       stats = hist.FindObject('stats')
       stats.SetOptFit(1111111)
       stats.SetX1NDC(0.51)
       stats.SetY1NDC(0.54)
       stats.SetX2NDC(0.98)
       stats.SetY2NDC(0.94)
       tc.Update()
  h[t+'E'].Update()
  h[t+'E'].Print(t+'mipElossMuFi.png')

