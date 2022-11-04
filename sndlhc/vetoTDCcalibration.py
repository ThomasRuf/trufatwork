import ROOT,os,sys
import rootUtils as ut
import pickle

A,B = ROOT.TVector3(),ROOT.TVector3()
refChannel = 0
detector = 'scifi'

class vetoTDCplaneCalibration(ROOT.FairTask):
   "plane alignment"
   def Init(self,options,monitor):
       self.M = monitor
       h = self.M.h
       self.minChannels = 4
       s = 1
       # delta T between bar i of plane 0 and bar i-1,i,i+1 of plane 1
       l = 0
       self.nbars = self.M.systemAndBars[s]
       for bar in range(self.nbars):
          ut.bookHist(h,'exBar_0'+str(bar),'ex y;dy [cm]',50,-10.,10.)
          ut.bookHist(h,'exBar_1'+str(bar),'ex y;dy [cm]',50,-10.,10.)
          for side in ['L','R']:
                for bar1 in [bar-1,bar,bar+1]:
                     if bar1 < 0 or bar1 > self.nbars: continue
                     key = self.M.sdict[s]+str(bar)+'_'+str(bar1)+side
                     ut.bookHist(h,'dtBar_'+key,'dt '+key+";dt [timestamp]",200,-1.,1.)
       with open('tdcVetoInternalCalibration', 'rb') as fh:
               self.tdcVetoCalib = pickle.load(fh)

       ut.bookHist(h,detector+'trackSlopes','track slope; x/z [mrad]; y/z [mrad]',1000,-100,100,1000,-100,100)
       ut.bookHist(h,detector+'trackSlopesXL','track slope; x/z [rad]; y/z [rad]',120,-1.1,1.1,120,-1.1,1.1)
       ut.bookHist(h,detector+'trackPos','track pos; x [cm]; y [cm]',100,-90,10.,80,0.,80.)
       ut.bookHist(h,detector+'trackPosBeam','beam track pos slopes<0.1rad; x [cm]; y [cm]',100,-90,10.,80,0.,80.)

   def ExecuteEvent(self,event):
       h = self.M.h
       s = 1
       vetoHits = {10:[],11:[]}
       for aHit in event.Digi_MuFilterHits:
          if not aHit.isValid(): continue
          detID = aHit.GetDetectorID()//1000
          if not detID<20: continue
          vetoHits[detID].append(aHit)
       if not(len(vetoHits[10])==1) and not(len(vetoHits[11])==1): return
       for aTrack in event.Reco_MuonTracks:
          tdc = {10:{},11:{}}
          S = aTrack.getFitStatus()
          if not S.isFitConverged(): continue
          mom    = aTrack.getFittedState().getMom()
          slopeX= mom.X()/mom.Z()
          slopeY= mom.Y()/mom.Z()
          pos = aTrack.getFittedState().getPos()
          rc = h[detector+'trackSlopes'].Fill(slopeX*1000,slopeY*1000)
          rc = h[detector+'trackSlopesXL'].Fill(slopeX,slopeY)
          rc = h[detector+'trackPos'].Fill(pos.X(),pos.Y())
          if abs(slopeX)<0.1 and abs(slopeY)<0.1:  rc = h[detector+'trackPosBeam'].Fill(pos.X(),pos.Y())

          if abs(mom.x()/mom.z())>0.25: continue   # 4cm distance, 250mrad = 1cm
          if mom.y()/mom.z()>0.05: continue
          pos      = aTrack.getFittedState().getPos()
          for l in range(2):
             zEx = self.M.zPos['MuFilter'][1*10+l]
             lam      = (zEx-pos.z())/mom.z()
             yEx        = pos.y()+lam*mom.y()
             xEx        = pos.x()+lam*mom.x()  # needed for correction of signal propagation
             for aHit in vetoHits[10+l]:
                detID = aHit.GetDetectorID()
                bar = (detID%1000)
                self.M.MuFilter.GetPosition(detID,A,B)
                D = (A[1]+B[1])/2. - yEx
                rc = h['exBar_'+str(l)+str(bar)].Fill(D)
                if abs(D)<5:
                   tdc[10+l][bar] = {'L':{},'R':{}}
                   for k in range(16):
                      qdc = aHit.GetSignal(k)
                      if qdc <0: continue
                      kx = k
                      side = 'L'
                      if not k < 8 : 
                           kx = k - 8
                           side = 'R'
                      cor = 0
                      if kx in self.tdcVetoCalib[s*10+l][side][bar]: 
                           cor = self.tdcVetoCalib[s*10+l][side][bar][kx][0]
                      elif kx>0: print('no correction:',s,l,side,bar,kx)
                      tdc[10+l][bar][side][kx] = aHit.GetTime(k) - cor
      # make plane alignment
          l0 = 0
          l1 = 1
          for bar in tdc[10+l0]:
             for side in tdc[10+l0][bar]:
                tdc0 = 0
                n=0
                for k in tdc[10+l0][bar][side]:
                     n+=1
                     tdc0+=tdc[10+l0][bar][side][k]
                if n<self.minChannels: continue
                tdc0 = tdc0/n
                for bar1 in [bar-1,bar,bar+1]:
                    if not bar1 in tdc[10+l1]: continue
                    if not side in tdc[10+l1][bar1]: continue
                    tdc1 = 0
                    n=0
                    for k in tdc[10+l1][bar1][side]:
                       n+=1
                       tdc1+=tdc[10+l1][bar1][side][k]
                    if n<self.minChannels: continue
                    tdc1 = tdc1/n
                    dt = tdc1-tdc0
                    key = self.M.sdict[s]+str(bar)+'_'+str(bar1)+side
                    rc = h['dtBar_'+key].Fill(dt)
   def Finalize(self):
       h = self.M.h
       s = 1
       h['matrix'] = {}
       for side in ['L','R']:
           h['matrix'][side] = {}
           for bar in range(self.nbars):
                h['matrix'][side][bar] = {}
                for bar1 in [bar-1,bar,bar+1]:
                    if bar1 < 0 or bar1 > self.nbars: continue
                    histo = h['dtBar_Veto'+str(bar)+'_'+str(bar1)+side]
                    rc = histo.Fit('gaus','SQ')
                    h['matrix'][side][bar][bar1] = [histo.GetMean(),histo.GetMeanError()]

