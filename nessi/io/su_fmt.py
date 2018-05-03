#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: pso_peaks.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Seismic Unix format support.
:copyright:
    Damien Pageot (nessi.develop@protonmail.com)
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt

class SUdata():
    """
    Seismic Unix format support
    """

    def __init__(self):
        """
        Define the Seismic Unix header.
        """

        self.sutype = np.dtype([
            ('tracl', np.int32), ('tracr', np.int32), \
            ('fldr', np.int32), ('tracf', np.int32), \
            ('ep', np.int32), ('cdp', np.int32), \
            ('cdpt', np.int32), ('trid', np.int16), \
            ('nvs', np.int16), ('nhs', np.int16), \
            ('duse', np.int16), ('offset', np.int32), \
            ('gelev', np.int32), ('selev', np.int32), \
            ('sdepth', np.int32), ('gdel', np.int32), \
            ('sdel', np.int32), ('swdep', np.int32), \
            ('gwdep', np.int32), ('scalel', np.int16), \
            ('scalco', np.int16), ('sx', np.int32), \
            ('sy', np.int32), ('gx', np.int32), \
            ('gy', np.int32), ('counit', np.int16), \
            ('wevel', np.int16), ('swevel', np.int16), \
            ('sut', np.int16), ('gut', np.int16), \
            ('sstat', np.int16), ('gstat', np.int16), \
            ('tstat', np.int16), ('laga', np.int16), \
            ('lagb', np.int16), ('delrt', np.int16), \
            ('muts', np.int16), ('mute', np.int16), \
            ('ns', np.uint16), ('dt', np.uint16), \
            ('gain', np.int16), ('igc', np.int16), \
            ('igi', np.int16), ('corr', np.int16), \
            ('sfs', np.int16), ('sfe', np.int16), \
            ('slen', np.int16), ('styp', np.int16), \
            ('stas', np.int16), ('stae', np.int16), \
            ('tatyp', np.int16), ('afilf', np.int16), \
            ('afils', np.int16), ('nofilf', np.int16), \
            ('nofils', np.int16), ('lcf', np.int16), \
            ('hcf', np.int16), ('lcs', np.int16), \
            ('hcs', np.int16), ('year', np.int16), \
            ('day', np.int16), ('hour', np.int16), \
            ('minute', np.int16), ('sec', np.int16), \
            ('timebas', np.int16), ('trwf', np.int16), \
            ('grnors', np.int16), ('grnofr', np.int16), \
            ('grnlof', np.int16), ('gaps', np.int16), \
            ('otrav', np.int16), ('cdpx', np.int32), \
            ('cdpy', np.int32), ('Inline3D', np.int32), \
            ('Crossline3D', np.int32), ('ShotPoint', np.int32), \
            ('ShotPointScalar', np.int16), \
            ('TraceValueMeasurementUnit', np.int16), \
            ('TransductionConstantMantissa', np.int32), \
            ('TransductionConstantPower', np.int16), \
            ('TransductionUnit', np.int16), \
            ('TraceIdentifier', np.int16), ('ScalarTraceHeader', np.int16), \
            ('SourceType', np.int16), \
            ('SourceEnergyDirectionMantissa', np.int32), \
            ('SourceEnergyDirectionExponent', np.int16), \
            ('SourceMeasurementMantissa', np.int32), \
            ('SourceMeasurementExponent', np.int16), \
            ('SourceMeasurementUnit', np.int16), \
            ('UnassignedInt1', np.int32), \
            ('UnassignedInt2', np.int32)])

        
        self.filename = ' '
        self.header = []
        self.trace = []
        self.endian = 'l'
        

    def _check_endian(self):
        """
        Check if little or big endian
        """
        file = open(self.filename, 'rb')
        btmp = file.read()
        bsize = os.stat(self.filename).st_size
        nsl = np.frombuffer(btmp, dtype='<h', count=1, offset=114)[0]
        nsb = np.frombuffer(btmp, dtype='>h', count=1, offset=114)[0]
        if(bsize%((nsl*4)+240) == 0):
            self.endian = 'l'
        else:
            if(bsize%((nsb*4)+240) == 0):
                self.endian = 'b'
            else:
                sys.exit("Unable to read "+self.filename+"\n")


    def read(self, filename, endian=' '):
        """Read Seismic Unix file.

        Parameters
        ------
            sufile : str
                Seismic Unix file name.
            endian : str
                File byte order: little endian (default) 'l', big endian 'b'.

        Return
        ------
            sudata : suhdr_dtype+traces
                Seismic Unix data with header.

        """
        self.filename = filename
        if endian == ' ':
            self._check_endian()
        
        file = open(filename, 'rb')
        bhdr = file.read(240)
        if self.endian == 'b':
            hdr = np.frombuffer(bhdr, dtype=self.sutype.newbyteorder(), count=1)[0]
            btrc = file.read(hdr['ns']*4)
            trc = np.frombuffer(btrc, dtype=('>f4', hdr['ns']), count=1)[0]
            self.header.append(hdr)
            self.trace.append(trc)
            EOF = False
            while EOF == False:
                try:
                    bhdr = file.read(240)
                    btrc = file.read(hdr['ns']*4)
                    hdr = np.frombuffer(bhdr, dtype=self.sutype.newbyteorder(), count=1)[0]
                    trc = np.frombuffer(btrc, dtype=('>f4', hdr['ns']), count=1)[0]
                    self.header.append(hdr)
                    self.trace.append(trc)
                except:
                    EOF = True
            self.trace = np.array(self.trace)  
            self.header = np.array(self.header)
            
        if self.endian == 'l':
            hdr = np.frombuffer(bhdr, dtype=self.sutype, count=1)[0]
            btrc = file.read(hdr['ns']*4)
            trc = np.frombuffer(btrc, dtype=('<f4', hdr['ns']), count=1)[0]
            self.header.append(hdr)
            self.trace.append(trc)
            EOF = False
            while EOF == False:
                try:
                    bhdr = file.read(240)
                    btrc = file.read(hdr['ns']*4)
                    hdr = np.frombuffer(bhdr, dtype=self.sutype, count=1)[0]
                    trc = np.frombuffer(btrc, dtype=('<f4', hdr['ns']), count=1)[0]
                    self.header.append(hdr)
                    self.trace.append(trc)
                except:
                    EOF = True
            self.header = np.array(self.header)
            self.trace = np.array(self.trace)
        
        
    def image(self):
        """
        matplotlib.pyplot.imshow adapted for SU files
        """
        t0 = float(self.header[0]['delrt'])/1000.
        t1 = float(self.header[0]['ns']-1)*float(self.header[0]['dt'])/1000000.+t0
        plt.imshow(self.trace.swapaxes(1,0), aspect='auto', cmap='gray',
                   extent=[0., len(self.trace), t1, t0])
        
    def wind(self, tmin=0., tmax=0.):
        """
        Windowing
        """
        print(tmin, tmax)
        dt = self.header[0]['dt']/1000000.
        dlrt = float(self.header[0]['delrt'])/1000.
        
        itmin = int((tmin-dlrt)/dt)
        itmax = int((tmax-dlrt)/dt)

        ns = itmax-itmin+1
        self.trace = self.trace[:, itmin:itmax+1]
        self.header[:]['ns'] = ns
        self.header[:]['delrt'] = int(tmin*1000)
        #for i in range(len(self.header)):
        #    self.header[i]['ns'] = ns