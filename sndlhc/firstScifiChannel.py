import ROOT
from array import array
# determine local position of first SiPM channel in a vertical and horoizontal plane
old = False

if old:
  geoFile = "/media/disk0/SNDBuild/H6/geofile_sndlhc_H6.root"
  path = "/cave_1/volTarget_1/"
else:
  geoFile = "geofile_full.PG_22-TGeant4.root"
  path = "/cave_1/Detector_0/volTarget_1/"
import SndlhcGeo
geo   = SndlhcGeo.GeoInterface(geoFile)
Scifi  = geo.modules['Scifi']
nav   = geo.sGeo.GetCurrentNavigator()

A,B   = ROOT.TVector3(),ROOT.TVector3()
""" STMRFFF
 First digit S: 		station # within the sub-detector
 Second digit T: 		type of the plane: 0-horizontal fiber plane, 1-vertical fiber plane
 Third digit M: 		determines the mat number 0-2
 Fourth digit S: 		SiPM number  0-3
 Last three digits F: 	local SiPM channel number in one mat  0-127

 1st channel on board = last channel in sndsw!  23127
"""

planes = {'H':{'first':0,'last':23127},'V':{'first':100000,'last':123127}}
globA = {}
globB = {}
for n in range(1,6):
 for o in ['H','V']:
  for i in planes[o]:
   channel = planes[o][i]+n*1000000
   Scifi.GetSiPMPosition(channel, A, B)
   vol = str(n*1000000)
# to to local coordinate system
   if o=='H': nav.cd(path+"ScifiVolume"+str(n)+"_"+vol)
   else: nav.cd(path+"ScifiVolume"+str(n)+"_"+vol)
   key = str(n)+o
   globA[key] = array('d',[A.X(),A.Y(),A.Z()])
   locA = array('d',[0,0,0])
   globB[key] = array('d',[B.X(),B.Y(),B.Z()])
   locB = array('d',[0,0,0])
   nav.MasterToLocal(globA[key],locA)
   nav.MasterToLocal(globB[key],locB)
   print("---> "+i+" channel of plane ", n,o,locA,locB)
   print("---> global",globA[key],globB[key])

o='H'
for k in range(1,5):
  print('distance ',k,globA[str(k+1)+o][2]-globA[str(k)+o][2])

#---> first channel of plane  1 H array('d', [19.5, -19.51350156404078, 0.625]) array('d', [-19.5, -19.51350156404078, 0.625])
#---> last channel of plane  1 H array('d', [19.5, -6.562201417982578, 0.625]) array('d', [-19.5, -6.562201417982578, 0.625])

#---> first channel of plane  1 V array('d', [-19.51350156404078, -19.5, 1.1849999874830246]) array('d', [-19.51350156404078, 19.5, 1.1849999874830246])
#---> last channel of plane  1 V array('d', [-6.562201417982578, -19.5, 1.1849999874830246]) array('d', [-6.562201417982578, 19.5, 1.1849999874830246])


# distance between hor and ver plane:
D = ROOT.TVector3(globA['1H'][0],globA['1H'][1],globA['1H'][2]) - ROOT.TVector3(globA['1V'][0],globA['1V'][1],globA['1V'][2])
print ('z distance between H and V:',D[2])
D.Print()
#TVector3 A 3D physics vector (x,y,z)=(39.513498,0.486502,-0.560000)
# from engineering drawing: 12.92-7.07 -> 5.85 mm

#  what is the distance between the scifi edge points? 13cm
zEdges = [298.94,311.94,324.94,337.94, 350.94]
Vedges = {}
for i in range(5):
        Vedges[i]=ROOT.TVector3(Scifi.GetConfParF("Scifi/Xpos"+str(i)),
                                                Scifi.GetConfParF("Scifi/Zpos"+str(i)),
                                                Scifi.GetConfParF("Scifi/Ypos"+str(i)))

#edge position in Scifi engineering drawing:
Sedge = ROOT.TVector3(Scifi.GetConfParF("Scifi/EdgeAX"),
                                     -Scifi.GetConfParF("Scifi/EdgeAY"),
                                     -Scifi.GetConfParF("Scifi/EdgeAZ"))
