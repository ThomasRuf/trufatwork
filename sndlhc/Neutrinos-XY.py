import rootUtils as ut
import ROOT
pids = {}
h={}
ut.bookHist(h,'xy','xy',100,-60,0,100,0,60)
ut.bookHist(h,'nxy','nxy',200,-100,100,200,-100,100)
ut.bookHist(h,'sxy','sxy',200,-100,100,200,-100,100)

f=ROOT.TFile.Open('root://eosuser.cern.ch//eos/user/c/cvilela/SND/neutrino/test_1k/109/sndLHC.Genie-TGeant4.root')

for event in f.cbmsim:
  N = event.MCTrack[1]
  rc = h['nxy'].Fill(N.GetStartX(),N.GetStartY())
  for hit in event.ScifiPoint:
              rc = h['sxy'].Fill(hit.GetX(),hit.GetY())
  for hit in event.MuFilterPoint:
       detID = hit.GetDetectorID()
       if detID//10000==1:
              t = hit.GetTrackID()
              P = ROOT.TVector3(hit.GetPx(),hit.GetPy(),hit.GetPz())
              rc = h['xy'].Fill(hit.GetX(),hit.GetY())
              p=hit.PdgCode()
              if not p in pids: pids[p]=0
              pids[p]+=1
              if not t<0:
                   T = event.MCTrack[hit.GetTrackID()]
                   print(t,p,hit.GetPz(),P.Mag(),hit.GetEnergyLoss()*1E6,hit.GetZ(),hit.GetZ()-T.GetStartZ())
              else:
                   print(t,p,hit.GetPz(),P.Mag(),hit.GetEnergyLoss()*1E6,hit.GetZ())

ReverseXAxis(h['xy'],'colz')

h={}
import rootUtils as ut
ut.bookHist(h,'2d','test',100,-80,80,100,-100,100)
h['2d'].Fill(-20,40)
h['2d'].Fill(30,20,100)
h['2d'].Draw('box')

def ReverseXAxis(hname,option):
# Remove the current axis
   h['front-'+hname]=h[hname].Clone('front-'+hname)
   histo = h['front-'+hname]
   histo.GetXaxis().SetLabelOffset(999)
   histo.GetXaxis().SetTickLength(0)
# re-order x
   for nx in range( (histo.GetNbinsX()+2)//2):
        for ny in range(histo.GetNbinsY()+2):
            A = histo.GetBinContent(nx,ny)
            B = histo.GetBinContent(histo.GetNbinsX()+1-nx,ny)
            histo.SetBinContent(nx,ny,B)
            histo.SetBinContent(histo.GetNbinsX()+1-nx,ny,A)
   histo.Draw(option)
# Redraw the new axis
   ROOT.gPad.Update()
   h['newaxis_'+histo.GetName()] = ROOT.TGaxis(ROOT.gPad.GetUxmax(),
                                ROOT.gPad.GetUymin(),
                                ROOT.gPad.GetUxmin(),
                                ROOT.gPad.GetUymin(),
                                histo.GetXaxis().GetXmin(),
                                histo.GetXaxis().GetXmax(),
                                510,"-")
   h['newaxis_'+histo.GetName()].SetLabelOffset(-0.03)
   h['newaxis_'+histo.GetName()].Draw()

