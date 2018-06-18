# -*- coding: utf-8 -*-
"""
Created on Sun May 27 22:19:11 2018

@author: Adrian
"""

import sympy
import numpy as np



def armijo_step(f,x,gradf,s,beta,sigma):
    i=0
    while(np.asarray(f(*x))-f(*tuple(np.asarray(x)-(beta**i)*s*np.asarray(gradf(*x)))) < sigma*(beta**i)*s*sum(np.asarray(gradf(*x))**2)):
        i=i+1
    return((beta**i)*s)

def steepest_descent(f,x0,eps,s,beta,sigma):
    f = sympy.sympify(f)
    gradf = [f.diff(x) for x in sorted(list(f.free_symbols), key = lambda x: str(x)[-1])]
    gradf = sympy.lambdify(sorted(list(f.free_symbols), key = lambda x: str(x)[-1]), gradf)
    f = sympy.lambdify((f.free_symbols),f)
    x=x0
    while((sum(np.asarray(gradf(*x))**2)>eps)==True):
        alpha = armijo_step(f,x,gradf,s,beta,sigma)
        x=x-alpha*np.asarray(gradf(*x))
    return(x)

def lagrange_multiplier(f,h,s,beta,sigma,n):
    lambda_coeff = [0 for i in range(len(h))]
    c=2
    eps = 1  
    x=[10 for i in range(len(sympy.sympify(f).free_symbols))]
    for _ in range(n):
        L = f +'+'+ "+".join([str(-x)+'*'+'('+str(y)+')' for x,y in zip(lambda_coeff,h)]) +'+'+  "+".join([str(c/2)+'*'+'('+h_i+')^2' for h_i in h])
        L = sympy.sympify(L)
        h_func = [sympy.lambdify(sorted(list(sympy.sympify(f).free_symbols), key = lambda x: str(x)[-1]),sympy.sympify(h_i)) for h_i in h]
        gradL = [L.diff(x) for x in sorted(list(sympy.sympify(f).free_symbols), key = lambda x: str(x)[-1])]
        gradL = sympy.lambdify((sorted(list(sympy.sympify(f).free_symbols), key = lambda x: str(x)[-1])),gradL)  
        x=steepest_descent(L,x,eps,s,beta,sigma)
        lambda_coeff = np.asarray(lambda_coeff) - c*np.asarray([h_i(*x) for h_i in h_func])              
        c=2*c
        eps = eps/2
    return(x)

f = 'x1^2+x2^2+x3^2'
h= ['x1+x2-1','x3-1']    
lagrange_multiplier(f,h,1,0.9,0.001,11)
    

    
    
    