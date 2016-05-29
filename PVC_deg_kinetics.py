# -*- coding: utf-8 -*-
"""
Created on Sun May 22 15:19:58 2016

@author: Imberproninja
"""

def add_component(lib):
    "add_component({'comp_name':C0})"
    C={}
    components=[]
    C.update(lib)
    for i,val in enumerate(C):
        components.append(val)
    return C,components


def rate(tup, C):
    stoic = tup[0]
    order = tup[1]
    k = tup[2]
    r = k

    if 'auto' in stoic:
        r *= C[stoic['auto']]**order

    # to implement double and half only occuring in absence of ps
    double_or_half = 'double' in stoic or 'half' in stoic

    for i in stoic:
        if double_or_half:
            if C['ps'] <= 0.01:
                r *= C[i]**order
            else:
                r == 0

        if i != 'auto':
            if stoic[i] <= 0:
                r *= C[i]**order

    return r


def mol_bal(components, reactions, C):
    delta = {}
    for i in components:
        delta[i] = 0
        for j in reactions:
            rxn_rate = rate(j, C)
            stoic = j[0]

            if i in stoic:
                delta[i] += rxn_rate*stoic[i]

    return delta


