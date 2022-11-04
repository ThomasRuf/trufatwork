from array import array
scifi = geo.modules['Scifi']
SiPMPos = scifi.GetSiPMPos()
def GetSiPMPosition(SiPMChan):
    """
 STMRFFF
  First digit S:         station # within the sub-detector
  Second digit T:         type of the plane: 0-horizontal fiber plane, 1-vertical fiber plane
  Third digit M:         determines the mat number 0-2
  Fourth digit S:         SiPM number  0-3
  Last three digits F:     local SiPM channel number in one mat  0-127
    """
    locNumber           = SiPMChan%100000
    globNumber         = (SiPMChan//100000)*100000
    locPosition        = SiPMPos[locNumber] # local position in plane of reference plane.
    fFiberLength  = scifi.GetConfParF("Scifi/fiber_length")
#
    sID = str(SiPMChan)
    locPosition += scifi.GetConfParF("Scifi/LocM"+sID[0:3])
    loc = array('d',[0,0,0])
    path = "/cave_1/Detector_0/volTarget_1/ScifiVolume"+sID[0:1]+"_"+sID[0:1]+"000000/"
    if sID[1:2]=="0":
        path+="ScifiHorPlaneVol"+sID[0:1]+"_"+sID[0:1]+"000000"
        loc[0] = -fFiberLength/2
        loc[1] = locPosition
    else:
        path+="ScifiVertPlaneVol"+sID[0:1]+"_"+sID[0:1]+"000000"
        loc[1] = -fFiberLength/2
        loc[0] = locPosition
#
    nav = ROOT.gGeoManager.GetCurrentNavigator()
    nav.cd(path)
    glob = array('d',[0,0,0])
    nav.LocalToMaster(loc, glob)
    A=ROOT.TVector3( glob[0], glob[1],glob[2] )
    if sID[1:2]=="0": loc[0]=-loc[0]
    else: loc[1]=-loc[1]
    nav.LocalToMaster(loc, glob)
    B=ROOT.TVector3( glob[0], glob[1],glob[2] )
    return A,B

for event in eventTree:
    for aHit in event.Digi_ScifiHits:
        if not aHit.isValid(): continue
        A,B =  GetSiPMPosition(aHit.GetDetectorID())

local = False
A,B = ROOT.TVector3()
if 1:
 fout = open('ScifiPositions.txt','w')
 for S in range(1,6):
   for T in range(2):
      for M in range(3):
           for X in range(4):
                for F in range(128):
                     SiPMChan = F+1000*X+10000*M+100000*T+1000000*S
                     Scifi.GetSiPMPosition(SiPMChan,A,B)
                     if local: 
                        Aa,Bb =  GetSiPMPosition(SiPMChan)
                        if Aa.Cross(A).Mag()>10/10000 or Bb.Cross(B).Mag()>10/10000:  # 10 micron
                             print(SiPMChan,Aa.Cross(A).Mag(), Bb.Cross(B).Mag())
                             A.Print()
                             Aa.Print()
                             B.Print()
                             Bb.Print()
                             1/0
                     txt = "%i %7.3F %7.3F %7.3F %7.3F %7.3F %7.3F \n "%(SiPMChan,A[0],A[1],A[2],B[0],B[1],B[2])
                     rc = fout.write(txt)
 fout.close()


Scifi.GetSiPMPos


f1 = open("/home/truf/ubuntu-1710/sndlhc-ubuntu2004-16/ScifiPositions-new.txt")
f2 = open("/home/truf/ubuntu-1710/sndlhc-ubuntu2004-32/testbeam/ScifiAlignment/ScifiPositions.txt")
F1 = f1.readlines()
F2 = f2.readlines()
for n in range(len(F1)):
     L1 = []
     for x in F1[n].split(' '):
           if x=='' or x=='\n': continue
           L1.append(x)
     L2 = []
     for x in F2[n].split(' '):
           if x=='' or x=='\n': continue
           L2.append(x)
     if len(L1)==0 or len(L2)==0:
           print('end of file?')
           break
     if not L1[0]==L2[0]:
         print('there is a problem',L1,L2)
         1/0
     channel = int(L1[0])
     for x in range(1,len(L1)-1):
          R1 = float(L1[x])
          R2 = float(L2[x])
          if abs(R1-R2)>0.001: print(channel,x,int((R1-R2)*10000),R1,R2)

#another check
if 1:
    A,B = ROOT.TVector3(),ROOT.TVector3()
    Nev = 1000
    N = -1
    for event in eventTree:
       if eventTree.EventHeader.GetEventTime()==0: continue
       N+=1
       if N>Nev: break
# select events with clusters in each plane
       theTrack = Scifi_track(nPlanes = 10, nClusters = 11)
       if not hasattr(theTrack,"getFittedState"): continue
       theTrack.Delete()
       DetID2Key={}
       for aCluster in event.ScifiClusters:
         for k in range(aCluster.GetFirst(),aCluster.GetFirst()+aCluster.GetN()):
           for nHit in range(event.Digi_ScifiHits.GetEntries()):
              if event.Digi_ScifiHits[nHit].GetDetectorID()==k:
                 DetID2Key[k] = nHit
       for aCl in eventTree.ScifiClusters:
             aCl.GetPosition(A,B)
             ifirst = aCl.GetFirst()
             QDCs = []
             for n in range(aCl.GetN()):
                 QDCs.append(event.Digi_ScifiHits[DetID2Key[ifirst+n]].GetSignal())
             print(A[0],A[1],A[2],QDCs)

if 1:
       print(N,eventTree.EventHeader.GetEventTime(),event.Digi_ScifiHits.GetEntries())
# select events with clusters in each plane
       theTrack = Scifi_track(nPlanes = 10, nClusters = 11)
       theTrack.Delete()
       for aCl in eventTree.ScifiClusters:
             aCl.GetPosition(A,B)
             A.Print()

