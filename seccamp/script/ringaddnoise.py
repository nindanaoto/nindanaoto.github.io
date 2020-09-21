#!/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import matplotlib.cm as cm
from scipy.stats import norm

μ=1/4
σ=0.1
scale = 200
boundary = 2000

ε=0.003

x = np.linspace(-3.0, 3.0, int(500))
y = np.linspace(-3.0, 3.0, int(500))
z = np.zeros([len(x),len(y)])

def ring(X,Y):
    for i in range(len(X)):
        for j in range(len(Y)):
            r = np.sqrt(X[i]**2+Y[j]**2)
            θ=np.arctan2(X[i],Y[j])/(2*np.pi)
            if 1.8<=r<=2:
                z[j,i]= scale*norm.pdf(x=θ, loc=μ, scale=σ)
            elif 1.75<=r<=2.05:
                z[j,i] = boundary
            elif 1.6<=r<=2.2 and (np.abs(θ)<ε or np.abs(np.abs(θ)-0.5)<ε):
                z[j,i] = boundary
            else: z[j,i] = 0
    return z

z = ring(x,y)

plt.imshow(z,cmap='Greens')
plt.text(250,50,'±0.5',ha='center')
plt.text(250,450,'0',ha='center')
plt.text(450,250,'1/4',ha='center')
plt.axis("off")
plt.show()