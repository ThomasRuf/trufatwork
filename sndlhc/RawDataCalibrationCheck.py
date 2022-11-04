import ROOT,os
import boardMappingParser
from XRootD import client
import rootUtils as ut
import atexit

def pyExit():
       print("Make suicide until solution found for freezing")
       os.system('kill '+str(os.getpid()))
atexit.register(pyExit)
h={}

server = os.environ['EOSSHIP']
path = "/eos/experiment/sndlhc/raw_data/commissioning/TI18/data/run_005024"
fname = server+path+"/data_0024.root"
with client.File() as f:
      f.open(server+path+"/board_mapping.json")
      status, jsonStr = f.read()
  # pass the read string to getBoardMapping()
      boardMaps = boardMappingParser.getBoardMapping(jsonStr)
      f.close()
      slots = {0:'A',1:'A',2:'B',3:'B',4:'C',5:'C',6:'D',7:'D'}
      MufiSystem = {}
      for b in boardMaps['MuFilter']:
           board_id = int(b.split('_')[1])
           MufiSystem[board_id]={}
           for x in boardMaps['MuFilter'][b]:
               for slot in slots:
                  s = 0
                  tmp = boardMaps['MuFilter'][b][x].split('_')[0]
                  if tmp=='US': s = 1
                  elif tmp=='DS': s = 2
                  if slots[slot]==x: MufiSystem[board_id][slot]=s

      f.open(server+path+"/qdc_cal.csv")
      status, L = f.read()
      Lqdc = L.decode().split('\n')
      f.close()
      f.open(server+path+"/tdc_cal.csv")
      status, L = f.read()
      Ltdc = L.decode().split('\n')
      f.close()
  # calibration data
      qdc_cal = {}
      L = Lqdc
      for l in range(1,len(L)):
               tmp = L[l].replace('\n','').split(',')
               if len(tmp)<10:continue
               board_id = int(tmp[0])
               if not board_id in qdc_cal: qdc_cal[board_id]={}
               fe_id = int(tmp[1])
               if not fe_id in qdc_cal[board_id]: qdc_cal[board_id][fe_id]={}
               channel = int(tmp[2])
               if not channel in qdc_cal[board_id][fe_id]: qdc_cal[board_id][fe_id][channel]={}
               tac = int(tmp[3])
               if not tac in qdc_cal[board_id][fe_id][channel]: qdc_cal[board_id][fe_id][channel][tac]={}
               X = qdc_cal[board_id][fe_id][channel][tac]
               X['a']=float(tmp[4])
               X['b']=float(tmp[5])
               X['c']=float(tmp[6])
               X['d']=float(tmp[8])
               X['e']=float(tmp[10])
               if float(tmp[9]) < 2: X['chi2Ndof'] = 999999.
               else:                  X['chi2Ndof']=float(tmp[7])/float(tmp[9])
      L=Ltdc
      for l in range(1,len(L)):
               tmp = L[l].replace('\n','').split(',')
               if len(tmp)<9:continue
               board_id = int(tmp[0])
               if not board_id in qdc_cal: qdc_cal[board_id]={}
               fe_id = int(tmp[1])
               if not fe_id in qdc_cal[board_id]: qdc_cal[board_id][fe_id]={}
               channel = int(tmp[2])
               if not channel in qdc_cal[board_id][fe_id]: qdc_cal[board_id][fe_id][channel]={}
               tac = int(tmp[3])
               if not tac in qdc_cal[board_id][fe_id][channel]: qdc_cal[board_id][fe_id][channel][tac]={}
               tdc = int(tmp[4])
               if not tdc in qdc_cal[board_id][fe_id][channel][tac]: qdc_cal[board_id][fe_id][channel][tac][tdc]={}
               X = qdc_cal[board_id][fe_id][channel][tac][tdc]
               X['a']=float(tmp[5])
               X['b']=float(tmp[6])
               X['c']=float(tmp[7])
               X['d']=float(tmp[9])
               if float(tmp[10]) < 2: X['chi2Ndof'] = 999999.
               else:                  X['chi2Ndof']=float(tmp[8])/float(tmp[10])

