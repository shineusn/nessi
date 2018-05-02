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
            ('fldr', np.int32), ('tracf', np.int32), ('ep', np.int32), ('cdp', np.int32), \
            ('cdpt', np.int32), ('trid', np.int16), ('nvs', np.int16), ('nhs', np.int16), \
            ('duse', np.int16), ('offset', np.int32), ('gelev', np.int32), ('selev', np.int32), \
            ('sdepth', np.int32), ('gdel', np.int32), ('sdel', np.int32), ('swdep', np.int32), \
            ('gwdep', np.int32), ('scalel', np.int16), ('scalco', np.int16), ('sx', np.int32), \
            ('sy', np.int32), ('gx', np.int32), ('gy', np.int32), ('counit', np.int16), \
            ('wevel', np.int16), ('swevel', np.int16), ('sut', np.int16), ('gut', np.int16), \
            ('sstat', np.int16), ('gstat', np.int16), ('tstat', np.int16), ('laga', np.int16), \
            ('lagb', np.int16), ('delrt', np.int16), ('muts', np.int16), ('mute', np.int16), \
            ('ns', np.uint16), ('dt', np.uint16), ('gain', np.int16), ('igc', np.int16), \
            ('igi', np.int16), ('corr', np.int16), ('sfs', np.int16), ('sfe', np.int16), \
            ('slen', np.int16), ('styp', np.int16), ('stas', np.int16), ('stae', np.int16), \
            ('tatyp', np.int16), ('afilf', np.int16), ('afils', np.int16), ('nofilf', np.int16), \
            ('nofils', np.int16), ('lcf', np.int16), ('hcf', np.int16), ('lcs', np.int16), \
            ('hcs', np.int16), ('year', np.int16), ('day', np.int16), ('hour', np.int16), \
            ('minute', np.int16), ('sec', np.int16), ('timebas', np.int16), ('trwf', np.int16), \
            ('grnors', np.int16), ('grnofr', np.int16), ('grnlof', np.int16), ('gaps', np.int16), \
            ('otrav', np.int16), ('cdpx', np.int32), ('cdpy', np.int32), ('Inline3D', np.int32), \
            ('Crossline3D', np.int32), ('ShotPoint', np.int32), ('ShotPointScalar', np.int16), \
            ('TraceValueMeasurementUnit', np.int16), \
            ('TransductionConstantMantissa', np.int32), \
            ('TransductionConstantPower', np.int16), ('TransductionUnit', np.int16), \
            ('TraceIdentifier', np.int16), ('ScalarTraceHeader', np.int16), \
            ('SourceType', np.int16), ('SourceEnergyDirectionMantissa', np.int32), \
            ('SourceEnergyDirectionExponent', np.int16), \
            ('SourceMeasurementMantissa', np.int32), ('SourceMeasurementExponent', np.int16), \
            ('SourceMeasurementUnit', np.int16), ('UnassignedInt1', np.int32), \
            ('UnassignedInt2', np.int32),])

        self.data = np.zeros(1, dtype=self.sutype)
        self.endian = 'l'


    def read(self, sufile, endian='l'):
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
        sutmp = open(sufile, 'rb').read()
        if endian == 'l':
            suhdr = np.fromstring(sutmp, dtype=self.sutype, count=1)
            ns = suhdr['ns'][0]
            file_dtype = np.dtype(self.sutype.descr+[('trace', ('<f4', ns))])
        elif endian == 'b':
            suhdr = np.fromstring(sutmp, dtype=self.sutype.newbyteorder(), count=1)
            ns = suhdr['ns'][0]
            file_dtype = np.dtype(self.sutype.newbyteorder().descr+[('trace', ('>f4', ns))])
            
        self.data = np.fromfile(sufile, dtype=file_dtype)
        self.endian = endian
        
    def image(self):
        """
        matplotlib.pyplot.imshow adapted for SU files
        """
        t0 = float(self.data[0]['delrt'])/1000.
        t1 = float(self.data[0]['ns']-1)*float(self.data[0]['dt'])/1000000.+t0
        plt.imshow(self.data[:]['trace'], aspect='auto', cmap='gray',
                   extent=[0., len(self.data), t1, t0])

    def wind(self, tmin=0., tmax=0.):
        """
        Windowing data.
        """

        dt = float(self.data[0]['dt'])/1000000.

        t0 = float(self.data[0]['delrt'])/1000.
        t1 = float(self.data[0]['ns']-1)*float(self.data[0]['dt'])/1000000.+t0
        
        it0 = int(t0/dt)
        it1 = int(t1/dt)
        
        trace = self.data[:]['trace']
        tracew = trace[:,it0:it1]
        
        if self.endian == 'l':
            sutype = self.sutype
            suhdr = np.array(self.data, dtype=sutype)
            file_dtype = np.dtype(self.sutype.descr+[('trace', ('<f4', tracew.shape[1]))])
        if self.endian == 'b':
            sutype = self.sutype.newbyteorder()
            suhdr = np.array(self.data, dtype=sutype)
            file_dtype = np.dtype(sutype.descr+[('trace', ('>f4', tracew.shape[1]))])
    
        self.data[:] = np.array(suhdr, dtype=file_dtype)
        self.data[:]['ns'] = tracew.shape[1]
        self.data[:]['delrt'] = 0
        self.data[:]['trace'] = tracew

        
        