class vetoTDCchannelCalibration(ROOT.FairTask):
   "internal alignment"
   def Init(self,options,monitor):
       self.M = monitor
       self.options = options
       self.xCheck = False
       self.tag = ""
       if options.xCheck : 
           self.xCheck = True
           self.tag = "X"
       h = self.M.h
       s = 1
       for l in range(self.M.systemAndPlanes[s]):
          for bar in range(self.M.systemAndBars[s]):
             for side in ['L','R']:
                for k in range(8):
                   key = self.M.sdict[s]+str(s*10+l)+'_'+str(bar)+side+str(k)+self.tag
                   ut.bookHist(h,'dtChan_'+key,'dt '+key+";dt [timestamp]",200,-1.,1.)
       if self.xCheck:
            with open('tdcVetoInternalCalibration', 'rb') as fh:
               self.tdcVetoCalib = pickle.load(fh)

   def ExecuteEvent(self,event):
       h = self.M.h
       s = 1
       vetoHits = {10:[],11:[]}
       for aHit in event.Digi_MuFilterHits:
          if not aHit.isValid(): continue
          detID = aHit.GetDetectorID()//1000
          if not detID<20: continue
          vetoHits[detID].append(aHit)
       if not(len(vetoHits[10])==1) and not(len(vetoHits[11])==1): return
       for aTrack in event.Reco_MuonTracks:
          tdc = {10:{},11:{}}
          S = aTrack.getFitStatus()
          if not S.isFitConverged(): continue
          mom    = aTrack.getFittedState().getMom()
          pos      = aTrack.getFittedState().getPos()
          for l in range(2):
             zEx = self.M.zPos['MuFilter'][1*10+l]
             lam      = (zEx-pos.z())/mom.z()
             yEx        = pos.y()+lam*mom.y()
             xEx        = pos.x()+lam*mom.x()  # needed for correction of signal propagation
             for aHit in vetoHits[10+l]:
                detID = aHit.GetDetectorID()
                self.M.MuFilter.GetPosition(detID,A,B)
                D = (A[1]+B[1])/2. - yEx
                if abs(D)<5:
                   bar = (detID%1000)
                   tdc[10+l][bar] = {'L':{},'R':{}}
                   for k in range(16):
                      qdc = aHit.GetSignal(k)
                      if qdc <0: continue
                      kx = k
                      side = 'L'
                      if not k < 8 : 
                           kx = k - 8
                           side = 'R'
                      tdc[10+l][bar][side][kx] = aHit.GetTime(k)
                      if self.xCheck:
                          cor = 0
                          if kx in self.tdcVetoCalib[s*10+l][side][bar]:
                              cor = self.tdcVetoCalib[s*10+l][side][bar][kx][0]
                              tdc[10+l][bar][side][kx] -= cor
      # make internal alignment
          for l in range(2):
            for bar in tdc[10+l]:
             for side in tdc[10+l][bar]:
                if not refChannel in tdc[10+l][bar][side]: continue
                t0 = tdc[10+l][bar][side][refChannel]
                for k in tdc[10+l][bar][side]:
                   dt = tdc[10+l][bar][side][k]-t0
                   key = self.M.sdict[s]+str(10+l)+'_'+str(bar)+side+str(k)+self.tag
                   rc = h['dtChan_'+key].Fill(dt)

   def Finalize(self):
       h = self.M.h
       s = 1
       h['tdcCalib'] = {10:{'L':{},'R':{}},11:{'L':{},'R':{}}}
       for l in range(self.M.systemAndPlanes[s]):
          for side in ['L','R']:
             tname = 'v'+str(l)+side+self.tag
             ut.bookCanvas(h,tname,tname,2048,2048,8,8)
             for bar in range(self.M.systemAndBars[s]):
                 h['tdcCalib'][s*10+l][side][bar] = {}
                 for k in range(0,8):
                    h[tname].cd(bar*8+k+1)
                    key = self.M.sdict[s]+str(10+l)+'_'+str(bar)+side+str(k)+self.tag
                    dt = h['dtChan_'+key]
                    if not k == refChannel:  
                        rc = dt.Fit('gaus','SQ')
                        result = rc.Get()
                        if result:    h['tdcCalib'][s*10+l][side][bar][k]=[result.Parameter(1),result.Parameter(2)]
                    h['dtChan_'+key].Draw()

       ut.bookHist(h,'TDCshiftsMean'+self.tag,'TDCshiftsMean '+self.tag,100,-0.2,0.2)
       ut.bookHist(h,'TDCshiftsSigma'+self.tag,'TDCshiftsSigma '+self.tag,100,0.,0.25)
       for l in h['tdcCalib']:
           for side in h['tdcCalib'][l]:
              for bar in h['tdcCalib'][l][side]:
                 for k in h['tdcCalib'][l][side][bar]:
                     if k==refChannel: continue
                     rc = h['TDCshiftsMean'+self.tag].Fill(h['tdcCalib'][l][side][bar][k][0])
                     rc = h['TDCshiftsSigma'+self.tag].Fill(h['tdcCalib'][l][side][bar][k][1])
       ut.bookCanvas(h,'ChannelSummary'+self.tag,'Channel Summary',1200,600,2,1)
       tc = h['ChannelSummary'+self.tag].cd(1)
       h['TDCshiftsMean'+self.tag].Draw()
       tc = h['ChannelSummary'+self.tag].cd(2)
       h['TDCshiftsSigma'+self.tag].Draw()

       if not self.xCheck:
           with open('tdcVetoInternalCalibration', 'wb') as fh:
               pickle.dump(h['tdcCalib'], fh)
           ut.writeHists(h,'tdcCalib.root')
       else:
           ut.writeHists(h,'tdcCalibCor.root')

