import ROOT
import os
import rootUtils as ut
h={}

# a basic example how to open a file and loop over events and hits

path = "/eos/experiment/sndlhc/testbeam/MuFilter/TB_data_commissioning/sndsw/"

# for later access to geometry info
import SndlhcGeo
geo = SndlhcGeo.GeoInterface(os.environ['EOSSHIP']+path+"geofile_sndlhc_H6.root")
MuFilter = geo.modules['MuFilter']

# histogram
ut.bookHist(h,'histo1','US bars fired',10,-0.5,9.5)

# data file
f=ROOT.TFile.Open(os.environ['EOSSHIP']+path+"sndsw_raw_000046.root")
eventTree = f.rawConv

N=0
Nev = 10  # just loop over 10 events
for event in eventTree:
    N+=1
    if N>Nev: break
# for each event loop over mufilter hits
    print('now at event:',N)
    for aHit in event.Digi_MuFilterHit:
        if not aHit.isValid(): continue
        detID = aHit.GetDetectorID()
        if aHit.isVertical():     withX = True
        s = detID//10000
        l  = (detID%10000)//1000  # plane number
        bar = (detID%1000)
        nSiPMs = aHit.GetnSiPMs()
        nSides  = aHit.GetnSides()
        print('ahit:',s,l,bar)
        if s==2: rc = h['histo1'].Fill(bar)
#
h['histo1'].Draw()
print('try: help(aHit) and typing aHit. followed by tab')
print('try: f.ls(), will show you the content of the file')
print('eventTree.Print(), shows you the branches of event tree')
