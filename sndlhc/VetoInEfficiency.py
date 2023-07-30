import ROOT
import os
import time,calendar
import rootUtils as ut
h={}
year = 2023
runs = {}
if year == 2022:
 runs = [5389,5408,5125,5396,5350,5399,5263,5377,5262,5259,5257,5253,5171,5159,5157,5154,5133,5132,5130,5122,5152,   # runs with prevTime  --> 6001 
5059,5120,5154,5170,5180,5236,5239,5036,5044,5056,
                        4572,4595,4617,4626,4612,4639,4661,4649,4724,4744,4758,4769,4815,4958,4964,4971,4976,4980,4990,5000,5005,5013,5024,5059,5094,5109]
else:
 runs =[6018,6042,6069,6121,6208,6215,6223,6226,6233,6264,6268,6273,6568,6574,6577,6593,6590,6596,6598,6605,6610,6622]

runs.sort()

# right side of plane 1 off: 5180, 5236, 5239, 5241
region = [22,92,22,83] # region = [21,91,34,89] # value from neutrino analysis?

#  0------1
#  --------
#  2------3
border = {0: {0:[-6.45325, 56.47542+3],1:[-48.45232, 56.19794+3],2:[-6.21519, 20.44299-3],3:[-48.21427, 20.16551-3]},
          1: {0:[-6.41871, 54.27478+3],1:[-48.41778, 53.99731+3],2:[-6.18065, 18.24235-3],3:[-48.17973, 17.96487-3]}} 

for sRef in range(2):
   h['TlineTop'+str(sRef)] = ROOT.TLine(border[sRef][0][0],border[sRef][0][1],border[sRef][1][0],border[sRef][1][1])
   h['TlineBot'+str(sRef)] = ROOT.TLine(border[sRef][2][0],border[sRef][2][1],border[sRef][3][0],border[sRef][3][1])
   h['TlineLef'+str(sRef)] = ROOT.TLine(border[sRef][2][0],border[sRef][2][1],border[sRef][0][0],border[sRef][0][1])
   h['TlineRig'+str(sRef)] = ROOT.TLine(border[sRef][3][0],border[sRef][3][1],border[sRef][1][0],border[sRef][1][1])
   for x in ['TlineTop'+str(sRef),'TlineBot'+str(sRef),'TlineLef'+str(sRef),'TlineRig'+str(sRef)]:
      h[x].SetLineWidth(2)
      h[x].SetLineColor(ROOT.kGreen)

''' list of events with no prev and no veto hits:
5408 4432851 mu=52
5408-event_56475214.png         0 sipms
5408-event_39520055.png -244    3 sipms at right place

5396 8644450 mu=44
5396-event_38759010.png  1 hit, 2 sipms at correct place
5396-event_40039412.png -180    0 sipms
5396-event_43110827.png -21940  0 sipms
5396-event_27432284.png -143774    0 sipms, 2 hits, 2 sipms at wrong place
5396-event_12296221.png 4cc later, event with missing Veto hits   2 hits 4 sipms, 1 hit at right place
5396-event_116661861.png  0 sipm  1 sipm at wrong place
5396-event_151729697.png 4cc later, event with missing Veto hits, prev event 265  0 sipms
5396-event_135090194.png 4cc later, event with missing Veto hits, 3 hits 7 channels, some at wrong place
5396-event_66313266.png  0 sipms
5396-event_84928154.png  0 sipms
5396-event_16704157.png  0 sipms

5125 7535931 mu=43
5125-event_6816028.png 7 events within 600 ns, event -7 looks like muon DIS, large QDC in Veto, many scifi hits in first station, 1 hit 2 sipms
5125-event_157147538.png 110 cc prev event  1 hit 1 sipm at right place

5263 5413742 mu=53
5263-event_34182496.png   1 hit, 1 sipm at correct place
5263-event_101650598.png  0 sipm
5263-event_90734532.png    1 hit, 3 sipm at correct place
5263-event_35847804.png    0 sipm
5263-event_5038083.png    1 hit 1 sipm at wrong place, 0 sipm matching
5263-event_17068451.png   1 hit 1 sipm at wrong place, 0 sipm matching
5263-event_74306146.png 197 cc prev event with veto hits, 44 cc later but mot relevant  0 sipm. 2 hits at wrong place

5350 7873294 mu=52
5350-event_115837036.png no prev but 20cc later event with many veto hits and nothing else  0 sipm
5350-event_23022923.png 10 events before, 848 cc, large activity in Veto, followed by many events with only veto hits  2 hits, 6 sipms at correct place
5350-event_55077814.png   1 hit, sipm at correct place
5350-event_39311734.png    ???  0 sipm
5350-event_61708157.png 104 cc prev event with veto hits, and 4cc later  1 sipm at correct place
5350-event_15005139.png   0 sipm
5350-event_30321940.png   1 sipm at correct place
5350-event_94108104.png   0 siom
5350-event_30972697.png   0 sipm

5377 5228076 mu=50
5377-event_90154981.png 6 events earlier, 196 cc, DIS event, lot of activity. 2 hits, 4 sipm at correct place
5377-event_36710391.png 7 events earlier, 208 cc, DIS event, lot of activity. 1 hit 5 sipm at correct place
5377-event_72750542.png 1 hit, 4 sipm at correct place
5377-event_105644361.png 4 cc later, missing veto hits appear, 0 siom

5399 5893020 mu=52
5399-event_42996523.png 0 sipm
5399-event_84194037.png 0 sipm

5389 4064773 mu=53
5389 fully efficient

5257-event_69593580.png  0 sipm
5257-event_42094088.png  0 sipm
5257-event_90351349.png  164 cc before DIS event many veto hits, 6 events following, 1 hit 5 sipm at correct place
5257-event_22284546.png   0 sipm
5257-event_50217932.png  209 cc, and 3 events earlier DIS, 4 cc later missing veto hits. 1 hit 1 sipm at correct place
5257-event_137444202.png  0 sipm 

5253-event_132547458.png  0 sipm
5253-event_117919731.png  0 sipm
5253-event_22352088.png  24 events earlier, 880 cc, heavy DIS 5253-event_22352064.png  event before DIS 74312 cc, 2 hits 5 sipm at correct place
5253-event_23340641.png   -944cc earlier DIS followed by 8 events with veto hits, 1 hit 5 sipm at correct place
5253-event_43043099.png  1 hit, 1 sipm at correct place
5253-event_94586745.png  1 hit 4 sipm

5262-event_50673466.png  0 sipm
5262-event_67319215.png  0 sipm
5262-event_83011110.png  0 sipm
5262-event_41597921.png  700cc earlier, 13 events earlier, DIS event, followed by veto only events  2 hits, 2 sipm at correct place

5259-event_33225154.png 0 sipm
5259-event_97802554.png veto hits appear 4cc later  0 sipm
5259-event_5981041.png   1 hit 2 sipm at correct place
5259-event_61021708.png 0 sipm
5259-event_82871073.png  4 cc later veto hits appear, 4 events before, 137 cc, some DIS  0 sipm 1 sipm at wrong place

58 events of 68282052: 8.5 E-7
total 58

>1000cc: 41
>100cc:  17
larger deadtime: 17
veto hits in next event, 4cc: 6
no explanation: 35   
'''

import subprocess,time
runsWithEventDisplays = [5125,5253, 5257, 5259, 5262, 5263, 5350, 5377, 5389, 5396, 5399, 5408]

def updateFigures():
   path = '/mnt/hgfs/microDisk/SND@LHC/Analysis Notes/VetoInefficiency - 2023/'
   listOfFigures = []
   for X in [path+"introduction.tex"]:
    t = open(X)
    for l in t.readlines():
      if l.find('figs/')<0: continue
      for x in l.split('figs/'):
         for ex in ['.pdf','.png']:
            if x.find(ex)<0: continue
            k = x.find(ex)+4
            listOfFigures.append(x[:k])
    t.close()
   for p in listOfFigures:
     if not p.find('eventsRun')<0: continue
     if os.path.isfile(path+"figs/"+p):
       print("%30s :  %25s, %25s"%(p,time.ctime(os.path.getmtime(p)), time.ctime(os.path.getmtime(path+"figs/"+p)) ) )
     os.system('cp '+p+' '+path.replace(' ','\ ')+'figs/')
   for p in listOfFigures:
      if p.find('-event')>0: os.system('cp '+p+' '+path.replace(' ','\ ')+'figs/')

def lowUpLimit(p,n):
      return [0.5*ROOT.TMath.ChisquareQuantile((1-p),2*n),0.5*ROOT.TMath.ChisquareQuantile(p,2*(n+1))]
