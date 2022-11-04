def goodEvent(event):
# can be replaced by any user selection
           flag = False
           veto = False
           stations = {'Scifi':{},'Mufi':{}}
           for d in event.Digi_ScifiHits:
               plane = d.GetDetectorID()//1000000
               if not plane in stations['Scifi']:stations['Scifi'][plane]=0
               stations['Scifi'][plane] +=1
           for d in event.Digi_MuFilterHits:
               plane = d.GetDetectorID()//1000
               if not plane in stations['Mufi']: stations['Mufi'][plane]=0
               stations['Mufi'][plane] +=1
           if 10 in stations['Mufi'] and 11 in stations['Mufi']:
              if stations['Mufi'][10]>0 and stations['Mufi'][11]>0: veto =  True
           if event.Digi_ScifiHits.GetEntries()>20 and veto:  flag =  True
           if flag: print(event.EventHeader.GetEventTime())
           return flag

timestamps = {}
n=-1
for event in eventTree:
      n+=1
      rc = goodEvent(event)
      if rc: timestamps[n]=event.EventHeader.GetEventTime()

t0 = timestamps[list(timestamps.keys())[0]]
for x in timestamps:
   print( "event %i  t=%5.2F"%(x, (timestamps[x]-t0)/160E6))

def timeOfFlight(p,s,m=0.105658):
    c = 299792458.
    beta = p/ROOT.TMath.Sqrt(m*m+p*p)
    tg = s/c
    tm = tg/beta
    return (tm-tg)*1E9

def firstTimeStamp(event):
        tmin = [1E9,'']
        digis = [event.Digi_MuFilterHits,event.Digi_ScifiHits]
        for digi in event.Digi_ScifiHits:
               dt = digi.GetTime()
               if dt<tmin[0]:
                    tmin[0]=dt
                    tmin[1]=digi
        for digi in event.Digi_MuFilterHits:
           for t in digi.GetAllTimes():
               dt = t.first
               if dt<tmin[0]:
                    tmin[0]=dt
                    tmin[1]=digi
        return tmin

def deltaT():
      lastT = -1
      N = 0
      for event in eventTree:
             T = event.EventHeader.GetEventTime()
             if lastT > 0:              
               dT = (T-lastT)/160.*1000.
               if dT < 20: print(N,dT)
             lastT = T
             N+=1

def mult():
        ut.bookHist(h,'scifiMult','scifi mult',100,0.,2000.)
        ut.bookHist(h,'mufiMult','mufi mult',100,0.,500.)
        for event in eventTree:
               rc=h['scifiMult'].Fill(event.Digi_ScifiHits.GetEntries())
               rc=h['mufiMult'].Fill(event.Digi_MuFilterHits.GetEntries())

def sipmMult():
        for aHit in event.Digi_MuFilterHits:
             print(aHit.GetDetectorID(),len(aHit.GetAllSignals()))

def tDiffLR(event):
        hitlist = {}
        for aHit in event.Digi_MuFilterHits:
             if aHit.GetSystem()==2:   hitlist[aHit.GetDetectorID()] = aHit.GetDeltaT()
        keys = list(hitlist.keys())
        keys.sort()
        for k in keys: print(k,hitlist[k])

def goodEvent(event):
     flag = False
     if event.Digi_MuFilterHits.GetEntries()>20 and event.Digi_ScifiHits.GetEntries()>2: flag = True
     return flag


