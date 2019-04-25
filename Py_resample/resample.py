#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import csv
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
from fractions import Fraction
from . import Interpolation as I
from . import Decimation as D


def main():

    ts = time.time()   # Execution start time

    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="Path to the input file")
    parser.add_argument("filename", help="Input filename")
    parser.add_argument("rate", help="New Sample Rate")
    args = parser.parse_args()

    # Reading samples from input file and load them into an array
    data = []
    sample_rate = None
    temp = None
    if os.path.exists(args.file_path):
        try:
            f = open(os.path.join(args.file_path, args.filename), 'r')
            reader = csv.reader(f, quoting=csv.QUOTE_NONE)
            for row in reader:
                if not row:
                    continue
                elif row[0].startswith('#'):
                    if 'Hz' in row[0].split():
                        for item in row[0].split():
                            if item == 'Hz':
                                sample_rate = int(temp)
                            temp = item
                else:
                    data.append(row)

        except OSError:
            print('file_path does not exit')

    if sample_rate is None:
        print('Sample rate of the sensor data is not found from the file provided.')
        sample_rate = input('Provide it here: ')
        assert sample_rate is int, 'Sample Rate must be an integer'

    o_signal = np.array(data, dtype='float64')

    new_rate = int(args.rate)
    if new_rate == sample_rate:
        raise Exception('The Signal is already sampled at the rate you desire.')

    print("Original Sample Rate: ", sample_rate)
    print("New Sample Rate: ", new_rate)

    k = new_rate / sample_rate

    uf = 9.8 / (2 ** 12)

    x_axis = o_signal[:, 0] * uf
    y_axis = o_signal[:, 1] * uf
    z_axis = o_signal[:, 2] * uf

    f = sample_rate
    dt = 1. / f
    n = o_signal.shape[0]
    t = np.arange(0, n * dt, dt)
    print('Number of samples: ', n)

    if k > 1:  # Interpolation by a factor of L
        print('Resampling factor: ', k, ', Interpolation')
        x_axis_r = I.upsample(x_axis, k)
        y_axis_r = I.upsample(y_axis, k)
        z_axis_r = I.upsample(z_axis, k)

    else:
        f = Fraction(new_rate, sample_rate).limit_denominator()
        L = f.numerator
        M = f.denominator
        if L == 1:  # Decimation by a factor of M
            print('Resampling factor: ', M, ', Decimation')

            x_axis_r = D.decimate(x_axis, M)
            y_axis_r = D.decimate(y_axis, M)
            z_axis_r = D.decimate(z_axis, M)

        else:
            # Performing L/M method. First interpolate by factor of L and decimate by factor of M
            print('Resampling factor: ', L, '/', M)
            print('Interpolation by a factor of ', L, 'and Decimation by a factor of ', M)

            # Interpolating by a factor of L
            x_axis_r = I.upsample(x_axis, L)
            y_axis_r = I.upsample(y_axis, L)
            z_axis_r = I.upsample(z_axis, L)

            # Decimating by a factor of M
            x_axis_r = D.decimate(x_axis_r, M)
            y_axis_r = D.decimate(y_axis_r, M)
            z_axis_r = D.decimate(z_axis_r, M)

    nf = new_rate
    ndt = 1. / nf
    nn = x_axis_r.shape[0]
    ut = np.linspace(min(t), max(t), nn)

    # The resampled signal is:
    r_signal = np.empty(shape=(nn, 3), dtype='float64')
    r_signal[:, 0] = x_axis_r
    r_signal[:, 1] = y_axis_r
    r_signal[:, 2] = z_axis_r

    xres = np.interp(t, ut, x_axis_r)
    xdiff = xres - x_axis
    mean_error = np.sum(xdiff) / len(xdiff)
    print('Mean Statistical Error of x-axis = ', mean_error)

    yres = np.interp(t, ut, y_axis_r)
    ydiff = yres - y_axis
    mean_error = np.sum(ydiff) / len(ydiff)
    print('Mean Statistical Error of y-axis = ', mean_error)

    zres = np.interp(t, ut, z_axis_r)
    zdiff = zres - z_axis
    mean_error = np.sum(zdiff) / len(zdiff)
    print('Mean Statistical Error of z-axis = ', mean_error)

    # Difference between Original and the Resampled Signal
    diff_signal = np.empty(shape=(n, 3), dtype='float64')
    diff_signal[:, 0] = xres
    diff_signal[:, 1] = yres
    diff_signal[:, 2] = zres

    tstp = time.time()
    print('Total execution time:', "{0:.3f}".format(tstp - ts))

    size = (3, 1)
    plt.figure(1)
    plt.suptitle(f'Sensor signal with {n} samples, sampled at {sample_rate} Hz is resampled to {new_rate} Hz')

    s1 = plt.subplot2grid(size, (0, 0))
    plt.title("Original Signal", y=1)
    plt.plot(t, x_axis, 'b', linewidth=1, label='x-axis')
    # plt.plot(t, y_axis, 'm', label='y-axis')
    # plt.plot(t, z_axis, 'g', label='z-axis')
    plt.xlabel('time (s)')
    plt.ylabel('Acceleration (m/s2)')
    s1.legend(loc='upper right', fontsize='x-small')

    s2 = plt.subplot2grid(size, (1, 0))
    plt.title("Resampled Signal", y=1)
    plt.plot(ut, x_axis_r, 'b', linewidth=1,  label='x-axis')
    # plt.plot(ut, y_axis_r, 'm', label='y-axis')
    # plt.plot(ut, z_axis_r, 'g', label='z-axis')
    plt.xlabel('time (s)')
    plt.ylabel('Acceleration (m/s2)')
    s2.legend(loc='upper right', fontsize='x-small')

    s3 = plt.subplot2grid(size, (2, 0))
    plt.title("Error", y=1)
    plt.plot(t, xdiff, 'b', linewidth=1, label='x-axis diff')
    # plt.plot(t, ydiff, 'm', label='y-axis diff')
    # plt.plot(t, zdiff, 'g', label='z-axis diff')
    plt.xlabel('time (s)')
    plt.ylabel('Acceleration (m/s2)')
    s3.legend(loc='upper right', fontsize='x-small')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    sys.exit(main())
