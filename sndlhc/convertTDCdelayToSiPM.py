# read constants from ascii file 
# channel number from 1 to 80  -> bar and SiPM channel

nSiPMs = 8
nSides =  2
direction = -1

def convert(channel):
   sipmChannel = channel -1
   bar_number = 9 + direction*(sipmChannel//(nSiPMs))
   sipm_number = sipmChannel%(nSiPMs)
   return bar_number, sipm_number

F = open("TDCdelays.CSV")
O = open("TDCdelays.txt","w")
X = {}
for l in F.readlines():
    tmp = l.split(';')
    channel = int(tmp[0].split(' ')[1])
    bar_number, sipm_number = convert(channel)
    X[ bar_number*10 + sipm_number ] = float(tmp[2])

n = 0
txt = "        "
for x in X:
    txt += "c.MuFilter.TDCshiftUS_%i%i = %5.1F,  "%(x//10,x%10,X[x])
    n+=1
    if n==4: 
       O.write(txt+"\n")
       n = 0
       txt = "        "

# make relative delays to local channel j=4
j=4
Xrel = {}
for bar_number in range(10):
   t0 = X[ bar_number*10 + j ]
   for sipm_number in range(nSiPMs):
         Xrel[ bar_number*10 + sipm_number ] = X[ bar_number*10 + sipm_number ]  - t0
O.write("\n")
   
n = 0
txt = "        "
for x in Xrel:
    txt += "c.MuFilter.TDCshiftUS_%i%i = %5.1F,  "%(x//10,x%10,Xrel[x])
    n+=1
    if n==4: 
       O.write(txt+"\n")
       n = 0
       txt = "        "
