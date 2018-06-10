# -*- coding: utf-8 -*-
"""
Created on Sun May 27 22:19:11 2018

@author: Adrian
"""

import sympy
import numpy as np

f = '2*x1^2+3*x2^2+3*x3^2+4*x4^2+2*x5^2+2*x6^2+2*x7^2'


def armijo_step(f,x,gradf,s,beta,sigma):
    i=0
    while(np.asarray(f(*x))-f(*tuple(np.asarray(x)-(beta**i)*s*np.asarray(gradf(*x)))) < sigma*(beta**i)*s*sum(np.asarray(gradf(*x))**2)):
        i=i+1
    return((beta**i)*s)

def steepest_descent(f,x0,eps,s,beta,sigma):
    f = sympy.sympify(f)
    gradf = [f.diff(x) for x in f.free_symbols]
    gradf = sympy.lambdify((f.free_symbols), gradf)
    f = sympy.lambdify((f.free_symbols),f)
    x=x0
    while((sum(np.asarray(gradf(*x))**2)>eps)==True):
        alpha = armijo_step(f,x,gradf,s,beta,sigma)
        print(alpha)
        x=x-alpha*np.asarray(gradf(*x))
    return(x)

steepest_descent(f,(5,15,5,5,5,5,5),0.00000000000000000000000000000001,1,0.5,0.5)     
