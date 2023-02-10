def veto():
    stats = [0,0]
    for event in eventTree:
       stats[0]+=1
       for aHit in eventTree.Digi_MuFilterHits:
           if not aHit.isValid(): continue
           detID = aHit.GetDetectorID()
           s = aHit.GetDetectorID()//10000
           if s==1: 
               stats[1]+=1
               break
def goodEvent(event):
       rc =True
       if len(event.Digi_ScifiHits)<8: return False
       for aHit in event.Digi_MuFilterHits:
           if not aHit.isValid(): continue
           detID = aHit.GetDetectorID()
           s = aHit.GetDetectorID()//10000
           if s==1: 
               rc = False
               break
       return rc

prefT = 0
def goodEvent(event):
       global prefT
       if event.EventHeader.GetEventTime()-prefT == 4: rc=True
       else:        rc = False
       prefT = event.EventHeader.GetEventTime()
       return rc

def goodEvent(event):
       stats = [0,0]
       for aHit in event.Digi_MuFilterHits:
           if not aHit.isValid(): continue
           detID = aHit.GetDetectorID()
           s = aHit.GetDetectorID()//1000
           if s//10==1:
               stats[s%10]+=1
       rc = stats[0]==1 and stats[1]==2
       return rc


emulsionReplacements = {0:1,4573:2,4859:3,5172:4}
import ROOT
import os,sys,subprocess
import SndlhcGeo
import SndlhcTracking
emulsion = {}
geoFiles = {}
emulsion[1] = [4572,4568,4541,4532,4527,4515,4513,4504,4503,4488,4449,4427,4423,4421,4415,4410]
geoFiles[1] =  "geofile_sndlhc_TI18_V3_08August2022.root"
emulsion[2] = [4964]
geoFiles[2] =  "geofile_sndlhc_TI18_V6_08October2022.root"
emulsion[3] = [5408,5399,5396,5389,5382,5377,5373,5350]
geoFiles[1] =  "geofile_sndlhc_TI18_V5_14August2022.root"
geoFiles[2] =  "geofile_sndlhc_TI18_V6_08October2022.root"
geoFiles[3] =  "geofile_sndlhc_TI18_V7_22November2022.root"
emulsion[101] = ["sndLHC.Ntuple-TGeant4_boost101.0_digCPP.root"]   # MC boost factor 101
geoFiles[101] = "geofile_full.Ntuple-TGeant4_boost101.0.root"
emulsion[1001] = ["sndLHC.Ntuple-TGeant4_boost1001.0_digCPP.root"]   # MC boost factor 1001
geoFiles[1001] = "geofile_full.Ntuple-TGeant4_boost1001.0.root"
#
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("--server", dest="server", help="xrootd server",default=os.environ["EOSSHIP"])
parser.add_argument("-p", "--path", dest="path", help="path to data",default="/eos/experiment/sndlhc/convertedData/commissioning/TI18/")
parser.add_argument("-period", dest="period", help="period emulsion or MC",default=2,type=int)
options = parser.parse_args()
period = options.period

snd_geo = SndlhcGeo.GeoInterface(options.server+options.path+geoFiles[period])
if period <10:
  eventChain = ROOT.TChain('rawConv')
  for r in emulsion[period]:
    dirlist  = str( subprocess.check_output("xrdfs "+options.server+" ls "+options.path+"run_"+str(r).zfill(6),shell=True) )
    for x in dirlist.split('\\n'):
      ix = x.find('sndsw_raw-')
      if ix<0: continue
      eventChain.Add(options.server+options.path+'run_'+str(r).zfill(6)+'/'+x[ix:])
else:
  eventChain = ROOT.TChain('cbmsim')
  for r in emulsion[period]:
      eventChain.Add(options.server+options.path+r)

eventTree = eventChain
trackTask = SndlhcTracking.Tracking() 
trackTask.SetName('simpleTracking')
trackTask.Init()
trackTask.event = eventTree
A= ROOT.TVector3()
B= ROOT.TVector3()
# for 3 tracks try with: multiTrackFinder(nstart=0,Nev=-1,sMin=10,dClMin=6,minDistance=0.5,debug=False)
# for 2 tracks try with: multiTrackFinder(nstart=0,Nev=-1,ntrack=2,sMin=10,dClMin=6,minDistance=1.5,debug=False)

