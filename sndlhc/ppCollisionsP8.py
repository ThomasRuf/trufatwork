import ROOT,time,os,sys
import rootUtils as ut

nEvents = 1000
h={}

myPythia = ROOT.TPythia8()
P8       = myPythia.Pythia8()
rnr      = ROOT.TRandom()
# Configure    myPythia.listAll()
#              myPythia.list(431) 

myPythia.ReadString("SoftQCD:inelastic = on")
myPythia.ReadString("SoftQCD:singleDiffractive = on")
myPythia.ReadString("SoftQCD:doubleDiffractive = on")
myPythia.ReadString("SoftQCD:centralDiffractive = on")
myPythia.ReadString("PhotonCollision:gmgm2mumu = on")
#
P8.settings.mode("Beams:idB",  2212)
P8.settings.mode("Beams:idA",  2212)
P8.settings.mode("Beams:frameType",1)
P8.settings.parm("Beams:eCM",13600.)

# set all resonances to mu+mu:
resonances = [221, 221, 223, 223,   113, 331, 333, 443, 553]
#  no onMode   bRatio   meMode     products 
#553  3     1   0.0248000    0       13      -13 
#443: 2     1   0.0593000    0       13      -13
#221: 7     1   0.0000060    0       13      -13
for r in resonances:
  V = P8.particleData.particleDataEntryPtr(r)
  V.clearChannels()
  V.addChannel(1,1.,1,13,-13)

P8.init()

for r in resonances:
  ut.bookHist(h,'oAngle'+str(r),'opening angle ; mrad',1000,0.,10.)
  ut.bookHist(h,'oAngleInAcc'+str(r),'opening angle ; mrad',1000,0.,10.)
  ut.bookHist(h,'angles'+str(r),'muon1 vs muon 2;mrad',100,0,10,100,0,10)
  ut.bookHist(h,'angles'+str(r),'muon1 vs muon 2;mrad',100,0,10,100,0,10)
  ut.bookHist(h,'XY'+str(r),'muon position;X[cm];Y[cm]',50,-50,0,50,10,60)
scifiAcc = {'xmin':-46.2,'xmax':-7.1, 'ymin':15.00,'ymax':54.0}
dist = 48200
for n in range(nEvents):
  rc = P8.next()
  for n in range(P8.event.size()):
     par= P8.event[n]
     pId = par.id()
     if not pId in resonances: continue
     d1,d2 = par.daughter1(),par.daughter2()
     if d1==d2: continue
     muons = []
     for d in [d1,d2]:
        m = P8.event[d]
        muons.append( ROOT.TVector3(m.px(),m.py(),m.pz()) )
     rc = h['angles'+str(pId)].Fill(muons[0].Theta()*1000,muons[1].Theta()*1000)
     if muons[0].Theta()>0.01 or muons[0].Theta()>0.01: continue
     XY={0:[],1:[]}
     inAcc = {0:False,1:False}
     for i in range(2):
        lam = dist/muons[i][2]
        XY[i] = [muons[i][0]*lam,muons[i][1]*lam]
        rc = h['XY'+str(pId)].Fill(XY[i][0],XY[i][1])
        if XY[i][0]>scifiAcc['xmin'] and XY[i][0]<scifiAcc['xmax'] and XY[i][1]>scifiAcc['ymin'] and XY[i][1]<scifiAcc['ymax']:
            inAcc[i] = True
     oangle = muons[0].Dot(muons[1])/(muons[0].Mag()*muons[1].Mag())
     X = ROOT.TMath.ACos(oangle)
     rc = h['oAngle'+str(pId)].Fill(X*1000)
     # print(inAcc[0] ,inAcc[1], XY,muons[0].Theta()*1000,muons[1].Theta()*1000,X )
     if inAcc[0] and inAcc[1]: rc = h['oAngleInAcc'+str(pId)].Fill(X*1000)



