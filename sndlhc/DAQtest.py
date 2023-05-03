import os
import ROOT
import rootUtils as ut

h={}
runs = [5170,5171,5180]
runs = [5170]
flavors = {"":1,"maxduration_4_hitgap_0_clkalign_False":2,"maxduration_4_hitgap_0_clkalign_True":6,
                  "maxduration_6_hitgap_1_clkalign_False":3,"maxduration_6_hitgap_1_clkalign_True":7,
                  "maxduration_8_hitgap_1_clkalign_False":4,"maxduration_8_hitgap_1_clkalign_True":8}

if 1<0:
   for o in flavors:
      os.system("mkdir /eos/experiment/sndlhc/convertedData/commissioning/event_builder_test_202301/"+o)
      os.system("ln -s /eos/experiment/sndlhc/convertedData/physics/2022/geofile_sndlhc_TI18_V0_2022.root /eos/experiment/sndlhc/convertedData/commissioning/event_builder_test_202301/"+o+"geofile_sndlhc_TI18_V0_2022.root")
def convert():
   command = "python $SNDSW_ROOT/shipLHC/rawData/runProd.py -P test -c convert -cpp"
   # python $SNDSW_ROOT/shipLHC/rawData/runProd.py -P test -c convert -cpp -p /eos/experiment/sndlhc/raw_data/physics/2022_desync_check/ -r 5178 -d /eos/experiment/sndlhc/convertedData/physics/2022/
   for r in runs:
    for o in flavors:
      command += " -r "+str(r)
      command += " -p /eos/experiment/sndlhc/raw_data/commissioning/event_builder_test_202301/"+o+'/'
      command += " -d /eos/experiment/sndlhc/convertedData/commissioning/event_builder_test_202301/"+o+'/'
      os.system(command)
def monitoring():
   command = "python $SNDSW_ROOT/shipLHC/run_Monitoring.py "
   for o in flavors:
    os.system('mkdir '+o)
    os.chdir(o)
    for r in runs:
      command += " -r "+str(r)
      command += " -p /eos/experiment/sndlhc/convertedData/commissioning/event_builder_test_202301/"+o+"/"
      command += "  --batch -b 1000000 --parallel 10"
      os.system(command)
    os.chdir('../')

def printStats(statistics,var,name,withMean,withRMS,prec='"%10i"'):
   txt = "                       %15s"%(name)
   for r in runs:
      txt += "        "+str(r)
   print(txt)
   for o in flavors:
    txt = "%40s"%(o)
    for r in runs:
       if withRMS:
          txt+=eval('  '+prec+",%5.2F'%(statistics[r][o][var][0],statistics[r][o][var][1])")
       elif withMean:
          txt+='   '+eval('  '+prec+'%(statistics[r][o][var][1])')
          txt+='   '+eval('  '+prec+'%(statistics[r][o][var][1]-statistics[r][""][var][1])')
       else:
          txt+='   '+eval('  '+prec+'%(statistics[r][o][var][0])')
          txt+='   '+eval('  '+prec+'%(statistics[r][o][var][0]-statistics[r][""][var][0])')
    print(txt)

def stats():
   # path = "/home/truf/ubuntu-1710/sndlhc-sndproduction/event_builder_test_202301/"
   path = "./"
   listOfHists = ["daq/T:Etime","scifi/scifi-trackDir:scifi-trackSlopes","mufilter/muonDSTracks:mufi-slopes"]
   for m in range(30): listOfHists.append("scifi/scifi-hitmaps:scifi-mat_"+str(m))
   for o in ['L','R']:
     for s in [10,11,20,21,22,23,24]:
         listOfHists.append("mufilter/signalUSVeto:mufi-sig"+o+"_"+str(s))
     for s in [30,31,32,33,34,35,36]:
         listOfHists.append("mufilter/signalUSVeto:mufi-sig"+o+"_"+str(s))
   listOfHists.append("daq/boardmaps:scifiboard")
   listOfHists.append("daq/boardmaps:mufiboard")
   listOfHists.append("daq/boards:Cckboard")
