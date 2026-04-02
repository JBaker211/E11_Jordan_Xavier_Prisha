#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  capemcae11.py
#  
#  Copyright 2026  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  



import time 
import board
import csv
import numpy as np
import busio
import sys
import matplotlib.pyplot as plt
import struct
import usb.core
import usb.util

sys.path.append('/home/pi/cape_mca') 
from capemca import *

spectra = []
read_times = []

arguments = sys.argv
data_path = 'hi.csv'
runtime = int(arguments[1])
now = time.time()
stop = now + runtime
beta = ['Time', 'Counts']
count_time = int(arguments[2])


output_file = open(data_path, 'w', newline = None)
csvwriter = csv.writer(output_file, delimiter = ',')
csvwriter.writerow(beta)



devices = find_all_mcas()
print(f"Found {len(devices)} MCA device(s)")

if not devices:
    sys.exit(1)

duration = float(runtime) 
window = float(count_time)


with CapeMCA() as mca:
    try:
        start = time.time()
        reads = 0
        next_read = count_time

        while time.time() - start < duration:
            # Wait until the next window boundary
            now = time.time()
            if now < next_read:
                time.sleep(next_read - now)

            read_start = time.time()
            status = mca.read_status()
            spectrum = mca.read_spectrum()
            read_end = time.time()
            
            print('Zeroing spectrum')
            mca.zero_spectrum()

            # Schedule next read from when this one started
            next_read = read_start + window

            spec_data = spectrum[1:]
            spec_total = sum(spec_data)
            nonzero = sum(1 for ch in spec_data if ch > 0)
            elapsed = read_start - start

            print(f"[{elapsed:6.1f}s] read {reads+1} "
                  f"(took {read_end - read_start:.2f}s): "
                  f"{status.cps} cps, "
                  f"totalCount={status.total_count:g}, "
                  f"intervals={status.total_intervals}")
            print(f"         spectrum: ch0={spectrum[0]}, specSum={spec_total}, "
                  f"nonzeroCh={nonzero}")

            active = [(ch, spectrum[ch]) for ch in range(1, SPECTRUM_CHANNELS)
                      if spectrum[ch] > 0]
            print(f"         channels: {active}")

            spectra.append(spec_data)
            read_times.append(elapsed)
            reads += 1
            
            csvwriter.writerow([elapsed, status.total_count])

        print(f"\nCompleted {reads} reads in {time.time() - start:.2f}s "
              f"(window={window}s)")

    except Exception as e:
        print(f"\nError after {reads} reads: {e}")

print("Device closed, exiting.")

output_file.close()
