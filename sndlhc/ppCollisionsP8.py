import ROOT,time,os,sys
import rootUtils as ut

nEvents = 100000
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
resNames = {}
for r in resonances:
  V = P8.particleData.particleDataEntryPtr(r)
  resNames[r] = V.name()
P8.init()

def resetChannels(resonances):
 for r in resonances:
   V = P8.particleData.particleDataEntryPtr(r)
   V.clearChannels()
   V.addChannel(1,1.,1,13,-13)

def run(nEvents):
 resetChannels(resonances)
 for r in resonances:
  ut.bookHist(h,'oAngle'+str(r),'opening angle '+resNames[r]+'; mrad',1000,0.,10.)
  ut.bookHist(h,'oAngleInAcc'+str(r),'opening angle '+resNames[r]+'; mrad',1000,0.,10.)
  ut.bookHist(h,'angles'+str(r),'muon1 vs muon 2 '+resNames[r]+';mrad',100,0,10,100,0,10)
  ut.bookHist(h,'E'+str(r),'muon1 vs muon 2 '+resNames[r]+';[GeV]',100,0,3000,100,0,3000)
  ut.bookHist(h,'XY'+str(r),'muon position '+resNames[r]+';X[cm];Y[cm]',50,-50,0,50,10,60)
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
     if muons[0].Z()<0 or muons[1].Z()<0 : continue
     rc = h['E'+str(pId)].Fill(muons[0].Mag(),muons[1].Mag())
     if muons[0].Mag()<30 or muons[1].Mag()<30: continue
     rc = h['angles'+str(pId)].Fill(muons[0].Theta()*1000,muons[1].Theta()*1000)
     if muons[0].Theta()>0.01 or muons[0].Theta()>0.01: continue
     XY={0:[],1:[]}
     inAcc = {0:False,1:False}
     for i in range(2):
        lam = dist/muons[i][2]
        XY[i] = ROOT.TVector3(muons[i][0]*lam,muons[i][1]*lam,dist)
        rc = h['XY'+str(pId)].Fill(XY[i].X(),XY[i].Y())
        if XY[i].X()>scifiAcc['xmin'] and XY[i].X()<scifiAcc['xmax'] and XY[i].Y()>scifiAcc['ymin'] and XY[i].Y()<scifiAcc['ymax']:
            inAcc[i] = True
     oangle = muons[0].Dot(muons[1])/(muons[0].Mag()*muons[1].Mag())
     X = ROOT.TMath.ACos(oangle)
     rc = h['oAngle'+str(pId)].Fill(X*1000)
     # print(inAcc[0] ,inAcc[1], XY,muons[0].Theta()*1000,muons[1].Theta()*1000,X )
     if inAcc[0] and inAcc[1]: rc = h['oAngleInAcc'+str(pId)].Fill(X*1000)
 ut.writeHists(h,'P8simDiMuon_'+str(nEvents)+'.root')

def Analysis(name):
 ut.readHists(h,name)
def rates(MCstats):
   resNames = {221: 'eta', 223: 'omega', 113: 'rho0', 331: "eta'", 333: 'phi', 443: 'J/psi', 553: 'Upsilon'}
   Brmumu = {}
   Brmumu[221] = 5.8E-6
   Brmumu[223] = 9.0E-5
   Brmumu[113] = 4.55E-5
   Brmumu[331] = 0 # only mumumgamma
   Brmumu[333] = 2.87E-4
   Brmumu[443] = 5.961E-2
   Brmumu[553] = 2.48E-2
   for r in Brmumu:
       exDiMuonRate = h['oAngleInAcc'+str(r)].GetSumOfWeights()*80E-27/1E-39/MCstats*Brmumu[r]
       # 80mbar / fbar * Br /MCstats
       print('expected rate for %s %5.2F'%(resNames[r],exDiMuonRate))
