#!/usr/bin/env python3
import sys
import os
import zipfile

GBP_BUTTON_A      = 0x0001
GBP_BUTTON_B      = 0x0002
GBP_BUTTON_SELECT = 0x0004
GBP_BUTTON_START  = 0x0008
GBP_BUTTON_RIGHT  = 0x0010
GBP_BUTTON_LEFT   = 0x0020
GBP_BUTTON_UP     = 0x0040
GBP_BUTTON_DOWN   = 0x0080
GBP_BUTTON_L      = 0x0100
GBP_BUTTON_R      = 0x0200

MAPPING = (GBP_BUTTON_UP,
           GBP_BUTTON_DOWN,
           GBP_BUTTON_LEFT,
           GBP_BUTTON_RIGHT,
           GBP_BUTTON_START,
           GBP_BUTTON_SELECT,
           GBP_BUTTON_B,
           GBP_BUTTON_A,
           GBP_BUTTON_L,
           GBP_BUTTON_R)

CYCLES_PER_FRAME = 280896

gbmv_path = sys.argv[1]
if not os.path.isfile(gbmv_path):
    print('ERROR: File does not exist!')
    sys.exit(1)
gbmv_abs = os.path.abspath(gbmv_path)
gbmv = zipfile.ZipFile(gbmv_abs)
inputs = gbmv.open('Input Log.txt')
lastInput = ""

def convert_frame(data):
  out = 0
  for index, button in enumerate(MAPPING):
    if data[index] != ".":
      out ^= button
  return out

cycle = -1232 * 65
#cycle = 0
with open("GBItimestamps.txt", "w") as f:
  for line in inputs:
    sline = line.decode().rstrip()
    if sline[0] == "|":
      data = sline[:-1]
      data = data[1:]
      #data = data[25:]
      if data != lastInput:
        if cycle < 0:
          f.write(f"{0:08X} {convert_frame(data):04X}\n")
        else:
          #sometimes need a -1 here, depends on timing of inputs per game
          f.write(f"{cycle//4096:08X} {convert_frame(data):04X}\n")
      lastInput = data
      cycle += CYCLES_PER_FRAME
      
  # write extra 0, for glitch in GBI
  f.write(f"{cycle//4096:08X} {0:04X}\n")