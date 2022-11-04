# make latex code 
if 1:
 runDescription = {}
 runDescription[46]="Run 46  muons? gain $2.5$"
 runDescription[47]="Run 47  muons? gain $2.5$"
 runDescription[49]="Run 49  180 GeV $\pi^+$ gain $3.65$"
 runDescription[50]="Run 50  180 GeV $\pi^+$ gain $3.65$"
 runDescription[51]="Run 51  180 GeV $\pi^+$ gain $3.65$"
 runDescription[52]="Run 52  muons gain $3.65$"
 runDescription[53]="Run 53 muons gain $3.65$"
 runDescription[54]="Run 54 muons gain $2.50$"
 runDescription[55]="Run 55 muons gain $2.50$"
 runDescription[56]="Run 56  140 GeV $\pi^+$ gain $2.50$"
 runDescription[58]="Run 58  140 GeV $\pi^+$ gain $3.65$"
 runDescription[59]="Run 59  180 or 100 GeV $\pi^+$ gain $3.65$"
 runDescription[60]="Run 60  180 or 100 GeV $\pi^+$ gain $2.50$"
 runDescription[71]="Run 71  240 GeV $\pi^-$ gain $3.65$"
 runDescription[72]="Run 72  240 GeV $\pi^-$ gain $2.50$"
 runDescription[73]="Run 73  240 GeV $\pi^-$ gain $1.00$"
 runDescription[74]="Run 74  240 GeV $\pi^-$ gain $3.65$"
 runDescription[80]="Run 80  300 GeV $\pi^-$ gain $3.65$"
 runDescription[81]="Run 81  300 GeV $\pi^-$ gain $2.50$"
 runDescription[82]="Run 82  300 GeV $\pi^-$ gain $1.00$"
 runDescription[86]="Run 86 cosmics gain $3.65$"
 runDescription[87]="Run 87 cosmics gain $2.50$"
 runDescription[88]="Run 88 cosmics gain $1.00$"
 runDescription[89]="Run 89  300 GeV $\pi^-$ gain $3.65$"
 runDescription[90]="Run 90  300 GeV $\pi^-$ gain $2.50$"
 runDescription[91]="Run 91  300 GeV $\pi^-$ gain $1.00$"

 gain[3.65]=[49,50,51,52,53,58,59,71,74,80,86,89]
 gain[2.5]=[46,47,54,55,56,60,72,81,87,90]
 gain[1.0]=[73,82,88,91]

 lines = []
 for r in runDescription:
    lines.append("\\begin{frame}{US 1-5  $\sigma$ and mean " + runDescription[r]+"}")
    lines.append(" sigma and mean")
    lines.append("\includegraphics[width = 0.90\\textwidth]{D:/SND@LHC/MuFilter/H8/NewCalib/TDCcalibration-run"+str(r)+".pdf}")
    lines.append("\end{frame}")
 lines.append(" ")
 lines.append("% detail plots")
 lines.append(" ")
 for l in range(5):
   for r in runDescription:
     lines.append("\\begin{frame}{US"+str(l) +" "+ runDescription[r]+"}")
     lines.append("\includegraphics[width = 0.95\\textwidth]{D:/SND@LHC/MuFilter/H8/NewCalib/TDCrms"+str(l)+"-run"+str(r)+".pdf}")
     lines.append("\end{frame}")
 outFile = open('text.tex','w')
 for l in lines:
    rc = outFile.write(l+"\n")
outFile.close()
