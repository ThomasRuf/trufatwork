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




nstart = 28043093

def ThreeTrackFinder(nstart=0,Nev=-1,sMin=10,dClMin=7,minDistance=1.5,sepDistance=0.5,debug=False):
    if Nev < 0 :
          nstop = eventTree.GetEntries() - nstart
    for ecounter in range(nstart,nstop):
        event = eventTree
        rc = eventTree.GetEvent(ecounter)
        E = eventTree.EventHeader
        if ecounter%1000000==0: print('still here',ecounter)
        trackTask.clusScifi.Clear()
        trackTask.scifiCluster()
        clusters = trackTask.clusScifi
        sortedClusters={}
        for aCl in clusters:
           so = aCl.GetFirst()//100000
           if not so in sortedClusters: sortedClusters[so]=[]
           sortedClusters[so].append(aCl)
        if len(sortedClusters)<sMin: continue
        M=0
        for x in sortedClusters:
           if len(sortedClusters[x]) == 3:  M+=1
        if M < dClMin: continue
        seeds = {}
        S = [-1,-1,-1]
        for o in range(0,2):
# same procedure for both projections
# take seeds from from first station with 3 clusters
             for s in range(1,6):
                 x = 10*s+o
                 if x in sortedClusters:
                    if len(sortedClusters[x])==3:
                       pos = []
                       for i in range(3):
                          cl = sortedClusters[x][i]
                          cl.GetPosition(A,B)
                          if o%2==1: pos.append( (A[0]+B[0])/2 )
                          else: pos.append( (A[1]+B[1])/2)
                       if abs(pos[0]-pos[1]) > minDistance and abs(pos[0]-pos[2]) > minDistance and abs(pos[1]-pos[2]) > minDistance:
                         S[o] = s
                         break
             if S[o]<0: break  # no seed found
             print(ecounter, '3 clusters')

