import math
import numpy as np
import matplotlib.pyplot as plt


def rk_solver(y, x, dx, f):
    """ y is the initial value for y
        x is the initial value for x
        dx is the time step in x
        f is derivative of function y(t)
    """
    k1 = dx * f(y, x)
    k2 = dx * f(y + 0.5 * k1, x + 0.5 * dx)
    k3 = dx * f(y + 0.5 * k2, x + 0.5 * dx)
    k4 = dx * f(y + k3, x + dx)
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.


def runge_kutta(y, x, dx, f):
    """ y is the initial value for y
        x is the initial value for x
        dx is the time step in x
        f is derivative of function y(t)
    """
    k1 = dx * f(y, x)
    k2 = dx * f(y + 0.5 * k1, x + 0.5 * dx)
    k3 = dx * f(y + 0.5 * k2, x + 0.5 * dx)
    k4 = dx * f(y + k3, x + dx)
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.


if __name__=='__main__':
    xin = 1
    a1 = 3.86; a2 = 7.46; a3 = 9.13; a4 = 7.46; a5 = 3.86; a6 =1
    w0 = 50; w2 = w0**2; w3 = w2 * w0; w4 = w3 * w0; w5 = w4 * w0; w6 = w5 * w0
    t = 0.
    y = [0.]*6
    dt = .0001
    ys, ts = [], []
    def func(x, t):
        dx = [0.]*6
        x1,x2,x3,x4,x5,x6 = x
        dx[0] = x2
        dx[1] = x3
        dx[2] = x4
        dx[3] = x5
        dx[4] = x6
        dx[5] = w6 *(xin - a5 * x6/w5 - a4 *x5/w4 - a3 * x4 / w3 - a2 * x3 / w2 -a1 * x2/w0-x1)/a6
        return np.array(dx)

    while t <= 0.5:
        y = runge_kutta(y, t, dt, func)
        t += dt
        ys.append(y[0])
        ts.append(t)

    plt.figure()
    plt.plot(ts,ys)
    plt.legend()
    plt.show()

