import ROOT,os
# from monitor file
Mfile ="/eos/experiment/sndlhc/www/offline/run004718.root"
F=ROOT.TFile.Open(os.environ['EOSSHIP']+Mfile)
residuals = F.mufilter.Get('mufi-residuals')
for pad in residuals.GetListOfPrimitives(): 
    for x in pad.GetListOfPrimitives(): 
           if x.GetName().find('mufi-res')<0: continue
           print( "%s20   : %5.2Fcm"%(x.GetName(),x.GetMean()))

# for some mysterious reason, shifts of horizontal planes neeed to be multiplied with -1.

mufi-resX_Veto10proj20   : -0.11cm
mufi-resX_Veto11proj20   :  0.04cm
mufi-resX_US20proj20   : -0.10cm
mufi-resX_US21proj20   : -0.26cm
mufi-resX_US22proj20   : -0.24cm
mufi-resX_US23proj20   : -0.31cm
mufi-resX_US24proj20   : -0.34cm
mufi-resX_DS30proj20 H  : -0.43cm
mufi-resX_DS31proj20 V  :  1.13cm
mufi-resX_DS32proj20 H  : -0.53cm
mufi-resX_DS33proj20 V  :  1.31cm
mufi-resX_DS34proj20 H  : -0.61cm
mufi-resX_DS35proj20 V  :  1.35cm
mufi-resX_DS36proj20 V  :  1.39cm

mufi-resX_Veto10proj20   : -0.10cm
mufi-resX_Veto11proj20   :  0.04cm
mufi-resX_US20proj20   : -0.10cm
mufi-resX_US21proj20   : -0.26cm
mufi-resX_US22proj20   : -0.24cm
mufi-resX_US23proj20   : -0.32cm
mufi-resX_US24proj20   : -0.34cm
mufi-resX_DS30proj20   : -0.42cm
mufi-resX_DS31proj20   :  1.13cm
mufi-resX_DS32proj20   : -0.53cm
mufi-resX_DS33proj20   :  1.31cm
mufi-resX_DS34proj20   : -0.60cm
mufi-resX_DS35proj20   :  1.36cm
mufi-resX_DS36proj20   :  1.40cm