def comb_calibration(board_id,tofpet_id,channel,tac,v_coarse,v_fine,t_coarse,t_fine,GQDC = 1.0, TDC=0): # max gain QDC = 3.6
      par  = qdc_cal[board_id][tofpet_id][channel][tac]
      parT = par[TDC]
      x    = t_fine
      ftdc = (-parT['b']-ROOT.TMath.Sqrt(parT['b']**2-4*parT['a']*(parT['c']-x)))/(2*parT['a']) #   Ettore 28/01/2022 +parT['d']
      timestamp = t_coarse + ftdc
      tf = timestamp - t_coarse
      x = v_coarse - tf
      fqdc = -par['c']*ROOT.TMath.Log(1+ROOT.TMath.Exp( par['a']*(x-par['e'])**2-par['b']*(x-par['e']) )) + par['d']
      fqdc0 = -par['c']*ROOT.TMath.Log(1+ROOT.TMath.Exp( par['a']*(v_coarse-par['e'])**2-par['b']*(v_coarse-par['e']) )) + par['d']
      value = (v_fine-fqdc)/GQDC
      board = 'board_'+str(board_id)
      system = "scifi"
      if not board in boardMaps['Scifi']:
            tmp = MufiSystem[board_id][tofpet_id]
            if tmp == 0: system = 'veto'
            if tmp == 1: system = 'us'
            if tmp == 2: system = 'ds'
      rc = h['delQDC_'+system].Fill(ftdc,value)
      return timestamp,value,max(par['chi2Ndof'],parT['chi2Ndof']),v_fine/par['d']


fiN = ROOT.TFile.Open(fname)
ut.bookHist(h,'delQDC_scifi','QDC vs fTDC',100,-0.5,1.5,102,-2,100)
ut.bookHist(h,'delQDC_veto','QDC vs fTDC',100,-0.5,1.5,102,-2,100)
ut.bookHist(h,'delQDC_us','QDC vs fTDC',100,-0.5,1.5,102,-2,100)
ut.bookHist(h,'delQDC_ds','QDC vs fTDC',100,-0.5,1.5,102,-2,100)

for detector in boardMaps:
     for board in boardMaps[detector]:
        b = board.split('_')[1]
        ut.bookHist(h,'vCoarse'+b,'vCoarse '+b+' '+detector,1110,-10,1100)
        ut.bookHist(h,'tCoarse'+b,'tCoarse '+b+' '+detector,100,-5,20)
        ut.bookHist(h,'vFine'+b,'vFine '+b+' '+detector,700,0,350)
        ut.bookHist(h,'tFine'+b,'tFine '+b+' '+detector,1000,0,500)

for event in fiN.data:
     for n in range(event.n_hits):
           board_id = event.boardId[n]
           tofpet_id = event.tofpetId[n]
           tofpet_channel = event.tofpetChannel[n]
           rc = h['vCoarse'+str(board_id)].Fill(event.vCoarse[n])
           rc = h['tCoarse'+str(board_id)].Fill(event.tCoarse[n])
           rc = h['vFine'+str(board_id)].Fill(event.vFine[n])
           rc = h['tFine'+str(board_id)].Fill(event.tFine[n])
           # TDC,QDC,Chi2ndof,satur = comb_calibration(board_id,tofpet_id,tofpet_channel,tac,event.vCoarse[n],event.vFine[n],event.tCoarse[n],event.tFine[n])

for c in ['vCoarse','tCoarse','vFine','tFine']:
     ut.bookCanvas(h,'scifi'+c,'scifi '+c,2400,1800,6,5)
     ut.bookCanvas(h,'mufi'+c,'mufilter '+c,1800,1200,4,2)
     j=1
     S = []
     for board in boardMaps['Scifi']:
        S.append( int(board.split('_')[1]) )
     S.sort()
     for board in S:
        b = str(board)
        tc = h['scifi'+c].cd(j)
        tc.SetLogy(True)
        h[c+b].GetXaxis().SetRangeUser(0,100)
        h[c+b].Draw()
        tc.Update()
        stats = h[c+b].FindObject('stats')
        stats.SetOptStat(110111)
        stats.SetX1NDC(0.71)
        stats.SetY1NDC(0.68)
        stats.SetX2NDC(0.98)
        stats.SetY2NDC(0.94)
        j+=1
        tc.Update()
     j=1
     S = []
     for board in boardMaps['MuFilter']:
        S.append( int(board.split('_')[1]) )
     S.sort()
     for board in S:
        tc = h['mufi'+c].cd(j)
        tc.SetLogy(True)
        b = str(board)
        h[c+b].Draw()
        tc.Update()
        stats = h[c+b].FindObject('stats')
        stats.SetOptStat(110111)
        stats.SetX1NDC(0.71)
        stats.SetY1NDC(0.68)
        stats.SetX2NDC(0.98)
        stats.SetY2NDC(0.94)
        j+=1
        tc.Update()
for c in ['vCoarse','tCoarse','vFine','tFine']:
     h['mufi'+c].Print('mufi'+c+'.png')
     h['scifi'+c].Print('scifi'+c+'.png')