def cosmicTracks(r=3575):
     TDC2ns = 1E9/160.E6
     f = ROOT.TFile('stracks_000'+str(r)+'.root')
     eventTree = f.rawConv
     rawEvents = ROOT.TChain('rawConv')
     for k in range(3):
            fname = 'sndsw_raw_00'+str(r)+'-000'+str(k)+'.root'
            if os.path.isfile(fname):      rawEvents.AddFile(fname)
     for event in eventTree:
            N = event.EventHeader.GetMCEntryNumber()
            rc = rawEvents.GetEvent(N)
            T0 = rawEvents.EventHeader.GetEventTime()
            rc = rawEvents.GetEvent(N+1)
            T1 = rawEvents.EventHeader.GetEventTime()
            if (T1-T0)*TDC2ns<100: 
                 print('+++ ',N,T0, (T1-T0)*TDC2ns)
                 for aHit in event.Digi_MuFilterHits:
                    print(aHit.GetDetectorID())
                    for x in aHit.GetAllSignals():
                         print(x.first,x.second)
                 print('----->    event n+1')
                 for aHit in rawEvents.Digi_MuFilterHits:
                    print(aHit.GetDetectorID())
                    for x in aHit.GetAllSignals():
                         print(x.first,x.second)


def nextTurn(N):
    T0 = eventTree.EventHeader.GetEventTime()
    for n in range(N,eventTree.GetEntries()):
        rc = eventTree.GetEvent(n)
        T = eventTree.EventHeader.GetEventTime()
        dT = (T-T0)/160.
        if dT>88.9: 
           print(n,dT,T)
           break

import json
def readConfiguration(path="."):
     f = open(path+"/configuration.json")
     jsonStr = f.read()
     j = json.loads(jsonStr)
     triggerSettings = j["daq"]["writer_settings"]["processors_settings"]["snd_fast_noise_filter"]
     # {'ds': {'n_hits_min': 3, 'n_total_hits_min': 3}, 'scifi': {'n_boards_min': 4, 'n_total_hits_min': 10}, 'us': {'n_hits_min': 7, 'n_total_hits_min': -1}}
"""
For ds and us you have two fields
- n_hits_min: minimum number of hits in a single BOARD to save an event
- n_total_hits_min: minimum number of hits in the full subsystem to save an event

for SciFi you have:
- n_boards_min: minimum number of boards with at least one hit to save an event
- n_total_hits_min: as above

all conditions are ORed
"""

def myPrint(runNumber,tc,name,subdir='',withRootFile=True):
     srun = 'run'+str(runNumber)
     tc.Update()
     pname = name+'-'+srun
     if withRootFile: tc.Print(pname+'.root')
     tc.Print(pname+'.png')
     tc.Print(pname+'.pdf')

# run 106
atlasEvents = [6959,7247]

# run 3831
atlasEvents =   [165093,168552,173128,175649,180630,183110,185575,301966,304665,307489,310259,312895,314575,317844,
 319491,321164,322868,324550,326143,327850,329509,331139,332814,334527,336188,337843,339421]
atlas2Events = [165216,168687,173270,175773,180750,183217,185680,302155,304855,307700,310453,313137,314784,318072,
 319690,321393,323106,324769,326377,328074,329738,331388,33052,334737,336391,338061,339604]
# run 3832 ?
aliceEvents =   [365240,366984,370255,372057,373835,375633,377475,379265,380994,382805]
# 43181?

def checkOrbit(splashes):
     Tprev = 0
     for N in splashes:
        rc = eventTree.GetEvent(N)
        T = eventTree.EventHeader.GetEventTime()
        if Tprev==0:
           Tprev = T
           delta = 0
        else: delta = T-Tprev
        # snd@lhc daq starts in synch with always the same LHC bunch
        test = delta % (4*3564)
        print(N,test,T%(4*3564)/4)


for x in atlasEvents:
   rc = eventTree.GetEvent(x)
   nextTurn(x)
for x in aliceEvents:
   rc = eventTree.GetEvent(x)
   nextTurn(x)

