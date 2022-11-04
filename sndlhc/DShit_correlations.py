def DS_hitCorrelations(Nev=-1):
 s=3
 for l in range(systemAndPlanes[s]):
       ut.bookHist(h,'cor_'+str(s*10+l),'2 hit correlations '+str(s*10+l),60,-0.5,59.5,60,-0.5,59.5)
       ut.bookHist(h,'diff_'+str(s*10+l),'2 hit correlations '+str(s*10+l),21,-10.5,10.5)
 N=-1
 if Nev < 0 : Nev = eventTree.GetEntries()
 for event in eventTree:
    N+=1
    if N%options.heartBeat == 0: print('event ',N,' ',time.ctime())
    if N>Nev: break
    listOfHits = {}
    for aHit in event.Digi_MuFilterHits:
        if not aHit.isValid(): continue
        detID = aHit.GetDetectorID()
        s = detID//10000
        if s<3: continue
        l  = (detID%10000)//1000  # plane number
        bar = (detID%1000)
        if s>2:
               l=2*l
               if bar>59:
                    bar=bar-60
                    if l<6: l+=1
        key = s*10+l
        if not key in listOfHits: listOfHits[key]=[]
        listOfHits[key].append(bar)
    for key in listOfHits:
          for i1 in range( len(listOfHits[key])-1):
             bar1 = listOfHits[key][i1]
             for i2 in range(i1+1,len(listOfHits[key])):
                bar2 = listOfHits[key][i2]
                rc = h['cor_'+str(key)].Fill(bar1,bar2)
                rc = h['diff_'+str(key)].Fill(bar1-bar2)
 ut.bookCanvas(h,'tcor','',1600,1200,2,2)
 ut.bookCanvas(h,'tdiff','',1600,1200,2,2)
 s=3
 for l in range(systemAndPlanes[s]):
       if l>3: continue
       tc = h['tcor'].cd(l+1)
       h['cor_'+str(s*10+l)].Draw('colz')
       tc = h['tdiff'].cd(l+1)
       h['diff_'+str(s*10+l)].Draw()

def cosmicEvent():
           cosmic = False
           stations = {'Scifi':{},'Mufi':{}}
           for d in eventTree.Digi_ScifiHits:
               stations['Scifi'][d.GetDetectorID()//1000000] = 1
           for d in eventTree.Digi_MuFilterHits:
               plane = d.GetDetectorID()//1000
               stations['Mufi'][plane] = 1
           if len(stations['Scifi']) > 3 : cosmic = True
           if len(stations['Mufi']) > 3 : cosmic = True
           return cosmic

freq      = 160.E6
TDC2ns = 1E9/freq

def eventRate():
  ut.bookHist(h,'delT','time between good events',1000,0.,1000.)
  tprev = 0
  for event in eventTree:
       if not cosmicEvent(): continue
       t = eventTree.EventHeader.GetEventTime()
       dt = (t - tprev)*TDC2ns/u.s
       rc = h['delT'].Fill(dt)
       tprev = t

def hitCounts():
    N=-1
    Nmu = 0
    for event in eventTree:
           N+=1
           # print('N: %i   mufiHits: %i    scifiHits: %i'%(N,event.Digi_MuFilterHits.GetEntries(), event.Digi_ScifiHits.GetEntries()))
           if event.Digi_MuFilterHits.GetEntries()>2 : Nmu+=1

        
