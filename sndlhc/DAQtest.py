runs = [5170,5171,5180]
flavors = ["maxduration_4_hitgap_0_clkalign_False","maxduration_4_hitgap_0_clkalign_True",
           "maxduration_6_hitgap_1_clkalign_False","maxduration_6_hitgap_1_clkalign_True",
           "maxduration_8_hitgap_1_clkalign_False","maxduration_8_hitgap_1_clkalign_True"]
           
command = "python $SNDSW_ROOT/shipLHC&/rawData/runProd.py -P test -c convert"

if 1<0:
   for o in flavors:
      os.system("mkdir /eos/experiment/sndlhc/convertedData/commissioning/event_builder_test_202301/"+o

for r in runs:
   for o in flavors:
      command += " -r "+str(r)
      command += " -p /eos/experiment/sndlhc/raw_data/commissioning/event_builder_test_202301/"+o
      command += " -d /eos/experiment/sndlhc/convertedData/commissioning/event_builder_test_202301/"+o
      command += " -c convert --parallel 10"
      os.system(command)
      
for r in runs:
   for o in flavors:
      command += " -r "+str(r)
      command += " -p /eos/experiment/sndlhc/convertedData/commissioning/event_builder_test_202301/"+o
      command += " --sH --parallel 10"
