import ROOT,os
from array import array
import rootUtils as ut

R = ''
#generate ccbar (msel=4) or bbbar(msel=5)
mselcb=4
nev=10000
nEpoints=20
Erange = [100,1000]
idbeam = [2112,130,3122]
target = {2212:'p+',2112:'n0'}

#  Assume tungsten target, fracp is the fraction of protons in nucleus, i.e. 74/184.
#  Used to average chi on p and n target in Pythia.
fracp=0.40

PDG = ROOT.TDatabasePDG.Instance()
myPythia = ROOT.TPythia6()
tp = ROOT.tPythia6Generator()

# Pythia6 can only accept names below in pyinit, hence reset PDG table:
PDG.GetParticle(2212).SetName('p+')
PDG.GetParticle(2112).SetName('n0')
PDG.GetParticle(-2112).SetName('nbar0')
PDG.GetParticle(130).SetName('KL0')
#lower lowest sqrt(s) allowed for generating events
myPythia.SetPARP(2,2.)

def PoorE791_tune(P6):
# settings with default Pythia6 pdf, based on getting <pt> at 500 GeV pi-
# same as that of E791: http://arxiv.org/pdf/hep-ex/9906034.pdf
  print(' ')
  print('********** PoorE791_tune **********')
  #change pt of D's to mimic E791 data.
  P6.SetPARP(91,1.6)
  print('PARP(91)=',P6.GetPARP(91))
  #what PDFs etc.. are being used:
  print('MSTP PDF info, i.e. (51) and (52)=',P6.GetMSTP(51),P6.GetMSTP(52))
  #set multiple interactions equal to Fortran version, i.e.=1, default=4, and adapt parp(89) accordingly
  P6.SetMSTP(82,1)
  P6.SetPARP(89,1000.)
  print('And corresponding multiple parton stuff, i.e. MSTP(82),PARP(81,89,90)=',P6.GetMSTP(82),P6.GetPARP(81),P6.GetPARP(89),P6.GetPARP(90))
  print('********** PoorE791_tune **********')
  print(' ')

def LHCb_tune(P6):
# settings by LHCb for Pythia 6.427 
# https://twiki.cern.ch/twiki/bin/view/LHCb/SettingsSim08
  print(' ')
  print('********** LHCb_tune **********')
  #P6.SetCKIN(41,3.0)
  P6.SetMSTP(2,	2)
  P6.SetMSTP(33,	3)
  #P6.SetMSTP(128,	2)  #store or not store 
  P6.SetMSTP(81,	21)
  P6.SetMSTP(82,	3)
  P6.SetMSTP(52,	1)  # 1 internal pythia, 2 PDFLIB
  P6.SetMSTP(51,	7)    # 10042)# (ie CTEQ6 LO fit, with LOrder alpha_S PDF from LHAPDF)
  P6.SetMSTP(142,	0) #do not weigh events
  P6.SetPARP(67,	1.0)
  P6.SetPARP(82,	4.28)
  P6.SetPARP(89,	14000)
  P6.SetPARP(90,	0.238)
  P6.SetPARP(85,	0.33)
  P6.SetPARP(86,	0.66)
  P6.SetPARP(91,	1.0)
  P6.SetPARP(149,	0.02)
  P6.SetPARP(150,	0.085)
  P6.SetPARJ(11,	0.4)
  P6.SetPARJ(12,	0.4)
  P6.SetPARJ(13,	0.769)
  P6.SetPARJ(14,	0.09)
  P6.SetPARJ(15,	0.018)
  P6.SetPARJ(16,	0.0815)
  P6.SetPARJ(17,	0.0815)
  P6.SetMSTJ(26,	0)
  P6.SetPARJ(33,	0.4)
  print('********** LHCb_tune **********')
  print(' ')

#choose the Pythia tune:
pythiaTune = "E791" # "LHCb"  # "E791"
if pythiaTune == "E791" : PoorE791_tune(myPythia)
if pythiaTune == "LHCb" : LHCb_tune(myPythia)
#avoid any printing to the screen, only when LHAPDF is used, i.e. LHCb tune.
#myPythia.OpenFortranFile(6, os.devnull)

#histogram helper
h={}

#  Pythia output to dummy (11) file (to screen use 6)
myPythia.OpenFortranFile(11, os.devnull)
myPythia.SetMSTU(11, 11) # myPythia.SetMSTU(11, 6), myPythia.Pystat(2)

