import ROOT
import rootUtils as ut
h={}
ut.readHists(h,'run004705-Xbnr.root')
ut.bookHist(h,'mod4','mod4',4,-0.5,3.5)
ut.bookHist(h,'mod4plus2','mod4',4,-0.5,3.5)
for n in range(h['Xbnr'].GetNbinsX()):
   rc = h['mod4'].Fill(n%4,h['Xbnr'].GetBinContent(n))
   rc = h['mod4plus2'].Fill((n+2)%4,h['Xbnr'].GetBinContent(n))

