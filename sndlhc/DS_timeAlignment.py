import ROOT,os,sys
import rootUtils as ut

f = ROOT.TFile('run004705.root')
ROOT.gROOT.cd()
h={}

def start():
 for x in ['dTScifiDS','dTcorScifiDS']:
  for d in ['','B2noB1','B1only']:
   dd=''
   if d!='': dd = d+'/'
   h['mufi-'+x+d] = f.mufilter.Get(dd+'mufi-'+x+d).Clone('mufi-'+x+d)
   h['mufi-'+x+d].Draw()
   h['mufi-'+x+d].Print('mufi-'+x+d+'.png')

def start0(p='tmp4705p9'):
   detector = 'mufi-'
   s=3
   wanted = []
   for d in ['','B2noB1','B1only']:
    for l in range(7):
     tag = str(s)+str(l)+d
     wanted.append(detector+'dT_'+tag)
     wanted.append(detector+'dTA_'+tag)
     wanted.append(detector+'dTB_'+tag)
   ut.readHists(h,p,wanted=wanted)
   S = {1:[1800,800,2,1],2:[1800,1500,2,3],3:[1800,1800,2,4]}
   ut.bookCanvas(h,detector+'dTScifimufi','dt rel to scifi DS',S[s][0],S[s][1],S[s][2],S[s][3])
   ut.bookCanvas(h,detector+'dTAScifimufi','dt rel to scifi DS',S[s][0],S[s][1],S[s][2],S[s][3])
   ut.bookCanvas(h,detector+'dTBScifimufi','dt rel to scifi DS',S[s][0],S[s][1],S[s][2],S[s][3])
   for l in range(7):
              n = l+1
              tag = str(s)+str(l)
              if s==3 and n==7: n=8
              tc = h[detector+'dTScifimufi'].cd(n)
              h[detector+'dT_'+tag].Draw('colz')
              tc = h[detector+'dTAScifimufi'].cd(n)
              h[detector+'dTA_'+tag].Draw('colz')
              tc = h[detector+'dTBScifimufi'].cd(n)
              h[detector+'dTB_'+tag].Draw('colz')
   h[detector+'dTScifimufi'].Print('mufi-dTScifiDS.png')

