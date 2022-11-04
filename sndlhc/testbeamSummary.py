import ROOT,os
import time
import ctypes
from array import array

import rootUtils as ut
import shipunit as u
h={}


runList = [46,49,52,54,56,58,71,72,73,74,82,86,87,88,89,90,91,47,48,50,51,53,55,59,60,80,81]
setup = 'H8'  # or 'H6'
path = os.environ['EOSSHIP']+"/eos/experiment/sndlhc/convertedData/MuFilter/TB_data_commissioning-NewCalib/"

import SndlhcGeo
geo = SndlhcGeo.GeoInterface(path+"geofile_sndlhc_H6.root")

A,B,locA,locB,globA,globB    = ROOT.TVector3(),ROOT.TVector3(),ROOT.TVector3(),ROOT.TVector3(),ROOT.TVector3(),ROOT.TVector3()
latex = ROOT.TLatex()

# MuFilter mapping of planes and bars 
systemAndPlanes = {1:2,2:5,3:7}
systemAndBars     = {1:7,2:10,3:60}
sdict                            = {1:'Veto',2:'US',3:'DS'}
def smallSiPMchannel(i):
    if i==2 or i==5 or i==10 or i==13: return True
    else: return False

freq      = 160.E6
TDC2ns = 1E9/freq

def myPrint(tc,name,run,withRootFile=False):
     tc.Print(name+'-run'+str(run)+'.png')
     if withRootFile: tc.Print(name+'-run'+str(run)+'.root')

def drawArea(s=3,p=0,opt='',color=ROOT.kGreen):
 ut.bookCanvas(h,'area','',900,900,1,1)
 hname = 'track_'+sdict[s]+str(s)+str(p)
 barw = 1.0
 if s<3: barw=3.
 h[hname].SetStats(0)
 h[hname].SetTitle('')
 h[hname].Draw('colz'+opt)
 mufi = geo.modules['MuFilter']
 if opt=='': h['lines'] = []
 lines = h['lines'] 
 latex.SetTextColor(ROOT.kRed)
 latex.SetTextSize(0.03)
 for bar in range(systemAndBars[s]):
    mufi.GetPosition(s*10000+p*1000+bar,A,B)
    barName = str(bar)
    botL = ROOT.TVector3(A.X(),A.Y()-barw,0)
    botR = ROOT.TVector3(B.X(),B.Y()-barw,0)
    topL = ROOT.TVector3(A.X(),A.Y()+barw,0)
    topR = ROOT.TVector3(B.X(),B.Y()+barw,0)
    lines.append(ROOT.TLine(topL.X(),topL.Y(),topR.X(),topR.Y()))
    lines.append(ROOT.TLine(botL.X(),botL.Y(),botR.X(),botR.Y()))
    lines.append(ROOT.TLine(botL.X(),botL.Y(),topL.X(),topL.Y()))
    lines.append(ROOT.TLine(botR.X(),botR.Y(),topR.X(),topR.Y()))
    if s<3 or (s==3 and bar%5==0): latex.DrawLatex(botR.X()-5.,botR.Y()+0.3,barName)
    N = len(lines)
    for n in range(N-4,N):
      l=lines[n]
      l.SetLineColor(color)
      l.SetLineWidth(1)
 for l in lines:  l.Draw('same')
 latex.DrawLatexNDC(0.2,0.2,"Right")
 latex.DrawLatexNDC(0.8,0.2,"Left")
 if s<3: return
 h['linesV'] = []
 linesV = h['linesV'] 
 for bar in range(systemAndBars[s]):
    mufi.GetPosition(s*10000+(p+1)*1000+bar+60,A,B)
    topL = ROOT.TVector3(A.X()+barw,A.Y(),0)
    botL = ROOT.TVector3(B.X()+barw,B.Y(),0)
    topR = ROOT.TVector3(A.X()-barw,A.Y(),0)
    botR = ROOT.TVector3(B.X()-barw,B.Y(),0)
    linesV.append(ROOT.TLine(topL.X(),topL.Y(),topR.X(),topR.Y()))
    linesV.append(ROOT.TLine(topR.X(),topR.Y(),botR.X(),botR.Y()))
    linesV.append(ROOT.TLine(botR.X(),botR.Y(),botL.X(),botL.Y()))
    linesV.append(ROOT.TLine(botL.X(),botL.Y(),topL.X(),topL.Y()))
    barName = str(bar)
    if bar%5==0: latex.DrawLatex(topR.X(),topR.Y()+2,barName)
 for l in linesV:
     l.SetLineColor(ROOT.kRed)
     l.SetLineWidth(1)
     l.Draw('same')

