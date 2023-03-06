import os
import ROOT
import rootUtils as ut
import SndlhcTracking

A=ROOT.TVector3()
B=ROOT.TVector3()
C = ROOT.TVector3()
D = ROOT.TVector3()

# muons_down/scoring_2.5/LHC_-160urad_magfield_2022TCL6_muons_rock_5e7pr, 1fb-1 = 1E+39cm2, 80mb = 80E-27cm2: 8 1E13 collisions

class MuonInter():
   def Init(self,options):
     self.options = options
     self.f = ROOT.TFile.Open(options.inputFile)
     self.eventTree = self.f.cbmsim
     self.tag = options.inputFile.split('.')[1]
     self.norm = 1./int(self.tag.split('boost')[1]) * 8E13/5E7

     self.h = {}
     self.output = []
     self.eventList = {}
         
     self.trackTask = SndlhcTracking.Tracking() 
     self.trackTask.Init()

   def Eloss(self):
     ut.bookHist(h,'dEzS','energyLoss in scifi',100,0.,0.1)
     ut.bookHist(h,'dEzM','energyLoss in US/DS',100,0.,0.1)
     for event in self.eventTree:
       O = {'S':event.ScifiPoint,'M':event.MuFilterPoint}
       for x in O:
        mctraj = {}
        for p in O[x]:
          if not abs(p.PdgCode())==13: continue
          if p.GetDetectorID()<200000: continue
          mcj = p.GetTrackID()
          if not mcj in mctraj: mctraj[mcj] = {}
          p.Momentum(A)
          mctraj[mcj][p.GetZ()] = A.Mag()
        for mcj in mctraj:
            if len(mctraj[mcj])<2: continue
            z = list(mctraj[mcj].keys())
            z.sort()
            for i in range(len(z)):
             for j in range(1,len(z)):
               dz = z[j]-z[i]
               if dz<5: continue
               dE = -(mctraj[mcj][z[i]] - mctraj[mcj][z[i-1]])
               rc = h['dEz'+x].Fill(dE/dz)
               break
               
               
   def Interactions(self):
     h = self.h
     eventTree = self.eventTree
     ut.bookHist(h,'IVz','interaction vertex',800,-500,300)
     ut.bookHist(h,'IVzmu','interaction vertex muon',800,-500,300)
     digiMap = {eventTree.Digi_MuFilterHits:eventTree.Digi_MuFilterHits2MCPoints[0],eventTree.Digi_ScifiHits:eventTree.Digi_ScifiHits2MCPoints[0]}
     pointMap = {eventTree.Digi_MuFilterHits:eventTree.MuFilterPoint,eventTree.Digi_ScifiHits:eventTree.ScifiPoint}
     V=ROOT.TVector3()
     for event in self.eventTree:
        for c in digiMap:
          for j, aHit in enumerate(c):
            if not aHit.isValid(): continue
            detID = aHit.GetDetectorID()
            wList = digiMap[c].wList(detID)
            for p in wList:
              i = p.first
              mcPoint = pointMap[c][i]
              mcTrack = mcPoint.GetTrackID()
              abspid = abs(mcPoint.GetPdgCode())
              if mcTrack<1: continue
              while mcTrack>0:
                t = event.MCTrack[mcTrack]
                mcTrack = t.GetMotherId()
              t.GetStartVertex(V)
              rc = h['IVz'].Fill(V.z())
              if abspid==13: rc = h['IVzmu'].Fill(V.z())

   def muonLosses(self):
     h=self.h
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
     for N,event in enumerate(self.eventTree):
        muon = event.MCTrack[0]
        W = muon.GetWeight()*self.norm
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

   def goodEvent(self):
      # search for hits
      hit = {} # list of mcpoints made by muon tracks
      for c in [self.event.ScifiPoint,self.event.MuFilterPoint]:
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

   def muonInter(self,pid=13,debug=False,mc=False):
      h = self.h
      self.interestingEvents = {}
      self.trackTask.event = self.eventTree
      print(self.eventTree,self.eventTree.GetEntries())
      P = ROOT.TVector3()
      ut.bookHist(h,'muI','muon interactions per event',20,-0.5,19.5)
      stat = {'':0,'gConv':0,'muPair':0,'posAni':0,'decay':0,'other':0}
      for x in stat:
         ut.bookHist(h,'muI'+x,'muon interactions per event',20,-0.5,19.5)
         ut.bookHist(h,'muIz'+x,'muon interaction z; z [m]; N/10cm',700,-6300.,700)
         ut.bookHist(h,'muIzW'+x,'muon interaction z; z [m]; N/fb^{-1}/10cm',700,-6300.,700)
         ut.bookHist(h,'dxyscifi'+x,'distance between tracks; dX [cm];dY [cm]',2000,-10.,10.,2000,-10.,10.)
         ut.bookHist(h,'dxymufi'+x,'distance between tracks; dX [cm];dY [cm]',2000,-10.,10.,2000,-10.,10.)
         ut.bookHist(h,'cosAngle'+x,x+' angle; [mrad]',100,0.,0.1)
         ut.bookHist(h,'dist'+x,x+' dist ; #Delta d [cm]',1000,0.0,100.0)
      self.counter = {'2tracks':0,'3tracks':0,'2mctracks':0,'3mctracks':0}
      for N, event in enumerate(self.eventTree):
         W = event.MCTrack[0].GetWeight() * self.norm
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
         zInter = -1E10
         for t1 in hit:
            if t1>0 and zInter<-70000 and len(hit[t1]['scifi'])>0:
              zInter = event.MCTrack[t1].GetStartZ()
              rc = h['muIzW'].Fill(zInter,W)
              rc = h['muIzW'+iType].Fill(zInter,W)
              rc = h['muIz'].Fill(zInter)
              rc = h['muIz'+iType].Fill(zInter)
            for t2 in hit:
              if not t2>t1:continue
              for det in ['scifi','mufi']:
                 if det in first[t1] and det in first[t2]: 
                    dx = first[t1][det][0]-first[t2][det][0]
                    dy = first[t1][det][1]-first[t2][det][1]
                    rc = h['dxy'+det+iType].Fill(dx,dy)
                    rc = h['dxy'+det].Fill(dx,dy)


         self.eventList[N] = [ntrack,zInter,list(hit.keys())]
         if ntrack==2: self.counter['2mctracks']+=W
         if ntrack==3: self.counter['3mctracks']+=W