def printInEffasFuncOfDate(noise=5,sel='NoPrev',p=0.9):
   for r in stats:
      t = stats[r][sel][noise]['date']
      inEff = stats[r][sel][noise]['OR'][0]
      einEff = stats[r][sel][noise]['OR'][1]
      Nr = stats[r][sel][noise]['Ntot_r']
      NinEff = inEff*Nr
      cL = lowUpLimit(p,NinEff)
      print("%i %s  %5.2F+/- [%5.2F,%5.2F] 1E-6  %i"%(r,time.ctime(t),cL[0]/Nr*1E6,cL[1]/Nr*1E6,einEff*1E6,NinEff))

def printNrOFEvents(runs,i='OR',noiseCut=5,c='NoPrev',p=0.9):
    for r in runs:
              inEff  = stats[r][c][noiseCut][i][0]
              Nr     = stats[r][c][noiseCut]['Ntot_r']
              NinEff = inEff*Nr
              cL = lowUpLimit(p,NinEff)
              print(r,':',NinEff,stats[r][c][noiseCut][i],cL[0]/Nr,cL[1]/Nr)

CB = {}
def makeEventDisplays():
  global eventTree
  F=open("/media/truf/SND/trufatwork/sndlhc/VetoInEfficiency.py")
  CB['eventList'] = {}
  CB['partitions'] = {}
  eventList = CB['eventList']
  partitions = CB['partitions']
  for l in F.readlines():
    if l.find('makeEventDisplays')>0: break
    if not l.find('-event_')>0: continue
    r = int(l[:4])
    if not r in eventList: eventList[r]=[]
    v = int(l.split('_')[1].split('.')[0])
    eventList[r].append(v)
  for r in eventList: eventList[r].sort()
  for r in eventList:
        partitions[r]=[]
        dirlist  = str( subprocess.check_output("xrdfs "+os.environ['EOSSHIP']+" ls /eos/experiment/sndlhc/convertedData/physics/2022/run_"+str(r).zfill(6),shell=True))
        for x in dirlist.split('\\n'):
              ix = x.find('sndsw_raw-')
              if ix<0: continue
              partitions[r].append(x[ix:])
  for r in partitions: print(r,len(partitions[r]))
  for r in eventList:
        if len(eventList[r])<1: continue
        path = os.environ['EOSSHIP']+"/eos/experiment/sndlhc/convertedData/physics/2022/run_"+str(r).zfill(6)
        eventTree=ROOT.TChain('rawConv')
        for p in partitions[r]:
           eventTree.AddFile(path+'/'+p)
        loopEvents(start=eventList[r],auto=True)

def makeDISEventDisplays(l = "5125-event_6816028.png",prev=8):
  global eventTree
  F=open("/media/truf/SND/trufatwork/sndlhc/VetoInEfficiency.py")
  CB['eventList'] = {}
  CB['partitions'] = {}
  eventList = CB['eventList']
  partitions = CB['partitions']
  r = int(l[:4])
  if not r in eventList: eventList[r]=[]
  v = int(l.split('_')[1].split('.')[0])
  eventList[r].append(v)
  for i in range(1,prev+1):  eventList[r].append(v-i)
  for r in eventList: eventList[r].sort()
  for r in eventList:
        partitions[r]=[]
        dirlist  = str( subprocess.check_output("xrdfs "+os.environ['EOSSHIP']+" ls /eos/experiment/sndlhc/convertedData/physics/2022/run_"+str(r).zfill(6),shell=True))
        for x in dirlist.split('\\n'):
              ix = x.find('sndsw_raw-')
              if ix<0: continue
              partitions[r].append(x[ix:])
  for r in eventList:
        if len(eventList[r])<1: continue
        path = os.environ['EOSSHIP']+"/eos/experiment/sndlhc/convertedData/physics/2022/run_"+str(r).zfill(6)
        eventTree=ROOT.TChain('rawConv')
        for p in partitions[r]:
           eventTree.AddFile(path+'/'+p)
        loopEvents(start=eventList[r],auto=True)
  
def makeEventLatex():
  f=open('eventPictures.tex','w')
  collection = {}
  p = 0
  collection[p]=[]
  for r in CB['eventList']:
   for E in CB['eventList'][r]:
     collection[p].append(str(r)+'-event_'+str(E)+'.png')
     if len(collection[p])==4: 
       p+=1
       collection[p]=[]
  for p in collection:
       f.write("\\begin{figure}[ht]\n")
       f.write("\\centering\n")
       tmp = ''
       for i in range(len(collection[p])):
          os.system('cp '+collection[p][i]+ ' /mnt/hgfs/microDisk/SND@LHC/Analysis\ Notes/VetoInefficiency/figs/ ')
          tmp+="\\includegraphics[width=0.40\\textwidth]{figs/"+collection[p][i]+"}"
          if i%2==1:
             f.write(tmp+"\n")
             tmp=''
       if i<3: f.write(tmp+"\n")
       f.write("\\caption{Inefficient events.}\n")
       f.write("\\label{fig:evDisp"+str(p)+"}\n")
       f.write("\\end{figure}\n")
  f.close()
  os.system('cp eventPictures.tex /mnt/hgfs/microDisk/SND@LHC/Analysis\ Notes/VetoInefficiency/ ')

def checkStatsPerRun(runs,nc=5):
   N = 0
   for r in runs:
     h.clear()
     ut.readHists(h,'noBackward/allHistos-run'+str(r).zfill(6)+'.root')
     Ntot = h['TNoPrev'+str(nc)+'PosVeto_1'].Clone('Ntot')
     Ntot.Add(h['TNoPrev'+str(nc)+'XPosVeto_1'])
     Ntot_r = Ntot.Integral(region[0],region[1],region[2],region[3])
     N += Ntot_r
     print('run ',r,Ntot_r)
   return N

def sumOfhistos(runs,newRun=6001):
   cmd = "hadd -f allHistos-run"+str(newRun).zfill(6)+'.root '
   for r in runs:
       cmd += " noBackward/allHistos-run00XXXX.root".replace('XXXX',str(r))
   os.system(cmd)
def sumOfhistos2(runs,newRun=6002):
   cmd = "hadd -f allHistos-run"+str(newRun).zfill(6)+'.root '
   for r in runs:
       if r==5170: continue
       if r<5125: continue
       cmd += " noBackward/allHistos-run00XXXX.root".replace('XXXX',str(r))
   os.system(cmd)
   
def printoutEvdisplay(r):
   eventTree.GetEvent(r)
   T0 = eventTree.EventHeader.GetEventTime()
   eventTree.GetEvent(r-1)
   delTM1 = eventTree.EventHeader.GetEventTime() - T0
   eventTree.GetEvent(r+1)
   delTP1 = eventTree.EventHeader.GetEventTime() - T0
   print('delta T',delTM1,delTP1)
   loopEvents(start=r)

def triggerConf():
   open('configuration.json')
   C = f.readlines()
   cx = eval('C[0]')
   fast_noise_filter = cx['daq']['writer_settings']['processors_settings']['snd_fast_noise_filter']
   for decision in fast_noise_filter:
         print(decision,fast_noise_filter[decision])
   adv_noise_filter = cx['daq']['writer_settings']['processors_settings']['snd_advanced_noise_filter']
   for decision in adv_noise_filter:
         print(decision,adv_noise_filter[decision])
         
         
def getRateOfVetoOnly():
   N_vetOnlyEvents = 0
   N_vetoEvents = 0
   for event in eventTree:
     decisions = []
     for x in eventTree.EventHeader.GetPassedAdvNFCriteria():
        decisions.append(x)
     if 'VETO_Planes' in decisions: N_vetoEvents+=1
     if len(decisions)>1: continue
     if not 'VETO_Planes' in decisions: continue
     N_vetOnlyEvents+=1
   rc = eventTree.GetEvent(0)
   T0 = eventTree.EventHeader.GetEventTime()
   rc = eventTree.GetEvent(eventTree.GetEntries()-1)
   TL = eventTree.EventHeader.GetEventTime()
   timeD = (TL-T0)*6.25/1E9
   print(eventTree.GetEntries(),N_vetOnlyEvents,N_vetOnlyEvents/eventTree.GetEntries(),timeD,N_vetOnlyEvents/timeD)
   print(eventTree.GetEntries(),N_vetoEvents,N_vetoEvents/eventTree.GetEntries(),timeD,N_vetoEvents/timeD)

