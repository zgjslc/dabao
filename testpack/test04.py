import numpy as np
from qdevset import qdevwin,odeslover
import matplotlib.pyplot as plt
from testpack.rk import rk_solver
qd = qdevwin()
ode = odeslover()
plt.figure()
a = np.array([0,2,4,6,8,10,12,15,20,25])
cna = np.array([0.0243,0.0243,0.0255,0.0294,0.0335,0.0356,0.0421,0.0540,0.0382,0.0298])
ca0 = np.array([0.2501,0.2513,0.2530,0.2542,0.2563,0.2560,0.2556,0.2529,0.2520,0.2533])
cza = np.array([0.0005,0.0005,0.0005,0.0006,0.0005,0.0004,0.0006,0.0007,0.0007,0.0008])
mza = np.array([-0.0018,-0.0018,-0.0019,-0.0018,-0.0018,-0.0021,-0.0024,-0.0027,-0.0025,-0.0021])
mx0 = np.array([0.0002,0.0002,0.0002,0.0002,0.0002,0.0002,0.0001,0.0001,0.0001,0.0001])
mya = np.array([-0.0001,-0.0001,-0.0002,-0.0002,-0.0002,-0.0003,-0.0004,-0.0005,-0.0007,-0.0009])

cnd = np.array([0,0.0043,0.0055,0.0054,0.0045,0.0056,0.0061,0.0040,0.0032,0.0028])
cad = np.array([0.0101,0.0113,0.0130,0.0142,0.0163,0.0160,0.0156,0.0129,0.0120,0.0133])
mzd = np.array([0,-0.0018,-0.0019,-0.0018,-0.0018,-0.0021,-0.0024,-0.0027,-0.0025,-0.0021])
mxd = np.array([0.0002,0.0002,0.0002,0.0002,0.0002,0.0002,0.0001,0.0001,0.0001,0.0001])

mzw = np.array([-0.0921,-0.0872,-0.0650,-0.0456,-0.0019,-0.0212,-0.0521,-0.0725,-0.0932,-0.1236])
myw = np.array([-0.0009,-0.0008,-0.0008,-0.0007,-0.0007,-0.0007,-0.0009,-0.0009,-0.0010,-0.0011])
y = myw
mxw = np.array([-0.0009,-0.0008,-0.0008,-0.0007,-0.0007,-0.0007,-0.0009,-0.0009,-0.0010,-0.0011])
mxw1 = np.array([-0.0009,-0.0008,-0.0008,-0.0007,-0.0007,-0.0007,-0.0009,-0.0009,-0.0010,-0.0011])
cna = np.mean(cna)
ca0 = np.mean(ca0)
cza = np.mean(cza)
mx0 = np.mean(mx0)


mza = qd.least_square([1,1],a,mza)
mz1a = mza[0][0]
mz0a = mza[0][1]

mya1 = qd.least_square([1,1],a,mya)
my0a = mya1[0][1]
my1a = mya1[0][0]

cnd = np.mean(cnd)
cad = np.mean(cad)
mzd = np.mean(mzd)
mxd = np.mean(mxd)

mzw = qd.least_square([1,1,1],a,mzw)
mz0w = mzw[0][2]
mz1w = mzw[0][1]
mz2w = mzw[0][0]

myw = qd.least_square([1,1,1],a,myw)
my0w = myw[0][2]
my1w = myw[0][1]
my2w = myw[0][0]


mxw = np.mean(mxw)

########################################开心就好##################################
Q = 452000
S = 0.003848
m = 7.5
It = 1.3
Ix = 0.005
wx = 75.4 * np.pi/180
P = 500
V = 850
ma = 2.5
L = 1.5

ode.param['a1'] = (Q*S*cna-Q*S*ca0+P)/m/V
ode.param['a2'] = Q*S*cza/m/V
ode.param['a3'] = Q*S*cnd/m/V
ode.param['b10'] = Q*S*L*mz0a/It
ode.param['b11'] = Q*S*L*mz1a/It
ode.param['b20'] = Q*S*L*my0a/It
ode.param['b21'] = Q*S*L*my1a/It
ode.param['b3']  = Q*S*L*mzd/It
ode.param['b40'] = Q*S*L*mz0w/V/It
ode.param['b41'] = Q*S*L*mz1w/V/It
ode.param['b42'] = Q*S*L**2*mz2w/V/It
ode.param['b50'] = Q*S*L**2*my0w/V/It
ode.param['b51'] = Q*S*L**2*my1w/V/It
ode.param['b52'] = Q*S*L**2*my2w/V/It
ode.param['c1']  = Q*S*L*mx0/Ix
ode.param['c2']  = Q*S*L**2*mxw/V/Ix      #这里要改一下
ode.param['c3'] = Q*S*L*mxd/Ix
ode.param['It'] = It
ode.param['Ix'] = Ix
ode.param['wx'] = wx


plt.plot(a,mxw*np.array([1]*len(a)))
plt.plot(a,mxw1)
plt.show()
