#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def decimate(x,k):

    # part of the code in this function is taken from
    # https://tomroelandts.com/articles/how-to-create-a-simple-low-pass-filter

    fc = 0.4  # Cutoff frequency as a fraction of the sampling rate (in (0, 0.5)).
    b = 0.08  # Transition band, as a fraction of the sampling rate (in (0, 0.5)).
    N = int(np.ceil((4 / b)))
    if not N % 2:
        N += 1  # Make sure that N is odd.
    n = np.arange(N)

    # Compute sinc filter.
    h = np.sinc(2 * fc * (n - (N - 1) / 2.))

    # Compute Blackman window.
    # w = np.blackman(N)
    w = np.hamming(N)

    # Multiply sinc filter with window.
    h = h * w

    # Normalize to get unity gain.
    h = h / np.sum(h)

    x = np.convolve(x, h, mode='same')
    # print(x.shape)

    # downsampling
    x = x[:x.size:k]
    # print(x.shape)
    return x