import ROOT
import rootUtils as ut
h={}
def timingPlots(r=3831):
   h['f'] = ROOT.TFile('run00'+str(r)+'.root')
   h['ctimez']  = h['f'].daq.channels.FindObject('ctimeZ').Clone('C')
   h['btime']  = h['f'].daq.channels.FindObject('btime').Clone('B')
   h['ctime']    = h['f'].daq.channels.FindObject('ctime').Clone('c')
   h['ctimem'] = h['f'].daq.channels.FindObject('ctimeM').Clone('M')
   ut.bookCanvas(h,'tc','test',1200,800,1,1)
   h['ctime'].SetStats(0)
   h['ctime'].Draw('colz')
   myPrint(r,h['tc'],"channelDeltaTsec",withRootFile=True)
   h['ctimem'].SetStats(0)
   h['ctimem'].Draw('colz')
   myPrint(r,h['tc'],"channelDeltaTms",withRootFile=True)
   h['ctimez'].SetStats(0)
   h['ctimez'].Draw('colz')
   myPrint(r,h['tc'],"channelDeltaTus",withRootFile=True)
#
   h['V'] = h['ctimez'].ProjectionX('veto',0,200)
   print(h['V'].GetBinCenter(8911))
   h['V'].GetXaxis().SetRangeUser(88,90)
   rc = h['V'].Fit('gaus','LS','',88.8,89.2)
   myPrint(r,h['tc'],"channelDeltaTVeto",withRootFile=True)
   h['DS'] = h['ctimez'].ProjectionX('DS',1200,1700)
   h['DS'].GetXaxis().SetRangeUser(88,90)
   rc =  h['DS'].Fit('gaus','LS','',88.4,89.2)
   myPrint(r,h['tc'],"channelDeltaDS",withRootFile=True)
   h['US'] = h['ctimez'].ProjectionX('US',300,1100)
   h['US'].GetXaxis().SetRangeUser(88,90)
   rc = h['US'].Fit('gaus','LS','',88.4,89.2)
   myPrint(r,h['tc'],"channelDeltaUS",withRootFile=True)
   h['V'].SetLineColor(ROOT.kRed)
   h['DS'].SetLineColor(ROOT.kBlue)
   h['US'].SetLineColor(ROOT.kGreen)
   h['V'].SetFillColor(ROOT.kRed)
   h['DS'].SetFillColor(ROOT.kBlue)
   h['US'].SetFillColor(ROOT.kGreen)
   h['V'].SetStats(0)
   h['V'].Draw('hist')
   h['US'].Draw('histsame')
   h['DS'].Draw('histsame')
   h['L'] = ROOT.TLegend(0.6,0.5,0.8,0.80)
   rc = h['L'].AddEntry(h['V'],'Veto','L')
   rc.SetTextColor(h['V'].GetLineColor())
   rc = h['L'].AddEntry(h['US'],'US','L')
   rc.SetTextColor(h['US'].GetLineColor())
   rc = h['L'].AddEntry(h['DS'],'DS','L')
   rc.SetTextColor(h['DS'].GetLineColor())
   rc = h['L'].Draw()
   myPrint(r,h['tc'],"channelDeltaAll",withRootFile=True)

twoExps = ROOT.TF1('twoEps','[0]*exp(-x*[1])+[2]*exp(-x*[3])',0,10000)



# new sipm settings and trigger
N=-1
freq      =  160.316E6
nev = 0
for event in eventTree:
   N+=1
   T= event.EventHeader.GetEventTime()/freq
   if T>110810: 
       print(N,T)
       nev+=1
   if T>110820:    break


