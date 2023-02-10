import ROOT,os
import rootUtils as ut
F=ROOT.TFile.Open(os.environ['EOSSHIP']+"/eos/experiment/sndlhc/www/offline/run004705.root")
ROOT.gROOT.cd()
h={}
h['mean&sigma'] = F.scifi.Get('mean&sigma').Clone('mean&sigma')
for x in h['mean&sigma'].GetListOfPrimitives():
   for y in x.GetListOfPrimitives():
       if y.ClassName().find('TGraphE')==0:
         h[y.GetTitle()]=y.Clone(y.GetTitle())
if 1:
 ut.bookHist(h,'mean','',100,-250,250)
 ut.bookHist(h,'sigma','',100,0,500)
 for c in ['mean','sigma']:
   for p in ['H','V']:
     for n in range(h['mean'+p].GetN()):
         rc = h[c].Fill(h[c+p].GetPointY(n))
    
 h['mean'].Fit('pol0')