def timeDiffPrevNextEvent(r=6001,path='noBackward/'):
   if not r in h: h[r]={}
   ut.readHists(h[r],path+'allHistos-run00'+str(r)+'.root')
   ut.bookCanvas(h,'TtimeDiff','',900,600,1,1)
   colors = {'timeDiffPrev_5':[ROOT.kMagenta,22],'XtimeDiffPrev_5':[ROOT.kRed,23]}
   for c in ['timeDiffPrev_5','XtimeDiffPrev_5']:
     h[r][c+'norm'] = h[r][c].Clone(c+'norm')
     h[r][c+'norm'].Scale(1./h[r][c].GetSumOfWeights())
     h[r][c+'norm'].SetStats(0)
     h[r][c+'norm'].SetMinimum(0)
     h[r][c+'norm'].SetMarkerColor(colors[c][0])
     h[r][c+'norm'].SetMarkerStyle(colors[c][1])
     h[r][c+'norm'].SetTitle(';clock cycles; arb. units')
   h[r]['timeDiffPrev_5norm'].Scale(10)
   h[r]['XtimeDiffPrev_5norm'].Draw()
   h[r]['timeDiffPrev_5norm'].Draw('same')
   h[r]['ltimeDiffPrev']=ROOT.TLegend(0.42,0.66,0.88,0.88)
   X = h[r]['ltimeDiffPrev'].AddEntry(h[r]['timeDiffPrev_5norm'],'all events',"LP")
   X.SetTextColor(colors['timeDiffPrev_5'][0])
   X = h[r]['ltimeDiffPrev'].AddEntry(h[r]['XtimeDiffPrev_5norm'],'events with inefficient Veto',"LP")
   X.SetTextColor(colors['XtimeDiffPrev_5'][0])
   h[r]['ltimeDiffPrev'].Draw()
   myPrint(h['TtimeDiff'],'timeDiffPrev_'+str(r))

from rootpyPickler import Unpickler
from rootpyPickler import Pickler
fg  = ROOT.TFile.Open(os.environ['EOSSHIP']+"/eos/experiment/sndlhc/convertedData/physics/"+str(year)+"/RunInfodict.root")
pkl = Unpickler(fg)
runInfo = pkl.load('runInfo')
fg.Close()

for rspecial in [1000,1001,1002,1003,1013,1023,6000,6001,6002]:
 runInfo[rspecial]={}
 runInfo[rspecial]['muAv']={}
 runInfo[rspecial]['muAv']['']=50
 runInfo[rspecial]['StartTime']=0

def myPrint(tc,outName):
   tc.Update()
   for t in ['.root','.png','.pdf']:
      tc.Print(outName+t)

def makePlotsForNote(r=5125,xname='noBackward/allHistos-run00XXXX.root'):
# 5125 after fixing time delay and noise filter
# 5120 after fixing time delay but still without veto in noise filter
# 4626 with doT1 6ns
# 4744 with doT1 3ns

     vetoEfficiency(runs=[r],v='',name=xname,noiseCuts = [1,5,10,12])
     hr = h[r]['']
     ut.bookCanvas(hr,'ThitVeto','',900,600,1,1)
     tc = hr['ThitVeto'].cd()
     tc.SetLogy(1)
     hr['hitVeto_X'].GetYaxis().SetTitle("N events")
     hr['hitVeto_X'].GetXaxis().SetTitle("N sipm channels firing per plane")
     hr['hitVeto_X'].SetLineWidth(2)
     hr['hitVeto_Y'].SetLineWidth(2)
     hr['hitVeto_X'].Draw('hist')
     hr['hitVeto_Y'].Draw('histsame')
     hr['lhitVeto']=ROOT.TLegend(0.72,0.77,0.99,0.93)
     hr['lhitVeto'].AddEntry(hr['hitVeto_X'],'plane 0',"L")
     hr['lhitVeto'].AddEntry(hr['hitVeto_Y'],'plane 1',"L")
     hr['lhitVeto'].Draw()
     myPrint(hr['ThitVeto'],'VetoChannelMult_'+str(r))

     ut.bookCanvas(hr,'TdeltaT','',900,600,1,1)
     tc = hr['TdeltaT'].cd()
     tc.SetLogy(1)
     hr['deltaT'].SetStats(0)
     hr['deltaT'].GetXaxis().SetTitle('#Deltat [ns]')
     hr['deltaT'].GetYaxis().SetTitle('dN/0.4ns')
     hr['deltaT'].Draw()
     myPrint(hr['TdeltaT'],'deltaTScifiDS_'+str(r))
     
     ut.bookCanvas(hr,'TX/Y','',900,600,1,1)
     tc = hr['TX/Y'].cd()
     tc.SetLogz(1)
     hr['X/Y'].SetStats(0)
     hr['X/Y'].GetXaxis().SetTitle('#DeltaX [cm]')
     hr['X/Y'].GetYaxis().SetTitle('#DeltaY [cm]')
     hr['X/Y'].Draw('colz')
     myPrint(hr['TX/Y'],'deltaXYScifiDS_'+str(r))

     b=''
     noiseCuts = [1,5,10,12]
     ut.bookCanvas(hr,'TPosVeto','',900,600,1,1)
     tc = hr['TPosVeto'].cd()
     c = 'NoPrev'
     allTracks = hr['T'+c+'1PosVeto_0'].Clone('tmp')
     allTracks.Add(hr['T'+c+'1XPosVeto_0'])
     allTracks.SetTitle('')
     allTracks.Draw('colz')
     myPrint(hr['TPosVeto'],'PosVeto_0_'+str(r))
     xax = allTracks.GetXaxis()
     yax = allTracks.GetYaxis()
     hr['tlineB'] = ROOT.TLine(xax.GetBinCenter(region[0]),yax.GetBinCenter(region[2]),xax.GetBinCenter(region[1]),yax.GetBinCenter(region[2]))
     hr['tlineT'] = ROOT.TLine(xax.GetBinCenter(region[0]),yax.GetBinCenter(region[3]),xax.GetBinCenter(region[1]),yax.GetBinCenter(region[3]))
     hr['tlineL'] = ROOT.TLine(xax.GetBinCenter(region[0]),yax.GetBinCenter(region[2]),xax.GetBinCenter(region[0]),yax.GetBinCenter(region[3]))
     hr['tlineR'] = ROOT.TLine(xax.GetBinCenter(region[1]),yax.GetBinCenter(region[2]),xax.GetBinCenter(region[1]),yax.GetBinCenter(region[3]))
     Marker = {'0':[22,ROOT.kMagenta],'1':[23,ROOT.kBlue],'11':[72,ROOT.kGreen],'10':[22,ROOT.kCyan],'01':[23,ROOT.kRed]}
     for nc in ['5','12']:
       for x in ['','X']:
         for p in ['0','1','11','01','10']:
           if x=='' and p in ['01','10']: 
               continue
           else:
               projY = 'T'+c+str(nc)+x+'PosVeto_'+p+'Y' 
               hr[projY] = hr['T'+c+str(nc)+x+'PosVeto_'+p].ProjectionY(projY)
               projX = 'T'+c+str(nc)+x+'PosVeto_'+p+'X' 
               hr[projX] = hr['T'+c+str(nc)+x+'PosVeto_'+p].ProjectionX(projX)
           hr[projY].Reset()
           hr[projX].Reset()
           for iy in range(region[2],region[3]):
             N = 0
             for ix in range(region[0],region[1]):
                N+=hr['T'+c+str(nc)+x+'PosVeto_'+p].GetBinContent(ix,iy)
             hr[projY].SetBinContent(iy,N)
           for ix in range(region[0],region[1]):
             N = 0
             for iy in range(region[2],region[3]):
                N+=hr['T'+c+str(nc)+x+'PosVeto_'+p].GetBinContent(ix,iy)
             hr[projX].SetBinContent(ix,N)
             
       for p in ['0','1','11','01','10','11']:
          hr['eff'+c+str(nc)+'PosVeto_'+p+'Y']=hr['T'+c+str(nc)+'XPosVeto_'+p+'Y'].Clone( 'eff'+c+str(nc)+'PosVeto_'+p+'Y')
          hr['eff'+c+str(nc)+'PosVeto_'+p+'X']=hr['T'+c+str(nc)+'XPosVeto_'+p+'X'].Clone( 'eff'+c+str(nc)+'PosVeto_'+p+'X')
          if p in ['01','10']:
             if p=='10':  hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].Divide(hr['T'+c+str(nc)+'PosVeto_0Y'])
             if p=='01':  hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].Divide(hr['T'+c+str(nc)+'PosVeto_1Y'])
          else:
             hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].Divide(hr['T'+c+str(nc)+'PosVeto_'+p+'Y'])
             hr['eff'+c+str(nc)+'PosVeto_'+p+'X'].Divide(hr['T'+c+str(nc)+'PosVeto_'+p+'X'])
          hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].SetStats(0)
          hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].SetTitle('')
          hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].SetLineColor(Marker[p][1])
          hr['eff'+c+str(nc)+'PosVeto_'+p+'X'].SetStats(0)
          hr['eff'+c+str(nc)+'PosVeto_'+p+'X'].SetTitle('')
          hr['eff'+c+str(nc)+'PosVeto_'+p+'X'].SetLineColor(Marker[p][1])
       hr['TPosVeto'].SetLogy(1)
       nmax = [hr['eff'+c+str(nc)+'PosVeto_0Y'].GetMaximum(),hr['eff'+c+str(nc)+'PosVeto_1Y'].GetMaximum()]
       nmax.reverse()
       hr['eff'+c+str(nc)+'PosVeto_11Y'].SetMaximum(1.1*nmax[0])
       hr['eff'+c+str(nc)+'PosVeto_11Y'].Draw()
       hr['eff'+c+str(nc)+'PosVeto_0Y'].Draw('same')
       hr['eff'+c+str(nc)+'PosVeto_1Y'].Draw('same')
       h['leff']=ROOT.TLegend(0.71,0.59,0.88,0.88)
       X = h['leff'].AddEntry(hr['eff'+c+str(nc)+'PosVeto_0Y'],'plane 0 ',"LP")
       X.SetTextColor(Marker['0'][1])
       X = h['leff'].AddEntry(hr['eff'+c+str(nc)+'PosVeto_1Y'],'plane 1 ',"LP")
       X.SetTextColor(Marker['1'][1])
       X = h['leff'].AddEntry(hr['eff'+c+str(nc)+'PosVeto_11Y'],'detector ',"LP")
       X.SetTextColor(Marker['11'][1])
       h['leff'].Draw()
       myPrint(hr['TPosVeto'],'VetoInEffvsY_'+str(nc)+'_'+str(r))
