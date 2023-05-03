import ROOT
import os
import rootUtils as ut
h={}
#     5399,5396,5262,5253,5408,5389,5377,5263,5259,5350,5257,5125 now running with proper xy distr, hopefully
runs=[5389,5408,5125,5396,5350,5399,5263,5377,5262,5259,5257,5253,   # runs with prevTime  --> 6001 
5059,5120,5154,5170,5180,5236,5239,5036,5044,5056,
                        4572,4595,4617,4626,4612,4639,4661,4649,4724,4744,4758,4769,4815,4958,4964,4971,4976,4980,4990,5000,5005,5013,5024,5059,5094,5109]
runs.sort()

region = [22,92,22,83] # region = [21,91,34,89] # value from neutrino analysis?

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
   path = "/mnt/hgfs/microDisk/SND@LHC/Analysis Notes/VetoInefficiency/"
   t = open(path+"introduction.tex")
   listOfFigures = []
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
     print("%30s :  %25s, %25s"%(p,time.ctime(os.path.getmtime(p)), time.ctime(os.path.getmtime(path+"figs/"+p)) ) )
 

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

def timeDiffPrevNextEvent(r=6001):
   ut.readHists(h,'noBackward/allHistos-run00'+str(r)+'.root')
   ut.bookCanvas(h,'TtimeDiff','',900,600,1,1)
   colors = {'timeDiffPrev_5':[ROOT.kMagenta,22],'XtimeDiffPrev_5':[ROOT.kRed,23]}
   for c in ['timeDiffPrev_5','XtimeDiffPrev_5']:
     h[c+'norm'] = h[c].Clone(c+'norm')
     h[c+'norm'].Scale(1./h[c].GetSumOfWeights())
     h[c+'norm'].SetStats(0)
     h[c+'norm'].SetMinimum(0)
     h[c+'norm'].SetMarkerColor(colors[c][0])
     h[c+'norm'].SetMarkerStyle(colors[c][1])
     h[c+'norm'].SetTitle(';clock cycles; arb. units')
   h['timeDiffPrev_5norm'].Scale(10)
   h['XtimeDiffPrev_5norm'].Draw()
   h['timeDiffPrev_5norm'].Draw('same')
   h['ltimeDiffPrev']=ROOT.TLegend(0.42,0.66,0.88,0.88)
   X = h['ltimeDiffPrev'].AddEntry(h['timeDiffPrev_5norm'],'all events',"LP")
   X.SetTextColor(colors['timeDiffPrev_5'][0])
   X = h['ltimeDiffPrev'].AddEntry(h['XtimeDiffPrev_5norm'],'events with inefficient Veto',"LP")
   X.SetTextColor(colors['XtimeDiffPrev_5'][0])
   h['ltimeDiffPrev'].Draw()
   myPrint(h['TtimeDiff'],'timeDiffPrev_'+str(r))

from rootpyPickler import Unpickler
fg  = ROOT.TFile.Open(os.environ['EOSSHIP']+"/eos/experiment/sndlhc/convertedData/physics/2022/RunInfodict.root")
pkl = Unpickler(fg)
runInfo = pkl.load('runInfo')
fg.Close()

for rspecial in [6000,6001]:
 runInfo[rspecial]={}
 runInfo[rspecial]['muAv']={}
 runInfo[rspecial]['muAv']['']=50
 runInfo[rspecial]['StartTime']=runInfo[5125]['StartTime']

def myPrint(tc,outName):
   tc.Update()
   for t in ['.root','.png','.pdf']:
      tc.Print(outName+t)