def multiTrackFinder(nstart=0,Nev=-1,ntrack=3,sMin=10,dClMin=6,minDistance=0.5,debug=False):
    # smin = 10: have hits in all 2*5 scifi planes
    # dClMin = 6: require at least 6 out of 10 planes with exactly ntrack clusters
    # minDistance = 1.5: require at least one plane with 3 clusters which are separated by 1.5cm each
    if Nev < 0 :
          nstop = eventTree.GetEntries()
    else: nstop = nstart + Nev
    print(nstart,nstop)
    for ecounter in range(nstart,nstop):
        event = eventTree
        rc = eventTree.GetEvent(ecounter)
        E = eventTree.EventHeader
        if ecounter%1000000==0: print('still alive',ecounter)
        trackTask.clusScifi.Clear()
        trackTask.scifiCluster()
        clusters = trackTask.clusScifi
        sortedClusters={}
        for aCl in clusters:
           so = aCl.GetFirst()//100000
           if not so in sortedClusters: sortedClusters[so]=[]
           sortedClusters[so].append(aCl)
        if debug: print(ecounter,len(sortedClusters))
        if len(sortedClusters)<sMin: continue
        M=0
        for x in sortedClusters:
           if len(sortedClusters[x]) == ntrack:  M+=1
        # special selection for Run0 emulsion with only emulsion in third brick
        thirdBrick = ''
        if period == 0:
          thirdBrick = False
          if len(sortedClusters[10])==1 and len(sortedClusters[11])==1 and len(sortedClusters[20])==1 and len(sortedClusters[21])==1: thirdBrick = True
          if M < dClMin and not thirdBrick: continue
          if thirdBrick and M < 2: continue
        if debug: print(" ->",M)
        if M < dClMin and not thirdBrick: continue
        seeds = {}
        S = [0,0,0]
        for o in range(0,2):
# same procedure for both projections
# count number of stations with 3 or 4 clusters
             for s in range(1,6):
                 x = 10*s+o
                 if x in sortedClusters:
                    if len(sortedClusters[x])>ntrack-1 and len(sortedClusters[x])<ntrack+2:
                       pos = []
                       for cl in sortedClusters[x]:
                          cl.GetPosition(A,B)
                          if o%2==1: pos.append( (A[0]+B[0])/2 )
                          else: pos.append( (A[1]+B[1])/2)
                       N = 0
                       for i1 in range(len(pos)-1):
                         for i2 in range(i1+1,len(pos)):
                           if abs(pos[i1]-pos[i2]) > minDistance: N+=1
                       if N>ntrack-1 or (N==1 and ntrack==2): S[o] +=1
        if debug: print(" --->",S[0],S[1])
        if S[0]<2 or S[1]<2: continue  # no seed found
        print(ecounter,S[0],S[1], thirdBrick)

eventList = {}
eventList['?'] = [17175055,19300869,80135751,85424401,93683521,100822424,105590103,107532459,5823205,8086243,132359441,31924135]
eventList[101] = [17105,75498,78911,81952,92988,157310,179702,191244,246604,249961,263769,273781,286900,345050]
eventList[1001] = [6472, 9789, 19373, 19523, 19576, 48825, 49050, 49790, 57052, 58114, 59020, 62999, 68183, 73752, 75237, 79585, 81392, 82690, 91727, 92465, 94300, 94961, 98123, 99532, 103323, 106940, 108414, 116558, 122835, 123592, 131933, 133277, 133482, 142698, 146664, 149819, 156938, 159718, 160726, 173136, 175961, 183386, 186674, 191120, 191179, 193227, 194053, 196052, 198436, 202028, 202484, 204194, 210153, 210621, 210707, 222379, 230330, 231250, 233268, 235153, 242281, 245666, 257368, 262071, 265819, 273375, 273684, 276857, 280377, 281309, 281562, 294695, 295016, 301022, 302055, 303203, 310132, 315826, 316670, 317046, 320022, 325755, 329052, 338379, 341934, 350081, 353268, 362001, 369672, 379246, 381855]


def calcWeight(eventList):
   w = 0
   for i in eventList:
     rc =  eventTree.GetEvent(i)
     w+=eventTree.MCTrack[0].GetWeight()
   return w
import numpy
def firstHits(eventList):
    for ecounter in eventList:
        rc = eventTree.GetEvent(ecounter)
        print('--->  event %10i   station       position '%(ecounter))
        event = eventTree
        trackTask.clusScifi.Clear()
        trackTask.scifiCluster()
        clusters = trackTask.clusScifi
        sortedClusters={}
        for aCl in clusters:
           so = aCl.GetFirst()//100000
           if not so in sortedClusters: sortedClusters[so]=[]
           sortedClusters[so].append(aCl)
        pos = {}
        for s in range(1,6):
         for o in range(0,2):
            so = 10*s+o
            pos[so]=[]
            for cl in sortedClusters[so]:
               cl.GetPosition(A,B)
               if o%2==1: pos[so].append( (A[0]+B[0])/2 )
               else: pos[so].append( (A[1]+B[1])/2 )
         X = numpy.mean(pos[10*s+1])
         Y = numpy.mean(pos[10*s+0])
         rms = numpy.std(pos[10*s+1])+numpy.std(pos[10*s+0])
         print('                    %i      X=%5.2Fcm   Y=%5.2Fcm  rms=%5.2F'%(s,X,Y,rms ) )
         
         
