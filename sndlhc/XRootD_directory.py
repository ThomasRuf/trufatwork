import ROOT,os

from XRootD import client
from XRootD.client.flags import DirListFlags

myclient = client.FileSystem(os.environ['EOSSHIP'])
status, listing = myclient.dirlist('/eos/experiment/sndlhc/convertedData/MuFilter/TB_data_commissioning/sndsw/', DirListFlags.STAT)

print(listing.parent)
for entry in listing:
  if entry.name.find('root')<0: continue
  f = ROOT.TFile.Open(os.environ['EOSSHIP']+listing.parent+'/'+entry.name)
  print("%s %s size = %5.2FGB   N events =%10i"%(entry.name,entry.statinfo.modtimestr, entry.statinfo.size/1E9, f.rawConv.GetEntries()))