def eventBursts():
    freq      =  160.316E6
    eventList = {}
    Tprev = -1000
    for event in eventTree:
         T = event.EventHeader.GetEventTime() / freq * 1E9
         if T-Tprev < 250:
              nscifi = eventTree.Digi_ScifiHits.GetEntries()
              nM = {1:0,2:0,3:0}
              for aHit in eventTree.Digi_MuFilterHits:
                   nM[aHit.GetDetectorID()//10000]+=1
              eventList[eventTree.GetReadEvent()-1]=[nscifi,nM[1],nM[2],nM[3]]
         Tprev = T
    categories = {}
    for i1 in range(2):
     for i2 in range(2):
      for i3 in range(2):
       for i4 in range(2):
         cat = 1000*i1+100*i2+10*i3+i4
         categories[cat] = 0
    for ev in eventList:
       cat = (eventList[ev][0]>0)*1000+(eventList[ev][1]>0)*100+(eventList[ev][2]>0)*10+(eventList[ev][3]>0)
       categories[cat] += 1
    return eventList,categories


systems = {0:'scifi',1:'Veto',2:'US',3:'DS'}
summary = {}
triggers = {0:0,1:0,2:0,3:0}
debug = False
for N in eventList:
    for i in [0,1]:
       if debug: print('---> event ',N+i)
       rc = eventTree.GetEvent(N+i)
       system = {0:[],1:[],2:[],3:[]}
       for aHit in eventTree.Digi_ScifiHits:
            detID = aHit.GetDetectorID()
            system[0].append("%i  %5.2F"%(detID,aHit.GetSignal(0) ))
       for aHit in eventTree.Digi_MuFilterHits:
             detID = aHit.GetDetectorID()
             s = detID//10000
             for x in aHit.GetAllSignals(ROOT.kFALSE,ROOT.kFALSE):
                system[s].append( "%i %i %5.2F"%(detID,x.first,x.second) )
       X = 0
       for s in systems:
          if debug: print(systems[s]+' hits:',len(system[s]))
          if len(system[s])>0: 
             X+=1
             triggers[s]+=1
             if s==0: print(N+i,len(system[0]),len(system[1]),len(system[2]),len(system[3]))
          if debug: 
           for x in system[s]:
             print(x)
       summary[N+i]=X

# for collaboration meeting
import rootUtils as ut
h={}
f = ROOT.TFile('run003831.root')
ROOT.gROOT.cd()
for x in ['Etime','EtimeZ']:
   h[x] = f.daq.T.FindObject(x).Clone(x)
   bw = h[x].GetXaxis().GetBinWidth(1)*1000
   if x=='EtimeZ': h[x].GetYaxis().SetTitle('events / %3.0Fns'%(bw))
   if x=='Etime': h[x].GetYaxis().SetTitle('events / %3.0Fms'%(bw))
ut.bookCanvas(h,'Ttime','',768,1024,1,1)
tc = h['Ttime'].cd()
tc.SetLogy(1)

tc.SetLogy(0)
for x in ['ctimeZ','btime']:
  h[x] = f.daq.channels.FindObject(x).Clone(x)
  h[x].SetStats(0)
  h[x].GetYaxis().SetTitle('Veto US DS channels                 ')
  h[x+'_x']= h[x].ProjectionX(x+'_x')
  h[x+'_x'].SetStats(0)
  if x=='ctimeZ':
      bw = h[x].GetXaxis().GetBinWidth(1)*1000
      h[x+'_x'].GetYaxis().SetTitle('events / %3.0Fns'%(bw))

ut.bookCanvas(h,'T','',1024,768,1,1)
h['splash11988']= f.daq.Tsplash.FindObject('Tsplash_13').FindObject('splash11988').Clone('splash11988')
h['splash11988'].SetTitle('; t [#mus];events per #mus')
h['USsplash11988']= f.daq.USsplash.FindObject('USsplash_13').FindObject('USsplash11988').Clone('USsplash11988')
h['DSsplash11988']= f.daq.DSsplash.FindObject('DSsplash_13').FindObject('DSsplash11988').Clone('DSsplash11988')
h['Scifisplash11988']= f.daq.Scifisplash.FindObject('Scifisplash_13').FindObject('Scifisplash11988').Clone('Scifisplash11988')
h['Vetosplash11988']= f.daq.Vetosplash.FindObject('Vetosplash_13').FindObject('Vetosplash11988').Clone('Vetosplash11988')
for s in ['US','Veto','DS','Scifi']:
      h[s+'splash11988'].GetXaxis().SetRange(630800,632000)
      h[s+'splash11988'].SetMarkerStyle(21)
      h[s+'splash11988'].SetStats(0)