#
       hr['TPosVeto'].SetLogy(0)
       nmax = [hr['eff'+c+str(nc)+'PosVeto_0X'].GetMaximum(),hr['eff'+c+str(nc)+'PosVeto_1X'].GetMaximum()]
       nmax.reverse()
       hr['eff'+c+str(nc)+'PosVeto_0X'].SetMaximum(1.1*nmax[0])
       hr['eff'+c+str(nc)+'PosVeto_0X'].Draw()
       hr['eff'+c+str(nc)+'PosVeto_1X'].Draw('same')
       h['leffX']=ROOT.TLegend(0.71,0.59,0.88,0.88)
       X = h['leffX'].AddEntry(hr['eff'+c+str(nc)+'PosVeto_0X'],'plane 0 ',"LP")
       X.SetTextColor(Marker['0'][1])
       X = h['leffX'].AddEntry(hr['eff'+c+str(nc)+'PosVeto_1X'],'plane 1 ',"LP")
       X.SetTextColor(Marker['1'][1])
       h['leffX'].Draw()
       myPrint(hr['TPosVeto'],'VetoInEffvsX_'+str(nc)+'_'+str(r))

     hr['TPosVeto'].SetLogy(0)
     c = 'NoPrev'
     for nc in ['5','12']:
          h['leff']=ROOT.TLegend(0.71,0.59,0.88,0.88)
          hr['eff'+c+str(nc)+'PosVeto_01Y'].SetMinimum()
          hr['eff'+c+str(nc)+'PosVeto_01Y'].Draw()
          hr['eff'+c+str(nc)+'PosVeto_10Y'].Draw('same')
          X = h['leff'].AddEntry(hr['eff'+c+str(nc)+'PosVeto_01Y'],'plane 0 if plane 1 fired',"LP")
          X.SetTextColor(Marker['01'][1])
          X = h['leff'].AddEntry(hr['eff'+c+str(nc)+'PosVeto_10Y'],'plane 1 if plane 0 fired',"LP")
          X.SetTextColor(Marker['10'][1])
          h['leff'].Draw()
          myPrint(hr['TPosVeto'],'VetoInEffPlanevsY_'+str(nc)+'_'+str(r))

     for nc in ['5','12']:
      for p in range(2):
       hr['T'+c+str(nc)+'XPosVeto_'+str(p)].SetTitle('')
       hr['T'+c+str(nc)+'XPosVeto_'+str(p)].Draw('colz')
       for l in ['B','T','L','R']:
           hr['tline'+l].SetLineColor(ROOT.kRed)
           hr['tline'+l].SetLineWidth(2)
           hr['tline'+l].Draw('same')
       for x in ['TlineTop'+str(p),'TlineBot'+str(p),'TlineLef'+str(p),'TlineRig'+str(p)]: h[x].Draw('same')
           
       myPrint(hr['TPosVeto'],'NoHitPosVeto_'+str(nc)+str(p)+'_'+str(r))
     flatex = open('table-'+str(r)+'.tex','w')
     for c in ['all','','NoPrev']:
        prev = stats[r][''][5]['trackPerEvent']/100
        eprev = int(ROOT.TMath.Log10(prev)-1)
        # if c=='': line = "\\multicolumn{4}{|c|}{With previous event, $%5.2F \\times 10^{%i}$ of the events}\\\\ \n"%(prev/10**eprev,eprev)
        if c=='': line = "\\multicolumn{4}{|c|}{With previous event, $%5.2F%% of the events}\\\\ \n"%(prev*100)
        elif c=='all':    line = "\\multicolumn{4}{|c|}{}\\\\ \n"
        else:    line = "\\multicolumn{4}{|c|}{No previous event}\\\\ \n"
        flatex.write(line)
        for noiseCut in stats[r][c]:
           val = stats[r][c][noiseCut]
       # $N_{hits}< & no Veto 0 & no Veto 1 & no Veto 0 and no Veto 1  
           e={}
           confInterval = {}
           for i in ['plane0','plane1','OR']:
              e[i] = -6
              if val['OR'][0]>0: e[i]=int(ROOT.TMath.Log10(val['OR'][0])-1)
              inEff  = stats[r][c][noiseCut][i][0]
              Nr     = stats[r][c][noiseCut]['Ntot_r']
              NinEff = inEff*Nr
              cL = lowUpLimit(0.9,NinEff)
              confInterval[i] = [cL[0]/Nr,cL[1]/Nr]

           line = "$%i$ & $(%5.2F \pm %5.2F)\\times 10^{%i}$ &  $(%5.2F \pm %5.2F)\\times 10^{%i}$ &  $(%5.2F [-%5.2F, +%5.2F])\\times 10^{%i}$ \\\\ \n"%(noiseCut,
              val['plane0'][0]/10**e['plane0'],val['plane0'][1]/10**e['plane0'],e['plane0'],val['plane1'][0]/10**e['plane1'],val['plane1'][1]/10**e['plane1'],e['plane1'],
              val['OR'][0]/10**e['OR'],confInterval['OR'][0]/10**e['OR'],confInterval['OR'][1]/10**e['OR'],e['OR'])
           flatex.write(line)
     flatex.write('--- single plane ineff\n')
     for c in ['all','','NoPrev']:
     # single plane inefficiencies if other plane has fired
      for noiseCut in stats[r][c]:
           val = stats[r][c][noiseCut]
       # $N_{hits}< & no Veto 0 & no Veto 1 & no Veto 0 and no Veto 1  
           e={}
           for i in ['plane10','plane01']:
              e[i] = -7
              if val[i][0]>0: e[i]=int(ROOT.TMath.Log10(val[i][0])-1)
           line = "$%i$ & $(%5.2F \pm %5.2F)\\times 10^{%i}$ &  $(%5.2F \pm %5.2F)\\times 10^{%i}$ \\\\ \n"%(noiseCut,
              val['plane10'][0]/10**e['plane10'],val['plane10'][1]/10**e['plane10'],e['plane10'],
              val['plane01'][0]/10**e['plane01'],val['plane01'][1]/10**e['plane01'],e['plane01'])
           flatex.write(line)
     flatex.close()

def boardSyncPlots():
   first  = 4572
   before = 4964
   after  = 5125
   www = os.environ['EOSSHIP']+"/eos/experiment/sndlhc/www/"
   ut.bookCanvas(h,'TC','',1200,900,1,1)
   h['TC'].cd()
   for r in [first,before,after]:
     R = ROOT.TFile.Open(www+"offline/run"+str(r).zfill(6)+".root")
     ROOT.gROOT.cd()
     bCanvas = R.daq.Get('boards')
     h['Tboard_'+str(r)] = bCanvas.FindObject('Tboard').Clone('Tboard_'+str(r))
     h['Tboard_'+str(r)].SetStats(0)
     h['Tboard_veto_'+str(r)] = h['Tboard_'+str(r)].Clone('Tboard_veto_'+str(r))
     h['Tboard_US12_'+str(r)] = h['Tboard_'+str(r)].Clone('Tboard_US12_'+str(r))
     xAx = h['Tboard_'+str(r)].GetXaxis()
     yAx = h['Tboard_'+str(r)].GetYaxis()
     for k in range(xAx.GetNbins()):
        if not 58==xAx.GetBinCenter(k+1):
           for m in range(yAx.GetNbins()): h['Tboard_veto_'+str(r)].SetBinContent(k+1,m+1,0)
        if not 7==xAx.GetBinCenter(k+1):
           for m in range(yAx.GetNbins()): h['Tboard_US12_'+str(r)].SetBinContent(k+1,m+1,0)
     h['Tboard_veto_'+str(r)].SetLineColor(ROOT.kRed)
     h['Tboard_US12_'+str(r)].SetLineColor(ROOT.kOrange)
     h['Tboard_'+str(r)].Draw('box')
     h['Tboard_veto_'+str(r)].Draw('boxsame')
     h['Tboard_US12_'+str(r)].Draw('boxsame')
     myPrint(h['TC'],'Tboard_'+str(r))

