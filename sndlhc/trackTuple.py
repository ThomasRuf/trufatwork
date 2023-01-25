# track ntuple
# type pos mom chi2 hits 
# extrapolation to US / DS, hit detid, residual
import ROOT
from array import array
import rootUtils as ut

def set_bit(value, n):
     return value | (1 << n)
def get_bit(value, n):
    return ((value >> n & 1) != 0)
A,B  = ROOT.TVector3(),ROOT.TVector3()

class TrackPersistency(ROOT.FairTask):
   " make track and related info persistent"
   def Init(self,options,monitor):
       self.options = options
       self.ftTrack = ROOT.TFile("tracks_"+str(options.runNumber).zfill(6)+".root",'recreate')
       self.M = monitor
       self.tTrack  = ROOT.TTree('tTrack','Trajectory')
       self.runNr   = array('i',1*[0])
       self.eventNr = array('i',1*[0])
       self.weight  = array('f',1*[0])
       self.bunchXtypes = array('i',1*[0])   # 
       self.trackConfig = array('i',1*[0])   # 01 scifi only, 10 DS only, 11 scifi and DS
       self.chi2        = array('f',2*[0])
       self.ndof        = array('f',2*[0])
       self.mom         = array('f',6*[0])
       self.pos         = array('f',6*[0])
       self.detIDs      = array('i',48*[0])
       self.qdcs        = array('f',48*[0])
       self.wqdcs        = array('f',48*[0])
       self.res         = array('f',48*[0])
       self.velocity    = array('f',2*[0])
       self.tTrack.Branch('runNr',self.runNr,'runNr/I')
       self.tTrack.Branch('eventNr',self.eventNr,'eventNr/I')
       self.tTrack.Branch('weight',self.weight,'weight/F')
       self.tTrack.Branch('bunchXtypes',self.bunchXtypes,'bunchXtypes/I')
       self.tTrack.Branch('trackConfig',self.trackConfig,'trackConfig/I')
       self.tTrack.Branch('mom',self.mom,'mom[6]/F')
       self.tTrack.Branch('pos',self.pos,'pos[6]/F')
       self.tTrack.Branch('detIDs',self.detIDs,'detIDs[48]/I')
       self.tTrack.Branch('qdcs',self.qdcs,'qdcs[48]/F')
       self.tTrack.Branch('wqdcs',self.wqdcs,'wqdcs[48]/F')
       self.tTrack.Branch('res',self.res,'res[48]/F')
       self.tTrack.Branch('velocity',self.velocity,'velocity[2]/F')
       self.tTrack.Branch('chi2',self.chi2,'chi2[2]/F')
       self.tTrack.Branch('ndof',self.ndof,'ndof[2]/F')
       self.trackTask = self.M.FairTasks['simpleTracking']
       self.trackTask.DSnPlanes = 3 
       self.muFilterNumber = {10:0,11:1,20:2,21:3,22:4,23:5,24:6,30:7,31:8,32:9,33:10,34:11,35:12,36:13}
       self.scifiNumber    = {10:0,11:1,20:2,21:3,30:4,31:5,40:6,41:7,50:8,51:9}

   def ExecuteEvent(self,event):
       self.weight[0] = self.M.Weight
       self.runNr[0]  = self.options.runNumber
       if hasattr(event.EventHeader,"GetEventNumber"):
            self.eventNr[0]  = event.EventHeader.GetEventNumber()
       else:
            self.eventNr[0]  = self.M.EventNumber
       trackTask = self.trackTask
       self.trackConfig[0] = 0
       tmp = 0
       if self.M.xing['B1']: tmp = set_bit(tmp, 1)
       if self.M.xing['B2']: tmp = set_bit(tmp, 2)
       if self.M.xing['IP1']: tmp = set_bit(tmp, 11)
       if self.M.xing['IP2']: tmp = set_bit(tmp, 12)
       if self.M.xing['B1only']: tmp = set_bit(tmp, 10)
       if self.M.xing['B2noB1']: tmp = set_bit(tmp, 20)
       if self.M.xing['noBeam']: tmp = set_bit(tmp, 0)
       self.bunchXtypes[0] = tmp
       for k in range(48):
          self.detIDs[k] = 0
          self.qdcs[k] = 0
          self.wqdcs[k] = 0
          self.res[k] = 0
       for k in range(2):
          self.velocity[k] = -999
          self.ndof[k] = -999
          self.chi2[k] = -999

       for theTrack in self.M.Reco_MuonTracks:
            fitStatus = theTrack.getFitStatus()
            if not fitStatus.isFitConverged(): continue
            if theTrack.GetUniqueID() ==1: 
                 self.trackConfig[0] +=1
                 ttype = 0
            if theTrack.GetUniqueID() ==3: 
                 self.trackConfig[0] +=10
                 ttype = 1
            if theTrack.GetUniqueID() ==1: 
              SL = trackTask.trackDir(theTrack)
              if SL: self.velocity[ttype] = SL[0]
            self.chi2[ttype] = fitStatus.getChi2()
            self.ndof[ttype] = fitStatus.getNdf()
            fstate =  theTrack.getFittedState()
            pos,mom = fstate.getPos(),fstate.getMom()
            self.mom[0+3*ttype] = mom.x()
            self.mom[1+3*ttype] = mom.y()
            self.mom[2+3*ttype] = mom.z()
            self.pos[0+3*ttype] = pos.x()
            self.pos[1+3*ttype] = pos.y()
            self.pos[2+3*ttype] = pos.z()

            residuals = {}
            detIDs = {}
            qdcs = {}
            wqdcs = {}
            for aHit in event.Digi_MuFilterHits:
               if not aHit.isValid(): continue
               Minfo = self.M.MuFilter_PlaneBars(aHit.GetDetectorID())
               s,l,bar = Minfo['station'],Minfo['plane'],Minfo['bar']
               k = s*10+l
               if not k in residuals: 
                   residuals[k] = []
                   detIDs[k] = []
                   qdcs[k] = []
                   wqdcs[k] = 0
               detIDs[k].append(aHit.GetDetectorID())
               qdc = aHit.SumOfSignals()['Sum']
               qdcs[k].append(qdc)
               self.M.MuFilter.GetPosition(aHit.GetDetectorID(),A,B)