#
   statistics = {}
   for r in runs:
    statistics[r] = {}
    h[r]={}
    for o in flavors:
      statistics[r][o] = {}
      h[r][o] = {}
      F = ROOT.TFile(path+o+"/run00"+str(r)+'.root')
      ROOT.gROOT.cd()
      for x in listOfHists:
         g = x.split(':')
         h[r][o][g[0]] = F.Get(g[0]).Clone(g[0])
         if not h[r][o][g[0]].FindObject(g[1]) : continue
         h[r][o][x] = h[r][o][g[0]].FindObject(g[1]).Clone(x)
         tmp = h[r][o][x]
         if tmp:
           if g[0]=='daq/boardmaps':
            nTot = 0
            for b in range(tmp.GetNbinsX()+1):
                proj = tmp.ProjectionY('proj',b,b)
                for N in range(1,tmp.GetNbinsY()+1):
                   nTot+=proj.GetBinContent(N)*int(proj.GetBinCenter(N)+0.5)
                   # print(b,N,proj.GetBinContent(N),int(proj.GetBinCenter(N)+0.5),nTot)
            statistics[r][o][x] = [nTot,tmp.GetMean(),tmp.GetRMS()]
           elif g[0]=='daq/boards':
            statistics[r][o][x] = []
            for k in range(tmp.GetNbinsX()):
                proj = tmp.ProjectionY('proj',k+1,k+1)
                if proj.GetEntries()==0: continue
                statistics[r][o][x].append(proj.GetMean())
           else:
            statistics[r][o][x] = [tmp.GetEntries(),tmp.GetMean()]
   printStats(statistics,"daq/T:Etime","N events",False,False)
   printStats(statistics,"scifi/scifi-trackDir:scifi-trackSlopes","N scifi tracks",False,False)
   printStats(statistics,"mufilter/muonDSTracks:mufi-slopes","N DS tracks",False,False)
   printStats(statistics,"daq/boardmaps:scifiboard","total scifi hits",False,False,'"%10i"')
   printStats(statistics,"daq/boardmaps:mufiboard","total mufi hits",False,False,'"%10i"')
   printStats(statistics,"daq/boardmaps:scifiboard","mean scifi hits per event",True,False,'"%5.4F"')
   printStats(statistics,"daq/boardmaps:mufiboard","mean mufi hits per event",True,False,'"%5.4F"')
   for r in runs:
       ut.bookCanvas(h,'tboard'+str(r),'',1800,900,4,2)
       for o in flavors:
          tc = h['tboard'+str(r)].cd(flavors[o])
          tc.SetLogz(1)
          h[r][o]["daq/boards:Cckboard"].SetStats(0)
          h[r][o]["daq/boards:Cckboard"].SetTitle("160Mhz bunch nr "+o+";board nr;hit timestamp")
          h[r][o]["daq/boards:Cckboard"].Draw('colz')
       for fm in ['.png','.root']: h['tboard'+str(r)].Print('tboard'+str(r)+fm)
   return statistics

from rootpyPickler import Unpickler
fg  = ROOT.TFile.Open(os.environ['EOSSHIP']+"/eos/experiment/sndlhc/convertedData/physics/2022/RunInfodict.root")
pkl = Unpickler(fg)
runInfo = pkl.load('runInfo')
fg.Close()


