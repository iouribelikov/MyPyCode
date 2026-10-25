import numpy as np

r = np.array([57529., 20710., 2477.5])
g = np.array([5552.8, 33944., 5386.4])
b = np.array([2231.7, 8311.6, 60449.])
w = np.array([29304., 45916., 27150.])

# Exposure equalisation
A = np.matrix.transpose(np.array([r,g,b]))
Ai = np.linalg.inv(A)
k = Ai.dot(w)
print("Exposure coefficients: ",k)
r = r*k[0]
g = g*k[1]
b = b*k[2]

# White balance
wb = np.array([w[1]/w[0],1,w[1]/w[2]])
print("WB coefficients: ",wb)
r[0] = r[0]*wb[0]
r[1] = r[1]*wb[1]
r[2] = r[2]*wb[2]

g[0] = g[0]*wb[0]
g[1] = g[1]*wb[1]
g[2] = g[2]*wb[2]

b[0] = b[0]*wb[0]
b[1] = b[1]*wb[1]
b[2] = b[2]*wb[2]

M = np.matrix.transpose(np.array([r,g,b]))
Mi = np.linalg.inv(M)
e = np.linalg.eigvals(Mi)
Mi = Mi/e[0]
print('Eigenvalues: ', np.linalg.eigvals(Mi),'\n')
print('Conversion matrix:')
print(Mi,'\n')
print('Checking white:',Mi.dot([w[1],w[1],w[1]]),'\n')
print('Checking red:',  Mi.dot(r))
print('Checking green:',Mi.dot(g))
print('Checking blue:', Mi.dot(b))