def eventDisplays():
   # run 4964 249352 and 3
   # run 5119 465355 and 6
     a=1
def checkPrevEvent(evtlist=[115837036,53699368,23022923,55077814,39311734,61708157, 15005139,30321940,94108104,30972697]):
   for n in evtlist:
     rc = eventTree.GetEvent(n)
     T0 = eventTree.EventHeader.GetEventTime()
     rc = eventTree.GetEvent(n-1)
     print ("T0-T=",n,T0-eventTree.EventHeader.GetEventTime())

stats = {}
timeRange = {}
def printVetoEff(noiseCut=[5],n='noBackward/allHistos-run00XXXX.root',sel='NoPrev',prob=0.9):
 vetoEfficiency(runs,v='',name=n,noiseCuts = noiseCut)
 for nc in noiseCut:
  for r in stats:
     Nr = stats[r][sel][nc]['Ntot_r']
     inEffOr = stats[r][sel][nc]['OR'][0]
     tmp = lowUpLimit(prob,inEffOr*Nr)
     cLOR = [ (inEffOr*Nr-tmp[0])/Nr,(tmp[1]-inEffOr*Nr)/Nr ]
     inEff0 = stats[r][sel][nc]['plane0'][0]
     tmp = lowUpLimit(prob,inEff0*Nr)
     cL0 =  [ (inEff0*Nr-tmp[0])/Nr,(tmp[1]-inEff0*Nr)/Nr ]
     inEff1 = stats[r][sel][nc]['plane1'][0]
     tmp = lowUpLimit(prob,inEff1*Nr)
     cL1 =  [ (inEff1*Nr-tmp[0])/Nr,(tmp[1]-inEff1*Nr)/Nr ]
     timeRange[stats[r][sel][nc]['date']] = [inEffOr,cLOR,inEff0,cL0,inEff1,cL1]
  T = list(timeRange.keys())
  T.sort()
  tstart = T[0]
  tend = T[len(T)-1]
  Marker = {'p0':[22,ROOT.kMagenta],'p1':[23,ROOT.kBlue],'':[72,ROOT.kGreen]}
  for p in Marker:
    evolnc = p+'evol'+str(nc)
    h[evolnc] = ROOT.TGraphAsymmErrors()
    h[evolnc].SetLineWidth(2)
    h[evolnc].SetMarkerStyle(Marker[p][0])
    h[evolnc].SetMarkerColor(Marker[p][1])
    h[evolnc].SetMarkerSize(2)
    n = 0
    for t in T:
      k=0
      if p=='p0': k = 2
      if p=='p1': k = 4
      if p=='':
         h[evolnc].SetPoint(n,t,timeRange[t][k+1][1])
         dy = timeRange[t][k+1][1] - timeRange[t][k]
         h[evolnc].SetPointError(n,500,500,timeRange[t][k+1][0]+dy,0)
      else:
         h[evolnc].SetPoint(n,t,timeRange[t][k])
         h[evolnc].SetPointError(n,500,500,timeRange[t][k+1][0],timeRange[t][k+1][1])
      n+=1
  if not 'inEff' in h:
   # delta = (tend-tstart)*0.025
   # ut.bookHist(h,'inEff',';time ; inEff',300,tstart-delta,tend+delta)
   if year == 2022:
      dateA = '07-20,2022-0'
      dateB = '12-01,2022-0'
   if year == 2023:
      dateA = '05-10,2023-0'
      dateB = '07-20,2023-0'
   time_objA = time.strptime(dateA,'%m-%d,%Y-%H')
   time_objB = time.strptime(dateB,'%m-%d,%Y-%H')
   TA = calendar.timegm(time_objA)
   TB = calendar.timegm(time_objB)
   ut.bookHist(h,'inEff',';time ; inEff',300,TA,TB)
   ut.bookCanvas(h,'TinEff','',2400,800,1,1)
   tc = h['TinEff'].cd()
   tc.SetLogy(1)
   h['inEff'].GetXaxis().SetTimeFormat("%d-%m")
   h['inEff'].GetXaxis().SetTimeOffset(0,'gmt')
   h['inEff'].GetXaxis().SetNdivisions(520)
   h['inEff'].GetYaxis().SetMaxDigits(2)
   if year == 2023: h['inEff'].SetMaximum(5E-4)
   if year == 2022: h['inEff'].SetMaximum(1E-2)
   h['inEff'].SetMinimum(1E-8)
   h['inEff'].SetStats(0)
  h['inEff'].Draw()
  for p in Marker:
    evolnc = p+'evol'+str(nc)
    h[evolnc].Draw('same')
    h[evolnc].Draw('sameP')
  if year == 2022:  h['levol']=ROOT.TLegend(0.32,0.28,0.49,0.57)
  if year == 2023:  h['levol']=ROOT.TLegend(0.46,0.43,0.69,0.65)
  X = h['levol'].AddEntry(h['p0evol'+str(nc)],'plane 0 ',"LP")
  X.SetTextColor(h['p0evol'+str(nc)].GetMarkerColor())
  X = h['levol'].AddEntry(h['p1evol'+str(nc)],'plane 1 ',"LP")
  X.SetTextColor(h['p1evol'+str(nc)].GetMarkerColor())
  X = h['levol'].AddEntry(h['evol'+str(nc)],'detector UL 90%',"LP")
  X.SetTextColor(h['evol'+str(nc)].GetMarkerColor())
  h['levol'].Draw()
  myPrint(h['TinEff'],'VetoInEffOverTime_'+str(nc))
 
 # deadtime
 # muon rate = 1.84E4 fb/cm2 * 6*42 cm2 
 # sigma = 80E6 # 80mb, mu = 50, 42*42 --> 800 events / sec.  From offline monitoring, ~500 events / sec 
 # 625 ns : 500*625/1E9 = 3.1E-4 / 625ns

def vetoEfficiency(runs,v='',name='noBackward/allHistos-run00XXXX.root',noiseCuts = [5]):
  path = "./"
  flavors={'': 1}
  for r in runs:
   h[r]={}
   for o in flavors:
     h[r][o] = {}
     fname = path+o+'/'+name.replace('XXXX',str(r))
     if not os.path.isfile(fname):
         print(fname +'not found')
         continue
     print('*** analyzing '+fname)
     wa = ['scaler','hitVeto_X','hitVeto_Y','deltaT','X/Y',
           'hitVeto_0','hitVeto_1','hitVeto_01']
     for noiseCut in [1,5,10,12]:
        wa.append('timeDiffPrev_'+str(noiseCut))
        wa.append('XtimeDiffPrev_'+str(noiseCut))
        for c in ['','NoPrev']:
          for b in ['','beam']:
               nc = 'T'+c+str(noiseCut)+b
               for l in range(2):
                 wa.append(nc+'PosVeto_'+str(l))
                 wa.append(nc+'XPosVeto_'+str(l))
               wa.append(nc+'PosVeto_11')
               wa.append(nc+'PosVeto_111')
               wa.append(nc+'XPosVeto_111')
               wa.append(nc+'PosVeto_00')
               wa.append(nc+'XPosVeto_11')
          wa.append('T'+c+'1PosVeto_0')
          wa.append('T'+c+'1XPosVeto_0')
          wa.append('scifi_trackChi2/ndof')
           
     ut.readHists(h[r][o],fname,wanted=wa)
     hr = h[r][o]
     if hr['T5PosVeto_0'].GetEntries()<1:
          print('run with no entries --->',r)
          continue
     stats[r]={}
     for c in ['','NoPrev','all']:
      if c=='all':
# print results for ignoring condition of previous event or not
        for hn in ['PosVeto_0','PosVeto_1','PosVeto_00','XPosVeto_0','XPosVeto_1','XPosVeto_11','PosVeto_11','PosVeto_111','XPosVeto_111']:
          for noiseCut in [1,5,10,12]:
            if not  'T'+str(noiseCut)+v+hn in hr: continue
            hr['T'+c+str(noiseCut)+v+hn] = hr['T'+str(noiseCut)+v+hn].Clone('T'+c+str(noiseCut)+v+hn+str(r))
            hr['T'+c+str(noiseCut)+v+hn].Add(hr['TNoPrev'+str(noiseCut)+v+hn])
      allTracks = hr['T'+c+'1PosVeto_0'].Clone('tmp'+str(r))
      allTracks.Add(hr['T'+c+'1XPosVeto_0'])
      stats[r][c]={}
      for noiseCut in noiseCuts:
       nc = 'T'+c+str(noiseCut)+v
       hr[nc+'XPosVeto_00']=allTracks.Clone(nc+'XPosVeto_00'+str(r))
       hr[nc+'XPosVeto_00'].Add(hr[nc+'PosVeto_00'],-1)
       # print('debug',nc,hr[nc+'XPosVeto_00'].GetSumOfWeights(),allTracks.GetSumOfWeights(),hr[nc+'PosVeto_00'].GetSumOfWeights())