#first channel position in Scifi engineering drawing:
SHfirst = ROOT.TVector3(Scifi.GetConfParF("Scifi/FirstChannelHX"),
                                      -Scifi.GetConfParF("Scifi/FirstChannelHY"),
                                      -Scifi.GetConfParF("Scifi/FirstChannelHZ"))
SVfirst = ROOT.TVector3(Scifi.GetConfParF("Scifi/FirstChannelVX"),
                                      -Scifi.GetConfParF("Scifi/FirstChannelVY"),
                                      -Scifi.GetConfParF("Scifi/FirstChannelVZ"))
#first channel position in sndsw local plane:
LHfirst = ROOT.TVector3(Scifi.GetConfParF("Scifi/LfirstChannelHX"),
                                      Scifi.GetConfParF("Scifi/LfirstChannelHY"),
                                      Scifi.GetConfParF("Scifi/LfirstChannelHZ"))
LVfirst = ROOT.TVector3(Scifi.GetConfParF("Scifi/LfirstChannelVX"),
                                     Scifi.GetConfParF("Scifi/LfirstChannelVY"),
                                     Scifi.GetConfParF("Scifi/LfirstChannelVZ"))
# from first channel to edge
X = Sedge-SHfirst

o='H'
for k in range(1,6):
  globE = array('d',[globA[str(k)+o][0]+X[0],globA[str(k)+o][1]+X[1],globA[str(k)+o][2]+X[2]])
  nav.cd("/cave_1/Detector_0")
  surE = array('d',[0,0,0])
  nav.MasterToLocal(globE,surE)
  print('edge position in survey coordinate system',k,surE)

DeltasH ={}
DeltasV = {}
for k in range(5):
  DeltasH[i] = Vedges[k] - LHfirst + SHfirst - Sedge
  DeltasV[i] = Vedges[k] - LVfirst + SVfirst - Sedge
  DeltasH[i].Print()
  DeltasV[i].Print()

#            DeltasH[i]  = Vedges[i] - LHfirst + SHfirst - Sedge;
#            DeltasV[i]  = Vedges[i] - LVfirst + SVfirst - Sedge;

M = array('d',[0.999978,-0.006606,0.0000821516,
                              0.00660651,0.999901,-0.0124347,
                              4.69368E-15,0.0124349,0.999923])

localSND_physCS_rot      = ROOT.TGeoRotation("localSND_physCS_rot")
localSND_physCS_rot.SetMatrix(M)
localSND_physCS_comb = ROOT.TGeoCombiTrans("localSND_physCS",0.,0.,0.,localSND_physCS_rot)

