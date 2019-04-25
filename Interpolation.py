#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def upsample(x, k):

    assert k >= 1, 'k must be equal or greater than 1'

    mn = x.shape
    if len(mn) == 2:
        m = mn[1]
        n = mn[0]
    elif len(mn) == 1:
        m = 1
        n = mn[0]
    else:
        raise ValueError ("x is greater than 2D")

    nn = n * k

    xt = np.linspace(1, n, n)
    xp = np.linspace(1, n, nn)

    return interp(xp, xt, x)


def interp(xp, xt, x):
    """
      Interpolate the signal to the new points using a sinc kernel

      input:
      xt    time points x is defined on
      x     input signal column vector or matrix, with a signal in each row
      xp    points to evaluate the new signal on

      output:
      y     the interpolated signal at points xp
      """

    mn = x.shape
    # print(mn)
    if len(mn) == 2:
        m = mn[1]
        n = mn[0]
    elif len(mn) == 1:
        m = 1
        n = mn[0]
    else:
        raise ValueError("x is greater than 2D")

    nn = len(xp)

    y = np.zeros((m, nn), dtype=x.dtype)

    for (pi, p) in enumerate(xp):
        si = np.tile(np.sinc(xt - p), (m, 1))
        dot = np.dot(si, x)
        y[:, pi] = np.sum(dot)

    # print(y.shape)

    return y.squeeze()