# make some printout
#   PosVeto_0/1 is filled if enough channels have fired
#  XPosVeto_0/1 is filled if not enough channels have fired
#   PosVeto_11  is filled if both planes have enough channels fired
#   PosVeto_00  is fileed if one of the two planes has enough hits
#  XPosVeto_11  is filled if none of the two planes has enough hits
#  histos are exclusive filled for no previous event (NoPrev) and with previous event ''

       Ntot = hr[nc+'PosVeto_0'].Clone('Ntot'+str(r))
       Ntot.Add(hr[nc+'XPosVeto_0'])
       ineff0 =  hr[nc+'XPosVeto_0'].GetEntries()/Ntot.GetEntries()
       ineff1 = hr[nc+'XPosVeto_1'].GetEntries()/Ntot.GetEntries()
       ineffOR =  hr[nc+'XPosVeto_11'].GetEntries()/Ntot.GetEntries()
       ineffAND = 1.-hr[nc+'PosVeto_11'].GetEntries()/Ntot.GetEntries()
       xax = hr[nc+'PosVeto_0'].GetXaxis()
       yax = hr[nc+'PosVeto_0'].GetYaxis()
       Ntot_r = Ntot.Integral(region[0],region[1],region[2],region[3])
       ineff0_r = hr[nc+'XPosVeto_0'].Integral(region[0],region[1],region[2],region[3])/Ntot_r
       ineff1_r = hr[nc+'XPosVeto_1'].Integral(region[0],region[1],region[2],region[3])/Ntot_r
       ineffOR_r =  hr[nc+'XPosVeto_11'].Integral(region[0],region[1],region[2],region[3])/Ntot_r
       ineffAND_r = 1.-hr[nc+'PosVeto_11'].Integral(region[0],region[1],region[2],region[3])/Ntot_r
       sig_ineff0_r = ROOT.TMath.Sqrt(hr[nc+'XPosVeto_0'].Integral(region[0],region[1],region[2],region[3]))/Ntot_r
       sig_ineff1_r = ROOT.TMath.Sqrt(hr[nc+'XPosVeto_1'].Integral(region[0],region[1],region[2],region[3]))/Ntot_r
       sig_ineffOR_r =  ROOT.TMath.Sqrt(hr[nc+'XPosVeto_11'].Integral(region[0],region[1],region[2],region[3]))/Ntot_r
       sig_ineffAND_r = ROOT.TMath.Sqrt(Ntot_r-hr[nc+'PosVeto_11'].Integral(region[0],region[1],region[2],region[3]))/Ntot_r
       print('noise cut = ',noiseCut, 'previous event:',c)
       print('global inefficiency veto0: %5.2F%% veto1: %5.2F%% veto0AND1: %5.2F%% veto0OR1: %5.2F%%'%(
        ineff0*100,ineff1*100,ineffAND*100,ineffOR*100))
       print('region %5.2F < X < %5.2F and %5.2F < Y < %5.2F '%(xax.GetBinCenter(region[0]),
          xax.GetBinCenter(region[1]),yax.GetBinCenter(region[0]),yax.GetBinCenter(region[1])))
       print('veto0: %3.1E +/- %3.1E veto1: %3.1E +/- %3.1E veto0AND1: %3.1E +/- %3.1E veto0OR1: %3.1E +/- %3.1E '%( ineff0_r,sig_ineff0_r,ineff1_r,sig_ineff1_r,ineffAND_r,sig_ineffAND_r,ineffOR_r,sig_ineffOR_r))
     #                                   1         2            3          4          5           6            7           8              9
       scifiTrackPrevEvent = 100*(1-h[r][o]['scaler'][2]/h[r][o]['scaler'][1])
       stats[r][c][noiseCut]={'date':runInfo[r]['StartTime'],'Ntot_r':Ntot_r,'plane0':[ineff0_r,sig_ineff0_r],'plane1':[ineff1_r,sig_ineff1_r],
                              'AND':[ineffAND_r,sig_ineffAND_r],'OR':[ineffOR_r,sig_ineffOR_r],'trackPerEvent':scifiTrackPrevEvent}
# inefficiency of plane 0(1) if plane 1(0) fired
       hr[nc+'XPosVeto_10'] = hr[nc+'PosVeto_0'].Clone(nc+'XPosVeto_10')
       hr[nc+'XPosVeto_01'] = hr[nc+'PosVeto_1'].Clone(nc+'XPosVeto_01')
       hr[nc+'XPosVeto_10'].Add(hr[nc+'PosVeto_11'],-1)
       if nc+'PosVeto_111' in hr:
         hr[nc+'XPosVeto_01'].Add(hr[nc+'PosVeto_111'],-1) 
       else:
         print(" houston, we have a problem. 11 is filled with position at 0. integration over xy about ok, but not per xy bin ",nc+'PosVeto_111')
         hr[nc+'XPosVeto_01'].Add(hr[nc+'PosVeto_11'],-1) 
       '''
  _0    P0 and (P1 or not P1) position at P0
  _1    P1 and (P1 or not P1) position at P1
  _11   P0 and P1  position at P0
  _111  P0 and P1  position at P1
  _00   P0 or P1   position at P0
X_0     not P0 and (P1 or not P1) position at P0
X_1     not P1 and (P1 or not P1) position at P1
X_11    not P0 and not P1 at position P0
X_111   not P0 and not P1 at position P1
       '''
       Ntot_r = hr[nc+'PosVeto_0'].Integral(region[0],region[1],region[2],region[3])
       ineff10_r = hr[nc+'XPosVeto_10'].Integral(region[0],region[1],region[2],region[3])/Ntot_r
       sig_ineff10_r = ROOT.TMath.Sqrt(hr[nc+'XPosVeto_10'].Integral(region[0],region[1],region[2],region[3]))/Ntot_r
       Ntot_r = hr[nc+'PosVeto_1'].Integral(region[0],region[1],region[2],region[3])
       ineff01_r = hr[nc+'XPosVeto_01'].Integral(region[0],region[1],region[2],region[3])/Ntot_r
       sig_ineff01_r = ROOT.TMath.Sqrt(hr[nc+'XPosVeto_01'].Integral(region[0],region[1],region[2],region[3]))/Ntot_r
       stats[r][c][noiseCut]['plane10'] = [ineff10_r,sig_ineff10_r]
       stats[r][c][noiseCut]['plane01'] = [ineff01_r,sig_ineff01_r]
       print('no veto1 veto0: %3.1E +/- %3.1E no veto0 veto1: %3.1E +/- %3.1E '%( ineff10_r,sig_ineff10_r,ineff01_r,sig_ineff01_r))

     print('%5.2F%% of events with a Scifi track have a prev event '%(scifiTrackPrevEvent))
     if r==5125: muAv = 43.4
     elif r==5170: muAv = 48.2
     elif not 'muAv' in runInfo[r]:
        muAv = 0
        print('mu average missing',r)
     else: muAv = runInfo[r]['muAv']['']
     print('mu = %5.2F'%(muAv))
  if len(runs)>10:
    fp = ROOT.TFile.Open('VetoInEffStats.root','recreate')
    pkl = Pickler(fp)
    pkl.dump(stats,'stats')
    fp.Close()

def debug(r=6000):
    c = 'NoPrev'
    noiseCut = 5
    v=''
    nc = 'T'+c+str(noiseCut)+v
    hr = h[r]['']
    for p in range(2):
        for hname in [nc+'PosVeto_'+str(p),nc+'XPosVeto_'+str(p)]:
            print(hname, hr[hname].GetEntries())
    for hname in [nc+'PosVeto_00',nc+'XPosVeto_00',nc+'PosVeto_11',nc+'XPosVeto_11']:
            print(hname, hr[hname].GetEntries())


