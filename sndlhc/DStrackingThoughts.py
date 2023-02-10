not converged 46
not converged 303
not converged 306
not converged 314
not converged 345
not converged 444
not converged 790
not converged 810
not converged 864
not converged 980
not converged 1439
not converged 1463
not converged 1469
not converged 1496
not converged 1727
not converged 1750
not converged 1806
not converged 1942
not converged 2181
not converged 2314
not converged 2493
not converged 2694
not converged 2904
not converged 2956
not converged 2988
not converged 3053
not converged 3197
not converged 3262
not converged 3685
not converged 4016
not converged 4107
not converged 4389
not converged 4593
not converged 4790
not converged 4795
not converged 4977
not converged 5080
not converged 5349
not converged 5530
not converged 5598
not converged 5729
not converged 5737

clPerPlane = {}
for aTrack in trackTask.trackCandidates['DS']:
 for key in aTrack:
    cl = aTrack[key]
    detID = cl.GetFirst()
    p = (detID//1000)%10
    proj = 2*p
    if (cl.GetFirst()%1000)>59: proj = 2*p+1
    if not proj in clPerPlane:clPerPlane[proj]=[]
    clPerPlane[proj].append([cl,key])
ncand = 1
cleanHitList = {0:{}}
for plane in clPerPlane:
   j=0
   for j in range(1,len(clPerPlane[plane])):
      cleanHitList[ncand+j-1]={}
      for key in cleanHitList[ncand-1]: 
          cleanHitList[ncand+j-1][key]=cleanHitList[ncand-1][key]
   for nCl in range(len(clPerPlane[plane])):
      clx = clPerPlane[plane][nCl]
      k = ncand+nCl-1
      print('add',k)
      cleanHitList[k][clx[1]] = clx[0]
   ncand+=j
chi2 = {}
trackTask.fittedTracks.Delete()
for ncand in cleanHitList:
    aTrack = cleanHitList[ncand]
    rc = trackTask.fitTrack(aTrack)
    chi2[ncand] = 1E10
    if type(rc)==type(1):
        print('trackfit failed',rc,aTrack)
        continue
    fitStatus = rc.getFitStatus()
    if not fitStatus.isFitConverged(): 
       print('trackfit not converged',aTrack)
       continue
    chi2[ncand] = fitStatus.getChi2()/(fitStatus.getNdf()+1E-10)


