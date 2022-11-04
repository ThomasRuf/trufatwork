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