def beamSpot(run):
  for s in range(1,4):
    if s==1 and setup == 'H8': continue
    drawArea(s,p=0,opt='',color=ROOT.kGreen)
    myPrint(h['area'],'areaDet_'+sdict[s],run)

for run in runList:
    fileName = 'MuFilterEff_run'+str(run)+'.root'
    if not fileName in os.listdir('./'): continue
    h = {}
    ut.readHists(h,fileName)
    beamSpot(run)

def tdcRMS():
  for s in systemAndPlanes:
    if s==3: continue
    for l in range(systemAndPlanes[s]):
        for side in ['L','R']:
          for bar in range(systemAndBars[s]):
             for sipm in range(systemAndChannels[s][0]+systemAndChannels[s][1]):
                key = sdict[s]+side+str(s*10+l)+'_'+str(bar)+'_'+str(sipm)
                ut.bookHist(h,'sigmaTDC_'+key,'rms TDC ;dt [ns]',200,-1.0,1.0)
  N = 1000000
  n=0
  for event in eventTree:
    n+=1
    if n>N:break
    for aHit in event.Digi_MuFilterHits:
         if not aHit.isValid(): continue
         s = aHit.GetDetectorID()//10000
         if s==3: continue
         p = (aHit.GetDetectorID()//1000)%10
         bar = (aHit.GetDetectorID()%1000)%60
         plane = s*10+p
         allTDCs = map2Dict(aHit,'GetAllTimes')
         meanL,meanR,nL,nR=0,0,0,0
         nSiPMs = aHit.GetnSiPMs()
         for i in allTDCs:
             if smallSiPMchannel(i): continue
             if  nSiPMs > i:  # left side
                nL+=1
                meanL+=allTDCs[i]
             else:
               nR+=1
               meanR+=allTDCs[i]
         meanL = meanL/(nL+1E-20)*TDC2ns
         meanR = meanR/(nR+1E-20)*TDC2ns
         for i in allTDCs:
            if smallSiPMchannel(i): continue
            t = allTDCs[i]*TDC2ns
            if i<nSiPMs and nL>0:
                 key =  sdict[s]+'L'+str(plane)+'_'+str(bar)+'_'+str(i)
                 rc = h['sigmaTDC_'+key].Fill(t-meanL)
            elif nR>0:
                 key =  sdict[s]+'R'+str(plane)+'_'+str(bar)+'_'+str(i-nSiPMs)
                 rc = h['sigmaTDC_'+key].Fill(t-meanR)

  resultsT0 = {}
  tc = h['dummy'].cd()
  for s in systemAndPlanes:
    if s==3: continue
    resultsT0[s]={}
    for l in range(systemAndPlanes[s]):
        for side in ['L','R']:
          for bar in range(systemAndBars[s]):
             for sipm in range(systemAndChannels[s][0]+systemAndChannels[s][1]):
                key = sdict[s]+str(s*10+l)+'_'+str(bar)
                name = 'tvsX'+side+'_'+key+'-c'+str(sipm)
                tname = 't'+name
                h['g'+key] = ROOT.TGraphErrors()
                h[tname] = h[key].ProjectionX(tname)
                h[tname].Reset()
                xax = h[tname].GetXaxis()
                yax = h[tname].GetYaxis()
                yax.SetTitle('#sigma_{t} [ns]')
                ymin = h[name].GetYaxis().GetBinCenter(1)
                ymax = h[name].GetYaxis().GetBinCenter(h[name].GetYaxis().GetNbins())
                minContent = max(50,h[name].GetEntries()*0.02)  # remove tails from bad track reconstruction and extrapolation.)
                for j in range(1,xax.GetNbins()+1):
                    jname = name+'-X'+str(j)
                    h[jname] = h[name].ProjectionY(jname,j,j)
                    if h[jname].GetEntries()<minContent: continue
                    xx =  h[jname].GetBinCenter(h[jname].GetMaximumBin())
                    xmin  = max(ymin,xx-2.)
                    xmax = min(ymax,xx+2.)
                    rc = h[jname].Fit('gaus','SQL','',xmin,xmax)
                    res = rc.Get()
                    h[tname].SetBinContent(j,res.Parameter(2))
                    h[tname].SetBinError(j,res.ParError(2))
                A = weightedY(h[tname])
                if A[1]<100:
                   h[mode+'tsigma_'+str(s)].SetBinContent(plane*systemAndBars[s]+bar,A[0])
                   h[mode+'tsigma_'+str(s)].SetBinError(plane*systemAndBars[s]+bar,A[1])


                binw = str(hk.GetBinWidth(1))
                N = 0
                if side == 'R' :  N=8
                if hk.GetEntries()>50:
                    myGauss = ROOT.TF1('gauss','abs([0])*'+binw+'/(abs([2])*sqrt(2*pi))*exp(-0.5*((x-[1])/[2])**2)+abs([3])',4)
                    myGauss.SetParameter(0,hk.GetEntries())
                    myGauss.SetParameter(1,0)
                    myGauss.SetParameter(2,2.)
                    rc = hk.Fit(myGauss,'SLQ','',-3.,3.)
                    fitResult = rc.Get() 
                    results[s][key]=[fitResult.Parameter(1),fitResult.Parameter(2)]
                    if not smallSiPMchannel(sipm): rc = h['dSTDC_'+str(s)].Fill(sipm+N,fitResult.Parameter(2))
                    txt+=" %5.2F"%(results[s][key][0])
                    if not smallSiPMchannel(sipm): rc = h['dMeanTDC_'+str(s)].Fill(results[s][key][0])
                    if not smallSiPMchannel(sipm): rc = h['dTDC_'+str(s)].Fill(sipm+N,results[s][key][0])
             print('%s%i%s %i   %s '%(sdict[s],l,side,bar,txt))

  results = {}
  for s in systemAndPlanes:
    if s==3: continue
    ut.bookHist(h,'dMeanTDC_'+str(s),'',100,-2.,2.)
    ut.bookHist(h,'dTDC_'+str(s),'',16,-0.5,15.5,100,-2.,2.)
    ut.bookHist(h,'dSTDC_'+str(s),'',16,-0.5,15.5,100,0.,2.)
    results[s]={}
    for l in range(systemAndPlanes[s]):
        for side in ['L','R']:
          for bar in range(systemAndBars[s]):
             txt = ""
             for sipm in range(systemAndChannels[s][0]+systemAndChannels[s][1]):
                key = sdict[s]+str(s*10+l)+'_'+str(bar)
                key = 'sigmaTDC'+side+'_'+key+'-c'+str(sipm)
                hk = h[key]
                binw = str(hk.GetBinWidth(1))
                N = 0
                if side == 'R' :  N=8
                if hk.GetEntries()>50:
                    myGauss = ROOT.TF1('gauss','abs([0])*'+binw+'/(abs([2])*sqrt(2*pi))*exp(-0.5*((x-[1])/[2])**2)+abs([3])',4)
                    myGauss.SetParameter(0,hk.GetEntries())
                    myGauss.SetParameter(1,0)
                    myGauss.SetParameter(2,2.)
                    rc = hk.Fit(myGauss,'SLQ','',-3.,3.)
                    fitResult = rc.Get() 
                    results[s][key]=[fitResult.Parameter(1),fitResult.Parameter(2)]
                    if not smallSiPMchannel(sipm): rc = h['dSTDC_'+str(s)].Fill(sipm+N,fitResult.Parameter(2))
                    txt+=" %5.2F"%(results[s][key][0])
                    if not smallSiPMchannel(sipm): rc = h['dMeanTDC_'+str(s)].Fill(results[s][key][0])
                    if not smallSiPMchannel(sipm): rc = h['dTDC_'+str(s)].Fill(sipm+N,results[s][key][0])
             print('%s%i%s %i   %s '%(sdict[s],l,side,bar,txt))

s=2
avSigma = {}
for l in range(systemAndPlanes[s]):
    mean={}
    for side in ['L','R']:
          A = [0,0]
          for bar in range(systemAndBars[s]):
             for sipm in range(systemAndChannels[s][0]+systemAndChannels[s][1]):
                if smallSiPMchannel(sipm): continue
                key = sdict[s]+str(s*10+l)+'_'+str(bar)
                key = 'sigmaTDC'+side+'_'+key+'-c'+str(sipm)
                if not key in results[s]:continue
                if results[s][key][0] == 0: continue
                A[0]+=abs(results[s][key][1])
                A[1]+=1
             mean[side] = A[0]/A[1]
    print('%i:   %5.2F        %5.2F'%(l,mean['L'],mean['R']))
 
