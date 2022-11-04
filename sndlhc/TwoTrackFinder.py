#!/usr/bin/env python
import ROOT,os,sys
import rootUtils as ut
import shipunit as u
import ctypes
from array import array

A,B  = ROOT.TVector3(),ROOT.TVector3()
parallelToZ = ROOT.TVector3(0., 0., 1.)

class TwoTrackReco(ROOT.FairTask):
   " find events with two tracks"
   def Init(self,options,monitor):
       self.M = monitor
       h = self.M.h
       self.projs = {1:'V',0:'H'}
       self.trackTask = self.M.FairTasks['simpleTracking']

       for s in range(1,6):
          for o in range(2):
             for p in self.projs:
               proj = self.projs[p]
               xmax = -xmin
               ut.bookHist(h,'res'+proj+'_Scifi'+str(s*10+o),'residual '+proj+str(s*10+o)+'; [#mum]',NbinsRes,xmin,xmax)
               ut.bookHist(h,'resX'+proj+'_Scifi'+str(s*10+o),'residual '+proj+str(s*10+o)+'; [#mum]',NbinsRes,xmin,xmax,100,-50.,0.)
               ut.bookHist(h,'resY'+proj+'_Scifi'+str(s*10+o),'residual '+proj+str(s*10+o)+'; [#mum]',NbinsRes,xmin,xmax,100,10.,60.)
               ut.bookHist(h,'resC'+proj+'_Scifi'+str(s*10+o),'residual '+proj+str(s*10+o)+'; [#mum]',NbinsRes,xmin,xmax,128*4*3,-0.5,128*4*3-0.5)
               ut.bookHist(h,'track_Scifi'+str(s*10+o),'track x/y '+str(s*10+o)+'; x [cm]; y [cm]',80,-70.,10.,80,0.,80.)

   def ExecuteEvent(self,event):
       h = self.M.h
       W = self.M.Weight
       if not hasattr(event,"Cluster_Scifi"):
               self.trackTask.scifiCluster()
               clusters = self.trackTask.clusScifi
       else:
               clusters = event.Cluster_Scifi

       sortedClusters={}
       for aCl in clusters:
           so = aCl.GetFirst()//100000
           if not so in sortedClusters: sortedClusters[so]=[]
           sortedClusters[so].append(aCl)
# select events with clusters in each plane
       if len(sortedClusters)<10: return
       goodEvent = True
       for s in sortedClusters:
          if len(sortedClusters[s])>1: goodEvent=False
       if not goodEvent: return

       for s in range(1,6):
            if self.unbiased:
# build trackCandidate
              hitlist = {}
              if self.unbiased or s==1:
                k=0
                for so in sortedClusters:
                    if so//10 == s and self.unbiased: continue
                    for x in sortedClusters[so]:
                       hitlist[k] = x
                       k+=1
                theTrack = self.trackTask.fitTrack(hitlist)
                if not hasattr(theTrack,"getFittedState"): continue
# check residuals
                fitStatus = theTrack.getFitStatus()
                if not fitStatus.isFitConverged(): 
                  theTrack.Delete()
                  continue
# test plane
            for o in range(2):
                testPlane = s*10+o
                z = self.M.zPos['Scifi'][testPlane]
                rep     = ROOT.genfit.RKTrackRep(13)
                state  = ROOT.genfit.StateOnPlane(rep)