charmContent={}
for idp in idbeam:
    name=PDG.GetParticle(idp).GetName()
    charmContent[idp]={}
    for t in [2212,2112]:
      tname=PDG.GetParticle(t).GetName()
      gname = 'sigma vs p, '+name+'->'+target[t]
      h[gname]=ROOT.TGraph() 
      cname = 'sigma charm vs p, '+name+'->'+target[t]
      h[cname]=ROOT.TGraph() 
      step = (Erange[1]-Erange[0])/nEpoints
      charmContent[idp][t]={}
      for n in range(nEpoints):
         E = n*step+Erange[0]
         charmContent[idp][t][E]={421:0,-421:0,411:0,-411:0,431:0,-431:0,13:0,-13:0,'muon':0}
         myPythia.SetMSEL(mselcb)       # set forced ccbar or bbbar generation
         myPythia.Initialize('FIXT',name,target[t],E)
         for iev in range(nev): 
            myPythia.GenerateEvent()
            # search for muon
            withMuon = False
            for itrk in range(1,myPythia.GetN()+1):
              ID = myPythia.GetK(itrk,2)
              if ID in charmContent[idp][t][E]: charmContent[idp][t][E][ID]+=1
              if abs(ID) == 13: withMuon = True
            if withMuon: charmContent[idp][t][E]['muon']+=1
                 
#  signal run finished, get inelastic cross-section, subtract elastic from total
         xsec = (tp.getPyint5_XSEC(2,0)-tp.getPyint5_XSEC(2,91)) * charmContent[idp][t][E]['muon']/nev
         print('%s->%s %5.1F, %5.2G'%(name,tname,E,xsec))
         h[gname].AddPoint(E,xsec)
         xsec = (tp.getPyint5_XSEC(2,0)-tp.getPyint5_XSEC(2,91))
         h[cname].AddPoint(E,xsec)

# get inelastic cross section
for idp in idbeam:
    name=PDG.GetParticle(idp).GetName()
    for t in [2212,2112]:
      tname=PDG.GetParticle(t).GetName()
      gname = 'inel sigma vs p, '+name+'->'+target[t]
      h[gname]=ROOT.TGraph() 
      step = (Erange[1]-Erange[0])/nEpoints
      for n in range(nEpoints):
         E = n*step+Erange[0]
         myPythia.SetMSEL(2)       # mbias event
         myPythia.Initialize('FIXT',name,target[t],E)
         for iev in range(nev): 
            myPythia.GenerateEvent()
#  get cross-section
         xsec = tp.getPyint5_XSEC(2,0)
         h[gname].AddPoint(E,xsec)
         
A=184  
sigma_inel = {'n0':8.7,'Lambda0':8.7,'KL0':8.7*2/3 }  # 8.7 mbarn proton/neutron per nucleon
# what about KL? should be 2/3 * 8.9

if 1:
 ut.bookHist(h,'xsec',';GeV;mbarn',100,0.,Erange[1])
 ut.bookCanvas(h,'tc','',1200,600,1,1)
 h['xsec'].SetMaximum(0.0025)
 h['xsec'].SetMinimum(0.0)
 h['xsec'].SetStats(0)
 h['xsec'].Draw()
 h['sigma vs p, n0->p+'].SetLineColor(ROOT.kBlue)
 h['sigma vs p, n0->n0'].SetLineColor(ROOT.kCyan)
 h['sigma vs p, KL0->p+'].SetLineColor(ROOT.kRed)
 h['sigma vs p, KL0->n0'].SetLineColor(ROOT.kOrange)
 h['sigma vs p, Lambda0->p+'].SetLineColor(ROOT.kGreen)
 h['sigma vs p, Lambda0->n0'].SetLineColor(ROOT.kGreen)
 h['sigma vs p, n0->p+'].Draw('same')
 h['sigma vs p, KL0->p+'].Draw('same')
 h['sigma vs p, KL0->n0'].Draw('same')
 h['sigma vs p, n0->n0'].Draw('same')
 h['sigma vs p, Lambda0->p+'].Draw('same')
 h['sigma vs p, Lambda0->n0'].Draw('same')
 for idp in idbeam:
    name=PDG.GetParticle(idp).GetName()
    for t in [2212,2112]:
      tname=PDG.GetParticle(t).GetName()
      gname = 'sigma vs p, '+name+'->'+target[t]
      h['chi '+gname]=ROOT.TGraph()
      h['chi '+gname].SetLineColor(h[gname].GetLineColor())
      for n in range(h[gname].GetN()):
         h['chi '+gname].SetPoint(n,h[gname].GetPointX(n),h[gname].GetPointY(n)/sigma_inel[name])
      gname = 'sigma charm vs p, '+name+'->'+target[t]
      h['chi '+gname]=ROOT.TGraph()
      h['chi '+gname].SetLineColor(h[gname].GetLineColor())
      for n in range(h[gname].GetN()):
         h['chi '+gname].SetPoint(n,h[gname].GetPointX(n),h[gname].GetPointY(n)/sigma_inel[name])
 ut.bookHist(h,'chi',';GeV;ccbar with muon / total',100,0.,Erange[1])
 h['chi'].SetMaximum(0.4/1000.)
 h['chi'].SetMinimum(0.0)
 h['chi'].SetStats(0)
 h['chi'].Draw()
 h['chi sigma vs p, n0->p+'].Draw('same')
 h['chi sigma vs p, KL0->p+'].Draw('same')
 h['chi sigma vs p, KL0->n0'].Draw('same')
 h['chi sigma vs p, Lambda0->p+'].Draw('same')
 h['chi sigma vs p, Lambda0->n0'].Draw('same')
 h['chi sigma vs p, n0->n0'].Draw('same')
 
 ut.bookHist(h,'chi charm',';GeV;ccbar / total',100,0.,Erange[1])
 h['chi charm'].SetMaximum(0.4/1000.)
 h['chi charm'].SetMinimum(0.0)
 h['chi charm'].SetStats(0)
 h['chi charm'].Draw()
 h['chi sigma charm vs p, n0->p+'].Draw('same')
 h['chi sigma charm vs p, KL0->p+'].Draw('same')
 h['chi sigma charm vs p, KL0->n0'].Draw('same')
 h['chi sigma charm vs p, Lambda0->p+'].Draw('same')
 h['chi sigma charm vs p, Lambda0->n0'].Draw('same')
 h['chi sigma charm vs p, n0->n0'].Draw('same')

