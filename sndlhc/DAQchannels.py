sw/SOURCES/CMake/v3.18.2/v3.18.2/Utilities/cmliblzma/liblzma/api/lzma/base.h
	LZMA_DATA_ERROR         = 9,
		/**<
		 * \brief       Data is corrupt
		 *
		 * The usage of this return value is different in encoders
		 * and decoders. In both encoder and decoder, the coding
		 * cannot continue after this error.
		 *
		 * Encoders return this if size limits of the target file
		 * format would be exceeded. These limits are huge, thus
		 * getting this error from an encoder is mostly theoretical.
		 * For example, the maximum compressed and uncompressed
		 * size of a .xz Stream is roughly 8 EiB (2^63 bytes).
		 *
		 * Decoders return this error if the input data is corrupt.
		 * This can mean, for example, invalid CRC32 in headers
		 * or invalid check of uncompressed data.


returnStatus = lzma_code(&stream, LZMA_FINISH);
LZMA_FINISH = 3

sw/SOURCES/CMake/v3.18.2/v3.18.2/Utilities/cmliblzma/liblzma/common/common.c:

extern LZMA_API(lzma_ret)
lzma_code(lzma_stream *strm, lzma_action action)
{

ROOT.gInterpreter.Declare("""
#include "lzma.h"
   int checkFile(lzma_stream *stream){
      int returnStatus = lzma_code(stream, LZMA_FINISH);
      return returnStatus;
   }
""")

import ROOT
f=ROOT.TFile('run003831_splashEventsOnly_UStrigger.root')
f=ROOT.TFile('run003831_splashEventsOnly_DStrigger.root')
f=ROOT.TFile('run003831_splashEventsOnly.root')
ctimeZ = f.daq.channels.FindObject('ctimeZ').Clone('Z')
f.daq.channels.Draw()
us = ctimeZ.ProjectionX('US',300,1000)
ctimeM = f.daq.channels.FindObject('ctimeM').Clone('M')
usM = ctimeM.ProjectionX('USM',300,1000)
usM.Draw()


ut.bookHist(h,'time','time',   125663,0,125663)
ut.bookHist(h,'timez','timez',200*1000,110800,111000)
ut.bookHist(h,'timeq','time quiet',200*1000,80800,81000)
for event in eventTree:
  T   = event.EventHeader.GetEventTime()/freq
  rc = h['timez'].Fill(T)
  rc = h['timeq'].Fill(T)
  rc = h['time'].Fill(T)



for aHit in eventTree.Digi_MuFilterHits:
     #aHit.Print()
     for c in aHit.GetAllSignals(False,False):
         print(aHit.GetDetectorID(),c.first,c.second,
            aHit.GetBoardID(c.first),aHit.GetTofpetID(c.first), aHit.Getchannel(c.first))

N = 279961
def dumpEvent(N):
  rc = f.event.GetEvent(N)
  print(N,f.event.timestamp)
  for b in f.GetListOfKeys():
          name = b.GetName()
          if name.find('board')!=0: continue
          bt = f.Get(name)
          rc = bt.GetEvent(N)
          for n in range(bt.n_hits):
             tofpet_id = bt.tofpet_id[n]
             tofpet_channel = bt.tofpet_channel[n]
             TDC = bt.timestamp[n]
             QDC = bt.value[n]
             print(name,tofpet_id,tofpet_channel,QDC,TDC)





