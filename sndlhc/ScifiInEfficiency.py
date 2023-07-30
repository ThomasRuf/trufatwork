import ROOT
import os
import rootUtils as ut
import subprocess,time,calendar
from rootpyPickler import Unpickler
from rootpyPickler import Pickler

""" three out of 5 measurements

P(N,k) = N! / [ (N-k)! * k!]

"""
def test(eta=0.01):
   noBias = 4*eta+(1-eta)**3
   bias = 6*eta**2
   ineff1 = eta/noBias
   ineff2 = eta/(noBias+bias)
   print('noBias/bias',ineff1/ineff2)

h={}

runs=[5389,5408,5125,5396,5350,5399,5263,5377,5262,5259,5257,5253,   # runs with prevTime  --> 6001 
5120,5154,5170,5180,5236,5239,5036,5044,5056,
                        4572,4595,4617,4626,4612,4639,4661,4649,4724,4744,4758,4769,4815,4958,4964,4971,4976,4980,4990,5000,5005,5013,5024,5059,5094,5109]
                        
                        
# scifi 5 off: 4976,4971,4969,4968
runs.sort()
stats = {}
timeRange = {}

if os.path.isfile('ScifiInEffStats.root'):
   fp = ROOT.TFile.Open('ScifiInEffStats.root')
   pkl = Unpickler(fp)
   stats = pkl.load('stats')
   fp.Close()

def checkIfUnbiased(method='Xscifi'):
   scifiTrack = method+'Track'
   for r in runs:
      f=ROOT.TFile('allHistos-run'+str(r).zfill(6)+'.root ')
      E = []
      for s in range(1,6):
          E.append(f.Get(scifiTrack+'_0'+str(s)).GetEntries())
      if E[0]==E[1] and E[1]==E[2] and E[2]==E[3] and E[3]==E[4]:
         print(r,'all equal')
      else:
         print(r,E)

def sumOfhistos(runs,path = "/mnt/hgfs/microDisk/SND@LHC/2022/Inefficiencies/unbiased/",newRun=6001):
   cmd = "hadd -f allHistos-run"+str(newRun).zfill(6)+'.root '
   for r in runs: 
      X={}
      fname = path+"allHistos-run"+str(r).zfill(6)+".root "
      ut.readHists(X,fname)
      if r<4980: continue   # 5 October, station 5 works again
      cmd += fname
   os.system(cmd)

def updateFigures():
   path = "/mnt/hgfs/microDisk/SND@LHC/Analysis Notes/ScifiInefficiency/"
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
     if not p.find('SciFi-X-Y Module')<0: continue
     if not p.find('png')<0: continue
     os.system('cp '+p+' '+path.replace(' ','\ ')+'figs/')
     # print("%30s :  %25s, %25s"%(p,time.ctime(os.path.getmtime(p)), time.ctime(os.path.getmtime(path+"figs/"+p)) ) )
   for p in listOfFigures:
      if p.find('-event')>0: os.system('cp '+p+' '+path.replace(' ','\ ')+'figs/')


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
         
fg  = ROOT.TFile.Open(os.environ['EOSSHIP']+"/eos/experiment/sndlhc/convertedData/physics/2022/RunInfodict.root")
pkl = Unpickler(fg)
runInfo = pkl.load('runInfo')
fg.Close()

for rspecial in [6000,6001,1000,1001]:
 runInfo[rspecial]={}
 runInfo[rspecial]['muAv']={}
 runInfo[rspecial]['muAv']['']=50
 runInfo[rspecial]['StartTime']=runInfo[5125]['StartTime']

def myPrint(tc,outName):
   tc.Update()
   for t in ['.root','.png','.pdf']:
      tc.Print(outName+t)

