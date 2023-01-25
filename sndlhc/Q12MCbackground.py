import ROOT,os
import rootUtils as ut
h={}
pdg = ROOT.TDatabasePDG.Instance()
# Q12 background
f = ROOT.TFile('sndLHC.Ntuple-TGeant4-Q12Background_dig.root')
eventTree = f.cbmsim
#
ut.bookHist(h,'mufi_xy_plane','xy_plane'+';X [cm]; Y [cm]',100,-90,10,80,0,80)
ut.bookHist(h,'scifi_xy_plane','xy_plane'+';X [cm]; Y [cm]',100,-90,10,80,0,80)
#
for event in eventTree:
    primPart = event.MCTrack[0].GetPdgCode()
    for aHit in event.MuFilterPoint:
         s = aHit.GetDetectorID()//10000
         p = (aHit.GetDetectorID()//1000)%10
         bar = (aHit.GetDetectorID()%1000)%60
         plane = s*10+p
         if s==3:
           if (aHit.GetDetectorID()%1000)>60: plane = s*10+2*p+1
           else:                 plane = s*10+2*p
         pid = aHit.PdgCode()
         key = 'mufi_xy_plane' + str(plane)+'_'+str(pid)
         if not key in h: h[key] = h['mufi_xy_plane'].Clone(key)
         rc = h[key].Fill(aHit.GetX(),aHit.GetY())
         key = 'mufi_xy_plane' + str(plane)+'_prim_'+str(primPart)
         if not key in h: h[key] = h['mufi_xy_plane'].Clone(key)
         rc = h[key].Fill(aHit.GetX(),aHit.GetY())
    for aHit in event.ScifiPoint:
         plane = aHit.GetDetectorID()//100000
         pid = aHit.PdgCode()
         key = 'scifi_xy_plane' + str(plane)+'_'+str(pid)
         if not key in h: h[key] = h['scifi_xy_plane'].Clone(key)
         rc = h[key].Fill(aHit.GetX(),aHit.GetY())
         key = 'scifi_xy_plane' + str(plane)+'_prim_'+str(primPart)
         if not key in h: h[key] = h['scifi_xy_plane'].Clone(key)
         rc = h[key].Fill(aHit.GetX(),aHit.GetY())

stats = {}
primStats = {}
for key in h:
   tmp = key.split('_')
   if len(tmp)==4:
     x = key.split('_')[3]
     if not x in stats: stats[x]=0
     stats[x]+=h[key].GetEntries()
   if len(tmp)==5:
     x = key.split('_')[4]
     if not x in primStats: primStats[x]=0
     primStats[x]+=h[key].GetEntries()

new_list = sorted(stats.items(), key=lambda x: x[1], reverse=True)
for x in new_list:
   pname = "     "
   if pdg.GetParticle(int(x[0])):
      pname = pdg.GetParticle(int(x[0])).GetName()
   print(x[0],pname,x[1])
prim_list = sorted(primStats.items(), key=lambda x: x[1], reverse=True)
for x in prim_list:
   pname = "     "
   if pdg.GetParticle(int(x[0])):
      pname = pdg.GetParticle(int(x[0])).GetName()
   print(x[0],pname,x[1])

keys = list(h.keys())
for x in keys:
   k = x.find('mufi_xy_plane')
   if k<0: continue
   k=15
   p=x[:k].replace('x','')
   if not p in h:
        h[p]=h['mufi_xy_plane'].ProjectionY(p)
   tmp = h[x].ProjectionY()
   rc = [p].Add(tmp)

import ROOT,os
h={}
www =os.environ['EOSSHIP']+"/eos/experiment/sndlhc/www/"
if 1:
 for beam in ['','B1only']:
  for runNumber in [4705,4661,4654,4708,4713]:
   r = str(runNumber).zfill(6)
   F = ROOT.TFile.Open(www+"offline/"+"run"+r+".root")
   h['scifi-trackDir'+beam+r] = F.scifi.Get('scifi-trackDir'+beam).Clone('scifi-trackDir'+beam)
  h['slopeX'+beam]=h['scifi-trackDir'+beam+r].FindObject('slopeX'+beam).Clone('slopeX'+beam)
  h['slopeX'+beam].Reset()
  for runNumber in [4705,4661,4654,4708,4713]:
   r = str(runNumber).zfill(6)
   h['slopeX'+beam].Add(h['scifi-trackDir'+beam+r].FindObject('slopeX'+beam).Clone('tmp'))
