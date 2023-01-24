import ROOT,os
use = '2.5down'
mcFile={}
path={}
run={}

mcFile['2.5up'] = ["sndLHC.Ntuple-TGeant4_150urad_1e7pr_dig.root"]
path['2.5up'] = os.environ['EOSSHIP']+"/eos/experiment/sndlhc/MonteCarlo/MuonBackground/muons_up/scoring_2.5/"
run['2.5up'] = 2

mcFile['2.5down'] = ["sndLHC.Ntuple-TGeant4_-150urad_1e7pr_dig.root","simona/down/set3/sndLHC.Ntuple-TGeant4_-150urad_1e7pr_dig.root",
                                 "simona/down/set2/sndLHC.Ntuple-TGeant4_-150urad_1e7pr_dig.root","simona/down/set1/sndLHC.Ntuple-TGeant4_-150urad_1e7pr_dig.root"]
# path['2.5down'] = os.environ['EOSSHIP']+ "/eos/experiment/sndlhc/MonteCarlo/MuonBackground/muons_down/scoring_2.5/"
path['2.5down'] = ""
run['2.5down'] = 1

mcFile['1.8down']=["sndLHC.Ntuple-TGeant4-Down_1_20_dig.root","sndLHC.Ntuple-TGeant4-Down_21_40_dig.root",
                                "sndLHC.Ntuple-TGeant4-Down_41_59_dig.root","sndLHC.Ntuple-TGeant4-Down_61_80_dig.root",
                                "sndLHC.Ntuple-TGeant4-Down_81_100_dig.root"]
path['1.8down'] =os.environ['EOSSHIP']+ "/eos/experiment/sndlhc/MonteCarlo/MuonBackground/muons_down/"
run['1.8down'] = 10
reco = False

if reco:
   for x in mcFile[use]:
       cmd = "$SNDSW_ROOT/shipLHC/scripts/run_Monitoring.py --server dummy -f "+path[use]+x+" \
 -g ../geofile_full.Ntuple-TGeant4.root --ScifiResUnbiased 1 -r "+str(run[use])
       print(cmd)
       os.system("python "+cmd + "  --batch")
       run[use]+=1

if reco: 1/0

eventChain = ROOT.TChain('cbmsim')
for x in mcFile[use]: eventChain.AddFile(path[use]+x)