def ScifiIneffienciency(runs,name='allHistos-run00XXXX.root',path = "/mnt/hgfs/microDisk/SND@LHC/2022/vetoEff_cleanTracks/noBackward/"):
# allHistos-run004572.root .allHistos-run005236.root with plane inefficiencies

  border = {1: {0: [-46.07642436338805, -7.076849538271483], 1: [14.823752494688986, 53.820324353220755]}, 
            2: {0: [-46.045690293545526, -7.046373102426196], 1: [14.662870326613831, 53.659184531258354]}, 
            3: {0: [-46.021234619428235, -7.022092619428233], 1: [14.498185143430852, 53.49432414343085]}, 
            4: {0: [-46.0186513529706, -7.0195299636900765], 1: [14.345028712321486, 53.341147100010815]}, 
            5: {0: [-46.016618021002316, -7.017380696423783], 1: [14.212008931397556, 53.20824326333539]}}
  if not border:  # create from detector module
     border = {}
     for sRef in range(1,6):
       border[sRef]={}
       for p in range(2):
         scifi.GetSiPMPosition(1000000*sRef+100000*p,A,B)
         border[sRef][p] = [A[p],B[p]]
  for w in ['2','4']:
    for sRef in range(1,6):
        h['TlineTop'+w+str(sRef)] = ROOT.TLine(border[sRef][0][0],border[sRef][1][1],border[sRef][0][1],border[sRef][1][1])
        h['TlineBot'+w+str(sRef)] = ROOT.TLine(border[sRef][0][0],border[sRef][1][0],border[sRef][0][1],border[sRef][1][0])
        h['TlineLef'+w+str(sRef)] = ROOT.TLine(border[sRef][0][0],border[sRef][1][0],border[sRef][0][0],border[sRef][1][1])
        h['TlineRig'+w+str(sRef)] = ROOT.TLine(border[sRef][0][1],border[sRef][1][0],border[sRef][0][1],border[sRef][1][1])
        for x in ['TlineTop'+w+str(sRef),'TlineBot'+w+str(sRef),'TlineLef'+w+str(sRef),'TlineRig'+w+str(sRef)]: 
          h[x].SetLineWidth(int(w))
          h[x].SetLineColor(ROOT.kRed)

  limits = {1:{'X':[-44,-8],'Y':[16,50]},2:{'X':[-41.5,-13.5],'Y':[20,49]}}
  wa=['scifiTrack','DStag']
  for s in range(0,6):
       for p in [-1,0,1]:
          if p<0:X = str(s)
          else: X=str(10*s+p)
          wa.append('scifiTrack_'+X)
  for r in runs:
   h[r]={}
   hr=h[r]
   stats[r]={}
   fname = path+name.replace('XXXX',str(r))
   if not os.path.isfile(fname):
         print(fname +'not found')
         continue
   print('*** analyzing '+fname)
   ut.readHists(h[r],fname,wanted=wa)
   if len(h[r])<6:   
       ut.readHists(h[r],path+name.replace('XXXX',str(r)),wanted=wa)
       if len(h[r])<6:    continue
   bins = {}
   for l in limits :
       bins[l] = []
       for p in limits[l]:
         for x in limits[l][p]:
             bins[l].append(eval('h['+str(r)+']["DStag"].Get'+p+'axis().FindBin(x)'))
       # station inefficiency, fiducial volume
   for w in ['2','4']:
    for i in [1,2]:
     hr['FlineTop'+w+str(i)] = ROOT.TLine(limits[i]['X'][0],limits[i]['Y'][1],limits[i]['X'][1],limits[i]['Y'][1])
     hr['FlineBot'+w+str(i)] = ROOT.TLine(limits[i]['X'][0],limits[i]['Y'][0],limits[i]['X'][1],limits[i]['Y'][0])
     hr['FlineLef'+w+str(i)] = ROOT.TLine(limits[i]['X'][0],limits[i]['Y'][0],limits[i]['X'][0],limits[i]['Y'][1])
     hr['FlineRig'+w+str(i)] = ROOT.TLine(limits[i]['X'][1],limits[i]['Y'][0],limits[i]['X'][1],limits[i]['Y'][1])
     for x in ['FlineTop'+w+str(i),'FlineBot'+w+str(i),'FlineLef'+w+str(i),'FlineRig'+w+str(i)]: 
          hr[x].SetLineWidth(int(w))
          if i==1: hr[x].SetLineColor(ROOT.kGreen)
          else: hr[x].SetLineColor(ROOT.kBlack)

   l=2
   for s in range(0,6):
     for p in [-1,0,1]:
        if p<0:X = str(s)
        else: X=str(10*s+p)
        if s==0 and not p<0: continue
        if not 'scifiTrack_'+X in h[r]: continue
        for proj in ['X','Y']:
           pname = 'scifiTrack_'+X+'_'+proj
           if proj=='X': hr[pname]=hr['scifiTrack_'+X].ProjectionX(pname)
           if proj=='Y': hr[pname]=hr['scifiTrack_'+X].ProjectionY(pname)
           hr[pname].Reset()
           if proj=='Y':
             for iy in range(bins[l][2],bins[l][3]):
               N = 0
               for ix in range(bins[l][0],bins[l][1]):
                  N+=hr['scifiTrack_'+X].GetBinContent(ix,iy)
               hr[pname].SetBinContent(iy,N)
           if proj=='X':
             for iy in range(bins[l][0],bins[l][1]):
               N = 0
               for ix in range(bins[l][2],bins[l][3]):
                  N+=hr['scifiTrack_'+X].GetBinContent(ix,iy)
               hr[pname].SetBinContent(iy,N)

   stats[r]['utc'] = runInfo[r]['StartTime']
   stats[r]['ineff'] = {}
   for l in limits :
      stats[r]['ineff'][l]={}
      for s in range(1,6):
       for p in [-1,0,1]:
          if p<0:X = str(s)
          else: X=str(10*s+p)
          if not 'scifiTrack_'+X in h[r]: continue
          e = h[r]['scifiTrack_'+X].Integral(bins[l][0],bins[l][1],bins[l][2],bins[l][3])/h[r]['scifiTrack_0'].Integral(bins[l][0],bins[l][1],bins[l][2],bins[l][3])
          sige = ROOT.TMath.Sqrt(h[r]['scifiTrack_'+X].Integral(bins[l][0],bins[l][1],bins[l][2],bins[l][3]))/h[r]['scifiTrack_0'].Integral(bins[l][0],bins[l][1],bins[l][2],bins[l][3])
          print('average efficiency station: %s %5.2F<X<%5.2F %5.2F<Y<%5.2F = %5.2G'%(X,limits[l]['X'][0],limits[l]['X'][1],limits[l]['Y'][0],limits[l]['Y'][1],e))
          stats[r]['ineff'][l][X] = [e,sige]
# make plots for note:
   ut.bookCanvas(h,'Tsineff','',1200,900,3,2)
   for s in range(1,6):
          tc = h['Tsineff'].cd(s)
          tc.SetRightMargin(0.1)
          tc.SetLogz(1)
          hr['sineff'+str(s)] = hr['scifiTrack_'+str(s)].Clone('sineff'+str(s))
          hr['sineff'+str(s)].Divide(hr['scifiTrack_0'])
          hr['sineff'+str(s)].SetStats(0)
          hr['sineff'+str(s)].SetMaximum(0.1)
          hr['sineff'+str(s)].DrawCopy('colz')
          for x in ['TlineTop2'+str(s),'TlineBot2'+str(s),'TlineLef2'+str(s),'TlineRig2'+str(s)]: h[x].Draw('same')
          for i in [2]:
              for x in ['FlineTop2'+str(i),'FlineBot2'+str(i),'FlineLef2'+str(i),'FlineRig2'+str(i)]: hr[x].Draw('same')
   h['Tsineff'].Update()
   myPrint(h['Tsineff'],'ScifiStationInEfficiency_run'+str(r).zfill(6))
   for s in [1,10,11]:
     if not 'sineff'+str(s) in hr: continue
     ut.bookCanvas(h,'Tsineff'+str(s),'',1200,900,1,1)
     tc = h['Tsineff'+str(s)].cd()
     tc.SetLogz(1)
     hr['sineff'+str(s)] = hr['scifiTrack_'+str(s)].Clone('sineff'+str(s))
     hr['sineff'+str(s)].Divide(hr['scifiTrack_0'])
     hr['sineff'+str(s)].SetStats(0)
     hr['sineff'+str(s)].SetMaximum(0.2)
     if s==1:  hr['sineff'+str(s)].Draw()
     else:  hr['sineff'+str(s)].Draw('colz')
     for x in ['TlineTop41','TlineBot41','TlineLef41','TlineRig41']: h[x].Draw('same')
     for i in [2]:
        for x in ['FlineTop4'+str(i),'FlineBot4'+str(i),'FlineLef4'+str(i),'FlineRig4'+str(i)]: hr[x].Draw('same')
     h['Tsineff'+str(s)].Update()
     myPrint(h['Tsineff'+str(s)],'ScifiStationInEfficiency'+str(s)+'_run'+str(r).zfill(6))
   for proj in ['X','Y']:
      if not 'sineff'+str(s) in hr: continue
      for X in ['1','10','11']:
         pname = 'scifiTrack_'+X+'_'+proj
         ut.bookCanvas(h,'Tsineff'+str(X)+'_'+proj,'',1200,900,1,1)
         tc = h['Tsineff'+str(s)].cd()
         hr['sineff'+X+'_'+proj] = hr['scifiTrack_'+X+'_'+proj].Clone('sineff'+X+'_'+proj)
         hr['sineff'+X+'_'+proj].Divide(hr['scifiTrack_0_'+proj])
         hr['sineff'+X+'_'+proj].SetStats(0)
         if X=='1': hr['sineff'+X+'_'+proj].SetMaximum(0.001)
         if X=='1': hr['sineff'+X+'_'+proj].SetMaximum(0.01)
         hr['sineff'+X+'_'+proj].Draw()
         myPrint(h['Tsineff'+X+'_'+proj],'ScifiStationInEfficiency'+X+'_'+proj+'_run'+str(r).zfill(6))
         
  if len(stats)<2: return