def ScifiIneffienciency(runs,name='allHistos-run00XXXX.root',path = "/mnt/hgfs/microDisk/SND@LHC/2022/Inefficiencies/unbiased/",unbiased=True,method='Xscifi'):
# allHistos-run004572.root .allHistos-run005236.root with plane inefficiencies
  scifiTrack = method+'Track'
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

  limits = {1:{'X':[-44,-8],'Y':[16,50]},2:{'X':[-41.5,-12.5],'Y':[20,49]}}
  wa=[scifiTrack,'DStag','clSize','hitPerPlane','dx','dy']
  for s in range(0,6):
       wa.append(scifiTrack+'_0'+str(s))
       for p in [-1,0,1]:
          if p<0:X = str(s)
          else: X=str(10*s+p)
          wa.append(scifiTrack+'_'+X)
  for r in runs:
   if r in stats: 
     if len(stats[r])>0: continue
   h[r]={}
   hr=h[r]
   stats[r]={}
   fname = path+name.replace('XXXX',str(r))
   if not os.path.isfile(fname):
         print(fname +'not found')
         continue
   print('*** analyzing '+fname)
   ut.readHists(h[r],fname,wanted=wa)
       
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
   # make plots for note:
   ut.bookCanvas(hr,'norm','',1200,900,1,1)
   tc = hr['norm'].cd()
   for s in range(1,6):
    hnorm = hr[scifiTrack+'_0'+str(s)]
    hnorm.SetStats(0)
    zax = hnorm.GetZaxis()
    zax.SetTitle('#tracks arb.units.')
    hnorm.SetTitle('')
    hnorm.Draw('colz')
    tc.SetRightMargin(0.2)
    tc.Update()
    zax.SetLabelOffset(0.01)
    zax.SetTitleOffset(1.65)
    pal = hnorm.FindObject('palette')
    pal.SetX1(0.214)
    for x in ['TlineTop2'+str(s),'TlineBot2'+str(s),'TlineLef2'+str(s),'TlineRig2'+str(s)]: h[x].Draw('same')
    for i in [2]:
       for x in ['FlineTop2'+str(i),'FlineBot2'+str(i),'FlineLef2'+str(i),'FlineRig2'+str(i)]: hr[x].Draw('same')
    hr['norm'].Update()
    myPrint(hr['norm'],'PositionAtScifi'+str(s)+'_run'+str(r).zfill(6))
   
   l=2
   for s in range(0,6):
     for X in [str(s),str(10*s),str(10*s+1),'0'+str(s)]:
        for proj in ['X','Y']:
           pname = scifiTrack+'_'+X+'_'+proj
           if proj=='X': hr[pname]=hr[scifiTrack+'_'+X].ProjectionX(pname)
           if proj=='Y': hr[pname]=hr[scifiTrack+'_'+X].ProjectionY(pname)
           hr[pname].Reset()
           if proj=='Y':
             for iy in range(bins[l][2],bins[l][3]):
               N = 0
               for ix in range(bins[l][0],bins[l][1]):
                  N+=hr[scifiTrack+'_'+X].GetBinContent(ix,iy)
               hr[pname].SetBinContent(iy,N)
               hr[pname].SetBinError(iy,ROOT.TMath.Sqrt(N))
           if proj=='X':
             for ix in range(bins[l][0],bins[l][1]):
               N = 0
               for iy in range(bins[l][2],bins[l][3]):
                  N+=hr[scifiTrack+'_'+X].GetBinContent(ix,iy)
               hr[pname].SetBinContent(ix,N)
               hr[pname].SetBinError(ix,ROOT.TMath.Sqrt(N))

   stats[r]['utc'] = runInfo[r]['StartTime']
   stats[r]['ineff'] = {}
   for l in limits :
      print('++++++++   Results for fiducial volume  %5.2F<X<%5.2F %5.2F<Y<%5.2F '%(limits[l]['X'][0],limits[l]['X'][1],limits[l]['Y'][0],limits[l]['Y'][1]))
      stats[r]['ineff'][l]={}
      for s in range(1,6):
       for p in [-1,0,1]:
          if p<0:X = str(s)
          else: X=str(10*s+p)
          norm = scifiTrack+'_0'+str(s)
          hnorm = hr[norm]
          e = h[r][scifiTrack+'_'+X].Integral(bins[l][0],bins[l][1],bins[l][2],bins[l][3])/hnorm.Integral(bins[l][0],bins[l][1],bins[l][2],bins[l][3])
          sige = ROOT.TMath.Sqrt(h[r][scifiTrack+'_'+X].Integral(bins[l][0],bins[l][1],bins[l][2],bins[l][3]))/hnorm.Integral(bins[l][0],bins[l][1],bins[l][2],bins[l][3])
          print('average efficiency station: %s = %5.2G'%(X,e))
          stats[r]['ineff'][l][X] = [e,sige]
