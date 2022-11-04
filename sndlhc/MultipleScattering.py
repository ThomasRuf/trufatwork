#python $SNDSW_ROOT/shipLHC/run_simSND.py --PG --pID 13 --Estart 1 --Eend 1000 --EVy 35. --EVx="-25." --EVz 250. -n 100000 --FastMuon
#python $SNDSW_ROOT/shipLHC/run_simSND.py --PG --pID 211 --Estart 1 --Eend 500 --EVy 35. --EVx="-25." --EVz 355. -n 100000

import ROOT
import rootUtils as ut
import shipunit as u

pid = 13

f = ROOT.TFile('sndLHC.PG_'+str(pid)+'-TGeant4.root')
sTree = f.cbmsim
h={}
ut.bookHist(h,'scifi20E','Eloss at scifi 2; E [GeV]',100,0.0,5.,100,0.,1000.)
ut.bookHist(h,'scifi50E','Eloss at scifi 5; E [GeV]',100,0.0,5.,100,0.,1000.)
ut.bookHist(h,'mufi20E','Eloss at US 1; E [GeV]',100,0.0,5.,100,0.,1000.)
ut.bookHist(h,'mufi30E','Eloss at DS 1; E [GeV]',100,0.0,5.,100,0.,1000.)
ut.bookHist(h,'mufi33E','Eloss at last DS; E [GeV]',100,0.0,5.,100,0.,1000.)

ut.bookHist(h,'scifi20x','dx at scifi 2;dx [cm]; p [GeV]',400,-0.2,0.2,100,0.,1000.)
ut.bookHist(h,'scifi51x','dx at scifi 5;dx [cm]; p [GeV]',1000,-1.,1.,100,0.,1000.)
ut.bookHist(h,'mufi20x','dx at US 1;dx [cm]; p [GeV]',240,-6.,6.,100,0.,1000.)
ut.bookHist(h,'mufi30x','dx at DS 1;dx [cm]; p [GeV]',240,-6.,6.,100,0.,1000.)
ut.bookHist(h,'scifi20y','dy at scifi 2;dy [cm]; p [GeV]',400,-0.2,0.2,100,0.,1000.)
ut.bookHist(h,'scifi51y','dy at scifi 5;dy [cm]; p [GeV]',1000,-1.,1.,100,0.,1000.)
ut.bookHist(h,'mufi20y','dy at US 1;dy [cm]; p [GeV]',240,-6.,6.,100,0.,1000.)
ut.bookHist(h,'mufi30y','dy at DS 1;dy [cm]; p [GeV]',240,-6.,6.,100,0.,1000.)
#
for event in sTree:
    detectorHits = {}
    dets = [event.MuFilterPoint,event.ScifiPoint]
    for aDet in dets:
      for aHit in aDet:
         if not aHit.GetTrackID()==0: continue
         if aHit.GetName()  == 'MuFilterPoint':
            sp = aHit.GetDetectorID()//1000
            detectorHits['mufi'+str(sp)] =  [aHit.GetX(),aHit.GetY(),aHit.GetZ(),aHit.GetPx(),aHit.GetPy(),aHit.GetPz()]
         else:
            sp = aHit.GetDetectorID()//100000
            detectorHits['scifi'+str(sp)] =  [aHit.GetX(),aHit.GetY(),aHit.GetZ(),aHit.GetPx(),aHit.GetPy(),aHit.GetPz()]

    first = detectorHits['scifi10']
    inMom    = ROOT.TVector3(first[3],first[4],first[5])
    P = inMom.Mag()
    for x in ['scifi20','scifi51','mufi20','mufi30']:
         if not x in detectorHits: continue
         next = detectorHits[x]
         lam = (next[2] - first[2]) / inMom[2]
         eVx = first[0]+lam*inMom[0]
         eVy = first[1]+lam*inMom[1]
         rc = h[x+'x'].Fill(eVx - next[0],P)
         rc = h[x+'y'].Fill(eVy - next[1],P)
    for x in ['scifi20','scifi50','mufi20','mufi30','mufi33']:
         if not x in detectorHits: continue
         next = detectorHits[x]
         Ploc = ROOT.TMath.Sqrt(next[3]**2+next[4]**2+next[5]**2)
         rc = h[x+'E'].Fill(P - Ploc,P)

ut.writeHists(h,'multScattering.root')
def plot():
     if len(h)==0:     ut.readHists(h,'multScattering.root')
     function = "13.6*0.001/x*sqrt([0])*(1.+0.038*log([0]))"
     h['MS'] = ROOT.TF1('MS',function,0,10000)
     h['MS'].SetParName(0,'X/X0')
     # https://pdg.lbl.gov/2020/AtomicNuclearProperties/HTML/tungsten_W.html
     xOverX0 = 10*u.cm/0.35*u.cm
     h['MS'].SetParameter(0,xOverX0)
     for p in ['x','y']:
      for x in ['scifi20'+p,'scifi51'+p,'mufi20'+p,'mufi30'+p]:
        ut.bookCanvas(h,'T'+x,'',1200,800,1,2)
        tc = h['T'+x].cd(1)
        h[x].Draw('colz')
        h[x+'sigma'] = h[x].ProjectionY(x+'sigma')
        h[x+'sigma'].Reset()
        h[x+'sigma'].GetYaxis().SetTitle('#sigma [cm]')
        for n in range(h[x].GetNbinsY()):
             h[x+str(n+1)] = h[x].ProjectionX(x+str(n+1),n+1,n+1)
             tmp = h[x+str(n+1)]
             m = tmp.FindBin(0)
             C = tmp.GetSumOfWeights()
             I = 0
             for i in range(m,1,-1):
                  I+= tmp.GetBinContent(m-i)
                  if I>0.9999*C/2.: break
             xmin = tmp.GetBinLowEdge(i)
             rc = tmp.Fit('gaus','SNQ','',xmin,abs(xmin))
             result = rc.Get()
             sigma = result.Parameter(2)
             error = result.ParError(2)
             h[x+'sigma'].SetBinContent(n+1,sigma)
             h[x+'sigma'].SetBinError(n+1,error)
        tc = h['T'+x].cd(2)
        tc.SetLogy(1)
        h[x+'sigma'].Fit(h['MS'])
        tc.Update()
        stats = h[x+'sigma'].FindObject('stats')
        stats.SetOptFit(111)
        stats.SetOptStat(10)
        h[x+'sigma'].Draw()
        tc.Update()
        h['T'+x].Print('MS'+x+'.png')
     for p in ['E']:
      for x in ['scifi20'+p,'scifi50'+p,'mufi20'+p,'mufi30'+p,'mufi33'+p]:
        ut.bookCanvas(h,'E'+x,'',1200,800,1,2)
        tc = h['E'+x].cd(1)
        h[x].Draw('colz')
        h[x+'mean'] = h[x].ProjectionY(x+'mean')
        h[x+'mean'].Reset()
        h[x+'mean'].GetYaxis().SetTitle('#Eloss [GeV]')
        for n in range(h[x].GetNbinsY()):
             h[x+str(n+1)] = h[x].ProjectionX(x+str(n+1),n+1,n+1)
             mean = h[x+str(n+1)].GetMean()
             h[x+'mean'].SetBinContent(n+1,mean)
        tc = h['E'+x].cd(2)
        h[x+'mean'].Draw()
        tc.Update()
        h['E'+x].Print('Eloss'+x+'.png')
        