N = [0,0,0]
stats = [0,0,0]
for event in eventChain:
   if event.ScifiPoint.GetEntries()>0:
      stats[0] += event.MCTrack[0].GetWeight()
      N[0]+=1
   s={}
   for p in event.ScifiPoint:
     if p.GetTrackID()>0: continue
     s[p.GetDetectorID()//1000000]=1
   if len(s)>2:
      stats[1] += event.MCTrack[0].GetWeight()
      N[1]+=1
   if len(s)>4:
      stats[2] += event.MCTrack[0].GetWeight()
      N[2]+=1

print('number of events with at least one ScifiPoint  N=%i   weighted = %5.2F'%(N[0],stats[0]))
print('number of events with at least 3 station hit by muon  N=%i   weighted = %5.2F'%(N[1],stats[1]))
print('number of events with 5 stations hit by muon  N=%i   weighted = %5.2F'%(N[2],stats[2]))

def DStrackResol(debug=False):
   trackTask.DSnPlanes=3
   ut.bookHist(h,'resSx','res Sx;[mrad]',100,-100,100)
   ut.bookHist(h,'resSy','res Sy;[mrad]',100,-100,100)
   ut.bookHist(h,'resSx_0','res Sx;[mrad]',100,-100,100)
   ut.bookHist(h,'resSy_0','res Sy;[mrad]',100,-100,100)
   ut.bookHist(h,'resSH','res Sx;[mrad]',100,-100,100)
   ut.bookHist(h,'resSV','res Sy;[mrad]',100,-100,100)
   ut.bookHist(h,'resSx_true','res Sx;[mrad]',100,-10,10)
   ut.bookHist(h,'resSy_true','res Sy;[mrad]',100,-10,10)
   ut.bookHist(h,'resX','res x;[mm]',100,-20,20)
   ut.bookHist(h,'resY','res y;[mm]',100,-20,20)
   ut.bookHist(h,'resX_last','res x;[mm]',100,-20,20)
   ut.bookHist(h,'resY_last','res y;[mm]',100,-20,20)
   for event in eventTree:
      trackTask.fittedTracks.Delete()
      trackTask.ExecuteTask("DS")
      for aTrack in trackTask.fittedTracks:
         if not aTrack.GetUniqueID()==3: continue
         fitStatus = aTrack.getFitStatus()
         if  not fitStatus.isFitConverged(): continue
         state = ROOT.getFittedState(aTrack,0)
         if not state: continue
         pos = state.getPos()
         mom = state.getMom()
         slopeX = mom.X()/mom.Z()
         slopeY = mom.Y()/mom.Z()
         laststate = ROOT.getFittedState(aTrack,aTrack.getNumPointsWithMeasurement()-1)
         lastpos = laststate.getPos()
         if not laststate: continue
         slopeX_0 = (lastpos[0]-pos[0])/(lastpos[2]-pos[2])
         slopeY_0 = (lastpos[1]-pos[1])/(lastpos[2]-pos[2])
         # true slope and position at first DS plane
         firstDShit = [9999,-1]
         lastDShit = [0,-1]
         # calc slope from digis
         posBars = {'H':{},'V':{}}
         for nM in range(aTrack.getNumPointsWithMeasurement()):
            M = aTrack.getPointWithMeasurement(nM)
            W = M.getRawMeasurement()
            detID = W.getDetId()
            geo.modules['MuFilter'].GetPosition(detID,A,B)
            bar = (detID%1000)
            o = 'H'
            coord = (A[1]+B[1])/2
            if bar>59:
                o = 'V'
                coord = (A[0]+B[0])/2
            posBars[o][A[2]]=[coord,detID]
         for aPoint in event.MuFilterPoint:
            detID = aPoint.GetDetectorID()//10000
            if detID < 3: continue
            if aPoint.GetZ() < firstDShit[0]:
                firstDShit[0]=aPoint.GetZ()
                firstDShit[1]=aPoint
            if aPoint.GetZ() > lastDShit[0]:
                lastDShit[0]=aPoint.GetZ()
                lastDShit[1]=aPoint
         trueslopeX = firstDShit[1].GetPx()/firstDShit[1].GetPz()
         trueslopeY = firstDShit[1].GetPy()/firstDShit[1].GetPz()
         slMCX = (lastDShit[1].GetX()-firstDShit[1].GetX() )/ (lastDShit[1].GetZ()-firstDShit[1].GetZ() )
         slMCY = (lastDShit[1].GetY()-firstDShit[1].GetY() )/ (lastDShit[1].GetZ()-firstDShit[1].GetZ() )
         rc = h['resSx'].Fill( (slopeX-trueslopeX)*1000 )
         rc = h['resSy'].Fill( (slopeY-trueslopeY)*1000 )
         rc = h['resSx_0'].Fill( (slopeX_0-trueslopeX)*1000 )
         rc = h['resSy_0'].Fill( (slopeY_0-trueslopeY)*1000 )
         rc = h['resSx_true'].Fill( (slMCX-trueslopeX)*1000 )
         rc = h['resSy_true'].Fill( (slMCY-trueslopeY)*1000 )
         rc = h['resX'].Fill( (pos[0]-firstDShit[1].GetX())*10 )
         rc = h['resY'].Fill( (pos[1]-firstDShit[1].GetY())*10 )
         rc = h['resX_last'].Fill( (lastpos[0]-lastDShit[1].GetX())*10 )
         rc = h['resY_last'].Fill( (lastpos[1]-lastDShit[1].GetY())*10 )
         posKeys = {}
         pTrue = {'H':trueslopeY,'V':trueslopeX}
         for o in ['H','V']:
            posKeys[o] = {'list':list(posBars[o]),'first':0,'last':0}
            posKeys[o]['list'].sort()
            posKeys[o]['first'] = posKeys[o]['list'][0]
            posKeys[o]['last'] = posKeys[o]['list'][len(posKeys[o]['list'])-1]
            dZ = posKeys[o]['last']-posKeys[o]['first']
            posKeys[o]['slope'] = (posBars[o][posKeys[o]['last']][0]-posBars[o][posKeys[o]['first']][0]) / dZ
            rc = h['resS'+o].Fill((posKeys[o]['slope']-pTrue[o])*1000)
            if debug: print(o,posBars[o][posKeys[o]['last']],posBars[o][posKeys[o]['first']],(posKeys[o]['slope'])*1000,(posKeys[o]['slope']-pTrue[o])*1000)


