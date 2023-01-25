import ROOT
import rootUtils as ut
h={}
A=ROOT.TVector3()
B=ROOT.TVector3()

def muonInteractions():
 f=ROOT.TFile('sndLHC.Ntuple-TGeant4_-150urad_1e7pr_dig.root')
 eventTree = f.cbmsim
 ut.bookHist(h,'IVz','interaction vertex',800,-500,300)
 digiMap = {eventTree.Digi_MuFilterHits:eventTree.Digi_MuFilterHits2MCPoints[0],eventTree.Digi_ScifiHits:eventTree.Digi_ScifiHits2MCPoints[0]}
 pointMap = {eventTree.Digi_MuFilterHits:eventTree.MuFilterPoint,eventTree.Digi_ScifiHits:eventTree.ScifiPoint}
 V=ROOT.TVector3()
 for event in eventTree:
   for c in digiMap:
     for j, aHit in enumerate(c):
        if not aHit.isValid(): continue
        detID = aHit.GetDetectorID()
        wList = digiMap[c].wList(detID)
        for p in wList:
           i = p.first
           mcPoint = pointMap[c][i]
           mcTrack = mcPoint.GetTrackID()
           if mcTrack<1: continue
           while mcTrack>0:
               t = event.MCTrack[mcTrack]
               mcTrack = t.GetMotherId()
           t.GetStartVertex(V)
           rc = h['IVz'].Fill(V.z())
           
def muonLosses():
 f=ROOT.TFile('sndLHC.Ntuple-TGeant4_digCPP.root')
 eventTree = f.cbmsim
 ut.bookHist(h,'XY0','XY pure extrapolation',90,-90,10,80,0,80)
 ut.bookHist(h,'XY1','XY dE/dx cut',         90,-90,10,80,0,80)
 ut.bookHist(h,'XY2','GEANT4',               90,-90,10,80,0,80)
 ut.bookHist(h,'XYD','no hit',               90,-90,10,80,0,80)
 ut.bookHist(h,'rate','rate as function of energy',500,0.,500.)
 ut.bookHist(h,'eD','no hit, energy',500,0.,5000)
 ut.bookHist(h,'XY3','actual pos',           90,-90,10,80,0,80)
 ut.bookHist(h,'eloss','dE/dx',100,0.,100)
 pos = ROOT.TVector3()
 mom = ROOT.TVector3()
 P = ROOT.TVector3()
 zex = 300.
 Eloss = 30.  # mean energy loss in 75m of rock
 N=-1
 for event in eventTree:
   N+=1
   muon = event.MCTrack[0]
   W = muon.GetWeight()
   muon.GetStartVertex(pos)
   muon.GetMomentum(mom)
   lam = (zex-pos.z())/mom.z()
   posEx = pos+lam*mom
   rc = h['XY0'].Fill(posEx[0],posEx[1],W)
   if muon.GetP() > Eloss: rc = h['XY1'].Fill(posEx[0],posEx[1],W)
   # find first muon hit
   hit = {}
   for c in [event.ScifiPoint,event.MuFilterPoint]:
      for mcPoint in c:
           if not mcPoint.GetTrackID()==0: continue
           mcPoint.Momentum(P)
           hit[mcPoint.GetZ()] = [P.Mag(),mcPoint.GetX(),mcPoint.GetY()]
   if len(hit)==0:
       rc = h['XYD'].Fill(posEx[0],posEx[1],W)
       rc = h['eD'].Fill(mom.Mag())
       continue
   tmp = list(hit.keys())
   tmp.sort()
   rc = h['XY2'].Fill(posEx[0],posEx[1],W)
   rc = h['XY3'].Fill(hit[tmp[0]][1],hit[tmp[0]][2],W)
   rc = h['eloss'].Fill( mom.Mag() - hit[tmp[0]][0] )
   rc = h['rate'].Fill( mom.Mag(), W )
 boundaries = {'X':[-80,0],'Y':[10,65]}
 iboundaries ={'iX':[0,0],'iY':[0,0]}
 for a in boundaries:
    axis = eval("h['XY0'].Get"+a+"axis()")
    for i in range( len(boundaries[a]) ):
       iboundaries['i'+a][i]=axis.FindBin(boundaries[a][i])
 for x in ['XY0','XY1','XY2','XY3','XYD']:
     print(h[x].GetTitle(),h[x].Integral(iboundaries['iX'][0],iboundaries['iX'][1],iboundaries['iY'][0],iboundaries['iY'][1]))
 
 N = h['rate'].GetNbinsX()
 h['rate'].SetBinContent(N,h['rate'].GetBinContent(N)+h['rate'].GetBinContent(N+1))
 ut.makeIntegralDistrib(h,'rate')

    
     