# make evolution plot
  for r in stats:
   if len(stats[r])<1:continue
   timeRange[stats[r]['utc']]={}
   for l in limits :
      timeRange[stats[r]['utc']][l]={}
      for s in range(1,6): timeRange[stats[r]['utc']][l][str(s)]=[ stats[r]['ineff'][l][str(s)][0],stats[r]['ineff'][l][str(s)][1] ]
  T = list(timeRange.keys())
  T.sort()
  tstart = T[0]
  tend = T[len(T)-1]
  for s in range(1,6): h['evol_'+str(s)] = ROOT.TGraphErrors()
  n = 0
  l = 1
  for t in T:
     for s in range(1,6):
       if timeRange[t][l][str(s)][0]<1E-9 or timeRange[t][l][str(s)][0]>1 :
         print('exclude time',s,t,l,timeRange[t][l][s][0])
         continue
       h['evol_'+str(s)].SetPoint(n,t,timeRange[t][1][str(s)][0])
       h['evol_'+str(s)].SetPointError(n,500,timeRange[t][1][str(s)][1])
     n+=1
  delta = (tend-tstart)*0.025
  ut.bookHist(h,'inEff',';time ; inEff',300,tstart-delta,tend+delta)
  ut.bookCanvas(h,'TinEff','',2400,800,1,1)
  tc = h['TinEff'].cd()
  h['inEff'].GetXaxis().SetTimeFormat("%d-%m")
  h['inEff'].GetXaxis().SetTimeOffset(0,'gmt')
  h['inEff'].GetXaxis().SetNdivisions(520)
  h['inEff'].GetYaxis().SetMaxDigits(2)
  h['inEff'].SetMaximum(1E-3)
  h['inEff'].SetMinimum(1E-7)
  h['inEff'].SetStats(0)
  h['inEff'].Draw()
  colors=[ROOT.kGreen,ROOT.kBlue,ROOT.kCyan,ROOT.kMagenta,ROOT.kRed]
  h['lscifi']=ROOT.TLegend(0.72,0.56,0.89,0.93)
  for s in range(1,6):
     h['evol_'+str(s)].SetMarkerStyle(20+s)
     h['evol_'+str(s)].SetMarkerColor(colors[s-1])
     h['evol_'+str(s)].SetLineColor(colors[s-1])
     h['evol_'+str(s)].Draw('sameP')
     h['evol_'+str(s)].Draw('same')
     X = h['lscifi'].AddEntry(h['evol_'+str(s)],'station '+str(s),"L")
     X.SetTextColor(colors[s-1])
  h['lscifi'].Draw()
  myPrint(h['TinEff'],'ScifiInEffOverTime')

def timeBoard(runs,stats=stats):
  if len(stats)<10:
      fp = ROOT.TFile.Open('VetoInEffStats.root')
      pkl = Unpickler(fp)
      stats  = pkl.load('stats')
  h['timeBoard'] = {}
  h['gTimeBoard'] = ROOT.TGraph()
  h['gTimeBoard'].SetMarkerStyle(21)
  h['gTimeBoard'].SetMarkerColor(ROOT.kBlue)
  if not 'TinEff' in h:
     ut.readHists(h,'VetoInEffOverTime_5.root')
     h['inEff'] = h['TinEff'].FindObject('inEff').Clone()
     h['TinEff'].Draw()
  tc = h['TinEff'].cd()
  tc.SetLogy(0)
  h['inEff'].GetYaxis().SetTitle('time offset [clock cycles]')
  h['inEff'].SetMaximum(0.5)
  h['inEff'].SetMinimum(-2)
  h['inEff'].Draw()
  n = -1
  for r in runs:
    if not r in h: h[r]={}
    n+=1
    g = ROOT.TFile.Open(os.environ['EOSSHIP']+'/eos/experiment/sndlhc/www/offline/run'+str(r).zfill(6)+'.root')
    ROOT.gROOT.cd()
    if g.daq.FindKey('boards'):
     h[r]['Tboard'] = g.daq.boards.FindObject('Tboard').Clone(str(r).zfill(6)+'Tboard')
     h[r]['TboardMean'] = h[r]['Tboard'].ProjectionX(str(r).zfill(6)+'TboardMean')
     h[r]['TboardMean'].Reset()
     for nx in range(1,h[r]['Tboard'].GetNbinsX()+1):
        tmp = h[r]['Tboard'].ProjectionY('tmp',nx,nx)
        h[r]['TboardMean'].SetBinContent(nx,tmp.GetMean())
        h[r]['TboardMean'].SetBinError(nx,tmp.GetRMS())
     h[r]['TboardMean'].SetMarkerStyle(20)
     h[r]['TboardMean'].Draw('P')
     h['timeBoard'][r]=h[r]['TboardMean'].GetBinContent(58)
     h['gTimeBoard'].SetPointX(n,stats[r]['NoPrev'][5]['date'])
     h['gTimeBoard'].SetPointY(n,h['timeBoard'][r])
     print('run',r,':',h['timeBoard'][r])
  h['gTimeBoard'].Draw('same')
  myPrint(h['TinEff'],'VetoBoardTime')
  
  mean = 0
  N = 0
  for r in stats:
      tdiff = -1
      if r in h['timeBoard']: tdiff = h['timeBoard'][r]
      print("%i %5.2F+/-%5.2F  %5.2F"%(r,stats[r]['NoPrev'][5]['OR'][0]*1E6,stats[r]['NoPrev'][5]['OR'][1]*1E6,tdiff))
      if r > 5180:
         mean += stats[r]['NoPrev'][5]['OR'][0]
         N+=1
  mean=mean/N
  chi2 = 0
  N = 0
  for r in stats:
    if r > 5180:
      chi2+=((stats[r]['NoPrev'][5]['OR'][0]-mean)/stats[r]['NoPrev'][5]['OR'][1])**2
      N+=1
  print(N,chi2)
def triggerSettings(path="/mnt/hgfs/microDisk/SND@LHC/2022/"):
  ft=open(path+'trigger_settings.csv')
  L = ft.readlines()
  keys = L[0].replace('\n','').split(',')
  triggerSettings = {}
  for l in range(1,len(L)):
     val = L[l].replace('\n','').split(',')
     triggerSettings[int(val[0])]={}
     for i in range(1,len(keys)):
        triggerSettings[int(val[0])][keys[i]]=val[i]
  allruns = list(triggerSettings.keys())
  allruns.sort()
  for iv in range(1,len(keys) ):
    prevVal = ''
    for r in allruns:
       if triggerSettings[r][keys[iv]] == prevVal: continue
       if not prevVal == '':
          print('change of settings',r,keys[iv],prevVal,triggerSettings[r][keys[iv]])
       prevVal = triggerSettings[r][keys[iv]]
"""
change of settings 5031 veto_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 5031 veto_del off 3_ns

change of settings 4453 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 4461 scifi_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 4517 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 4523 scifi_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 4545 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 4557 scifi_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 4576 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 4579 scifi_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 4630 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 4635 scifi_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 4642 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 4647 scifi_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 4692 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 4693 scifi_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 4772 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 4791 scifi_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 4824 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 4831 scifi_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 4841 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 4843 scifi_trig dtt_t1t2 dtt_fdcr_t1t2
change of settings 4965 scifi_trig dtt_fdcr_t1t2 
change of settings 5030 scifi_trig dtt_fdcr_t1t2 dtt_t1t2
change of settings 5031 scifi_trig dtt_t1t2 dtt_fdcr_t1t2

change of settings 4453 scifi_del 6_ns off
change of settings 4461 scifi_del off 6_ns
change of settings 4517 scifi_del 6_ns off
change of settings 4523 scifi_del off 6_ns
change of settings 4545 scifi_del 6_ns off
change of settings 4557 scifi_del off 6_ns
change of settings 4576 scifi_del 6_ns off
change of settings 4579 scifi_del off 6_ns
change of settings 4629 scifi_del 6_ns 3_ns
change of settings 4630 scifi_del 3_ns off
change of settings 4635 scifi_del off 3_ns
change of settings 4642 scifi_del 3_ns off
change of settings 4647 scifi_del off 3_ns
change of settings 4692 scifi_del 3_ns off
change of settings 4693 scifi_del off 3_ns
change of settings 4772 scifi_del 3_ns off
change of settings 4791 scifi_del off 3_ns
change of settings 4824 scifi_del 3_ns off
change of settings 4831 scifi_del off 3_ns
change of settings 4841 scifi_del 3_ns off
change of settings 4843 scifi_del off 3_ns
change of settings 4965 scifi_del 3_ns 
change of settings 5028 scifi_del 3_ns 6_ns
change of settings 5030 scifi_del 6_ns off
change of settings 5031 scifi_del off 3_ns
"""