def timestamp(withDisplay=False):
  # runs=[4449,4612,4724,4964,5109,5120,5144,5263,5408]
  runs = []
  for r in runInfo:
     if len(runInfo[r]['partitions']) > 50:
        runs.append(r)
  flavors={'': 1}
  meanHitTimes = {}
  for r in runs:
    meanHitTimes[r] = {}
    for o in flavors:
       meanHitTimes[r][o] = {}
       if o.find('max')==0: path = "/eos/experiment/sndlhc/raw_data/commissioning/event_builder_test_202301/"+o+'/'
       else: path = "/eos/experiment/sndlhc/raw_data/physics/2022/"
       ut.bookHist(h,'eventTime'+o,'evt_timestamp%4 '+o,5,-0.5,4.5)
       ut.bookHist(h,'timestamp'+o,'timestamp '+o,70,-0.5,69.5,100,-1.,9.)
       f=ROOT.TFile.Open(os.environ['EOSSHIP']+path+'run_'+str(r).zfill(6)+'/data_0005.root')
       ROOT.gROOT.cd()
       f.data.Draw('evt_timestamp%4>>eventTime'+o)
       f.data.Draw('timestamp:board_id>>timestamp'+o)
    if withDisplay:
     ut.bookCanvas(h,'Ttimestamp'+str(r),'',1800,900,4,2)
     ut.bookCanvas(h,'Ttimestamp2'+str(r),'',1800,900,4,2)
     ut.bookCanvas(h,'TeventTime'+str(r),'',1800,900,4,2)
     for o in flavors:
       tc = h['Ttimestamp'+str(r)].cd(flavors[o])
       h['timestamp'+o+'proj'] = h['timestamp'+o].ProjectionY('timestamp'+o+'proj')
       h['timestamp'+o+'proj'].Draw()
       tc = h['Ttimestamp2'+str(r)].cd(flavors[o])
       tc.SetLogz(1)
       h['timestamp'+o].Draw('colz')
       tc = h['TeventTime'+str(r)].cd(flavors[o])
       h['eventTime'+o].Draw()
     for t in ['Ttimestamp'+str(r),'Ttimestamp2'+str(r),'TeventTime'+str(r)]:
       for fm in ['.png','.root']: h[t].Print(t+fm)
    for o in flavors:
       tmp = h['timestamp'+o].ProjectionY('tmp')
       meanHitTimes[r][o] = [tmp.GetMean(),runInfo[r]['StartTimeC'],runInfo[r]['StartTime']]
  print('mean hit times')
  O = open('meanHitTimes.txt','w')
  runs.sort()
  for r in runs:
    for o in flavors:
      txt = "%8i %s %i15 %5.3F"%(r,meanHitTimes[r][o][1],meanHitTimes[r][o][2],meanHitTimes[r][o][0])
      print(txt)
      O.write(txt+"\n")
  O.close()

def printVetoEff(prev=100):
   if prev==100:  runs=[4626,4964,5120,5125,5408,4744,5109,5170,5180,5350]
   if prev==1000: runs=[4964,5125,5350]
   runs.sort()
   vetoEfficiency(runs,v='',name='allHistos-run00XXXX.root')
def scifiEff(name='allHistos-run00XXXX.root'):
   path = "./"
   runs=[4626,4964,5120,5408,4744,5109,5350]
   runs.sort()
   wa = ['eff','DStag','scifiTrack','dx','dy']
   for s in range(6): wa.append('scifiTrack_'+str(s))
   for r in runs:
     fname = path+'/'+name.replace('XXXX',str(r))
     h[r]={}
     ut.readHists(h[r],fname,wanted=wa)
     if len(h[r])<1: continue
     limits = {1:{'X':[-44,-8],'Y':[16,50]},2:{'X':[-40,-12],'Y':[18,47]}}
     bins = {}
     for l in limits :
        bins[l] = []
        for p in limits[l]:
           for x in limits[l][p]:
             bins[l].append(h[r]["scifiTrack_0_proj"+p.lower()].FindBin(x))
     for l in limits :
        for p in limits[l]:
           for s in range(1,6):
             X = "scifiTrack_"+str(s)+'_proj'+p.lower()
             h[r]['eff_'+X] =  h[r][X].Clone('eff_'+X)
             h[r]['eff_'+X].Divide(h[r]["scifiTrack_0_proj"+p.lower()])
             h[r]['eff_'+X].SetMaximum(0.01)
             h[r]['eff_'+X].SetMinimum(0.0)
           if p=='X': 
              h[r]['trackEff'+p+str(l)]=h[r]['scifiTrack'].ProjectionX('trackEff'+p+str(l)+str(r))
              h[r]['trackEff'+p+str(l)].Reset()
              for ix in range(1,h[r]['scifiTrack'].GetNbinsX()+1):
               A = 0
               B = 0
               for iy in range(bins[l][2],bins[l][3]):
                 B += h[r]['scifiTrack'].GetBinContent(ix,iy)
                 A += h[r]['DStag'].GetBinContent(ix,iy)
               h[r]['trackEff'+p+str(l)].SetBinContent(ix,B/A)
           if p=='Y': 
              h[r]['trackEff'+p+str(l)]=h[r]['scifiTrack'].ProjectionY('trackEff'+p+str(l)+str(r))
              h[r]['trackEff'+p+str(l)].Reset()
              for iy in range(1,h[r]['scifiTrack'].GetNbinsY()+1):
               A = 0
               B = 0
               for ix in range(bins[l][0],bins[l][1]):
                 B += h[r]['scifiTrack'].GetBinContent(ix,iy)
                 A += h[r]['DStag'].GetBinContent(ix,iy)
               h[r]['trackEff'+p+str(l)].SetBinContent(iy,B/A)
           