'''
TEST 1.81 0 0 0 -18.16 -7.2945 297.273
TEST 1.81 0 0 0 -18.16 -7.2945 310.273
TEST 1.81 0 0 0 -18.16 -7.2945 323.273
TEST 1.81 0 0 0 -18.16 -7.2945 336.273
TEST 1.81 0 0 0 -18.16 -7.2945 349.273

es sollte bei positiv y und x sein

von 1st channel to edge: X = Sedge - SHfirst

coordinate of edge in local coordinate system:        Eloc   = LHfirst + X
coordinate of edge in global coordinate system:      Eglob = Vedges[i]

translation of local to global:  T = Eglob - Eloc

= Eglob - LHfirst - X = Eglob - LHfirst - Sedge + SHfirst

  DeltasH[i] = Vedges[k] - LHfirst + SHfirst - Sedge

# y down, z towards IP1, pos X left.
# need y up, z away from IP1, pos X left:  y and z need to change sign.

Sedge  = (22.500000,-22.500000,0.000000)
SHfirst = (-20.000000,19.528000,0.707000)
SVfirst = (-19.528000,20.000000,1.292000)

X         = (42.500000,-42.028000,-0.707000)

LHfirst = (19.517799,-19.500000,1.185000)      # does this make sense?
LVfirst = (19.500000,19.517799,0.625000)

global H:
Scifi.GetPosition(1011001,A,B) =(19.652972,-23.347989,298.985230), = (-19.346170,-23.090336,298.985230)
nav.cd('/cave_1/Detector_0/volTarget_1/ScifiVolume1_1000000/ScifiHorPlaneVol1_1000000')
 [19.75761146648502, -19.75763294952503, -0.05804447692534451] , -19.24237473951201, -19.24237712512003, -0.06445215659837172

engineering drawing, first horizontal channel on top, first vertical channel positive X
sndsw, first horizontal channel on bottom? YES and also in reality

need a complete overhaul, where is mat 0,1,2 ?

Eloc   = LHfirst + X = (22.500000,-61.541500,0.253000)

something wrong with rotations
switch of detector rotation


test = {'1Hfirst':1012001,'1Hlast':1032472,'1Vfirst':1112001,'1Vlast':1132472}
for key in test:
 Scifi.GetPosition(test[key],A,B)
 globA[key] = array('d',[A.X(),A.Y(),A.Z()])
 globB[key] = array('d',[B.X(),B.Y(),B.Z()])
 nav.cd('/cave_1/Detector_0/volTarget_1/ScifiVolume1_1000000/ScifiHorPlaneVol1_1000000')
 nav.MasterToLocal(globA[key],locA)
 nav.MasterToLocal(globB[key],locB)
 print(key,locA,locB)
1Hfirst  [19.5, -19.513499656692147, -0.04025000287219882]  [-19.5, -19.513499656692147, -0.04025000287219882])
1Hlast  [19.5,  19.518999816849828,  -0.04025000287219882]   [-19.5,  19.518999816849828, -0.04025000287219882])

---> first channel of plane  1 H array('d', [-19.5, -19.51350212097168, 0.625]) array('d', [19.5, -19.51350212097168, 0.625])
---> last channel of plane  1 H array('d', [-19.5,  19.517799377441406, 0.625]) array('d', [19.5, 19.517799377441406, 0.625])

1Vfirst  [-19.513499656692147, -19.5, 0.5197499846108258]     [-19.513499656692147, 19.5, 0.5197499846108258]
1Vlast  [19.518999816849828, -19.5,   0.5197499846108258]      [19.518999816849828, 19.5, 0.5197499846108258]
LOOKS OK

X=Scifi.GetSiPMPos()
X[23127] =  19.517799377441406
X[0]         = -19.51350212097168

'''
from array import array

Mufi = geo.modules['MuFilter']

det = ROOT.gGeoManager.FindVolumeFast('Detector')

A,B   = ROOT.TVector3(),ROOT.TVector3()
nav=ROOT.gGeoManager.GetCurrentNavigator()

bars = {1:{'first':10000,'last':10006},2:{'first':20000,'last':20009},3:{'first':30000,'last':30059},4:{'first':30060,'last':30119}}
globA = {}
globB = {}
for n in bars:
  for c in bars[n]:
   channel = bars[n][c]
   Mufi.GetPosition(channel, A, B)
# to to local coordinate system
   key = str(n)+c
   globA[key] = array('d',[A.X(),A.Y(),A.Z()])
   locA = array('d',[0,0,0])
   globB[key] = array('d',[B.X(),B.Y(),B.Z()])
   locB = array('d',[0,0,0])
   if n == 3 or n == 4:   path = '/cave_1/Detector_0/volMuFilter_1/volMuDownstreamDet_0_7'
   if n == 2:   path = '/cave_1/Detector_0/volMuFilter_1/volMuUpstreamDet_0_2'
   if n == 1:   path = '/cave_1/Detector_0/volVeto_1/volVetoPlane_0_0'
   nav.cd(path)
   nav.MasterToLocal(globA[key],locA)
   nav.MasterToLocal(globB[key],locB)
   print("---> "+c+" channel of plane ", n,channel,locA,locB)
   # print("---> global",globA[key],globB[key])

iron = {}
muon = {}
for s in range(1,10):
   si = str(s)
   iron[s] = ROOT.TVector3( -Mufi.GetConfParF("MuFilter/Iron"+si+"Dx"),Mufi.GetConfParF("MuFilter/Iron"+si+"Dz"),Mufi.GetConfParF("MuFilter/Iron"+si+"Dy"))
   muon[s] = ROOT.TVector3( -Mufi.GetConfParF("MuFilter/Muon"+si+"Dx"),Mufi.GetConfParF("MuFilter/Muon"+si+"Dz"),Mufi.GetConfParF("MuFilter/Muon"+si+"Dy"))

for s in range(1,9):
   print("%i %i  iron dist: %5.3F  empty space: %5.3F    muon dist: %5.3F"%(s,s+1, iron[s+1].Z() - iron[s].Z(), iron[s+1].Z() - iron[s].Z()-20.0, muon[s+1].Z() - muon[s].Z()))