# make plots for note:
   ut.bookCanvas(h,'Tsineff','',1200,900,3,2)
   for s in range(1,6):
          tc = h['Tsineff'].cd(s)
          tc.SetRightMargin(0.2)
          tc.SetLogz(1)
          for p in [-1,0,1]:
            if p<0:X = str(s)
            else: X=str(10*s+p)
            hr['sineff'+X] = hr[scifiTrack+'_'+X].Clone('sineff'+X)
            norm = scifiTrack+'_0'+str(s)
            if norm in hr and unbiased: hr['sineff'+X].Divide(hr[norm])
            else:                       hr['sineff'+X].Divide(hr[scifiTrack+'_0'])
            hr['sineff'+X].SetStats(0)
          hr['sineff'+str(s)].SetMaximum(0.1)
          hr['sineff'+str(s)].SetTitle('')
          hr['sineff'+str(s)].DrawCopy('colz')
          for x in ['TlineTop2'+str(s),'TlineBot2'+str(s),'TlineLef2'+str(s),'TlineRig2'+str(s)]: h[x].Draw('same')
          for i in [2]:
              for x in ['FlineTop2'+str(i),'FlineBot2'+str(i),'FlineLef2'+str(i),'FlineRig2'+str(i)]: hr[x].Draw('same')
   h['Tsineff'].Update()
   myPrint(h['Tsineff'],'ScifiStationInEfficiency_run'+str(r).zfill(6))
   ut.bookCanvas(h,'TsineffS','',1200,900,1,1)
   for S in range(1,6):
    for p in [-1,0,1]:
     if p < 0: s=S
     else: s=S*10+p
     if not 'sineff'+str(s) in hr: continue
     tc = h['TsineffS'].cd()
     tc.SetRightMargin(0.2)
     tc.SetLogz(1)
     hr['sineff'+str(s)] = hr[scifiTrack+'_'+str(s)].Clone('sineff'+str(s))
     X=s
     if s>9:  X = s//10
     norm = scifiTrack+'_0'+str(X)
     if norm in hr and unbiased: hr['sineff'+str(s)].Divide(hr[norm])
     else:                       hr['sineff'+str(s)].Divide(hr[scifiTrack+'_0'])
     hr['sineff'+str(s)].SetTitle('')
     hr['sineff'+str(s)].SetStats(0)
     hr['sineff'+str(s)].SetMaximum(0.2)
     zax = hr['sineff'+str(s)].GetZaxis()
     zax.SetTitle('inefficiency')
     if s>6: hr['sineff'+str(s)].SetMinimum(0.001)
     hr['sineff'+str(s)].Draw('colz')
     tc.Update()
     pal = hr['sineff'+str(s)].FindObject('palette')
     pal.SetX1(0.214)
     for x in ['TlineTop41','TlineBot41','TlineLef41','TlineRig41']: h[x].Draw('same')
     for i in [2]:
        for x in ['FlineTop4'+str(i),'FlineBot4'+str(i),'FlineLef4'+str(i),'FlineRig4'+str(i)]: hr[x].Draw('same')
     h['TsineffS'].Update()
     myPrint(h['TsineffS'],'ScifiStationInEfficiency'+str(s)+'_run'+str(r).zfill(6))
   for proj in ['X','Y']:
      if not 'sineff'+str(s) in hr: continue
      for s in range(1,6):
       for p in [-1,0,1]:
         if p<0:X = str(s)
         else: X=str(10*s+p)
         pname = scifiTrack+'_'+X+'_'+proj
         tc = h['TsineffS'].cd()
         hr['sineff'+X+'_'+proj] = hr[scifiTrack+'_'+X+'_'+proj].Clone('sineff'+X+'_'+proj)
         norm = scifiTrack+'_0'+str(s)+'_'+proj
         if norm in hr and unbiased:  hr['sineff'+X+'_'+proj].Divide(hr[norm])
         else:                        hr['sineff'+X+'_'+proj].Divide(hr[scifiTrack+'_0_'+proj])
         hr['sineff'+X+'_'+proj].SetStats(0)
         if p<0: hr['sineff'+X+'_'+proj].SetMaximum(0.001)
         elif (p==1 and proj=='X') or (p==0 and proj=='Y')  : hr['sineff'+X+'_'+proj].SetMaximum(0.10)
         else: 
           hr['sineff'+X+'_'+proj].SetMaximum(0.020)
           hr['sineff'+X+'_'+proj].SetMinimum(0.006)
         hr['sineff'+X+'_'+proj].Draw('hist')
         myPrint(h['TsineffS'],'ScifiStationInEfficiency'+X+'_'+proj+'_run'+str(r).zfill(6))
         l=2
         if proj=='Y'and p==1 or proj=='X'and p==0:
           opts = 'SQ'
           if proj=='Y': E = ROOT.TF1('E','1-[0]*exp(-x/[1])',10,60)
           if proj=='X': E = ROOT.TF1('E','1-[0]*exp(x/[1])',10,60)
           E.SetParameter(0,0.98)
           E.SetParameter(1,-1000)
           if proj=='Y': rc = hr['sineff'+X+'_'+proj].Fit(E,opts,'',limits[2]['Y'][0],limits[2]['Y'][1])
           if proj=='X': rc = hr['sineff'+X+'_'+proj].Fit(E,opts,'',limits[2]['X'][0],limits[2]['X'][1])
           result = rc.Get()
           stats[r]['ineff'][l][X].append([result.Parameter(0),result.ParError(0)])
           stats[r]['ineff'][l][X].append([result.Parameter(1),result.ParError(1)])
           hr['sineff'+X+'_'+proj].Draw()
           myPrint(h['TsineffS'],'ScifiStationInEfficiency'+X+'_'+proj+'_run'+str(r).zfill(6))
   ut.bookHist(hr,'attLength','attLength; L [m]',10,0,100)
   ut.bookCanvas(h,'TattLength','',900,600,1,1)
   tc = h['TattLength'].cd()
   for s in range(1,6):
    for p in [0,1]:
      X=str(10*s+p)
      rc = hr['attLength'].Fill(abs(stats[r]['ineff'][2][X][3][0]/100.))
   hr['attLength'].Draw()
   myPrint(h['TattLength'],'attLength_run'+str(r).zfill(6))
  if len(stats)<2: return
