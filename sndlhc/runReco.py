import os,subprocess,ROOT
runs = [4004,4006,4010,4011,4016,4018,4019,4020,4046,4060,4061,4062,4063,4066,4067,4069,4070,4071,4073,4074,4075,4077,4078,4062,4063,4067,4069,4071,4073,4075,4078,4093,4112]

def run():
   for r in runs:
     os.system("python $SNDSW_ROOT/shipLHC/scripts/run_TrackSelections.py -o RunWithTracks"+str(r)+".root -p /eos/experiment/sndlhc/convertedData/commissioning/TI18/ -g ../geofile_sndlhc_TI18.root -t  Scifi --withTrack --goodEvents --save -r "+str(r))

def merge():
   command = "hadd RunWithTracks"+str(runs[0])+"-"+str(runs[len(runs)-1])+".root "
   for r in runs:
         command+= " RunWithTracks"+str(r)+".root "
   os.system(command)
   
def inspect():
    fullList = {}
    dirlist  = str( subprocess.check_output("xrdfs root://snd-server-1.cern.ch/  ls -l /mnt/raid1/data_online/",shell=True) ) 
    for L in dirlist.split('\\n'):
      if L.find("run_")<0: continue
      x = L.split()
      D = x[len(x)-1]
      filelist  = str( subprocess.check_output("xrdfs root://snd-server-1.cern.ch/  ls -l "+D,shell=True) )
      for F in filelist.split('\\n'):
        if F.find('.root')<0: continue
        x = F.split()
        dataFile = x[-1]
        f = ROOT.TFile.Open('root://snd-server-1.cern.ch/'+dataFile)
        size = f.event.GetEntries()
        f.Close()
        x = dataFile.split("/")
        partition = int(x[-1][5:9])
        if not D in fullList: fullList[D]=[]
        fullList[D].append([partition,size])
    return fullList
    
def runMonitoring(lastRun,minEvents=10000):
   fullList = inspect()
   for d in fullList:
       r = int(d.split('_')[2])
       if not r > lastRun: continue
       for p in fullList[d]:
           if p[1]< minEvents: continue
           print('executing run ',r)
           command = "python $SNDSW_ROOT/shipLHC/scripts/run_Monitoring.py --server=root://snd-server-1.cern.ch/ -p /mnt/raid1/data_online/  -g ../geofile_sndlhc_TI18.root"
           os.system(command +" --sudo -M -r "+str(r)+" -P "+str(p[0])+" --batch ")
           print("finished run ",r)
           
def statsFromMonitoring(lastRun):
   stats = {}
   dirlist  = str( subprocess.check_output("xrdfs "+os.environ['EOSSHIP']+"  ls -l /eos/experiment/sndlhc/www/online/",shell=True) )
   for L in dirlist.split('\\n'):
      if L.find(".root")<0: continue
      if not L.find('dcs')<0: continue
      fname = '/eos'+L.split('/eos')[1]
      r = int( fname[fname.find('run')+3:fname.find('.root')] )
      if not r > lastRun: continue
      F = ROOT.TFile.Open(os.environ['EOSSHIP']+fname)
      # scifi tracks
      scifiCanvas = F.scifi.Get("scifi-trackDir")
      X = F.scifi.Get("scifi-trackDir").FindObject('scifi-trackSlopes')
      nBeam = X.GetSumOfWeights()
      X = F.scifi.Get("scifi-trackDir").FindObject('scifi-trackSlopesXL')
      nTot = X.GetSumOfWeights()
      if nTot>10: print('run %i: total= %i beam= %i '%(r,nTot,nBeam))
      stats[r]=[nTot,nBeam]
   nBeam = 0
   nTot = 0
   for r in stats:
        nBeam+=stats[r][1]
        nTot+=stats[r][0]
   print('total: all= %i beam= %i '%(nTot,nBeam))
   return stats

# take raw data from onine cluster
def convertRuns():
   runs = [4062,4063,4067,4069,4071,4073,4075,4078,4093,4112]
   command = "python $SNDSW_ROOT/shipLHC/rawData/runProd.py -r 4062,4063,4067,4069,4071,4073,4075,4078,4093,4112 -c convert --server=root://snd-server-1.cern.ch/"
   

      