# find closest track state
                mClose = 0
                mZmin = 999999.
                for m in range(0,theTrack.getNumPointsWithMeasurement()):
                   st   = theTrack.getFittedState(m)
                   Pos = st.getPos()
                   if abs(z-Pos.z())<mZmin:
                      mZmin = abs(z-Pos.z())
                      mClose = m
                if mZmin>10000:
                    print("something wrong here with measurements",mClose,mZmin,theTrack.getNumPointsWithMeasurement())
                fstate =  theTrack.getFittedState(mClose)
                pos,mom = fstate.getPos(),fstate.getMom()
                rep.setPosMom(state,pos,mom)
                NewPosition = ROOT.TVector3(0., 0., z)   # assumes that plane in global coordinates is perpendicular to z-axis, which is not true for TI18 geometry.
                rep.extrapolateToPlane(state, NewPosition, parallelToZ )
                pos = state.getPos()
                xEx,yEx = pos.x(),pos.y()
                rc = h['track_Scifi'+str(testPlane)].Fill(xEx,yEx,W)
                for aCl in sortedClusters[testPlane]:
                   aCl.GetPosition(A,B)
                   detID = aCl.GetFirst()
                   channel = detID%1000 + ((detID%10000)//1000)*128 + (detID%100000//10000)*512
# calculate DOCA
                   pq = A-pos
                   uCrossv= (B-A).Cross(mom)
                   doca = pq.Dot(uCrossv)/uCrossv.Mag()
                   rc = h['resC'+self.projs[o]+'_Scifi'+str(testPlane)].Fill(doca/u.um,channel,W)
                   rc = h['res'+self.projs[o]+'_Scifi'+str(testPlane)].Fill(doca/u.um,W)
                   rc = h['resX'+self.projs[o]+'_Scifi'+str(testPlane)].Fill(doca/u.um,xEx,W)
                   rc = h['resY'+self.projs[o]+'_Scifi'+str(testPlane)].Fill(doca/u.um,yEx,W)

            if self.unbiased: theTrack.Delete()

# analysis and plots 
   def Plot(self):
       h = self.M.h
       P = {'':'','X':'colz','Y':'colz','C':'colz'}
       Par = {'mean':1,'sigma':2}
       h['globalPos']   = {'meanH':ROOT.TGraphErrors(),'sigmaH':ROOT.TGraphErrors(),'meanV':ROOT.TGraphErrors(),'sigmaV':ROOT.TGraphErrors()}
       h['globalPosM'] = {'meanH':ROOT.TGraphErrors(),'sigmaH':ROOT.TGraphErrors(),'meanV':ROOT.TGraphErrors(),'sigmaV':ROOT.TGraphErrors()}
       for x in h['globalPosM']:
            h['globalPos'][x].SetMarkerStyle(21)
            h['globalPos'][x].SetMarkerColor(ROOT.kBlue)
            h['globalPosM'][x].SetMarkerStyle(21)
            h['globalPosM'][x].SetMarkerColor(ROOT.kBlue)
       globalPos = h['globalPos']
       for proj in P:
           ut.bookCanvas(h,'scifiRes'+proj,'',1600,1900,2,5)
           k=1
           j = {0:0,1:0}
           for s in range(1,6):
               for o in range(2):
                  so = s*10+o
                  tc = h['scifiRes'+proj].cd(k)
                  k+=1
                  hname = 'res'+proj+self.projs[o]+'_Scifi'+str(so)
                  h[hname].Draw(P[proj])
                  if proj == '':
                     rc = h[hname].Fit('gaus','SQ')
                     fitResult = rc.Get()
                     if not fitResult: continue
                     for p in Par:
                          globalPos[p+self.projs[o]].SetPoint(s-1,s,fitResult.Parameter(Par[p]))
                          globalPos[p+self.projs[o]].SetPointError(s-1,0.5,fitResult.ParError(1))
                  if proj == 'C':
                       for m in range(3):
                             h[hname+str(m)] = h[hname].ProjectionX(hname+str(m),m*512,m*512+512)
                             rc = h[hname+str(m)].Fit('gaus','SQ0')
                             fitResult = rc.Get()
                             if not fitResult: continue
                             for p in Par:
                                 h['globalPosM'][p+self.projs[o]].SetPoint(j[o], s*10+m,   fitResult.Parameter(Par[p]))
                                 h['globalPosM'][p+self.projs[o]].SetPointError(j[o],0.5,fitResult.ParError(1))
                             j[o]+=1
       
       S  = ctypes.c_double()
       M = ctypes.c_double()
       h['alignPar'] = {}
       alignPar = h['alignPar']
       for p in globalPos:
           ut.bookCanvas(h,p,p,750,750,1,1)
           tc = h[p].cd()
           globalPos[p].SetTitle(p+';station; offset [#mum]')
           globalPos[p].Draw("ALP")
           if p.find('mean')==0:
               for n in range(globalPos[p].GetN()):
                  rc = globalPos[p].GetPoint(n,S,M)
                  print("station %i: offset %s =  %5.2F um"%(S.value,p[4:5],M.value))
                  s = int(S.value*10)
                  if p[4:5] == "V": s+=1
                  alignPar["Scifi/LocD"+str(s)] = M.value

       ut.bookCanvas(h,'mean&sigma',"mean and sigma",1200,1200,2,2)
       k=1
       for p in h['globalPosM']:
           ut.bookCanvas(h,p+'M',p,750,750,1,1)
           tc = h[p+'M'].cd()
           h['globalPosM'][p].SetTitle(p+';mat ; offset [#mum]')
           h['globalPosM'][p].Draw("ALP")
           tc = h['mean&sigma'].cd(k)
           h['globalPosM'][p].Draw("ALP")
           k+=1
           if p.find('mean')==0:
              for n in range(h['globalPosM'][p].GetN()):
                 rc = h['globalPosM'][p].GetPoint(n,S,M)
                 print("station %i: offset %s =  %5.2F um"%(S.value,p[4:5],M.value))
                 s = int(S.value*10)
                 if p[4:5] == "V": s+=1
                 alignPar["Scifi/LocM"+str(s)] = M.value
       T = ['mean&sigma']
       for proj in P: T.append('scifiRes'+proj)
       for canvas in T:
           self.M.myPrint(self.M.h[canvas],"Scifi-"+canvas,subdir='scifi')
       for x in self.xing:
           if not self.M.fsdict and x!='': continue
           tname = detector+'trackDir'+x
           ut.bookCanvas(h,tname,"track directions",1600,1800,3,2)
           h[tname].cd(1)
           rc = h[detector+'trackSlopes'+x].Draw('colz')
           h[tname].cd(2)
           rc = h[detector+'trackSlopes'+x].ProjectionX("slopeX"+x).Draw()
           h[tname].cd(3)
           rc = h[detector+'trackSlopes'+x].ProjectionY("slopeY"+x).Draw()
           h[tname].cd(4)
           rc = h[detector+'trackSlopesXL'+x].Draw('colz')
           h[tname].cd(5)
           rc = h[detector+'trackSlopesXL'+x].ProjectionX("slopeXL"+x).Draw()
           h[tname].cd(6)
           rc = h[detector+'trackSlopesXL'+x].ProjectionY("slopeYL"+x).Draw()
           self.M.myPrint(self.M.h[tname],tname,subdir='scifi')
           tname = detector+'TtrackPos'+x
           ut.bookCanvas(h,tname,"track position first state",1200,800,1,2)
           h[tname].cd(1)
           rc = h[detector+'trackPosBeam'+x].Draw('colz')
           h[tname].cd(2)
           rc = h[detector+'trackPos'+x].Draw('colz')
           self.M.myPrint(self.M.h[tname],detector+'trackPos'+x,subdir='scifi')