# make evolution plot
  for r in stats:
   if len(stats[r])<1:continue
   timeRange[stats[r]['utc']]={}
   for l in limits :
      timeRange[stats[r]['utc']][l]={}
      for s in range(1,6): 
       for p in [-1,0,1]:
        if p<0: S = str(s)
        else: S=str(10*s+p)
        timeRange[stats[r]['utc']][l][S]=[ stats[r]['ineff'][l][S][0],stats[r]['ineff'][l][S][1] ]
  T = list(timeRange.keys())
  T.sort()
  tstart = T[0]
  tend = T[len(T)-1]
  n = 0
  l = 2
  for t in T:
     for s in range(1,6):
       if timeRange[t][l][str(s)][0]<1E-9 or timeRange[t][l][str(s)][0]>1 :
         print('exclude time',s,t,l,timeRange[t][l][str(s)][0])
         continue
       for p in [-1,0,1]:
        if p<0: S = str(s)
        else: S=str(10*s+p)
        if not 'evol_'+S in h: h['evol_'+S] = ROOT.TGraphErrors()
        h['evol_'+S].SetPoint(n,t,timeRange[t][l][S][0])
        h['evol_'+S].SetPointError(n,500,timeRange[t][l][S][1])
     n+=1
  delta = (tend-tstart)*0.025
  dateA = '07-01,2022-0'
  dateB = '12-01,2022-0'
  time_objA = time.strptime(dateA,'%m-%d,%Y-%H')
  time_objB = time.strptime(dateB,'%m-%d,%Y-%H')
  TA = calendar.timegm(time_objA)
  TB = calendar.timegm(time_objB)
  ut.bookHist(h,'inEff',';time ; inEff',300,TA,TB)
  #ut.bookHist(h,'inEff',';time ; inEff',300,tstart-delta,tend+delta)
  h['inEff'].GetXaxis().SetTimeFormat("%d-%m")
  h['inEff'].GetXaxis().SetTimeOffset(0,'gmt')
  h['inEff'].GetXaxis().SetNdivisions(520)
  h['inEff'].GetYaxis().SetMaxDigits(2)
  h['inEff'].SetMinimum(0)
  h['inEff'].SetStats(0)
  h['inEff'].SetMaximum(0.75E-3)
  colors=[ROOT.kGreen,ROOT.kBlue,ROOT.kCyan,ROOT.kMagenta,ROOT.kRed]
  for p in ['','0','1']:
   ut.bookCanvas(h,'TinEff'+p,'',2400,800,1,1)
   tc = h['TinEff'+p].cd()
   if not p=='':
     h['inEff'+p] = h['inEff'].Clone('inEff'+p)
     h['inEff'+p].SetMaximum(0.023)
     h['inEff'+p].SetMinimum(0.006)
   h['inEff'+p].Draw()
   tc.SetGridx(1)
   tc.SetGridy(1)
   h['lscifi'+p]=ROOT.TLegend(0.72,0.56,0.89,0.93)
   for s in range(1,6):
     X=str(s)+p
     h['evol_'+X].SetMarkerStyle(20+s)
     h['evol_'+X].SetMarkerColor(colors[s-1])
     h['evol_'+X].SetLineColor(colors[s-1])
     h['evol_'+X].Draw('sameP')
     h['evol_'+X].Draw('same')
     if p=='':   L = h['lscifi'+p].AddEntry(h['evol_'+X],'station '+str(s),"L")
     if p=='0':  L = h['lscifi'+p].AddEntry(h['evol_'+X],'station '+str(s)+ "H plane","L")
     if p=='1':  L = h['lscifi'+p].AddEntry(h['evol_'+X],'station '+str(s)+ "V plane","L")
     L.SetTextColor(colors[s-1])
   h['lscifi'+p].Draw()
   myPrint(h['TinEff'+p],'ScifiInEffOverTime'+p)
   fp = ROOT.TFile.Open('ScifiInEffStats.root','recreate')
   pkl = Pickler(fp)
   pkl.dump(stats,'stats')
   fp.Close()

