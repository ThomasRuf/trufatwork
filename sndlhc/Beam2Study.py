
trackTask.DSnPlanes = 3
trackTask.DSnHits = 2

def goodEvent(event):
        xing = bunchXtype()
        if xing['B2noB1']: return True
        return False
def goodEvent(event):
        xing = bunchXtype()
        if xing['B1only']: return True
        return False

def bunch():
             xing = {'all':True,'B1only':False,'B2noB1':False,'noBeam':False}
             bunchNumber = eventTree.EventHeader.GetEventTime()%(4*3564)//4+1
             nb1 = (3564 + bunchNumber - fsdict['phaseShift1'])%3564
             nb2 = (3564 + bunchNumber - fsdict['phaseShift1']- fsdict['phaseShift2'])%3564
             b1 = nb1 in fsdict['B1']
             b2 = nb2 in fsdict['B2']
             IP1 = False
             IP2 = False
             if b1:
                IP1 =  fsdict['B1'][nb1]['IP1']
             if b2:
                IP2 =  fsdict['B2'][nb2]['IP2']
             if b2 and not b1:
                xing['B2noB1'] = True
             if b1 and not b2 and not IP1:
                xing['B1only'] = True
             if not b1 and not b2: xing['noBeam'] = True
             print('bunchNumber',bunchNumber,'nb1',nb1,'nb2',nb2,b1,b2)

for aHit in eventTree.Digi_ScifiHits:
     print(aHit.GetTime())
for aHit in eventTree.Digi_MuFilterHits:
             for x in aHit.GetAllTimes():
                print(aHit.GetDetectorID(),x.second)

def dT(nstart=0,Nev=-1):
    if Nev < 0 :
          nstop = eventTree.GetEntries() - nstart
    prevT = 0
    prevT2 = 0
    prevT3 = 0
    ut.bookHist(h,'dT','dT',200,0.,200.)
    ut.bookHist(h,'dT2','dT3',200,0.,200.)
    ut.bookHist(h,'dT3','dT3',200,0.,200.)
    for ecounter in range(nstart,nstop):
        event = eventTree
        rc = eventTree.GetEvent(ecounter)
        E = eventTree.EventHeader
        if ecounter%1000000==0: print('still here',ecounter)
        deltaT = E.GetEventTime()-prevT
        if prevT > 0: rc = h['dT'].Fill(deltaT)
        if prevT2 > 0 and deltaT==4: rc = h['dT2'].Fill(E.GetEventTime()-prevT2)
        if prevT3 > 0 and prevT-prevT2==4 and deltaT==4: rc = h['dT3'].Fill(E.GetEventTime()-prevT3)
        prevT3 = prevT2
        prevT2 = prevT
        prevT = E.GetEventTime()

def hitTime(nstart=0,Nev=-1,board0 = 40):
    nstop = nstart + Nev
    if Nev < 0 :
          nstop = eventTree.GetEntries()
    ut.bookHist(h,'TVeto','hit time',100,0.,10.)
    ut.bookHist(h,'TUS','hit time',100,0.,10.)
    ut.bookHist(h,'TDS','hit time',100,0.,10.)
    ut.bookHist(h,'Tscifi','hit time',100,0.,10.)
    ut.bookHist(h,'Tboard','hit time per board',70,0.5,70.5,100,-5.,5.)
    h['Tscifi'].SetLineColor(ROOT.kRed)
    h['TVeto'].SetLineColor(ROOT.kGreen)
    h['TUS'].SetLineColor(ROOT.kBlue)
    h['TDS'].SetLineColor(ROOT.kCyan)
    stats = [0,0,0,0,0]
    for ecounter in range(nstart,nstop):
        event = eventTree
        rc = eventTree.GetEvent(ecounter)
        foundMu = False
        foundVeto = False
        boards = {}
        for aHit in event.Digi_MuFilterHits:
             for x in aHit.GetAllTimes():
                t = aHit.GetDetectorID()//10000
                if t==1: rc = h['TVeto'].Fill(x.second)
                if t==2: rc = h['TUS'].Fill(x.second)
                if t==3: rc = h['TDS'].Fill(x.second)
                if x.second>4: 
                     foundMu = True
                     if aHit.GetDetectorID()//10000==1: 
                         foundVeto=True
                bid = aHit.GetBoardID(x.first)
                if not bid in boards:  boards[bid]=[]
                boards[bid].append(x.second)
        if foundMu: stats[0]+=1
        if foundVeto: stats[4]+=1
        found = False
        for aHit in event.Digi_ScifiHits:
                rc = h['Tscifi'].Fill(aHit.GetTime())
                if aHit.GetTime()>4: found = True
                bid = aHit.GetBoardID(0)
                if not bid in boards:  boards[bid]=[]
                boards[bid].append(aHit.GetTime())
        if found: stats[1]+=1
        if found or foundMu :  stats[2]+=1
        if found and foundMu :  stats[3]+=1
# times relative to board 40
        if not board0 in boards: continue
        boards[board0].sort()
        T0 = 0
        for x in boards[board0]: T0+=x
        T0 = T0/len(boards[board0])
        for b in boards:
           for x in boards[b]:
              rc = h['Tboard'].Fill(b,x-T0)
    print(stats)
    h['Tscifi'].Draw()
    h['TVeto'].Draw('same')
    h['TUS'].Draw('same')
    h['TDS'].Draw('same')
    B = {}
    for b in range(1,h['Tboard'].GetNbinsX()+1):
       h['Tboard'+str(b)] = h['Tboard'].ProjectionY('tmp'+str(b),b,b)
       if h['Tboard'+str(b)].GetEntries()>0:  B[b] = h['Tboard'+str(b)]
    ut.bookCanvas(h,'xboards','',2400,1800,10,4)
    k=1
    for b in B:
        h['xboards'].cd(k)
        k+=1
        h['Tboard'+str(b)].Draw()

