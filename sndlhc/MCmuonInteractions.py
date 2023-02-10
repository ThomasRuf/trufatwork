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

if 0>1:
 import MCmuonInteractions
 MCmuonInteractions.trackTask = trackTask
 import importlib
 importlib.reload(MCmuonInteractions)

 for n in MCmuonInteractions.eventList:
     if MCmuonInteractions.eventList[n][0]>1:E.append(n)

def goodEvent(event):
      # search for hits
   hit = {} # list of mcpoints made by muon tracks
   for c in [event.ScifiPoint,event.MuFilterPoint]:
      for mcPoint in c:
        if not abs(mcPoint.PdgCode())==13: continue
        t = mcPoint.GetTrackID()
        mcPoint.Momentum(P)
        if not t in hit: hit[t]={'scifi':{},'mufi':{}}
        if mcPoint.ClassName() == 'ScifiPoint':
           hit[t]['scifi'][mcPoint.GetDetectorID()//100000]=[P.Mag(),mcPoint]
        else:
           hit[t]['mufi'][mcPoint.GetDetectorID()//1000]=[P.Mag(),mcPoint]
   ntrack = 0
   txt = ""
   for t in hit: 
        txt += ",%i %s   %5.2F scifi %i mufi %i  %5.2F"%(t,event.MCTrack[t].GetProcName(),event.MCTrack[t].GetP(),len(hit[t]['scifi']),len(hit[t]['mufi']),event.MCTrack[t].GetStartZ())
        if len(hit[t]['scifi'])>7: ntrack+=1
   print(txt)
   print(ntrack)
   return True
import ROOT
import rootUtils as ut
h={}
A = ROOT.TVector3()
B = ROOT.TVector3()
C = ROOT.TVector3()
D = ROOT.TVector3()
output = []
eventList = {}

def muonInter(h,pid=13,debug=False,flist=[],mc=False):
 if len(flist)==0:
     ioman = ROOT.FairRootManager.Instance()
     S = ioman.GetSource()
     eventTree = S.GetInTree()
 else:
     eventTree = ROOT.TChain('cbmsim')
     for n in flist: rc = eventTree.Add('sndLHC.Ntuple-TGeant4_boost'+str(n)+'.0_digCPP.root')
 trackTask.event = eventTree
 print(eventTree,eventTree.GetEntries())
 P = ROOT.TVector3()
 ut.bookHist(h,'muI','muon interactions per event',20,-0.5,19.5)
 stat = {'gConv':0,'muPair':0,'posAni':0,'decay':0,'other':0}
 for x in stat:
   ut.bookHist(h,'muI'+x,'muon interactions per event',20,-0.5,19.5)
   ut.bookHist(h,'dxyscifi'+x,'distance between tracks',2000,-10.,10.,2000,-10.,10.)
   ut.bookHist(h,'dxymufi'+x,'distance between tracks',2000,-10.,10.,2000,-10.,10.)
   
 ut.bookHist(h,'cosAngle','cosAngle',100,0.99,1.0)
 ut.bookHist(h,'dist','dist',1000,0.0,100.0)
 counter = {'2tracks':0,'3tracks':0,'2mctracks':0,'3mctracks':0}
 for N, event in enumerate(eventTree):
   W = event.MCTrack[0].GetWeight()
   if mc:
      muHistory = {} # key = mother, {z-vertex}[daughters]
      for index, t in enumerate(event.MCTrack):
         if abs(t.GetPdgCode())==pid:
            mo = t.GetMotherId()
            zStart = t.GetStartZ()
            if not (mo in muHistory): 
               muHistory[mo] = {}
            if not (zStart in muHistory[mo]): muHistory[mo][zStart] = []
            muHistory[mo][zStart].append(index)
#
      stat = {'gConv':0,'muPair':0,'posAni':0,'decay':0,'other':0}
      for mu in muHistory:
        if mu<0: continue
        for z in muHistory[mu]:
           if event.MCTrack[mu].GetPdgCode() == 22: iType = 'gConv'
           elif abs(event.MCTrack[mu].GetPdgCode()) == 13: iType = 'muPair'
           elif event.MCTrack[muHistory[mu][z][0]].GetProcID()==4: iType = 'decay'
           elif event.MCTrack[muHistory[mu][z][0]].GetProcID()==10: iType = 'posAni'
           else: 
             iType = 'other'
             print('what is this?',N,muHistory)
           stat[iType]+=1
      if debug and len(muHistory)>2: print(muHistory)
      tot = 0
      for x in stat:
         if not x=='decay': tot+=stat[x]
         rc = h['muI'+x].Fill(stat[x])
      rc = h['muI'].Fill(tot)
      Q = stat['gConv']>0 or stat['muPair']>0 or stat['decay']>0 or stat['posAni']>0
      if not Q : continue
   # search for hits
   hit = {} # list of mcpoints made by muon tracks
   for c in [event.ScifiPoint,event.MuFilterPoint]:
      for mcPoint in c:
        if not abs(mcPoint.PdgCode())==13: continue
        t = mcPoint.GetTrackID()
        mcPoint.Momentum(P)
        if not t in hit: hit[t]={'scifi':{},'mufi':{}}
        if mcPoint.ClassName() == 'ScifiPoint':
           hit[t]['scifi'][mcPoint.GetDetectorID()//100000]=[P.Mag(),mcPoint]
        else:
           hit[t]['mufi'][mcPoint.GetDetectorID()//1000]=[P.Mag(),mcPoint]
   if len(hit)<2: continue   # only look for 2 or more track events
   txt = "hurra %i "%(N)
   ntrack = 0
   for t in hit: 
        txt += ",%i %s scifi %i mufi %i  %5.2F"%(t,event.MCTrack[t].GetProcName(),len(hit[t]['scifi']),len(hit[t]['mufi']),event.MCTrack[t].GetStartZ())
        if len(hit[t]['scifi'])>7: ntrack+=1
   first = {}
   for t in hit:
     zMin = {}
     first[t] = {}
     for det in hit[t]:
        zMin[det] = [9999,-1]
        for plane in hit[t][det]:
           aHit=hit[t][det][plane][1]
           if aHit.GetZ()<zMin[det][0]:
              zMin[det][0]=aHit.GetZ()
              zMin[det][1]=[aHit.GetX(),aHit.GetY()]
        if zMin[det][0]<1000:
           first[t][det] = [zMin[det][1][0],zMin[det][1][1]]
   iType = 'other'
   for t1 in hit:
      mo = event.MCTrack[t1].GetMotherId()
      if mo<0: continue
      elif event.MCTrack[mo].GetPdgCode() == 22: iType = 'gConv'
      elif abs(event.MCTrack[mo].GetPdgCode()) == 13: iType = 'muPair'
      elif event.MCTrack[t1].GetProcID()==4: iType = 'decay'
      elif event.MCTrack[t1].GetProcID()==10: iType = 'posAni'
   for t1 in hit:
      for t2 in hit:
        if not t2>t1:continue
        for det in ['scifi','mufi']:
           if det in first[t1] and det in first[t2]: 
              dx = first[t1][det][0]-first[t2][det][0]
              dy = first[t1][det][1]-first[t2][det][1]
              rc = h['dxy'+det+iType].Fill(dx,dy)

   eventList[N] = [ntrack,list(hit.keys())]
   if ntrack==2: counter['2mctracks']+=W
   if ntrack==3: counter['3mctracks']+=W
#
   output.append(txt)
   keyHits = list(hit.keys())
   for it1 in range(len(hit)-1):
          t1 = keyHits[it1]
          if len(hit[t1]['scifi'])==0: continue
          tmp = list(hit[t1]['scifi'].keys())
          tmp.sort()
          hit[t1]['scifi'][tmp[0]][1].Momentum(A)
          hit[t1]['scifi'][tmp[0]][1].Position(C)
          for it2 in range(t1+1,len(hit)):
            t2 = keyHits[it2]
            if len(hit[t2]['scifi'])==0: continue
            tmp = list(hit[t2]['scifi'].keys())
            tmp.sort()
            hit[t2]['scifi'][tmp[0]][1].Momentum(B)
            hit[t2]['scifi'][tmp[0]][1].Position(D)
            cosAB = A.Dot(B)/(A.Mag()*B.Mag())
            rc = h['cosAngle'].Fill(cosAB)
            dist = ROOT.TMath.Sqrt((C.X()-D.X())**2+(C.Y()-D.Y())**2)
            rc = h['dist'].Fill(dist)
   # count digits
   trackTask.scifiCluster()
   clusters = trackTask.clusScifi
   txt = 'digits ---> %i %i %i'%(N,clusters.GetEntries(),event.Digi_MuFilterHits.GetEntries())
   output.append(txt)
   if clusters.GetEntries()>16: counter['2tracks']+=W
   if clusters.GetEntries()>25: counter['3tracks']+=W
 print('---> Summary')
 for x in stat:
        print(x,h['muI'+x].GetEntries() - h['muI'+x].GetBinContent(1))
        h['muI'+x].GetXaxis().SetRangeUser(0.6,10.)
 print(counter)
 
# muons_down/scoring_2.5/LHC_-160urad_magfield_2022TCL6_muons_rock_5e7pr, 1fb-1 = 1E+39cm2, 80mb = 80E-27cm2: 8 1E13 collisions
# scale factor for 1fb-1: 8E13/5E7/ 1000(boostFactor) / 1 (iterations) = 1600