def makePlotsForNote(r=5125):
# 5125 after fixing time delay and noise filter
# 5120 after fixing time delay but still without veto in noise filter
# 4626 with doT1 6ns
# 4744 with doT1 3ns

     vetoEfficiency(runs=[r],v='',name='noBackward/allHistos-run00XXXX.root',noiseCuts = [1,5,10,12])
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
           hr[projY].Reset()
           for iy in range(region[2],region[3]):
             N = 0
             for ix in range(region[0],region[1]):
                N+=hr['T'+c+str(nc)+x+'PosVeto_'+p].GetBinContent(ix,iy)
             hr[projY].SetBinContent(iy,N)
       for p in ['0','1','11','01','10','11']:
          hr['eff'+c+str(nc)+'PosVeto_'+p+'Y']=hr['T'+c+str(nc)+'XPosVeto_'+p+'Y'].Clone( 'eff'+c+str(nc)+'PosVeto_'+p+'Y')
          if p in ['01','10']:
             if p=='10':  hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].Divide(hr['T'+c+str(nc)+'PosVeto_0Y'])
             if p=='01':  hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].Divide(hr['T'+c+str(nc)+'PosVeto_1Y'])
          else:
             hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].Divide(hr['T'+c+str(nc)+'PosVeto_'+p+'Y'])
          hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].SetStats(0)
          hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].SetTitle('')
          hr['eff'+c+str(nc)+'PosVeto_'+p+'Y'].SetLineColor(Marker[p][1])
       hr['TPosVeto'].SetLogy(1)
       hr['eff'+c+str(nc)+'PosVeto_11Y'].SetMaximum(4E-4)
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
       myPrint(hr['TPosVeto'],'NoHitPosVeto_'+str(nc)+str(p)+'_'+str(r))
     flatex = open('table-'+str(r)+'.tex','w')
     for c in ['all','','NoPrev']:
        prev = stats[r][''][5][9]/100
        eprev = int(ROOT.TMath.Log10(prev)-1)
        # if c=='': line = "\\multicolumn{4}{|c|}{With previous event, $%5.2F \\times 10^{%i}$ of the events}\\\\ \n"%(prev/10**eprev,eprev)
        if c=='': line = "\\multicolumn{4}{|c|}{With previous event, $%5.2F%% of the events}\\\\ \n"%(prev*100)
        elif c=='':    line = "\\multicolumn{4}{|c|}{}\\\\ \n"
        else:    line = "\\multicolumn{4}{|c|}{No previous event}\\\\ \n"
        flatex.write(line)
        for noiseCut in stats[r][c]:
           val = stats[r][c][noiseCut]
       # $N_{hits}< & no Veto 0 & no Veto 1 & no Veto 0 and no Veto 1  
           e={}
           for i in [1,3,7]:
              e[i]=int(ROOT.TMath.Log10(val[i])-1)
           line = "$%i$ & $(%5.2F \pm %5.2F)\\times 10^{%i}$ &  $(%5.2F \pm %5.2F)\\times 10^{%i}$ &  $(%5.2F \pm %5.2F)\\times 10^{%i}$ \\\\ \n"%(noiseCut,
              val[1]/10**e[1],val[2]/10**e[1],e[1],val[3]/10**e[3],val[4]/10**e[3],e[3],val[7]/10**e[7],val[8]/10**e[7],e[7])
           flatex.write(line)
     flatex.write('--- single plane ineff\n')
     for c in ['all','','NoPrev']:
     # single plane inefficiencies if other plane has fired
      for noiseCut in stats[r][c]:
           val = stats[r][c][noiseCut]
       # $N_{hits}< & no Veto 0 & no Veto 1 & no Veto 0 and no Veto 1  
           e={}
           for i in [0,2]:
              e[i]=int(ROOT.TMath.Log10(val[10][i])-1)
           line = "$%i$ & $(%5.2F \pm %5.2F)\\times 10^{%i}$ &  $(%5.2F \pm %5.2F)\\times 10^{%i}$ \\\\ \n"%(noiseCut,
              val[10][0]/10**e[0],val[10][1]/10**e[0],e[0],val[10][2]/10**e[2],val[10][3]/10**e[2],e[2])
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
def printVetoEff(noiseCut=[5]):
   # if prev==1000: runs=[4964,5125,5350]  different prev event 1000 clock cycles
 vetoEfficiency(runs,v='',name='noBackward/allHistos-run00XXXX.root',noiseCuts = noiseCut)
 for nc in noiseCut:
  for r in stats:
     timeRange[stats[r]['NoPrev'][nc][0]] = [stats[r]['NoPrev'][nc][7],stats[r]['NoPrev'][nc][8],
     stats[r]['NoPrev'][nc][1],stats[r]['NoPrev'][nc][2],
     stats[r]['NoPrev'][nc][3],stats[r]['NoPrev'][nc][4]]
  T = list(timeRange.keys())
  T.sort()
  tstart = T[0]
  tend = T[len(T)-1]
  Marker = {'p0':[22,ROOT.kMagenta],'p1':[23,ROOT.kBlue],'':[72,ROOT.kGreen]}
  for p in Marker:
    evolnc = p+'evol'+str(nc)
    h[evolnc] = ROOT.TGraphErrors()
    h[evolnc].SetLineWidth(2)
    h[evolnc].SetMarkerStyle(Marker[p][0])
    h[evolnc].SetMarkerColor(Marker[p][1])
    h[evolnc].SetMarkerSize(2)
    n = 0
    for t in T:
      if timeRange[t][0]<1E-9: continue
      k=0
      if p=='p0': k = 2
      if p=='p1': k = 4
      h[evolnc].SetPoint(n,t,timeRange[t][k])
      h[evolnc].SetPointError(n,500,timeRange[t][k+1])
      n+=1
  if not 'inEff' in h:
   delta = (tend-tstart)*0.025
   ut.bookHist(h,'inEff',';time ; inEff',300,tstart-delta,tend+delta)
   ut.bookCanvas(h,'TinEff','',2400,800,1,1)
   tc = h['TinEff'].cd()
   tc.SetLogy(1)
   h['inEff'].GetXaxis().SetTimeFormat("%d-%m")
   h['inEff'].GetXaxis().SetTimeOffset(0,'gmt')
   h['inEff'].GetXaxis().SetNdivisions(520)
   h['inEff'].GetYaxis().SetMaxDigits(2)
   h['inEff'].SetMaximum(1E-2)
   h['inEff'].SetMinimum(1E-7)
   h['inEff'].SetStats(0)
   h['inEff'].Draw()
  for p in Marker:
    evolnc = p+'evol'+str(nc)
    h[evolnc].Draw('same')
    h[evolnc].Draw('sameP')
 h['levol']=ROOT.TLegend(0.32,0.28,0.49,0.57)
 X = h['levol'].AddEntry(h['p0evol'+str(nc)],'plane 0 ',"LP")
 X.SetTextColor(h['p0evol'+str(nc)].GetMarkerColor())
 X = h['levol'].AddEntry(h['p1evol'+str(nc)],'plane 1 ',"LP")
 X.SetTextColor(h['p1evol'+str(nc)].GetMarkerColor())
 X = h['levol'].AddEntry(h['evol'+str(nc)],'detector ',"LP")
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
     wa = ['scaler','hitVeto_X','hitVeto_Y','deltaT','X/Y','timeDiffPrev','XStimeDiffPrev']
     for noiseCut in [1,5,10,12]:
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
       stats[r][c][noiseCut]=[runInfo[r]['StartTime'],ineff0_r,sig_ineff0_r,ineff1_r,sig_ineff1_r,ineffAND_r,sig_ineffAND_r,ineffOR_r,sig_ineffOR_r,scifiTrackPrevEvent]
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
       stats[r][c][noiseCut].append([ineff10_r,sig_ineff10_r,ineff01_r,sig_ineff01_r])
       print('no veto1 veto0: %3.1E +/- %3.1E no veto0 veto1: %3.1E +/- %3.1E '%( ineff10_r,sig_ineff10_r,ineff01_r,sig_ineff01_r))

     print('%5.2F%% of events with a Scifi track have a prev event '%(scifiTrackPrevEvent))
     if r==5125: muAv = 43.4
     elif r==5170: muAv = 48.2
     elif not 'muAv' in runInfo[r]: print('mu average missing',r)
     else: muAv = runInfo[r]['muAv']['']
     print('mu = %5.2F'%(muAv))

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


