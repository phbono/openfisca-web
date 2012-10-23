# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

'''
Created on 22 dec. 2011

@author: benjello
'''
from __future__ import division

import numpy as np
from numpy import exp, ones, zeros, unique, array, dot
from scipy.optimize import fsolve

def linear(u):
    return 1+u
   
def linear_prime(u):
    return ones(u.shape, dtype = float) 
   
def raking_ratio(u):
    return exp(u)
        
def raking_ratio_prime(u):
    return exp(u)        
        
def logit(u,low,up):
    a=(up-low)/((1-low)*(up-1))
    return (low*(up-1)+up*(1-low)*exp(a*u))/(up-1+(1-low)*exp(a*u))

def logit_prime(u,low,up):
    a=(up-low)/((1-low)*(up-1))
    return ( (a*up*(1-low)*exp(a*u))*(up-1+(1-low)*exp(a*u))-
              (low*(up-1)+up*(1-low)*exp(a*u))*(1-low)*a*exp(a*u) )/(up-1+(1-low)*exp(a*u))**2

def build_dummies_dict(data):
    '''
    return a dict with unique values as keys and vectors as values
    '''
    unique_val_list = unique(data) 
    output = {}
    for val in unique_val_list:    
        output[val] = (data==val)
    return output

def calmar(data, margins, param = {}, pondini='wprm_init'):
    ''' 
    calmar : calibration of weights according to some margins
      - data is a dict containing individual data
      - pondini (char) is the inital weight
     margins is a dict containing for each var:
      - a scalar var numeric variables
      - a dict with categories key and population
      - eventually a key named totalpop : total population. If absent initialized to actual total population 
     param is a dict containing the following keys
      - method : 'linear', 'raking ratio', 'logit'
      - lo     : lower bound on weights ratio  <1
      - up     : upper bound on weights ration >1
      - use_proportions : default FALSE; if TRUE use proportions if total population from margins doesn't match total population
      - param xtol  : relative precision on lagrangian multipliers. By default xtol = 1.49012e-08 (default fsolve xtol)
      - param maxfev :  maximum number of function evaluation TODO  
    '''   
    # choice of method
    
    if not margins:
        raise Exception("Calmar requires non empty dict of margins")
    
    if not 'method' in param:
        param['method'] = 'linear'

    if param['method'] == 'linear': 
        F = linear
        F_prime = linear_prime
    elif param['method'] == 'raking ratio': 
        F =  raking_ratio
        F_prime =  raking_ratio_prime
    elif param['method'] == 'logit':
        if not 'up' in param:
            raise Exception("When method is 'logit', 'up' parameter is needed in param")
        if not 'lo' in param:
            raise Exception("When method is 'logit', 'lo' parameter is needed in param")
        if param['up'] <= 1:
            raise Exception("When method is 'logit', 'up' should be strictly greater than 1")
        if param['lo'] >= 1:
            raise Exception("When method is 'logit', 'lo' should be strictly less than 1")        
        F = lambda x: logit(x, param['lo'], param['up'])
        F_prime = lambda x: logit_prime(x, param['lo'], param['up'])
    
    else:
        raise Exception("method should be 'linear', 'raking ratio' or 'logit'")
    # construction observations matrix
    if 'totalpop' in margins:
        totalpop = margins.pop('totalpop')
    else:
        totalpop = data[pondini].sum()

    if 'use_proportions' in param:
        use_proportions = param['use_proportions']    
    else:
        use_proportions = False   

    nk = len(data[pondini])

    # number of Lagrange parameters (at least total population)
    nj = 1
    
    margins_new = {}
    margins_new_dict = {}
    for var, val in margins.iteritems():
        if isinstance(val, dict):
            dummies_dict = build_dummies_dict(data[var])            
            k, pop = 0, 0
            for cat, nb in val.iteritems():
                cat_varname =  var + '_' + str(cat)
                data[cat_varname] = dummies_dict[cat]
                margins_new[cat_varname] = nb
                if not margins_new_dict.has_key(var):
                    margins_new_dict[var] = {}
                margins_new_dict[var][cat] = nb
                pop += nb
                k += 1
                nj += 1
            # Check total popualtion
            if pop != totalpop:
                if use_proportions:
                    print 'calmar: categorical variable %s is inconsistent with population; using proportions' % var
                    for cat, nb in val.iteritems():
                        cat_varname =  var + '_' + str(cat)
                        margins_new[cat_varname] = nb*totalpop/pop
                        margins_new_dict[var][cat] = nb*totalpop/pop
                else:
                    raise Exception('calmar: categorical variable ', var, ' is inconsistent with population')
        else:
            margins_new[var] = val
            margins_new_dict[var] = val
            nj += 1

    # On conserve systematiquement la population  
    if  hasattr(data,'dummy_is_in_pop'):
        raise Exception('dummy_is_in_pop is not a valid variable name') 
        
    data['dummy_is_in_pop'] = ones(nk)
    margins_new['dummy_is_in_pop'] = totalpop

    # paramètres de Lagrange initialisés à zéro
    lambda0 = zeros(nj)
    
    # initial weights
    d = data[pondini]
    x = zeros((nk, nj)) # nb obs x nb constraints
    xmargins = zeros(nj)
    margins_dict = {}
    j=0
    for var , val in margins_new.iteritems():
        x[:,j] = data[var]
        xmargins[j] = val
        margins_dict[var] =val
        j += 1

    # Résolution des équations du premier ordre
    constraint = lambda l: dot(d*F(dot(x, l)), x) - xmargins
    constraint_prime = lambda l: dot(d*( x.T*F_prime( dot(x, l))), x )
    ## le jacobien celui ci-dessus est constraintprime = @(l) x*(d.*Fprime(x'*l)*x');
    
    essai, ier = 0, 2
    if 'xtol' in param: 
        xtol = param['xtol']
    else:
        xtol = 1.49012e-08
        
    err_max = 1    
    conv = 1
    while (ier==2 or ier==5 or ier==4) and not (essai >= 10 or (err_max < 1e-4 and conv < 1e-8 )):
        lambdasol, infodict, ier, mesg = fsolve(constraint, lambda0, fprime=constraint_prime, maxfev= 256, xtol=xtol, full_output=1)
        lambda0 = 1*lambdasol
        essai += 1
        
        pondfin = d*F( dot(x, lambdasol))
        rel_error ={}
        for var, val in margins_new.iteritems():
            rel_error[var] =  abs((data[var]*pondfin).sum() - margins_dict[var])/margins_dict[var]
        import operator
        sorted_err = sorted(rel_error.iteritems(), key=operator.itemgetter(1), reverse = True)
        
        conv = abs(err_max - sorted_err[0][1])
        err_max = sorted_err[0][1]
            
    if (ier==2 or ier==5 or ier==4): 
        print "calmar: stopped after ", essai, "tries"
    return pondfin, lambdasol, margins_new_dict 