#
         self.output.append(txt)
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
               alpha = ROOT.TMath.ACos(cosAB)
               rc = h['cosAngle'+iType].Fill(alpha)
               rc = h['cosAngle'].Fill(alpha)
               dist = ROOT.TMath.Sqrt((C.X()-D.X())**2+(C.Y()-D.Y())**2)
               rc = h['dist'+iType].Fill(dist)
               rc = h['dist'].Fill(dist)
               if alpha>0.01:
                   if not N in self.interestingEvents: self.interestingEvents[N]=[]
                   self.interestingEvents[N].append(['large angle',alpha,zInter,t1,t2])
               if dist>2:
                   if not N in self.interestingEvents: self.interestingEvents[N]=[]
                   self.interestingEvents[N].append(['large dist',dist,zInter,t1,t2])
   # count digits
         self.trackTask.scifiCluster()
         clusters = self.trackTask.clusScifi
         txt = 'digits ---> %i %i %i'%(N,clusters.GetEntries(),event.Digi_MuFilterHits.GetEntries())
         self.output.append(txt)
         if clusters.GetEntries()>16: self.counter['2tracks']+=W
         if clusters.GetEntries()>25: self.counter['3tracks']+=W
         if clusters.GetEntries()>16:  self.interestingEvents[N].append(['clusters',clusters.GetEntries(),zInter])

      print('---> Summary')
      if mc:
        for x in stat:
          print(x,h['muI'+x].GetEntries() - h['muI'+x].GetBinContent(1))
          h['muI'+x].GetXaxis().SetRangeUser(0.6,10.)
      for x in stat:
         print(x,"with mu tracks", h['muIz'+x].GetEntries())
      print(self.counter)
      ut.bookCanvas(h,'z','',1200,900,1,1)
      tc = h['z'].cd()
      for w in ['','W']:
        h['muIz'+w].SetStats(0)
        h['muIz5'+w] = M.h['muIz'+w].Clone('muIz5'+w)
        h['muIz5'+w].Rebin(5)
        if not w=='': h['muIz5'+w].SetTitle('muon interaction z; z [m]; N/fb^{-1}/50cm')
        h['muIz5'+w].Draw()
        name = "muInterWithTracksZ"+w
        for c in ['.png','.pdf']:     tc.Print(name+'-'+self.tag+c)

      ut.bookCanvas(h,'d','',1600,1600,2,2)
      j=1
      for x in stat:
         if x=='': continue
         tc = h['d'].cd(j)
         j+=1
         h['dist'+x].SetStats(0)
         h['dist'+x].GetXaxis().SetRangeUser(0.,30.)
         h['dist'+x].Draw()
      name = "muScifiTrackDist"
      h['d'].Update()
      for c in ['.png','.pdf']:     h['d'].Print(name+'-'+self.tag+c)
      ut.bookCanvas(h,'a','',1600,1600,2,2)
      j=1
      for x in stat:
         if x=='': continue
         if x=='other': continue
         tc = h['a'].cd(j)
         j+=1
         h['cosAngle'+x].SetStats(0)
         h['cosAngle'+x].Draw()
      name = "muScifiTrackAngle"
      h['a'].Update()
      for c in ['.png','.pdf']:     h['a'].Print(name+'-'+self.tag+c)