def ScifiIneffienciency(runs,name='allHistos-run00XXXX.root',path = "noBackward/"):
# allHistos-run004572.root .allHistos-run005236.root with plane inefficiencies

  border = [14.964849051657234, 54.00431913184336, -46.21974599493218, -7.146496817384938]
  limits = {1:{'X':[-44,-8],'Y':[16,50]},2:{'X':[-40,-12],'Y':[18,47]}}
  sRef=1
  h['TlineTop'+str(sRef)] = ROOT.TLine(border[2],border[1],border[3],border[1])
  h['TlineBot'+str(sRef)] = ROOT.TLine(border[2],border[0],border[3],border[0])
  h['TlineLef'+str(sRef)] = ROOT.TLine(border[2],border[0],border[2],border[1])
  h['TlineRig'+str(sRef)] = ROOT.TLine(border[3],border[0],border[3],border[1])
  wa=['scifiTrack','DStag']
  for s in range(0,6):
       for p in [-1,0,1]:
          if p<0:X = str(s)
          else: X=str(10*s+p)
          wa.append('scifiTrack_'+X)
  for x in ['TlineTop'+str(sRef),'TlineBot'+str(sRef),'TlineLef'+str(sRef),'TlineRig'+str(sRef)]: 
     h[x].SetLineWidth(2)
     h[x].SetLineColor(ROOT.kRed)
  for r in runs:
   h[r]={}
   stats[r]={}
   fname = path+name.replace('XXXX',str(r))
   if not os.path.isfile(fname):
         print(fname +'not found')
         continue
   print('*** analyzing '+fname)
   ut.readHists(h[r],fname,wanted=wa)
   if len(h[r])<6:   
       ut.readHists(h[r],name.replace('XXXX',str(r)),wanted=wa)
       if len(h[r])<6:    continue
   bins = {}
   for l in limits :
       bins[l] = []
       for p in limits[l]:
         for x in limits[l][p]:
             bins[l].append(eval('h['+str(r)+']["DStag"].Get'+p+'axis().FindBin(x)'))
       # station inefficiency
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

