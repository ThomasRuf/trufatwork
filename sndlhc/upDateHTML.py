import ROOT,os,sys,subprocess
import time
import rootUtils as ut
import shipunit as u
from XRootD import client
from XRootD.client.flags import DirListFlags, OpenFlags, MkDirFlags, QueryCode

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--rmin",      dest="rmin", help="last run",default=6583,type=int)
parser.add_argument("--server", dest="server", help="xrootd server",default=os.environ["EOSSHIP"])
parser.add_argument("--postScale", dest="postScale",help="post scale events, 1..10..100", default=-1,type=int)
parser.add_argument("--rawDataPath", dest="rawDataPath",help="rawDataPath", default="/eos/experiment/sndlhc/raw_data/physics/2023_tmp/")
parser.add_argument("--path", dest="path",help="path", default="/eos/experiment/sndlhc/convertedData/physics/2023/")
options = parser.parse_args()
options.dashboard = "/mnt/raid1/data_online/run_status.json"
def StartTime(r):
      runDir = options.rawDataPath+"run_"+str(r).zfill(6)
      jname = "run_timestamps.json"
      with client.File() as f:
           f.open(options.server+runDir+"/run_timestamps.json")
           status, jsonStr = f.read()
      X = jsonStr.decode()
      date = eval(X)
      s = date['start_time'].replace('Z','')
      if 'stop_time' in date:
          s += " - "+ date['stop_time'].replace('Z','')
      return s
         
def nEvents(r):
    partitions = []
    dirlist  = str( subprocess.check_output("xrdfs "+options.server+" ls "+options.path+"run_"+str(r).zfill(6),shell=True) )
    for x in dirlist.split('\\n'):
         ix = x.find('sndsw_raw-')
         if ix<0: continue
         partitions.append(x[ix:])
    eventChain = ROOT.TChain('rawConv')
    for p in partitions:
      eventChain.Add(options.server+options.path+'run_'+str(r).zfill(6)+'/'+p)
    rc = eventChain.GetEvent(0)
    return eventChain.GetEntries()

filelist  = str( subprocess.check_output("xrdfs root://eospublic.cern.ch/ ls /eos/experiment/sndlhc/www/offline",shell=True) )
runList = {}
for f in filelist.split('\\n'):
   if f.find('root')<0: continue
   if f.find('run')<0: continue
   tmp = f.split('/')
   fname = tmp[len(tmp)-1]
   r = int(fname.split('.')[0].replace('run',''))
   runList[r] = fname
runs = list(runList.keys())
runs.reverse()

destination="offline"
rc = os.system("xrdcp -f "+os.environ['EOSSHIP']+"/eos/experiment/sndlhc/www/"+destination+".html  . ")
old = open(destination+".html")
oldL = old.readlines()
old.close()
tmp = open("tmp.html",'w')
finished = False
for L in oldL:
    if L.find('Current runs 2023')<0 or finished:
      tmp.write(L)
      continue
    for r in runs:
      if r < options.rmin: break
      startTime = StartTime(r)
      N = nEvents(r)
      startTime += " #events="+str(N)
      ftmp = ROOT.TFile.Open(os.environ['EOSSHIP']+"/eos/experiment/sndlhc/www/"+destination+"/"+runList[r])
      if not ftmp.daq.Get('T'):
         print('++++ ATTENTION ++++ something wrong with ',ftmp.GetName())
         continue
      postScale = int(N/ftmp.daq.T.FindObject('time').GetEntries()+0.5)
      Lnew = '            <li> <a href="https://snd-lhc-monitoring.web.cern.ch/'+destination+'/run.html?file=run'
      Lnew+= str(r).zfill(6)+'.root&lastcycle">run '+str(r)+' </a>'+startTime
      if postScale>1: Lnew+="  post scaled:"+str(postScale)
      Lnew+='\n'
      tmp.write(Lnew)
      print(Lnew)
tmp.close()
#os.system('cp '+destination+'.html '+destination+time.ctime().replace(' ','')+'.html ')  # make backup
#rc = os.system("xrdcp -f "+destination+".html  "+os.environ['EOSSHIP']+"/eos/experiment/sndlhc/www/")

def timeALign(run,online=False):
   if not online: f=ROOT.TFile.Open(os.environ['EOSSHIP']+'/eos/experiment/sndlhc/www/offline/run'+str(run).zfill(6)+'.root')
   else:         f=ROOT.TFile.Open(os.environ['EOSSHIP']+'/eos/experiment/sndlhc/www/online/run'+str(run).zfill(6)+'.root')
   dT = f.daq.boards.FindObject('Tboard').Clone('Tb')
   xax = dT.GetXaxis()
   for ix in range(xax.GetNbins()):
       tmp = dT.ProjectionY('tmp',ix+1,ix+1)
       if tmp.GetEntries()>1000:
          M = tmp.GetMean()
          rc = tmp.Fit('gaus','SQ')
          fr = rc.Get()
          M =  fr.Parameter(1)
          print('board %i : dT (42) %5.2F'%(int(xax.GetBinCenter(ix+1)+0.5),M))
       
       
