# Differential equations describing the kinetics of PVC thermal degradation with primary
# and secondary stabilisers 

def der_HCl(n, k3, HCl, LDH, k4, poly_act):
	der_HCl = -n*k3*HCl*LDH + k4*HCl*poly_act
	return der_HCl

def der_LDH(n, k3, HCl, LDH):
	der_LDH = -k3*HCl*LDH
	return der_LDH

def der_poly_act(k4, HCl, poly_act):
	# poly_act is the polymer active sites
	der_poly_act = -k4*HCl*poly_act
	return der_poly_act

def der_radical(k4, HCl, poly_act, k5, radical, prim_stab, k6):
	der_radical = k4*HCl*poly_act - k5*radical*(prim_stab**4) - k6*radical
	return der_radical

def der_prim_stab(k5, radical, prim_stab):
	# prim_stab is primary stabiliser
	der_prim_stab = -k5*radical*(prim_stab**4)
	return der_prim_stab

def der_deg_poly(k6, radical):
	# deg_poly is degraded polymer
	der_deg_poly = k6*radical
	return der_deg_poly