if __name__ == '__main__':
    path = {}
    path['1.8downBfield'] =os.environ['EOSSHIP']+ "/eos/experiment/sndlhc/MonteCarlo/MuonBackground/muons_down/scoring_1.8_Bfield/sndLHC.Ntuple-TGeant4-160urad_magfield_2022TCL6_muons_rock_5e7pr_digCPP.root"

    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument("-f", dest="inputFile", help="input file MC",required=True, type=str,default="sndLHC.Ntuple-TGeant4_digCPP.root") 
    # 'sndLHC.Ntuple-TGeant4_-150urad_1e7pr_dig.root
    parser.add_argument("-g", "--geoFile", dest="geoFile", help="geofile", required=True)
    parser.add_argument("-c", "--command", dest="command",       help="command", default=None)
    options = parser.parse_args()
    import SndlhcGeo
    geo = SndlhcGeo.GeoInterface(options.geoFile)

    M = MuonInter()
    M.Init(options)

if 0>1:  # for use with 2dEventDisplay
 import MCmuonInteractions
 MCmuonInteractions.trackTask = trackTask
 import importlib
 importlib.reload(MCmuonInteractions)
 E = []
 for n in M.eventList:
     if M.eventList[n][0]>2:E.append(n)
 D={}
 for x in M.interestingEvents: 
    for c in M.interestingEvents[x]:
        if c[0].find('dist')>0: D[x]=1
 E=list(D.keys())
 G={}
 for x in M.interestingEvents: 
    for c in M.interestingEvents[x]:
        if c[0].find('angl')>0 and c[1]>0.05: G[x]=1
 E=list(G.keys())

# scale factor for 1fb-1: 8E13/5E7/ 1000(boostFactor) / 1 (iterations) = 1600

def poisson(mu,k):
    p = ROOT.TMath.Power(mu,k)*ROOT.TMath.Exp(-mu)/ROOT.TMath.Factorial(k)
    return p
