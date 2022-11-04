import rootUtils as ut
import ROOT
pids = {}
h={}
ut.bookHist(h,'xy','xy;X;Y',100,-60,0,100,0,60)
ut.bookHist(h,'de0','de',100,0.,0.00001)
ut.bookHist(h,'de1','de',100,0.,0.001)
ut.bookHist(h,'de2','de',100,0.,0.1)
ut.bookHist(h,'nxy','nxy;X;Y',200,-100,100,200,-100,100)
ut.bookHist(h,'nFxy','nxy in fiuducial;X;Y',200,-100,100,200,-100,100)
ut.bookHist(h,'Nveto','n veto hits',100,-0.5,99.5)
ut.bookHist(h,'sxy','sxy;X;Y',200,-100,100,200,-100,100)
ut.bookHist(h,'bxyz','bxyz;X;Y;Z',100,-100,100,100,-100,100,100,-100,200)

sTree = ROOT.TChain("cbmsim")
for n in [82,85,86,89,90,91,92,93,94,96,97,99,111,113,115,116,117,118,119,122,123,125,126,127,129,131,132,133,134]:
   sTree.AddFile('root://eosuser.cern.ch//eos/user/c/cvilela/SND/neutrino/test_1k/'+str(n)+'/sndLHC.Genie-TGeant4.root')

debug = False

def run():
 for event in sTree:
  N = event.MCTrack[1]
  rc = h['nxy'].Fill(N.GetStartX(),N.GetStartY())
  inFiducial = True
  if N.GetStartX()<-47 or N.GetStartX()>-7: inFiducial = False
  if N.GetStartY()<15 or N.GetStartX()>56: inFiducial = False
  for hit in event.ScifiPoint:
              rc = h['sxy'].Fill(hit.GetX(),hit.GetY())
  if not inFiducial: continue
  rc = h['nFxy'].Fill(N.GetStartX(),N.GetStartY())
  nVeto = 0
  for hit in event.MuFilterPoint:
       detID = hit.GetDetectorID()
       if detID//10000==1:
              t = hit.GetTrackID()
              P = ROOT.TVector3(hit.GetPx(),hit.GetPy(),hit.GetPz())
              rc = h['xy'].Fill(hit.GetX(),hit.GetY())
              rc = h['de0'].Fill(hit.GetEnergyLoss())
              rc = h['de1'].Fill(hit.GetEnergyLoss())
              rc = h['de2'].Fill(hit.GetEnergyLoss())
              if hit.GetEnergyLoss()>1E-5: nVeto += 1
              p=hit.PdgCode()
              if not p in pids: pids[p]=0
              pids[p]+=1
              if not t<0:
                   T = event.MCTrack[hit.GetTrackID()]
                   if debug: print(t,p,hit.GetPz(),P.Mag(),hit.GetEnergyLoss()*1E6,hit.GetZ(),hit.GetZ()-T.GetStartZ())
                   rc = h['bxyz'].Fill(T.GetStartX(),T.GetStartY(),T.GetStartZ())
              else:
                   if debug: print(t,p,hit.GetPz(),P.Mag(),hit.GetEnergyLoss()*1E6,hit.GetZ())
  rc = h['Nveto'].Fill(nVeto)
def draw():
  ReverseXAxis(h['xy'],'colz')


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