# calculate DOCA
               zEx = self.M.zPos['MuFilter'][k]
               lam = (zEx-pos.z())/mom.z()
               xEx,yEx = pos.x()+lam*mom.x(),pos.y()+lam*mom.y()
               pq = A-pos
               uCrossv= (B-A).Cross(mom)
               res = pq.Dot(uCrossv)/uCrossv.Mag()
               residuals[k].append(res)
               wqdcs[k]+= abs(res)*qdc
            for k in wqdcs: wqdcs[k] = wqdcs[k]/(sum(qdcs[k])+1E-10)
            for k in residuals:
               tmp = []
               for x in residuals[k]: tmp.append(abs(x))
               minRes = min(tmp)
               minK = tmp.index(minRes)
               self.detIDs[10+self.muFilterNumber[k]+ttype*24] = detIDs[k][minK]
               self.res[10+self.muFilterNumber[k]+ttype*24] = residuals[k][minK]
               self.qdcs[10+self.muFilterNumber[k]+ttype*24] = qdcs[k][minK]
               self.wqdcs[10+self.muFilterNumber[k]+ttype*24] = wqdcs[k]

            residuals = {}
            detIDs = {}
            for aCl in self.trackTask.clusScifi:
               detID = aCl.GetFirst()
               k = detID//100000
               if not k in residuals: 
                 residuals[k] = []
                 detIDs[k] = []
               detIDs[k].append(detID)
# calculate DOCA
               aCl.GetPosition(A,B)
               pq = A-pos
               uCrossv= (B-A).Cross(mom)
               residuals[k].append(pq.Dot(uCrossv)/uCrossv.Mag())
            for k in residuals:
               tmp = []
               for x in residuals[k]: tmp.append(abs(x))
               minRes = min(tmp)
               minK = tmp.index(minRes)
               self.detIDs[self.scifiNumber[k]+ttype*24] = detIDs[k][minK]
               self.res[self.scifiNumber[k]+ttype*24] = residuals[k][minK]
#

       if self.trackConfig[0]>0: self.tTrack.Fill()
          
   def Plot(self):
    self.ftTrack.Write() 
    self.ftTrack.Close()
   
class TrackReading(ROOT.FairTask):
   " read info from track ttree"
   def Init(self,runNumber):
       self.h = {}
       self.ftTrack = ROOT.TFile("tracks_"+str(runNumber).zfill(6)+".root")
       self.tTrack  = self.ftTrack.tTrack
       self.muFilterNumber = {10:0,11:1,20:2,21:3,22:4,23:5,24:6,30:7,31:8,32:9,33:10,34:11,35:12,36:13}
       self.rev_muFilterNumber = dict(map(reversed, self.muFilterNumber.items()))
       self.scifiNumber = {10:0,11:1,20:2,21:3,30:4,31:5,40:6,41:7,50:8,51:9}
       self.rev_scifiNumber = dict(map(reversed, self.scifiNumber.items()))
       self.planeNumber = {'mufi':{10:0,11:1,20:12,21:13,22:14,23:15,24:16,30:17,31:18,32:19,33:20,34:21,35:22,36:23},
                           'scifi':{10:2,11:3,20:4,21:5,30:6,31:7,40:8,41:9,50:10,51:11} }
