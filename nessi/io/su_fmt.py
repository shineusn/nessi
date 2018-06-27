#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Filename: su_fmt.py
#   Author: Damien Pageot
#    Email: nessi.develop@protonmail.com
#
# Copyright (C) 2018 Damien Pageot
# ------------------------------------------------------------------
"""
Support of Seismic Unix format and some commands.
"""

# Import __future__ for python2/3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import python modules
import os
import sys
import copy
import numpy as np
from scipy.signal import resample
import matplotlib.pyplot as plt

# Import fonctions from NeSSI package
from nessi.signal import time_window
from nessi.signal import space_window
from nessi.signal import taper1d
from nessi.signal import sin2filter


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
            ('otrav', np.int16), ('d1', np.float32),\
            ('f1', np.float32), ('d2', np.float32), \
            ('f2', np.float32), ('ungpow', np.float32), \
            ('unscale', np.float32), ('ntr', np.int32), \
            ('mark', np.int16), ('shortpad', np.int16), \
            ('unassignedInt1', np.int32), ('unassignedInt2', np.int32), \
            ('unassignedInt3', np.int32), ('unassignedInt4', np.int32), \
            ('unassignedFloat1', np.float32), ('unassignedFloat2', np.float32), \
            ('unassignedFloat3', np.float32)])

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
        """
        Read Seismic Unix file.

        :param filename: name of the SU file to read
        :param endian: byte order: little endian 'l', big endian 'b'.
        """

        # This method can be easily simplified... for [0.3.0] version ?
        self.filename = filename

        if endian == ' ':
            # Automatic checking of endianess
            self._check_endian()

        # Open the file to read
        file = open(filename, 'rb')

        # Get the header of the first trace (240 bytes)
        bhdr = file.read(240)

        if self.endian == 'b':
            # Read the header of the first trace
            hdr = np.frombuffer(bhdr, dtype=self.sutype.newbyteorder(), count=1)[0]
            # Get the  the first trace data values
            btrc = file.read(hdr['ns']*4)
            trc = np.frombuffer(btrc, dtype=('>f4', hdr['ns']), count=1)[0]
            # Save the header and the trace
            self.header.append(hdr)
            self.trace.append(trc)
            # Loop over traces until end of file
            EOF = False
            while EOF == False:
                try:
                    # Get header and trace
                    bhdr = file.read(240)
                    btrc = file.read(hdr['ns']*4)
                    hdr = np.frombuffer(bhdr, dtype=self.sutype.newbyteorder(), count=1)[0]
                    trc = np.frombuffer(btrc, dtype=('>f4', hdr['ns']), count=1)[0]
                    # Save
                    self.header.append(hdr)
                    self.trace.append(trc)
                except:
                    EOF = True
            # Convert in numpy array format
            self.trace = np.array(self.trace)
            self.header = np.array(self.header)

        if self.endian == 'l':
            # Read the header of the first trace
            hdr = np.frombuffer(bhdr, dtype=self.sutype, count=1)[0]
            # Get the  the first trace data values
            btrc = file.read(hdr['ns']*4)
            trc = np.frombuffer(btrc, dtype=('<f4', hdr['ns']), count=1)[0]
            # Save the header and the trace
            self.header.append(hdr)
            self.trace.append(trc)
            # Loop over traces until end of file
            EOF = False
            while EOF == False:
                try:
                    # Get header and trace
                    bhdr = file.read(240)
                    btrc = file.read(hdr['ns']*4)
                    hdr = np.frombuffer(bhdr, dtype=self.sutype, count=1)[0]
                    trc = np.frombuffer(btrc, dtype=('<f4', hdr['ns']), count=1)[0]
                    # Save the header and the trace
                    self.header.append(hdr)
                    self.trace.append(trc)
                except:
                    EOF = True
            # Convert in numpy array format
            self.header = np.array(self.header)
            self.trace = np.array(self.trace)


    def image(self, key='tracl', bclip=None, wclip=None, clip=None, legend=0, label1=' ',
              label2=' ', title=' ', cmap='gray', style='normal'):
        """
        matplotlib.pyplot.imshow adapted to plot SU files

        :param key: header keyword (default tracl)
        :param bclip: data values outside of [bclip,wclip] are clipped
        :param wclip: data values outside of [bclip,wclip] are clipped
        :param clip: clip used to determine bclip and wclip
        :param legend: colorbar 0=no colorbar (default) 1=colorbar
        :param label1: x-axis label
        :param label2: y-axis label
        :param title: title of the image
        :param cmap: color map (defautl 'gray'): gray, jet, ...
        """

        # Check clip, bclip and wclip
        if(clip == None and bclip == None and clip == None):
            bclip = np.amin(self.trace)
            wclip = np.amax(self.trace)
        else:
            if(clip != None and bclip == None and wclip == None):
                bclip = -1.*clip
                wclip = clip

        # Get ns and dt from header
        ns = self.header[0]['ns']
        dt = float(self.header[0]['dt']/1000000.)
        if dt != 0:
            y0 = float(self.header[0]['delrt'])/1000.
            y1 = float(ns-1)*dt+y0
            x0 = self.header[0][key]
            x1 = self.header[-1][key]

        if self.header[0]['trid'] == 118:
            # Get d1
            d1 = float(self.header[0]['d1'])
            y0 = 0.
            y1 = float(ns-1)*d1
            x0 = self.header[0][key]
            x1 = self.header[-1][key]

        if self.header[0]['trid'] == 122:
            # Get d1
            d1 = float(self.header[0]['d1'])
            y0 = 0.
            y1 = float(ns-1)*d1
            # Get d2
            d2 = float(self.header[0]['d2'])
            x0 = float(self.header[0]['f2'])
            x1 = x0+float(len(self.header)-1)*d2

        if self.header[0]['trid'] == 132:
            # Get d1
            d1 = float(self.header[0]['d1'])
            y0 = float(self.header[0]['f1'])
            y1 = y0+float(ns-1)*d1
            # Get d2
            d2 = float(self.header[0]['d2'])
            x0 = float(self.header[0]['f2'])
            x1 = x0+float(len(self.header)-1)*d2

        if style == 'normal':
            # Add labels to axes
            plt.xlabel(label1)
            plt.ylabel(label2)

            # Add title to axis
            plt.title(title)

            # Plot surface
            plt.imshow(self.trace.swapaxes(1,0), aspect='auto', cmap=cmap,
                        extent=[x0, x1, y1, y0],
                        vmin=bclip, vmax=wclip)
        if style == 'masw':
            # Add labels to axes
            plt.xlabel(label1)
            plt.ylabel(label2)

            # Add title to axis
            plt.title(title)

            # Plot surface
            plt.imshow(self.trace, origin='bottom-left', aspect='auto', cmap=cmap,
                        extent=[y0, y1, x0, x1],
                        vmin=bclip, vmax=wclip)

        # Add legend
        if legend == 1:
            plt.colorbar()

    def wiggle(self, clip=-1., key='tracl', label1=' ', label2=' ', title=' ', tracecolor='black', tracestyle='-', skip=1, xcur=1):
        """
        Wiggle for SU files

        :param clip: clip used to determine outside values to be clipped [-clip, clip]
        :param key: header keyword (default tracl)
        :param label1: x-axis label
        :param label2: y-axis label
        :param title: title of the image
        :param tracecolor: color of the traces
        :param tracestyle: style of the traces ('--', ':', ...)
        :param skip: number of traces to skip for each plotted trace
        :param xcur: factor to increase trace amplitudes on output
        """

        # Get ns and dt from header
        ns = self.header[0]['ns']
        dt = float(self.header[0]['dt']/1000000.)
        ntrac = len(self.header)
        if dt != 0:
            y0 = float(self.header[0]['delrt'])/1000.
            y1 = float(ns-1)*dt+y0
            x0 = self.header[0][key]
            x1 = self.header[-1][key]
            d2 = 1.

        if self.header[0]['trid'] == 118:
            # Get d1
            d1 = float(self.header[0]['d1'])
            y0 = 0.
            y1 = float(ns-1)*d1
            x0 = self.header[0][key]
            x1 = self.header[-1][key]

        if self.header[0]['trid'] == 122:
            # Get d1
            d1 = float(self.header[0]['d1'])
            y0 = 0.
            y1 = float(ns-1)*d1
            # Get d2
            d2 = float(self.header[0]['d2'])
            x0 = float(self.header[0]['f2'])
            x1 = x0+float(len(self.header)-1)*d2

        # Add labels
        plt.xlabel(label1)
        plt.ylabel(label2)

        # Add axes
        plt.title(title)

        # Get the normalization parameter (for output)
        y = np.linspace(y0, y1, ns)
        if clip >= 0. :
            norm = clip
        else:
            norm = np.amax(np.abs(self.trace))

        # Plot the traces
        for itrac in range(0, ntrac, skip):
            wig = self.trace[itrac]/norm*d2*float(skip-1)*xcur
            plt.plot(wig+x0+float(itrac)*d2, y, color=tracecolor, linestyle=tracestyle)

    def kill(self, key=' ', a=1, min=0, count=1):
        """
        Zero out traces.
        If min= is set it overrides selecting traces by header.

        :param key: SU header keyword
        :param a: header value identifying traces to kill
        :param min: first trace to kill
        :param count: number of traces to kill
        """

        # Create a copy of the input SU data
        dobskill = copy.deepcopy(self)

        # Get the number of traces
        ntrac = self.trace.shape[0]

        # Kill traces from min to min+icount
        if key == ' ':
            for icount in range(0, count):
                if min+icount < ntrac:
                    dobskill.trace[min+icount, :] = 0.
        # Kill traces with the given header value
        else:
            if key != ' ':
                for itrac in range(0, ntrac):
                    if dobskill.header[itrac][key] == a:
                        dobskill.trace[itrac, :] = 0.

        return dobskill

    def wind(self, key=' ', min=0, max=0, tmin=0., tmax=0.):
        """
        Window SU traces in time or space.

        :param key: SU header key
        :param imin: minimum value of key to pass (=0)
        :param imax: maximum value of key to pass (=0)
        :param tmin: minimum time to pass (=0)
        :param tmax: maximum time to pass (=0)
        """

        # Create a copy of the input SU data
        dobsw = copy.deepcopy(self)

        if key != ' ' and (min != max): # Window traces in space
            # Get traces indices from key
            imin = np.argmin(np.abs(dobsw.header[:][key]-min))
            imax = np.argmin(np.abs(dobsw.header[:][key]-max))

            # Call nessi.signal.space_window function
            dobsw.trace = space_window(dobsw.trace, imin, imax, axis=0)

            # Edit SU header
            dobsw.header = dobsw.header[imin:imax+1][:]
            for ir in range(0, len(dobsw.header)):
                dobsw.header[ir]['cdpt'] = ir+1

        if tmax != tmin: # Window traces in time
            # Get parameters from SU header
            dt = dobsw.header[0]['dt']/1000000.
            delrt = float(dobsw.header[0]['delrt'])/1000.

            # Call nessi.signal.time_window function
            dobsw.trace = time_window(dobsw.trace, tmin, tmax, dt, delrt, axis=1)

            # Edit SU header
            dobsw.header[:]['ns'] = np.size(dobsw.trace, axis=1)
            dobsw.header[:]['delrt'] = int(tmin*1000)

        return dobsw

    def pfilter(self, freq, amps):
        """
        Applies a zero-phase, sine-squared tapered filter (adapted from the
        sufilter command - Seismic Unix 44R1).

        :param freq: array of filter frequencies (Hz)
        :param amps: array of filter amplitudes
        :param axis: time axis if dobs is a 2D array
        """
        # Create a copy of the input SU data
        dobsfilter = copy.deepcopy(self)

        # Get values from SU header
        dt = self.header[0]['dt']/1000000.

        # Apply filter
        dobsfilter.trace = sin2filter(self.trace, freq, amps, dt, axis=1)

        return dobsfilter

    def taper(self, tr1=0, tr2=0, min=0., tbeg=0., tend=0., type='linear'):
        """
        Taper the edge traces of a data panel to zero.

        :param dobs: input data to window
        :param tr1: number of traces to be tapered at beginning.
        :param tr2: number of traces to be tapered at end.
        :param min: minimum amplitude to taper (<1., default=0.)
        :param tbeg: length of taper (ms) at trace start (=0.).
        :param tend: length of taper (ms) at trace end (=0).
        :param taper: taper type: 'linear'(default), 'sine', 'cosine'
        """
        # Create a copy of the input SU data
        dobstaper = copy.deepcopy(self)

        # Get values from SU header
        ns = self.header[0]['ns']
        dt = self.header[0]['dt']/1000000.

        # Taper in space
        if(tr1 !=0 or tr2 !=0):
            dobstaper.trace = taper1d(dobstaper.trace, tr1, tr2, min, type, axis=0)

        # Taper in time
        if(tbeg !=0. or tend !=0.):
            ntap1 = int(tbeg/1000./dt)
            ntap2 = int(tend/1000./dt)
            dobstaper.trace = taper1d(dobstaper.trace, ntap1, ntap2, min, type, axis=1)

        return dobstaper

    def create(self, data, dt):
        """
        Create a minimal SU file
        """
        # Get size of data
        nr = data.shape[0]
        ns = data.shape[1]

        # Create
        for ir in range(0, nr):
            self.header.append(np.zeros(1, dtype=self.sutype))
            self.header[ir]['tracl'] = int(ir+1)
            self.header[ir]['tracf'] = int(ir+1)
            self.header[ir]['ns'] = ns
            self.header[ir]['dt'] = int(dt*1000000.)
            self.header[ir]['sx'] = 0
            self.header[ir]['sy'] = 0
            self.header[ir]['selev'] = 0
            self.header[ir]['gx'] = int(ir+1)
            self.header[ir]['gy'] = 0
            self.header[ir]['gelev'] = 0
            self.header[ir]['scalco'] = 1
            self.header[ir]['scalel'] = 1
            self.trace.append(data[ir,:])
        self.header = np.array(self.header)
        self.trace = np.array(self.trace)

    def write(self, filename):
        """
        Write SU file on disk
        """

        # Open binary file
        file = open(filename, 'wb')

        # Loop over traces
        for ir in range(0, len(self.header)):
            # Write header
            file.write(self.header[ir])
            # Write data
            file.write(self.trace[ir,:])

        # Close the binary file
        file.close()

    def masw(self, vmin=0., vmax=1000., dv=5., fmin=1., fmax=100.):
        """
        Calculate the dispersion diagram using MASW method.
        Return the dispersion diagram, the velocity vector and the frequency vector.

        :param vmin: minimum value to consider for the dispersion diagram
        :param vmax: maximum value to consider for the dispersion diagram
        :param dv: velocity sampling
        :param fmin: minimum frequency to consider
        :param fmax: maximum frequency to consider
        """

        # Conversion to cython for performance (?)

        # Declare SU ouput
        sumasw = SUdata()

        # Get scaling factor on coordinates from header
        scalco = self.header[0]['scalco']
        if scalco < 0:
            scale_coordinates = -1./float(scalco)
        if scalco == 0:
            scale_coordinates = 1.
        if scalco > 0:
            scale_coordinates = float(scalco)

        # Get (X, Y) coordinates
        x = self.header[:]['sx']*scale_coordinates-self.header[:]['gx']*scale_coordinates
        y = self.header[:]['sy']*scale_coordinates-self.header[:]['gy']*scale_coordinates

        # Get Z coordinates
        z = np.zeros(len(x), dtype=np.float32)
        for irec in range(0, len(x)):
            scalel = self.header[irec]['scalel']
            if scalel < 0:
                scale_elevation = -1./float(scalel)
            if scalel == 0:
                scale_elevation = 1.
            if scalel > 0:
                scale_elevation = float(scalel)
        z = self.header[:]['selev']*scale_elevation-self.header[:]['gelev']*scale_elevation

        # Calculate offsets
        offset = np.sqrt(x**2+y**2+z**2)

        # Create the velocity vector
        nv = int((vmax-vmin)/dv)+1
        vel = np.linspace(vmin, vmax, nv, dtype=np.float32)

        # Get the number of samples and the time sampling from header
        ns = int(self.header[0]['ns'])
        dt = self.header[0]['dt']/1000000.

        # Apply Real Fourier transform to data
        gobs = np.fft.rfft(self.trace, axis=1)

        # Get the corresponding frequency vector
        freq = np.fft.rfftfreq(ns, d=dt)
        dw = freq[1]
        iwmin = int(fmin/dw)
        nw = int((fmax-fmin)/dw)+1

        # Initialize temporary and dispersion diagram arrays
        tmp = np.zeros(nw, dtype=np.complex64)
        disp = np.zeros((nv, nw), dtype=np.float32)

        # Loop over velocities
        for iv in range(0, nv):
            tmp[:] = complex(0., 0.)
            # Loop over traces
            for ir in range(0, len(offset)):
                # Loop over frequencies
                for iw in range(0, nw):
                    # Calculate the phase
                    phase = complex(0., 1.)*2.*np.pi*offset[ir]*freq[iw+iwmin]/vel[iv]
                    # Stack over frequencies and receivers
                    tmp[iw] += gobs[ir, iw+iwmin]*np.exp(phase)
            # Stack over velocities
            disp[iv,:] += np.abs(tmp[:])

        # Create SU file
        sumasw.create(disp, dw)

        # Update SU header
        sumasw.header[:]['ns'] = len(freq[iwmin:iwmin+nw])
        sumasw.header[:]['d1'] = dw
        sumasw.header[:]['d2'] = np.abs(vel[1]-vel[0])
        sumasw.header[:]['dt'] = 0
        sumasw.header[:]['f1'] = freq[iwmin]
        sumasw.header[:]['f2'] = vel[0]
        sumasw.header[:]['trid'] = 132 # Like 122 but for MASW

        return sumasw, vel, freq[iwmin:iwmin+nw]

    def dispick(self, vpick, wpick, dltv=50.):
        """
        Pick the effective dispersion curve from a MASW dispersion diagram (SU structure).
        Return a 2D numpy array containing the velocity picked (2nd column) for each frequency (1st column).

        :param vpick: starting position in velocity for picking
        :param wpick: starting position in frequency for picking
        :param dltv: accepted velocity jump between two contiguous frequencies
        """

        # Get the frequency vector
        nfrq = int(self.header[0]['ns'])
        dfrq = float(self.header[0]['d1'])
        frq_min = float(self.header[0]['f1'])
        frq_max = frq_min+float(nfrq-1)*dfrq
        frq = np.linspace(frq_min, frq_max, nfrq)

        # Get the velocity vector
        nvel = int(self.header.shape[0])
        dvel = float(self.header[0]['d2'])
        vel_min = float(self.header[0]['f2'])
        vel_max = vel_min+float(nvel-1)*dvel
        vel = np.linspace(vel_min, vel_max, nvel)

        # Declare picking array
        pick = np.zeros((nfrq, 2), dtype=np.float32)

        # Determine Vmin and Vmax indices at starting velocity
        if vpick-dltv > vel_min:
            ivmin = int((vpick-dltv-vel_min)/dvel)
        else:
            ivmin = 0
        if vpick+dltv < vel_max:
            ivmax = int((vpick+dltv-vel_min)/dvel)
        else:
            ivmax = nvel-1

        # Determine the point at the starting frequency
        iwpick0 = int((wpick-frq_min)/dfrq)
        ivpick0 = np.argmax(self.trace[ivmin:ivmax, iwpick0])
        pick[iwpick0, 0] = frq[iwpick0]
        pick[iwpick0, 1] = vel[ivmin+ivpick0]

        # Left-side
        for iw in range(0, iwpick0):
            # Get frequency indicde
            iwpick = iwpick0-iw-1
            # Get velocity range
            vpick = pick[iwpick+1, 1]
            if vpick-dltv > vel_min:
                ivmin = int((vpick-dltv-vel_min)/dvel)
            else:
                ivmin = 0
            if vpick+dltv < vel_max:
                ivmax = int((vpick+dltv-vel_min)/dvel)
            else:
                ivmax = nvel-1
            # Pick
            ivpick = np.argmax(self.trace[ivmin:ivmax,iwpick])
            pick[iwpick, 0] = frq[iwpick]
            pick[iwpick, 1] = vel[ivmin+ivpick]

        # Right-side
        for iw in range(iwpick0+1, nfrq):
            # Get frequency indicde
            iwpick = iw
            # Get velocity range
            vpick = pick[iwpick-1, 1]
            if vpick-dltv > vel_min:
                ivmin = int((vpick-dltv-vel_min)/dvel)
            else:
                ivmin = 0
            if vpick+dltv < vel_max:
                ivmax = int((vpick+dltv-vel_min)/dvel)
            else:
                ivmax = nvel-1
            # Pick
            ivpick = np.argmax(self.trace[ivmin:ivmax,iwpick])
            pick[iwpick, 0] = frq[iwpick]
            pick[iwpick, 1] = vel[ivmin+ivpick]

        return pick

    def resamp(self, nso, dto):
        """
        Resample data in time.
        Based on scipy.signal.resample

        :param nso: number of time samples in output
        :param dto: time sampling in output
        """

        # Create a copy of the input SU data
        dobsresamp = copy.deepcopy(self)

        # Get values from header
        ns = self.header[0]['ns']
        dt = self.header[0]['dt']/1000000.

        # Calculate time lenght for the old data
        t_old = float(ns-1)*dt

        # Calculate time lenght for the resampled data
        t_resamp = float(nso-1)*dto

        # Calculate the number of time samples of the old trace to resample
        nsamp = int(t_resamp/dt)+1

        # Resampling
        if nsamp > ns:
            print('Impossible to resample \n')
        else:
            if np.ndim(self.trace) == 1:
                dobsresamp.trace = resample(self.trace[:,:nsamp], num=nso)
            else:
                dobsresamp.trace = resample(self.trace[:,:nsamp], num=nso, axis=1 )

        # Edit header
        dobsresamp.header[:]['ns'] = nso
        dobsresamp.header[:]['dt'] = int(dto*1000000.)

        return dobsresamp

    def mute(self, xmute, tmute, key='tracl', ntaper=0, mode=0):
        """
        Mute above or below a user-defined polygonal lineself.

        :param key: SU header key
        :param xmute: array of position values
        :param tmute: array of time values
        :param ntaper: number of points to taper before mute
        :param mode: mute below (0) or above (1)
        """

        # Create a copy of the input SU data
        dobsmute = copy.deepcopy(self)

        # Get values from header
        ns = self.header[0]['ns']
        dt = self.header[0]['dt']/1000000.
        delrt = self.header[0]['delrt']/1000.
        ntrac = len(self.header)

        # Get the number of points
        npts = len(xmute)

        # Get the keyword values
        keyval = self.header[:][key]

        # Get trace number for each point
        keytracn = np.zeros(npts, dtype=np.int)
        for ipts in range(0, npts):
            keytracn[ipts] = np.argmin(np.abs(xmute[ipts]-keyval[:]))

        # Build the sine squared taper
        taper = np.zeros(ntaper, dtype=np.float32)
        for itaper in range(0, ntaper):
            ftap = np.sin(float(itaper+1)*np.pi/(float(2*ntaper)))
            taper[itaper] = ftap**2

        # Build the polygonal line
        polyline = np.zeros(ntrac, dtype=np.int)
        ## First point
        if keytracn[0] > 0:
            polyline[:keytracn[0]] = int((tmute[0]-delrt)/dt)
        ## Last point
        if keytracn[-1] < ntrac:
            polyline[keytracn[-1]:] = int((tmute[-1]-delrt)/dt)
        ## Middle points
        for ipts in range(1, npts):
            slope = (tmute[ipts]-tmute[ipts-1])/(xmute[ipts]-xmute[ipts-1])
            origin = tmute[ipts-1]
            i = 0
            for itrac in range(keytracn[ipts-1], keytracn[ipts]):
                polyline[itrac] = int((slope*float(i)+tmute[ipts-1]-delrt)/dt)
                i += 1

        # Mute
        if mode == 0: # Mute above
            for itrac in range(0, ntrac):
                imute = polyline[itrac]
                # Apply taper
                for j in range(0, ntaper):
                    if imute-j >= 0:
                        dobsmute.trace[itrac, imute-j] *= taper[ntaper-j-1]
                if imute-ntaper >= 0:
                    dobsmute.trace[itrac,:imute-ntaper] = 0.
        if mode == 1: # Mute below
            for itrac in range(0, ntrac):
                imute = polyline[itrac]
                # Apply taper
                for j in range(0, ntaper):
                    if imute+j < ns:
                        dobsmute.trace[itrac, imute+j] *= taper[j]
                if imute+ntaper < ns:
                    dobsmute.trace[itrac,imute+ntaper:] = 0.

        return dobsmute

    def specfx(self):
        """
        Fourier spectrum (time to frequency) of traces using the numpy.fft functions.
        """

        # Create a copy of the input SU data
        dobsspecfx = copy.deepcopy(self)

        # Amplitude of the real Fourier transform
        dobsspecfx.trace = np.absolute(np.fft.rfft(self.trace, axis=1))

        # Get the frequency vector
        ns = dobsspecfx.header[0]['ns']
        dt = dobsspecfx.header[0]['dt']/1000000.
        frqv = np.fft.rfftfreq(ns, dt)

        # Update the SU header
        dobsspecfx.header[:]['ns'] = len(frqv)
        dobsspecfx.header[:]['d1'] = frqv[1]-frqv[0]
        dobsspecfx.header[:]['dt'] = 0
        dobsspecfx.header[:]['trid'] = 118 # Amplitude of complex trace from 0 to Nyquist

        return dobsspecfx

    def specfk(self):
        """
        FK spectrum of traces using the numpy.fft functions.
        """

        # Create a copy of the input SU data
        dobsspecfk = copy.deepcopy(self)

        # Get dx from header, if not set dx=1.0
        d2 = dobsspecfk.header[0]['d2']
        if d2 == 0:
            d2 = 1.0
        ntrac = len(dobsspecfk.header)

        # Amplitude of the real Fourier transform
        dobsspecfk.trace = np.fft.rfft(self.trace, axis=1)
        dobsspecfk.trace = np.fft.fft(dobsspecfk.trace, axis=0)
        dobsspecfk.trace = np.flip(np.fft.fftshift(dobsspecfk.trace, axes=0), axis=0)
        dobsspecfk.trace = np.absolute(dobsspecfk.trace)

        # Get the frequency and K vectors
        ns = dobsspecfk.header[0]['ns']
        dt = dobsspecfk.header[0]['dt']/1000000.
        frqv = np.fft.rfftfreq(ns, dt)
        wavv = np.fft.fftfreq(ntrac, d2)
        # Centering
        wavv = np.fft.fftshift(wavv)

        # Update the SU header
        dobsspecfk.header[:]['ns'] = len(frqv)
        dobsspecfk.header[:]['d1'] = frqv[1]-frqv[0]
        dobsspecfk.header[:]['d2'] = np.abs(wavv[1]-wavv[0])
        dobsspecfk.header[:]['dt'] = 0
        dobsspecfk.header[:]['f1'] = frqv[0] #frqv[1]-frqv[0]
        dobsspecfk.header[:]['f2'] = wavv[0]
        dobsspecfk.header[:]['trid'] = 122 # Amplitude of complex trace from 0 to Nyquist

        return dobsspecfk
