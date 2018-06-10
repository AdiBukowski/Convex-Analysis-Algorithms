# -*- coding: utf-8 -*-
"""
Created on Mon May 28 12:05:03 2018

@author: Adrian
"""
import numpy as np


def simplex_matrix(A,b,c):
    n,m = A.shape
    b = b.reshape(n,1)
    c = np.concatenate((c,[[0]]),axis=1)
    c = -c
    D=np.concatenate((A,b),axis=1)
    D=np.concatenate((D,c),axis=0)
    return(D)


def move(D,x,z,i0,j0):
    n,m = D.shape
    A = np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            if(i==i0 and j==j0):
                A[i,j]=1/D[i,j].astype(float)
            elif(i==i0 and j!=j0):
                A[i,j]=D[i0,j].astype(float)/D[i0,j0].astype(float)
            elif(i!=i0 and j==j0):
                A[i,j]=-D[i,j0].astype(float)/D[i0,j0].astype(float)
            else:
                A[i,j]=D[i,j].astype(float)-D[i0,j].astype(float)*D[i,j0].astype(float)/D[i0,j0].astype(float)
    temp_var = x[j0]
    x[j0]=z[i0]
    z[i0]=temp_var
    return([A,x,z])

def simplex(D):
    n,m = D.shape
    x=[]
    z=[]
    for i in range(1,m):
        x.append('x'+str(i))
    for i in range(1,n):
        z.append('z'+str(i))
    while((D[:,m-1].astype(float)<0).any()==True):
        i0_temp=n-list(reversed(D[:,m-1].astype(float)<0)).index(1)-1
        if(((D[i0_temp,:-1].astype(float)<0).any())==False):
            return('Nie ma rozwiazan dopuszczalnych')
        else:
            j0=(D[i0_temp,:-1].astype(float)<0).tolist().index(1)
            temp_vec = D[i0_temp:-1,j0].astype(float)/(D[i0_temp:-1,m-1].astype(float))
            i0=i0_temp+np.argmax(temp_vec)
            lst=move(D,x,z,i0,j0)
            D=lst[0]
            x=lst[1]
            z=lst[2]
            print(D)
    while((D[n-1,:-1].astype(float)<0).any()==True):
        j0=np.argmax(D[-1,:-1].astype(float)<0)
        if(((D[:-1,j0].astype(float)>0).any())==False):
            return('Funkcja celu jest nieograniczona')
        else:
            temp_vec = D[:-1,j0].astype(float)/D[:-1,m-1].astype(float)*(D[:-1,j0].astype(float)>0)
            i0=np.argmax(temp_vec)
            lst=move(D,x,z,i0,j0)
            D=lst[0]
            x=lst[1]
            z=lst[2]
            print(D)
    x_best = []  
    for i in range(1,m):
        xIndex = 'x' + str(i)
        if(xIndex in x):
            x_best.append(D[-1,x.index(xIndex)])
        else:
            x_best.append(D[z.index(xIndex),-1])
    return([D[n-1,m-1],x_best])

D=np.array([[-1,0,-1],[0,1,5],[-1,-1,-4],[1,-1,2],[2,1,6],[-1,-2,0]])
simplex(D)