#
       self.tt = {0:'scifi',1:'DS'}
# type of crossing, check for b1only,b2nob1,nobeam
       h = self.h
       for x in ['IP1','B1only','B2noB1','noBeam']:
        for d in ['scifi','DS']:
          ut.bookHist(h,d+'_trackSlopes'+x,'track slope; x/z [mrad]; y/z [mrad]',1000,-100,100,1000,-100,100)
          ut.bookHist(h,d+'_trackSlopesXL'+x,'track slope; x/z [rad]; y/z [rad]',2200,-1.1,1.1,2200,-1.1,1.1)
          ut.bookHist(h,d+'_trackPos'+x,'track pos; x [cm]; y [cm]',100,-90,10.,80,0.,80.)
          if d=='scifi':
            ut.bookHist(h,d+'_scifiplanes'+x,'planes and residual; n; residual [mm]',10,-0.5,9.5,100,-5.,5.)
            ut.bookHist(h,d+'_veusplanes'+x,'planes and residual; n; residual [cm]',7,-0.5,6.5,100,-10.,10.)
            ut.bookHist(h,d+'_dsplanes'+x,'planes and residual; n; residual [cm]',7,-0.5,6.5,200,-10.,10.)
          else:
            ut.bookHist(h,d+'_scifiplanes'+x,'planes and residual; n; residual [cm]',10,-0.5,9.5,100,-10.,10.)
            ut.bookHist(h,d+'_veusplanes'+x,'planes and residual; n; residual [cm]',7,-0.5,6.5,100,-10.,10.)
            ut.bookHist(h,d+'_dsplanes'+x,'planes and residual; n; residual [cm]',7,-0.5,6.5,100,-5.,5.)
          ut.bookHist(h,d+'_scifiQDC'+x,'planes and qdc; n; qdc',10,-0.5,9.5,100,-1.,10.)
          ut.bookHist(h,d+'_veusQDC'+x,'planes and qdc; n; qdc',7,-0.5,6.5,100,-5.,500.)
          ut.bookHist(h,d+'_dsQDC'+x,'planes and qdc; n; qdc',7,-0.5,6.5,100,-5.,200.)

          ut.bookHist(h,d+'_planes'+x,'planes hit by track; n',24,-0.5,23.5)
          ut.bookHist(h,d+'_planesT'+x,'planes hit by track; n',24,-0.5,23.5)
          ut.bookHist(h,d+'_planesE'+x,'planes hit by track; n',24,-0.5,23.5)
          ut.bookHist(h,d+'_planesET'+x,'planes hit by track; n',24,-0.5,23.5)
          ut.bookHist(h,d+'_tracksE'+x,'planes hit by track; n',24,-0.5,23.5)
          ut.bookHist(h,d+'_tracksET'+x,'planes hit by track; n',24,-0.5,23.5)
#
   def ExecuteEvent(self,n):
       tTrack = self.tTrack
       rc = tTrack.GetEvent(n)
       runNr   = tTrack.runNr
       eventNr = tTrack.eventNr
       weight  = tTrack.weight
       xing = {}
       xing['B1']     = get_bit(tTrack.bunchXtypes, 1)
       xing['B2']     = get_bit(tTrack.bunchXtypes, 2)
       xing['IP1']    = get_bit(tTrack.bunchXtypes, 11)
       xing['IP2']    = get_bit(tTrack.bunchXtypes, 12)
       xing['B1only'] = get_bit(tTrack.bunchXtypes, 10)
       xing['B2noB1'] = get_bit(tTrack.bunchXtypes, 20)
       xing['noBeam'] = get_bit(tTrack.bunchXtypes, 0)
       trackConfig = tTrack.trackConfig
       mom         = [ROOT.TVector3(tTrack.mom[0],tTrack.mom[1],tTrack.mom[2]),ROOT.TVector3(tTrack.mom[3],tTrack.mom[4],tTrack.mom[5])]
       pos         = [ROOT.TVector3(tTrack.pos[0],tTrack.pos[1],tTrack.pos[2]),ROOT.TVector3(tTrack.pos[3],tTrack.pos[4],tTrack.pos[5])]
       velocity    = tTrack.velocity
       chi2    = tTrack.chi2
       ndof    = tTrack.ndof
       detIDs = {'scifi':[{},{}],'mufi':[{},{}]}
       res    = {'scifi':[{},{}],'mufi':[{},{}]}
       qdcs   = {'scifi':[{},{}],'mufi':[{},{}]}
       wqdcs   = {'scifi':[{},{}],'mufi':[{},{}]}
       for k in range(10):
         for ttype in range(2):
            detIDs['scifi'][ttype][self.rev_scifiNumber[k]] = tTrack.detIDs[k+ttype*24]
            res['scifi'][ttype][self.rev_scifiNumber[k]] = tTrack.res[k+ttype*24]
            qdcs['scifi'][ttype][self.rev_scifiNumber[k]] = tTrack.qdcs[k+ttype*24]
       for k in range(14):
         for ttype in range(2):
            detIDs['mufi'][ttype][self.rev_muFilterNumber[k]] = tTrack.detIDs[10+k+ttype*24]
            res['mufi'][ttype][self.rev_muFilterNumber[k]] = tTrack.res[10+k+ttype*24]
            qdcs['mufi'][ttype][self.rev_muFilterNumber[k]] = tTrack.qdcs[10+k+ttype*24]
            wqdcs['mufi'][ttype][self.rev_muFilterNumber[k]] = tTrack.wqdcs[10+k+ttype*24]