neutralRates = {}
neutralRatesG = {}
neutralRatesG['n0']={100:6.8E3+6.1E3,200:1.9E3+2.1E3,300:1E3+483.7,500:95.6+119.1,1000:0}
neutralRatesG['KL0']={100:1.2E4,200:3.9E3,300:1.6E3,500:527.4,1000:26.4}
neutralRatesG['KS0']={100:1.2E4,200:4.4E3,300:2.4E3,500:444.7,1000:0}
neutralRatesG['Lambda0']={100:1.8E3+2.9E3,200:573.6+1.4E3,300:134.3+132.5,500:18.9+81.7,1000:0}
# differential rates
for m in neutralRatesG:
  neutralRates[m]={}
  E = list(neutralRatesG[m].keys())
  E.reverse()
  S = 0
  for e in E:
     v = neutralRatesG[m][e] - S
     if m == 'KS0': name = 'KL0'
     else: name = m
     neutralRates[m][e] = v/150.*30.*0.5*(h['chi sigma vs p, '+name+'->n0'].Eval(e)+h['chi sigma vs p, '+name+'->p+'].Eval(e))
     S += neutralRatesG[m][e]

if 1:
 E.sort()
 txt = "energy        "
 for e in E:
     txt+=" %5i   "%(e)
 print(txt)
 for m in neutralRates:
   txt = "%10s  "%(m)
   for e in E:
     txt+="   %5.1G "%(neutralRates[m][e] )
   print(txt)

ut.writeHists(h,'neutralXsec-'+pythiaTune+'.root')
import pickle
f=open("neutralXsec-"+pythiaTune+".pkl",'wb')
pickle.dump(charmContent,f)
f.close()


def charmXsec():
   energies = list(charmContent[2112][2212].keys())
   energies.sort()
   for E in energies:
      h['charmXsec'] = {}
      for X in charmContent[2112][2212][E]:
         if not X in h['charmXsec']: h['charmXsec'][X]=ROOT.TGraph()
         xsec = h['sigma vs p, n0->p+'].Eval(E)/charmContent[2112][2212][E]['muon']*charmContent[2112][2212][E][X]
         h['charmXsec'][X].AddPoint(E,xsec)
   for X in h['charmXsec']:
        if X=='muon': continue
        print('%s  xsec at 400GeV = %5.2F ub'%(PDG.GetParticle(X).GetName(),h['charmXsec'][X].Eval(400)*1000))

#  C. Lourenco and H. Wohri, Heavy flavour hadro-production from fixed-target to collider energies, P hys.Rept. 433, 127180, https://arxiv.org/pdf/hep-ph/0609101.pdf
# NA27 D0+D0bar 400GeV = 18.3+/-2.5
#      D++D-           = 11.9+/-1.5

charmXsec()

