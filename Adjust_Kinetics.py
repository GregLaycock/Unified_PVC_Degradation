def rxns(parameters):

    k3,k4,k5,k6,k7,k8,k12,k13,n = parameters      # kinetic parameters (remember to add these to the function call in Simulation.py

    reactions = [({'HCL': -n, 'LDH': -1}, 1, k3),
                 ({'HCL': 1, 'pas': -1, 'rad': 1,'auto': 'HCL'}, 1, k4),
                 ({'pas': -1, 'HCL': 1, 'rad': 1}, 1, k5),
                 ({'rad': -1, 'ps': -1}, 1, k6),
                 ({'rad': -1, 'dp': 1}, 1, k7),
                 ({'rad': -1, 'xl': 1}, 1, k8),
                 ({'rad': -1, 'half': 2}, 2, k12),         # half
                 ({'rad': -2, 'double': 1}, 1, k13)]       # double

    return reactions

components = {'HCL': 0,      # With initial
#               'LDH': 1.3,
#               'pas': 5,
               'rad': 0,
 #              'ps': 1.3,       # LDH and ps were varied
               'dp': 0,
               'xl': 0,
               'double': 0,
               'half': 0,
               'none': 1}


def params(ini_values):
    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11,k12,k13, k14, k15, UA, pas_0, mu_0, E, q = ini_values
    #          (         Name,       Value,  Vary,    Min,     Max)
    lis =      [(         'k1',          k1,  True,    1.6,     2.1),             #k1*mu = torque
                (         'k2',          k2,  True,    8.0,    50),             # thermocouple
                (         'k3',          k3,  True,    0.0,     20),           #HCL ---> LDH.HCL
                (         'k4',          k4,  True,    0.0,     20),            # HCL + pas --> 2HCL plus radical
                (         'k5',          k5,  True,    0.0,    0.1),          # pas --> rad + HCL       # should be very low since once HCL initiates it goes ham
                (         'k6',          k6,  True,    0.,    200),            # rad +ps --> rad.ps   this should be high as half and double kinetics must only happen once ps is gone
                (         'k7',          k7,  True,    0.0,     10),             # rad ---> degraded (ups viscosity should happen all the time not only when ps is gone)
                (         'k8',          k8,  True,    0.0,     12),             # rad ---> xl (similar to degraded)
                (         'k9',          k9,  True,    0.0,    20),                # effect of degraded on mu
                (        'k10',         k10,  True,    0.0,    15),             # effect of xl on mu
                (        'k11',         k11,  True,    2,     3.6),                #effect of temp on mu
                (      'k12',           k12,  True,    5.,     20),      # half rate
                (      'k13',           k13,  True,    0.,     20),     # double rate
                (      'k14',           k14,  True,    0.,   100),     # half effect
                (      'k15',           k15,  True,    0.,     20),       # double effect
                (         'UA',          UA,  True,    275.0,  402.0),
                (      'pas_0',       pas_0,  False ,   0.0,    6),
                (       'mu_0',        mu_0,  False,   0.0372,    0.03721),
                (          'E',           E,  False,   6208.5, 6208.6),
                (          'q',           q,  False,   2.50,    2.51)]

      #          ('prim_stab_0', prim_stab_0,  False,   0.5,    1.3)]         # removed as parameters
      #          (      'LDH_0',       LDH_0,  False,   None,   None)]
               
    return lis



limits = [[1.6, 2.1],
          [8, 50],
          [0.0, 20],
          [0.0, 20],
          [0.0, 0.05],
          [30, 200],
          [5.0, 20],
          [8., 20],
          [10.0, 20],
          [10.0, 20.],
          [2, 3.6],
          [0.,  20.],         #half rate
          [0.,  20.],        #double rate
          [0.,  100.],          # half effect
          [0.,  20.],            # double effect
          [275.0, 402.0],
          [5,6]]                 # pas_0






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
                'k15',
                'UA',
                'mu_0',
                'E',
                'q',
                'prim_stab_0',
                'LDH_0']





