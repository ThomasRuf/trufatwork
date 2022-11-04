import ROOT,os
listOfFiles = ["sndsw_raw_000046.root","sndsw_raw_000047.root","sndsw_raw_000049.root","sndsw_raw_000050.root","sndsw_raw_000051.root","sndsw_raw_000052.root",
"sndsw_raw_000053.root","sndsw_raw_000054.root","sndsw_raw_000055.root","sndsw_raw_000056.root","sndsw_raw_000058.root","sndsw_raw_000059.root",
"sndsw_raw_000060.root","sndsw_raw_000061.root","sndsw_raw_000062.root","sndsw_raw_000063.root","sndsw_raw_000071.root","sndsw_raw_000072.root",
"sndsw_raw_000073.root","sndsw_raw_000074.root","sndsw_raw_000080.root","sndsw_raw_000081.root","sndsw_raw_000082.root",
"sndsw_raw_000086.root","sndsw_raw_000087.root","sndsw_raw_000088.root","sndsw_raw_000089.root","sndsw_raw_000090.root","sndsw_raw_000091.root"]
badFiles = ["sndsw_raw_000050.root"]

path    = os.environ['EOSSHIP']+"/eos/experiment/sndlhc/convertedData/MuFilter/TB_data_commissioning-NewCalib/"
newpath = os.environ['EOSSHIP']+"/eos/experiment/sndlhc/convertedData/commissioning/TB_H8_october/"

for F in listOfFiles:
    if F in badFiles: continue
    os.system('xrdcp '+path+F+" "+F)
    f = ROOT.TFile.Open(F,'update')
    eventTree = f.rawConv
    if not eventTree.GetBranch('Digi_MuFilterHits'): eventTree.GetBranch('Digi_MuFilterHit').SetName("Digi_MuFilterHits")
    eventTree.Write()
    f.Close()
    location = F.replace("sndsw_raw","run").replace('.root','/')+"sndsw_raw-0000.root"
    os.system('xrdcp -f '+F+" "+newpath+location)
    os.system('rm '+F)

def makeMonitorFiles():
  for F in listOfFiles:
    if F in badFiles: continue
    location = F.replace("sndsw_raw","run").replace('.root','/')+"sndsw_raw-0000.root"
    run = str(int(F.split('_')[2].split('.')[0]))
    command = "python $SNDSW_ROOT/shipLHC/scripts/run_Monitoring.py --server=$EOSSHIP -p /eos/experiment/sndlhc/convertedData/commissioning/TB_H8_october/  -g geofile_sndlhc_H6.root -r "+run+" -P 0 --batch -n 1000000"
    os.system(command)
    os.system("xrdcp -f run0000"+run+".root $EOSSHIP/eos/experiment/sndlhc/www/H8/run0000"+run+".root")