def vetoEfficiency(runs,v='',name='run00XXXX_WithVetoEff.root'):
  path = "./"
  noiseCuts = [5] # [1,5,10,12]
  for r in runs:
   h[r]={}
   for o in flavors:
     h[r][o] = {}
     fname = path+o+'/'+name.replace('XXXX',str(r))
     if not os.path.isfile(fname):
         print(fname +'not found')
         continue
     print('*** analyzing '+fname)
     wa = ['scaler']
     for noiseCut in noiseCuts:
        for c in ['','NoPrev']:
          for b in ['','beam']:
               nc = 'T'+c+str(noiseCut)+b
               for l in range(2):
                 wa.append(nc+'PosVeto_'+str(l))
                 wa.append(nc+'XPosVeto_'+str(l))
               wa.append(nc+'PosVeto_11')
               wa.append(nc+'PosVeto_00')
               wa.append(nc+'XPosVeto_11')
          wa.append('T'+c+'1PosVeto_0')
          wa.append('T'+c+'1XPosVeto_0')
          wa.append('scifi_trackChi2/ndof')
           
     ut.readHists(h[r][o],fname,wanted=wa)
     hr = h[r][o]
     for c in ['','NoPrev']:
      allTracks = hr['T'+c+'1PosVeto_0'].Clone('tmp')
      allTracks.Add(hr['T'+c+'1XPosVeto_0'])
      for noiseCut in noiseCuts:
       nc = 'T'+c+str(noiseCut)+v
       hr[nc+'XPosVeto_00']=allTracks.Clone(nc+'XPosVeto_00')
       hr[nc+'XPosVeto_00'].Add(hr[nc+'PosVeto_00'],-1)

# make some printout
       Ntot = hr[nc+'PosVeto_0'].Clone('Ntot')
       Ntot.Add(hr[nc+'XPosVeto_0'])
       ineff0 =  hr[nc+'XPosVeto_0'].GetEntries()/Ntot.GetEntries()
       ineff1 = hr[nc+'XPosVeto_1'].GetEntries()/Ntot.GetEntries()
       ineffOR =  hr[nc+'XPosVeto_11'].GetEntries()/Ntot.GetEntries()
       ineffAND = 1.-hr[nc+'PosVeto_11'].GetEntries()/Ntot.GetEntries()
       region = [21,91,34,89]
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
     print('%5.2F%% of events with a Scifi track have a prev event '%(100*(1-h[r][o]['scaler'][2]/h[r][o]['scaler'][1])))
     if r==5125: muAv = 43.4
     elif r==5170: muAv = 48.2
     else: muAv = runInfo[r]['muAv']['']
     print('mu = %5.2F'%(muAv))
