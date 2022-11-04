import os,subprocess,time,multiprocessing
import pwd
import ROOT
ncpus = multiprocessing.cpu_count() - 10
def count_python_processes(macroName):
    username = pwd.getpwuid(os.getuid()).pw_name
    callstring = "ps -f -u " + username
# only works if screen is wide enough to print full name!
    status = subprocess.check_output(callstring,shell=True)
    n=0
    for x in status.decode().split('\n'):
        if not x.find(macroName)<0 and not x.find('python') <0: n+=1
    return n

"""
- Run 46, 180 GeV, gain 2.50      
- Run 49, 180 GeV, gain 3.65     
- Run 52, Beam Muons, gain 3.65    
- Run 54, Beam Muons, gain 2.50   
- Run 56, 140 GeV, gain 2.50     
- Run 58, 140 GeV, gain 3.65      
- Run 72, 240 GeV, gain 1.00     
- Run 73, 240 GeV, gain 2.50      
- Run 74, 240 GeV, gain 3.65r    
- Run 86, Cosmics, gain 3.65   
- Run 87, Cosmics, gain 2.50
- Run 88, Cosmics, gain 1.00 (First half of the run, second half had beam)
- Run 89, 300 GeV, gain 3.65        
- Run 90, 300 GeV, gain 2.50       
- Run 91, 300 GeV, gain 1.00      
                                done 5M
"""
Nevents = str(int(15*1E6))

path = "/eos/experiment/sndlhc/testbeam/MuFilter/TB_data_commissioning/"

runList = [46,47,49,50,51,52,53,54,55,56,58,59,60,71,72,73,74,80,81,82,86,87,88,89,90,91]


pathConv = "/eos/experiment/sndlhc/convertedData/MuFilter/TB_data_commissioning/"
pathConv = "/eos/experiment/sndlhc/convertedData/MuFilter/TB_data_commissioning-NewCalib/"

def exe(runList):
  for run in runList:
    os.system("python $SNDSW_ROOT/shipLHC/rawData/convertRawData_muTestbeam.py  -r "+str(run)+"  -p "+path+" -n "+Nevents+"  &")
    while count_python_processes('convertRawData')>ncpus: 
       time.sleep(200)
def copy(runList):
  for run in runList:
    os.system("xrdcp sndsw_raw_0000"+str(run)+".root  "+os.environ['EOSSHIP']+path)

import ROOT
def stats(runList,option ='eos'):
  if option == 'eos': path = os.environ['EOSSHIP']+path
  elif option == 'sshfs': path = "/home/truf/ubuntu-1710/ship-ubuntu-1710-48/SND/testbeam/mufi"
  else : path = "./"
  for run in runList:
     f=ROOT.TFile.Open(path+"/sndsw_raw_0000"+str(run)+".root")
     if f.Get('rawConv'): print(run,':',f.rawConv.GetEntries())
def rawStats(runList):
  for run in runList:
     f=ROOT.TFile.Open(os.environ['EOSSHIP']+path+"run_"+str(run).zfill(6)+'/data.root')
     print(run,':',f.event.GetEntries())
def makeHistos(runList):
  for run in runList:
    command = "Survey-MufiScifi.py -r "+str(run)+" -p "+pathConv+" -g geofile_sndlhc_H6.root -c Mufi_Efficiency -n -1 -t DS"
    os.system("python "+command+ " &")
    while count_python_processes('Survey-MufiScifi')>ncpus: 
       time.sleep(200)
def mips(runList):
  for run in runList:
    command = "Survey-MufiScifi.py -r "+str(run)+" -p "+pathConv+" -g geofile_sndlhc_H6.root -c mips"
    os.system("python "+command+ " &")
    while count_python_processes('Survey-MufiScifi')>multiprocessing.cpu_count()-2: 
       time.sleep(200)
def largeVSsmall(runList):
  for run in runList:
    command = "Survey-MufiScifi.py -b 100000 -r "+str(run)+" -p "+pathConv+" -g geofile_sndlhc_H6.root -c  smallVsLargeSiPMs "
    os.system("python "+command+ " &")
    while count_python_processes('Survey-MufiScifi')>multiprocessing.cpu_count()-2: 
       time.sleep(200)
def anyCommand(c):
  for run in runList:
    command = "Survey-MufiScifi.py -b 100000 -r "+str(run)+" -p "+pathConv+" -g geofile_sndlhc_H6.root -c "+c
    os.system("python "+command+ " &")
    while count_python_processes('Survey-MufiScifi')>multiprocessing.cpu_count()-2: 
       time.sleep(200)

