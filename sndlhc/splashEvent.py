sort digits by plane, look for earliest tdc per plane. plot tdc versus z
python -i /media/disk0/SNDBuild/sndsw/shipLHC/scripts/eventDisplay.py -g geofile_sndlhc_TI18.root -f sndsw_raw-0000.root
SHiPDisplay.NextEvent(6959)


for aHit in sTree.Digi_MuFilterHits:
              if not aHit.isValid(): continue
              s = aHit.GetDetectorID()//10000
              S = aHit.GetAllSignals()
              print(s,len(S))
import rootUtils as ut

def MuFilter_PlaneBars(detID):
         s = detID//10000
         l  = (detID%10000)//1000  # plane number
         bar = (detID%1000)
         if s>2:
             l=2*l
             if bar>59:
                  bar=bar-60
                  if l<6: l+=1
         return {'station':s,'plane':l,'bar':bar}

def Scifi_xPos(detID):
        orientation = (detID//100000)%10
        nStation = 2*(detID//1000000-1)+orientation
        mat   = (detID%100000)//10000
        X = detID%1000+(detID%10000)//1000*128
        return [nStation,mat,X]   # even numbers are Y (horizontal plane), odd numbers X (vertical plane)

if 1:
  for s in range(1,4): 
    ut.bookHist(h,'mult'+str(s),'hit mult for system '+str(s),100,-0.5,99.5)
    ut.bookHist(h,'multb'+str(s),'hit mult per bar for system '+str(s),20,-0.5,19.5)
  eventTree = sTree
  mult = {1:0,2:0,3:0}
  for aHit in eventTree.Digi_MuFilterHits:
              if not aHit.isValid(): continue
              s = aHit.GetDetectorID()//10000
              S = aHit.GetAllSignals()
              rc = h['multb'+str(s)].Fill(len(S))
              mult[s]+=len(S)
  for s in mult: rc = h['mult'+str(s)].Fill(mult[s])
  ut.bookCanvas(h,'noise','',1200,1200,2,3)
  for s in range(1,4):
   tc = h['noise'].cd(s*2-1)
   tc.SetLogy(1)
   h['mult'+str(s)].Draw()
   h['noise'].cd(s*2)
   h['multb'+str(s)].Draw()

 digis = {0:{},1:{},2:{},3:{}}
 for aHit in eventTree.Digi_MuFilterHits:
              if not aHit.isValid(): continue
              s = aHit.GetDetectorID()//10000
              tmin = 1E20
              for T in aHit.GetAllTimes():
                    if T.second<tmin: tmin = T.second
              Minfo = MuFilter_PlaneBars(aHit.GetDetectorID())
              s,l,bar = Minfo['station'],Minfo['plane'],Minfo['bar']
              if not l in digis[s]: digis[s][l]=[]
              digis[s][l].append(tmin)
 for aHit in eventTree.Digi_ScifiHits:
          if not aHit.isValid(): continue
          X =  Scifi_xPos(aHit.GetDetectorID())
          s = 0
          l = X[0]
          if not l in digis[s]: digis[s][l]=[]
          digis[s][l].append(aHit.GetTime(0))

 minTimePerPlane = {}
 for s in digis:
   for l in digis[s]:
    minTimePerPlane[s*10+l]  = sorted(digis[s][l])[0]