def xCheck():
   ut.bookCanvas(h,'xCheckH',' ',1200,600,1,1)
   ut.bookCanvas(h,'xCheckV',' ',1200,600,1,1)
   tcolors = [0,ROOT.kRed,ROOT.kRed,ROOT.kBlue,ROOT.kBlue,ROOT.kGreen,ROOT.kGreen,ROOT.kCyan,ROOT.kCyan]
   h['meanAndSig'] = {}
   for b in ['','B2noB1']:
    j=0
    tc = h['mufi-dTcorScifiDS'+b]
    h['meanAndSig'][b] = {}
    xmin,xmax = -5.,5.
    if b=='B2noB1': xmin,xmax = -18.,-8.
    for pad in tc.GetListOfPrimitives():
      j+=1
      if j==7: j==8
      tpad = tc.cd(j)
      for x in pad.GetListOfPrimitives():
         if not x.ClassName().find('TH')<0:
            if j%2==1: tcX = h['xCheckH'].cd()
            else: tcX = h['xCheckV'].cd()
            hname = x.GetName()
            h[hname] = x.Clone(hname)
            h[hname+'B1'] = h[hname].ProjectionX(hname+'B1')
            h[hname+'B1'].SetStats(0)
            h[hname+'B1'].SetLineColor(tcolors[j])
            h[hname+'B1'].SetMarkerColor(tcolors[j])
            h[hname+'B1'].SetMarkerStyle(30+j)
            rc = h[hname+'B1'].Fit('gaus','SQ','',xmin,xmax)
            fitRes = rc.Get()
            h[hname+'B1'].GetFunction('gaus').SetLineColor(tcolors[j])
            h['meanAndSig'][b][j] = [fitRes.Parameter(1),fitRes.Parameter(2)]
   plots = {'H':[0,2,4],'V':[1,3,5,6]}
   b=''
   txt = ROOT.TLatex()
   txt.SetTextFont(42)
   txt.SetTextSize(0.04)
   for c in plots:
      tcX = h['xCheck'+c].cd()
      tcX.SetLogy(1)
      j=0
      for x in plots[c]:
         if x<2: h['mufi-dTcor_3'+str(x)+'B1'].Draw()
         else: h['mufi-dTcor_3'+str(x)+'B1'].Draw('same')
         if x==6: m,s = h['meanAndSig'][b][x+2]
         else: m,s = h['meanAndSig'][b][x+1]
         h['txt'+str(x)] = txt.DrawLatexNDC(0.15,0.85-j*0.05,"DS%i%s  m=%5.2Fns  #sigma=%5.2Fns"%(x//2,c,m,s))
         h['txt'+str(x)].SetTextColor(h['mufi-dTcor_3'+str(x)+'B1'].GetLineColor())
         j+=1
      j+=1
      if c=='H':
       h['txtB2H'] = txt.DrawLatexNDC(0.15,0.85-j*0.05,"BW tracks DS0H: %5.2Fns DS1H: %5.2Fns DS2H: %5.2Fns  "%(
         h['meanAndSig']['B2noB1'][1][0],h['meanAndSig']['B2noB1'][3][0],h['meanAndSig']['B2noB1'][5][0]))
       h['txtB2H'].SetTextColor(ROOT.kMagenta)
      else:
       h['txtB2V'] = txt.DrawLatexNDC(0.15,0.85-j*0.05,"BW tracks DS0V: %5.2Fns DS1V: %5.2Fns DS2V: %5.2Fns  DS3V: %5.2Fns  "%(
         h['meanAndSig']['B2noB1'][2][0],h['meanAndSig']['B2noB1'][4][0],h['meanAndSig']['B2noB1'][6][0],h['meanAndSig']['B2noB1'][8][0]))
       h['txtB2V'].SetTextColor(ROOT.kMagenta)
      h['xCheck'+c].Update()
      h['xCheck'+c].Print('mufi-dTScifiDS-xCheck'+c+'.png')


par0={}
alignTpar = {}
alignTparB2 = {}

def execute():
  s=3
  detector = 'mufi-'
  ut.bookCanvas(h,'c1','',640,480,1,1)
  h['c1'].cd()
  for l in range(7):
    tag = str(s*10+l)
    hist = h[detector+'dT_'+tag]
    alignTpar[s*10+l] = {}
    alignTparB2[s*10+l] = {}
    for i in range(hist.GetNbinsY()):
        tagi = str(i*1000+s*10+l)
        alignTpar[s*10+l][i] = [100,-100]
        h['tmp'+tagi] = hist.ProjectionX('tmp'+tagi,i+1,i+1)
        tmp = h['tmp'+tagi]
        rc = tmp.Fit('gaus','SQ','',-10,-2)
        fitres = rc.Get()
        if fitres:
             alignTpar[s*10+l][i]=[fitres.Parameter(1),fitres.Parameter(2)]
        alignTparB2[s*10+l][i] = [100,-100]
        tmp = h[detector+'dT_'+tag+'B2noB1'].ProjectionX('tmp',i+1,i+1)
        rc = tmp.Fit('gaus','SQ','',-25,-15)
        fitres = rc.Get()
        if fitres:
             alignTparB2[s*10+l][i]=[fitres.Parameter(1),fitres.Parameter(2)]
  ut.bookHist(h,'talign','time alignment B1;channel;offset [ns]',7*120,-0.5,7*120-0.5)
  ut.bookHist(h,'talign2','time alignment B2;channel;offset [ns]',7*120,-0.5,7*120-0.5)
  ut.bookHist(h,'tres','time diff res;channel;sigma [ns]',7*120,-0.5,7*120-0.5)
  ut.bookHist(h,'t12','time diff B1 B2;channel;sigma [ns]',7*120,-0.5,7*120-0.5)
  for l in range(7):
    for i in range(hist.GetNbinsY()):
       k = l*120
       rc = h['talign'].Fill(k+i,alignTpar[s*10+l][i][0])
       rc = h['talign2'].Fill(k+i,alignTparB2[s*10+l][i][0])
       rc = h['tres'].Fill(k+i,abs(alignTpar[s*10+l][i][1]))
       if alignTpar[s*10+l][i][0]<99 and alignTparB2[s*10+l][i][0]<99:
           rc = h['t12'].Fill(k+i,alignTparB2[s*10+l][i][0]-alignTpar[s*10+l][i][0])
       else: rc = h['t12'].Fill(k+i,100)
  h['talign'].SetMinimum(-10)
  h['talign'].SetMaximum(1)
  h['talign2'].SetMinimum(-25)
  h['talign2'].SetMaximum(1)
  h['tres'].SetMinimum(0)
  h['tres'].SetMaximum(2.5)
  h['talign'].SetMarkerStyle(30)
  h['talign'].SetMarkerColor(ROOT.kRed)
  h['talign2'].SetMarkerStyle(32)
  h['talign2'].SetMarkerColor(ROOT.kBlue)
  h['tres'].SetMarkerStyle(31)
  h['tres'].SetMarkerColor(ROOT.kGreen)
  h['tres'].SetStats(0)
  h['talign'].SetStats(0)
  h['talign2'].SetStats(0)
  ut.bookCanvas(h,'results','DS time alignment',2400,1200,1,2)
  tc = h['results'].cd(1)
  h['talign'].Draw('phist')
  tc = h['results'].cd(2)
  h['tres'].Draw('phist')
  h['results'].Print('DStimeAlign-run004705.png')
  h['t12'].SetMinimum(-30)
  h['t12'].SetMaximum(0)
  h['t12'].SetStats(0)
  h['t12'].SetMarkerColor(ROOT.kMagenta)
  h['t12'].SetMarkerStyle(53)

  ut.bookCanvas(h,'results2','time diff between FW and BW tracks',1200,600,1,1)
  h ['results2'].cd()
  h['t12'].Draw('phist')
  h['results2'].Print('DStimeAlignFWBW-run004705.png')
  
  for k in range(0,4):
    h['talignReorder'+str(k)] = h['talign'].Clone('talignReorder'+str(k))
    h['talignReorder'+str(k)].Reset()
  slope = 0.082
  for i in range(h['talign'].GetNbinsX()):
     if i<120 and i%2==0: p=0
     elif i<120 and i%2==1: p=1
     elif i<240 and i%2==0: p=2
     elif i<360 and i%2==0: p=3
     elif i<360 and i%2==1: p=4
     elif i<480 and i%2==0: p=5
     elif i<600 and i%2==0: p=6
     elif i<600 and i%2==1: p=7
     elif i<720 and i%2==0: p=8
     elif i<840 and i%2==0: p=9
     else: continue
     if i%2==0: j=(i//2)%60
     if i%2==1: j=((i-1)//2)%60
     X = h['talign'].GetBinContent(i+1)
     h['talignReorder0'].SetBinContent(j+1+p*60,X)
     h['talignReorder1'].SetBinContent(j+1+p*60,X)
     channel = (j+1+p*60)%60
     if channel<30: X+= channel*slope - 15*slope
     else: X-=(channel-30)*slope - 15*slope
     h['talignReorder2'].SetBinContent(j+1+p*60,X)

  for l in range(0,3):
    c = 'talignReorder'+str(l)
    ut.bookCanvas(h,'results'+c,'DS time alignment '+str(l),1200,600,1,1)
    h['results'+c].SetGridy(1)
    h['results'+c].cd()
    par0[l]={}
    for x in h[c].GetListOfFunctions(): x.Delete()
    if l==2:
       par1 = 0
       planes = 20
       iv = 30
       h[c].SetMinimum(-7)
       h[c].SetMaximum(-4)
    else: 
       par1 = slope
       planes = 20
       iv = 30
       h[c].SetMinimum(-8)
       h[c].SetMaximum(-3)
    for p in range(planes):
      imin = 0.+p*iv
      imax = 0.+imin+iv
      theFun =  'fun'+str(l*100+p)
      h[theFun]=ROOT.TF1(theFun,'[0]+x*[1]')
      sign = 1
      if p%2==0: sign = -1
      h[theFun].SetParameter(0, -6)
      if l>0: h[theFun].FixParameter(1, sign*par1)
      rc = h[c].Fit(h[theFun],'SQw+','',imin+2,imax-2)
      res = rc.Get()
      ix = 2
      while res.Chi2() > 1.5:
          ix+=2
          if imax-ix < imin+2: 1/0
          if h[c].GetFunction(theFun): h[c].GetFunction(theFun).Delete()
          if p==3: rc = h[c].Fit(h[theFun],'SQw+','',imin+ix,imax-ix)
          else   : rc = h[c].Fit(h[theFun],'SQw+','',imin+2,imax-ix)  # vertical no statistics
          res = rc.Get()
      par0[l][p]=[res.Parameter(0),res.Parameter(1)]
      print("%i slope %5.3F b = %5.2F"%(p,res.Parameter(1),res.Parameter(0)))
    h[c].GetXaxis().SetRange(1,600)
    h[c].Draw()
    h['results'+c].Print('DStimeAlignFit'+str(l)+'-run004705.png')
    
  c = 'talignReorder3'
  ut.bookHist(h,'resT','t residuals',100,-3.,3.)
  for i in range(h[c].GetNbinsX()):
     p = i//30
     if p<20:
         res = h[c.replace('3','2')].GetBinContent(i+1)-par0[2][p][0]
         h[c].SetBinContent(i+1,res)
         rc = h['resT'].Fill(res)
  ut.bookCanvas(h,'results'+c,'DS time alignment 3',1200,600,1,1)
  h['results'+c].SetGridy(1)
  h['results'+c].cd()
  h[c].GetXaxis().SetRange(1,600)
  h[c].SetMinimum(-1)
  h[c].SetMaximum(1)
  h[c].Draw()
  h['results'+c].Print('DStimeAlignFit3'+'-run004705.png')
  h['c1'].cd()
  rc = h['resT'].Fit('gaus','S','')
  h['c1'].Update()
  stats = h['resT'].FindObject('stats')
  stats.SetOptFit(1)
  stats.SetOptStat(1000000000)
  stats.SetX1NDC(0.595611)
  stats.SetY1NDC(0.614035)
  stats.SetX2NDC(0.979624)
  stats.SetY2NDC(0.936404)
  h['c1'].Print('DStimeResiudals'+'-run004705.png')
      
  h['c1'].cd()
  for I in [ [10.5,89.5],[249.5,328.5],[492.5,571.5] ]:
      p+=1
      rc = h['t12'].Fit('pol1','SQ','',I[0],I[1])
      res = rc.Get()
      print("%i delta t = %5.2F"%(p,res.Parameter(0)))
  m=0
  for i in par0[0]:
   m+=abs(par0[0][i][1])
  print('average slope = ',m/len(par0[0]))


