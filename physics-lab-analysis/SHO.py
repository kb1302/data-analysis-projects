from math import factorial
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

q = 1000
NA = 100
NB = 100
Total = 0

# this section creates the data points
Omega = []
q_A = []
Omega_max = 0.
for qA in range(0,q+1):
   OmegaA = factorial(qA+NA-1)/(factorial(qA)*factorial(NA-1))
   qB = q - qA
   OmegaB = factorial(qB+NB-1)/(factorial(qB)*factorial(NA-1))
   # print (qA, OmegaA, qB, OmegaB, OmegaA*OmegaB)
   Total += OmegaA*OmegaB
   q_A.append(qA)
   Omega.append(OmegaA*OmegaB)
   if Omega[-1]>Omega_max:
      Omega_max = Omega[-1]
print ("Total=",Total)
qA_i = np.array(q_A)
P_i = np.array(Omega)/Total  # probability of the q_A=i macrostate

def Gaussian(x,A,x0,sigma):
   return A*np.exp(-(x-x0)*(x-x0)/(2*sigma*sigma))

# this fits the Gaussian to the data points
popt,pcov = curve_fit(Gaussian,qA_i,P_i, p0=[0.1,500.,100.] )
print ("A = {:3.3e}, x0 = {:3.1f}, sigma = {:3.3f}".format(popt[0],popt[1],popt[2]))

########################################################
N_min = 350  # by adjusting these vars you can zoom in or out, to look for .
N_max = 450  # deviations between the fitted line and calculated points
########################################################

plt.plot(qA_i[N_min:N_max],P_i[N_min:N_max],'o',markersize=1,linewidth=0)
plt.plot(qA_i[N_min:N_max],Gaussian(qA_i[N_min:N_max],*popt))
plt.xlabel(r'$q_A$')
plt.ylabel(r'$P(q_A)$')

plt.show()
