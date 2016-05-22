def rxns(parameters):

    k3,k4,k5,k6,k7,k8,k12,k13,n = parameters      # kinetic parameters (remember to add these to the function call in Simulation.py

    reactions = [({'HCL': -n, 'LDH': -1}, 1, k3),
                 ({'HCL': 1, 'pas': -1, 'rad': 1,'auto': 'HCL'}, 1, k4),
                 ({'pas': -1, 'HCL': 1, 'rad': 1}, 1, k5),
                 ({'rad': -1, 'ps': -1}, 1, k6),
                 ({'rad': -1, 'dp': 1}, 1, k7),
                 ({'rad': -1, 'xl': 1}, 1, k8),
                 ({'rad': -1, 'half': 2}, 2, k12),          # half
                 ({'rad': -2, 'double': 1}, 1, k13)]

    return reactions

components = {'HCL': 0,      # With initial
               'LDH': 1.3,
               'pas': 5,
               'rad': 0,
               'ps': 1.3,
               'dp': 0,
               'xl': 0,
               'double': 0,
               'half': 0,
               'none': 1}


def params(ini_values):
    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11,k12, k13, k14, k15, UA, mu_0, E, q, prim_stab_0, LDH_0 = ini_values
    #          (         Name,       Value,  Vary,    Min,     Max)
    lis =      [(         'k1',          k1,  True,    1.6,     2.1),
                (         'k2',          k2,  True,    8.0,    46.0),
                (         'k3',          k3,  True,    0.0,     6.0),
                (         'k4',          k4,  True,    0.0,     2.1),
                (         'k5',          k5,  True,    0.0,    0.03),
                (         'k6',          k6,  True,    0.0,    39.0),
                (         'k7',          k7,  True,    0.0,     2.7),
                (         'k8',          k8,  True,    0.0,     7.9),
                (         'k9',          k9,  True,    0.0,    13.1),
                (        'k10',         k10,  True,    0.7,    10.9),
                (        'k11',         k11,  True,    2.0,     3.6),
                (      'k12',           k12,  True,    0.,     100),
                (      'k13',           k13,  True,    0.,     100),
                (      'k14',           k14,  True,    0.,     100),
                (      'k15',           k15,  True,    0.,     100),
                (         'UA',          UA,  True,    275.0,  402.0),
                (       'mu_0',        mu_0,  False,   0.0,    0.1),
                (          'E',           E,  False,   5000.0, None),
                (          'q',           q,  False,   0.0,    17.0),
                ('prim_stab_0', prim_stab_0,  False,   0.5,    1.3),
                (      'LDH_0',       LDH_0,  False,   None,   None)]
               
    return lis



limits = [[1.6, 2.1],
          [8.0, 46.0],
          [0.0, 6.0],
          [0.0, 2.1],
          [0.0, 0.03],
          [0.0, 39.0],
          [0.0, 2.7],
          [0.0, 7.9],
          [0.0, 13.1],
          [0.7, 10.9],
          [2.0, 3.6],
          [0.,  100.],
          [0.,  100.],
          [0.,  100.],
          [0.,  100.],
          [275.0, 402.0]]





figure_heads = ['k1, visc-torque',
                'k2, Tm-T',
                'k3, LDH rxn',
                'k4, auto-catalytic HCl production rxn',
                'k5, initiation rxn for HCl production',
                'k6, primary stabiliser rxn',
                'k7, radical to degraded polymer',
                'k8, radical to cross-link',
                'k9, degraded polymer effect on visc',
                'k10, cross-linking effect on visc',
                'k11, mechanical work affecting temp',
                'k12',
                'k13',
                'k14',
                'k15'
                'UA',
                'mu_0',
                'E',
                'q',
                'prim_stab_0',
                'LDH_0']





