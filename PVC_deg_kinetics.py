
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
    comps = list(stoic.keys())
    r = k

    if 'auto' in stoic.keys():
        r *= C[stoic['auto']]**order

    for i in comps:

        if i != 'auto':
            if stoic[i] <= 0:
                r *= C[i]**order
            else:
                pass
        else:
            pass

    return r


def mol_bal(components, reactions, C):
    delta = {}
    for i in components:
        delta[i] = 0
        for j in reactions:
            rxn_rate = rate(j, C)
            stoic = j[0]

            if i in stoic.keys():
                delta[i] += rxn_rate*stoic[i]

            else:
                pass

    return delta