def readList(fname):
       g = open(fname)
       evtList = {}
       for l in g.readlines():
           runNr=l.split(' ')[0]
           evtList[int(runNr)] = l[len(runNr):].replace('\n','')
       return evtList

if 1<0:
# for event display
 period = 3
 emulsion = {}
 geoFiles = {}
 emulsion[1] = [4572,4568,4541,4532,4527,4515,4513,4504,4503,4488,4449,4427,4423,4421,4415,4410]
 geoFiles[1] =  "geofile_sndlhc_TI18_V3_08August2022.root"
 emulsion[3] = [5408,5399,5396,5389,5382,5377,5373,5350]
 emulsion[2] = [4964]
 geoFiles[1] =  "geofile_sndlhc_TI18_V5_14August2022.root"
 geoFiles[2] =  "geofile_sndlhc_TI18_V6_08October2022.root"
 geoFiles[3] =  "geofile_sndlhc_TI18_V7_22November2022.root"
 options.path="/eos/experiment/sndlhc/convertedData/commissioning/TI18/"
 eventChain = ROOT.TChain('rawConv')
 def readList(fname):
       g = open(fname)
       evtList = {}
       for l in g.readlines():
           if not l.find('still')<0: continue
           runNr=l.split(' ')[0]
           evtList[int(runNr)] = l[len(runNr):].replace('\n','')
       return evtList
 for r in emulsion[period]:
   dirlist  = str( subprocess.check_output("xrdfs "+options.server+" ls "+options.path+"run_"+str(r).zfill(6),shell=True) )
   for x in dirlist.split('\\n'):
      ix = x.find('sndsw_raw-')
      if ix<0: continue
      eventChain.Add(options.server+options.path+'run_'+str(r).zfill(6)+'/'+x[ix:])
 eventTree = eventChain
 if period == 3: v2 = readList('period3_v2.txt')
 if period == 2: v2 = readList('period2_v1.txt')
 L = list(v2.keys())
 L.sort()
 options.storePic = "/home/truf/eventDisplay/"

if 1<0:
# for event display
 period = 2
 emulsion = {}
 geoFiles = {}
 emulsion[1] = [4572,4568,4541,4532,4527,4515,4513,4504,4503,4488,4449,4427,4423,4421,4415,4410]
 geoFiles[1] =  "geofile_sndlhc_TI18_V3_08August2022.root"
 emulsion[2] = [4964]
 geoFiles[2] =  "geofile_sndlhc_TI18_V6_08October2022.root"
 emulsion[3] = [5408,5399,5396,5389,5382,5377,5373,5350]
 geoFiles[1] =  "geofile_sndlhc_TI18_V5_14August2022.root"
 geoFiles[2] =  "geofile_sndlhc_TI18_V6_08October2022.root"
 geoFiles[3] =  "geofile_sndlhc_TI18_V7_22November2022.root"
 options.path="/eos/experiment/sndlhc/convertedData/commissioning/TI18/"
 eventChain = ROOT.TChain('rawConv')
 def readList(fname):
       g = open(fname)
       evtList = {}
       for l in g.readlines():
           if not l.find('still')<0: continue
           runNr=l.split(' ')[0]
           evtList[int(runNr)] = l[len(runNr):].replace('\n','')
       return evtList
 for r in emulsion[period]:
   dirlist  = str( subprocess.check_output("xrdfs "+options.server+" ls "+options.path+"run_"+str(r).zfill(6),shell=True) )
   for x in dirlist.split('\\n'):
      ix = x.find('sndsw_raw-')
      if ix<0: continue
      eventChain.Add(options.server+options.path+'run_'+str(r).zfill(6)+'/'+x[ix:])
 eventTree = eventChain
 trackTask.event = eventTree
 v2 = readList('period2_v2.txt')
 L = list(v2.keys())
 L.sort()
 options.storePic = "/home/truf/eventDisplay/"
 
def goodEvent(event):
       stats = [0,0,0,0]
       for aHit in event.Digi_MuFilterHits:
           if not aHit.isValid(): continue
           detID = aHit.GetDetectorID()
           s = aHit.GetDetectorID()//10000
           stats[s]+=1
       rc = stats[2]>6 and stats[3]>10
       return rc

def makeIndexRunEventNumer(L):
   eventMap = {}
   for N in L:
      rc = eventTree.GetEvent(N)
      eventMap[N] = [eventTree.EventHeader.GetRunId(),eventTree.EventHeader.GetEventNumber()]
   return eventMap

def makeSelectedEventList(rl):
   evtList = {}
   for r in rl:
    sr = str(r)
    evtList[r]=[]
    for x in os.listdir('.'):
       if not x.find(sr)<0 and not x.find('png')<0:
           evtList[r].append(int(x.split('.')[0].split('_')[1]))
   return evtList
   
# run 5399: 571.2 pb-1  
# 5408:     430.2 pb-1