# fill histograms
       h = self.h
       for x in ['IP1','B1only','B2noB1','noBeam']:
            if xing[x]: break
       
       for t in self.tt:
         if t==0 and trackConfig%2==0: continue
         if t==1 and trackConfig//10==0: continue
         if t==0 and velocity[t]<-0.04: continue     # remove backward tracks
         d = self.tt[t]
         sx = mom[t].x()/mom[t].z()
         sy = mom[t].y()/mom[t].z()
         rc = h[d+'_trackSlopes'+x].Fill(sx,sy)
         rc = h[d+'_trackSlopesXL'+x].Fill(sx,sy)
         rc = h[d+'_trackPos'+x].Fill(pos[t].x(),pos[t].y())
#
# select tracks in the center:
         if abs(sx)>0.1: continue
         if abs(sy)>0.1: continue
         if pos[t].x() < -40 or pos[t].x()>-15: continue
         if pos[t].y() < 20 or pos[t].y()>30: continue
#
         hitList = {'':[],'T':[]}
         for k in detIDs['scifi'][t]:
              if detIDs['scifi'][t][k]==0: continue
              s = (k//10-1)*2+k%2
              rs = res['scifi'][t][k]
              qdc = qdcs['scifi'][t][k]
              if t==0: rc = h[d+'_scifiplanes'+x].Fill(s,rs*10)
              if t==1: rc = h[d+'_scifiplanes'+x].Fill(s,rs)
              rc = h[d+'_scifiQDC'+x].Fill(s,qdc)
              rc = h[d+'_planes'+x].Fill(self.planeNumber['scifi'][k])
              hitList[''].append(self.planeNumber['scifi'][k])
              if abs(rs)>0.5 and t==0: continue
              if ndof[0]>12: continue
              rc = h[d+'_planesT'+x].Fill(self.planeNumber['scifi'][k])
              hitList['T'].append(self.planeNumber['scifi'][k])
         for k in detIDs['mufi'][t]:
              if detIDs['mufi'][t][k]==0: continue
              s = self.muFilterNumber[k]
              rs = res['mufi'][t][k]
              qdc = qdcs['mufi'][t][k]
              tagged = True
              if ndof[0]>12: tagged = False
              if k>26:
                      dsnr = s-7
                      rc = h[d+'_dsplanes'+x].Fill(dsnr,rs)
                      rc = h[d+'_dsQDC'+x].Fill(dsnr,qdc)
                      if abs(rs)>5 and t==0: tagged = False
                      if qdc<55 and (dsnr==0 or dsnr==2 or dsnr==4): tagged = False
                      if qdc<40 and (dsnr==1 or dsnr==3 or dsnr==5): tagged = False
                      if qdc<35 and (dsnr==6): tagged = False
              else:    
                      rc = h[d+'_veusplanes'+x].Fill(s,rs)
                      rc = h[d+'_veusQDC'+x].Fill(s,qdc)
                      if t==0:
                         if abs(rs)>10: tagged = False
                         if abs(rs)>5 and qdc<100: tagged = False  # low energy muons with lot of MS
                      if qdc<10 and (s==0): tagged = False
                      if qdc<10 and (s==1): tagged = False
                      if qdc<45 and (s==2): tagged = False
                      if qdc<55 and (s==3): tagged = False
                      if qdc<20 and (s==4): tagged = False
                      if qdc<45 and (s==5): tagged = False
                      if qdc<60 and (s==6): tagged = False
              rc = h[d+'_planes'+x].Fill(self.planeNumber['mufi'][k])
              hitList[''].append(self.planeNumber['mufi'][k])
              if tagged: 
                    rc = h[d+'_planesT'+x].Fill(self.planeNumber['mufi'][k])
                    hitList['T'].append(self.planeNumber['mufi'][k])
         rc = h[d+'_planes'+x].Fill(-1)  # put number of tracks in underflow
         if not ndof[0]>12: rc = h[d+'_planesT'+x].Fill(-1)  # put number of tracks in underflow
# special histo with hits only if hit in station n+1 exist
         for c in hitList:
            for n in hitList[c]:
               rc = h[d+'_tracksE'+c+x].Fill(n-1)
               if (n-1) in hitList[c]: rc = h[d+'_planesE'+c+x].Fill(n-1)
               else:
#                  if t==0 and (n-1)==0 and c=='T' and (1 in hitList['T'] and not 0 in hitList['T']) and 0 in hitList[''] :
                  if t==0 and (n-1)>(2+10+5) and c=='T' and (n in hitList['T'] and not n-1 in hitList['T']) and n-1 in hitList[''] :
                          k0 = self.rev_muFilterNumber[n-1-17]
                          k1 = self.rev_muFilterNumber[n-17]
                          print('event',eventNr,n,k0,detIDs['mufi'][t][k0],detIDs['mufi'][t][k1],
                          res['mufi'][t][k0],res['mufi'][t][k1],
                          qdcs['mufi'][t][k0],qdcs['mufi'][t][k1])

   def Plot(self):
       h = self.h
       for x in ['IP1','B1only','B2noB1','noBeam']:
          for d in ['scifi','DS']:
             for c in ['','E']:
               for t in ['','T']:
                  hname = d+'_planes'+c+t+x
                  if c=='':
                     h[hname].Scale(1/(h[hname].GetBinContent(-1)+1E-10))
                  else:
                     h[hname].Divide(h[d+'_tracks'+c+t+x])
                  h[hname].SetMinimum(0.95)
                  h[hname].SetMaximum(1.019)
                  h[hname].SetStats(0)
       x = 'IP1'
       for d in ['scifi','DS']:
          ut.bookCanvas(h,'res_'+d,'',1800,1200,2,2)
          ut.bookCanvas(h,'qdc_'+d,'',1800,1200,2,2)
          for c in ['planes','QDC']:
           for p in [d+'_scifi'+c+x,d+'_veus'+c+x,d+'_ds'+c+x]:
            for n in range(h[p].GetNbinsX()):
                s = p+'_'+str(n)
                h[s]=h[p].ProjectionY(s,n+1,n+1)
          tc = h['res_'+d].cd(1)
          s = d+'_veusplanes'+x+'_'+str(0)
          h[s].SetLineColor(ROOT.kRed)
          h[s].Draw()
          s = d+'_veusplanes'+x+'_'+str(1)
          h[s].SetLineColor(ROOT.kGreen)
          h[s].Draw('same')
          tc = h['res_'+d].cd(2)
          for n in range(10):
             s = d+'_scifiplanes'+x+'_'+str(n)
             h[s].SetLineColor(ROOT.kPink-n)
             if n==0: h[s].Draw()
             else: h[s].Draw('same')
          tc = h['res_'+d].cd(3)
          for n in range(2,2+5):
             s = d+'_veusplanes'+x+'_'+str(n)
             h[s].SetLineColor(ROOT.kViolet+3+n)
             if n==0: h[s].Draw()
             else: h[s].Draw('same')
          tc = h['res_'+d].cd(4)
          for n in range(7):
             s = d+'_dsplanes'+x+'_'+str(n)
             h[s].SetLineColor(ROOT.kOrange+n)
             if n==0: h[s].Draw()
             else: h[s].Draw('same')
          tc = h['qdc_'+d].cd(4)
          for n in range(7):
             s = d+'_dsQDC'+x+'_'+str(n)
             h[s].SetLineColor(ROOT.kOrange+n)
             if n==0: h[s].Draw()
             else: h[s].Draw('same')

if 0>1:
 run = 4705
 run = 5259
 import ROOT
 import trackTuple
 import rootUtils as ut
 test = trackTuple.TrackReading()
 test.Init(run)
 for n in range(250000): 
   test.ExecuteEvent(n)

            