"""
large scoring plane

XY pure extrapolation 36.15670425503049
XY dE/dx cut 24.83367397985421
GEANT4 20.131493368186057
actual pos 28.632078592083417
no hit 16.025210886844434
"""

import ROOT
import rootUtils as ut
h={}
A = ROOT.TVector3()
B = ROOT.TVector3()
C = ROOT.TVector3()
D = ROOT.TVector3()
def muonInter(pid=13,debug=False):
 eventTree = ROOT.TChain('cbmsim')
 for n in range(2,6): eventTree.Add('sndLHC.Ntuple-TGeant4_boost100'+str(n)+'.0_digCPP.root')
 N=-1
 P = ROOT.TVector3()
 ut.bookHist(h,'cosAngle','cosAngle',100,0.99,1.0)
 ut.bookHist(h,'dist','dist',1000,0.0,100.0)
 counter = {'2tracks':0,'3tracks':0}
 trackTask.event = eventTree
 for event in eventTree:
   W = event.MCTrack[0].GetWeight()
   N+=1
   foundMu = []
   for k in range(1,event.MCTrack.GetEntries()):
       if k in foundMu: continue
       t = event.MCTrack[k]
       if abs(t.GetPdgCode())==pid:
           if debug: print('---->   event ',N,k)
           foundMu.append(k)
           mo = t.GetMotherId()
           if event.MCTrack[mo].GetPdgCode()!=22:
              if debug: print('?? mother ID',mo,event.MCTrack[mo].GetPdgCode())
           else:  # search for second muon
              for m in range(1,event.MCTrack.GetEntries()):
                 if m==k: continue
                 if event.MCTrack[m].GetMotherId()==mo:
                      t2 = event.MCTrack[m]
                      foundMu.append(m)
                      if debug: 
                         print('second muon found',k,m)
                         ROOT.ShipMCTrack.__repr__(t)
                         ROOT.ShipMCTrack.__repr__(t2)
   # search for hits
   if len(foundMu)<2: continue
   hit = {}
   for c in [event.ScifiPoint,event.MuFilterPoint]:
      for mcPoint in c:
        if not abs(mcPoint.PdgCode())==13: continue
        t = mcPoint.GetTrackID()
        mcPoint.Momentum(P)
        if not t in hit: hit[t]={}
        hit[t][mcPoint.GetZ()] = [P.Mag(),mcPoint]
   if len(hit)>1:
       txt = "hurra %i  "%(N)
       for t in hit: 
          if t==0: txt += ",%i %i %5.2F"%(t,len(hit[t]),event.MCTrack[t].GetStartZ())
          else: txt += ",%i %s %i %5.2F"%(t,event.MCTrack[t].GetProcName(),len(hit[t]),event.MCTrack[t].GetStartZ())
       print(txt)
       keyHits = list(hit.keys())
       for it1 in range(len(hit)-1):
          t1 = keyHits[it1]
          tmp = list(hit[t1].keys())
          tmp.sort()
          hit[t1][tmp[0]][1].Momentum(A)
          hit[t1][tmp[0]][1].Position(C)
          for it2 in range(t1+1,len(hit)):
            t2 = keyHits[it2]
            tmp = list(hit[t2].keys())
            tmp.sort()
            hit[t2][tmp[0]][1].Momentum(B)
            hit[t2][tmp[0]][1].Position(D)
            cosAB = A.Dot(B)/(A.Mag()*B.Mag())
            rc = h['cosAngle'].Fill(cosAB)
            dist = ROOT.TMath.Sqrt((C.X()-D.X())**2+(C.Y()-D.Y())**2)
            rc = h['dist'].Fill(dist)
   # count digits
       trackTask.scifiCluster()
       clusters = trackTask.clusScifi
       print('digits ---> ',clusters.GetEntries(),event.Digi_MuFilterHits.GetEntries())
       if clusters.GetEntries()>16: counter['2tracks']+=W
       if clusters.GetEntries()>25: counter['3tracks']+=W
 print(counter)
 
# muons_down/scoring_2.5/muons_-150urad_1e7pr, 1fb-1 = 1E+39cm2, 80mb = 80E-27cm2: 8 1E13 collisions
# scale factor for 1fb-1: 8E6/ 1000(boostFactor) / 4 (iterations) = 2000

